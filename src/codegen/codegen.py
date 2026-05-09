"""
Code generator for TyC.
"""

from typing import Any

from ..utils.nodes import *
from ..utils.visitor import BaseVisitor
from .emitter import *
from .frame import *
from .io import IO_SYMBOL_LIST
from .utils import *


class StringArrayType:
    """Marker type for JVM main(String[] args)."""
    pass


class CodeGenerator(BaseVisitor):
    """Minimal AST -> Jasmin code generator."""

    def __init__(self):
        self.emit = None
        self.functions = {}
        self.structs = {}
        self.current_return_type = VoidType()
        self.class_name = "TyC"
        self.break_labels = []
        self.continue_labels = []

    def _lookup_symbol(self, name: str, sym_list: list[Symbol]) -> Symbol:
        for sym in reversed(sym_list):
            if sym.name == name:
                return sym
        raise RuntimeError(f"Undeclared symbol: {name}")

    def _infer_type(self, node: Expr, o: Access):
        if isinstance(node, IntLiteral):
            return IntType()
        if isinstance(node, FloatLiteral):
            return FloatType()
        if isinstance(node, StringLiteral):
            return StringType()
        if isinstance(node, Identifier):
            return self._lookup_symbol(node.name, o.sym).type
        if isinstance(node, AssignExpr):
            return self._infer_type(node.rhs, o)
        if isinstance(node, FuncCall):
            return self.functions[node.name].type.return_type
        if isinstance(node, MemberAccess):
            obj_type = self._infer_type(node.obj, o)
            if is_struct_type(obj_type):
                for member in self.structs.get(obj_type.struct_name, []):
                    if member.name == node.member:
                        return member.member_type
            return IntType()
        if isinstance(node, PrefixOp):
            if node.operator == "-":
                return self._infer_type(node.operand, o)
            return IntType()
        if isinstance(node, PostfixOp):
            return IntType()
        if isinstance(node, StructLiteral):
            if isinstance(o, tuple) and len(o) > 1:
                return o[1]
            return IntType()
        if isinstance(node, BinaryOp):
            if node.operator in ["+", "-", "*", "/", "%"]:
                left_type = self._infer_type(node.left, o)
                right_type = self._infer_type(node.right, o)
                if is_float_type(left_type) or is_float_type(right_type):
                    return FloatType()
                return IntType()
            if node.operator in ["<", "<=", ">", ">=", "==", "!=", "&&", "||"]:
                return IntType()
        return IntType()

    def _emit_default_value(self, in_type, frame):
        if is_int_type(in_type):
            return self.emit.emit_push_iconst(0, frame)
        if is_float_type(in_type):
            return self.emit.emit_push_fconst("0.0", frame)
        if is_string_type(in_type):
            return self.emit.emit_push_const("", StringType(), frame)
        if is_struct_type(in_type):
            return self.emit.emit_new_instance(in_type.struct_name, frame)
        raise RuntimeError(f"Unsupported default value type: {type(in_type)}")

    def _coerce_value(self, code: str, from_type, to_type, frame) -> str:
        if is_float_type(to_type) and is_int_type(from_type):
            return code + self.emit.emit_i2f(frame)
        return code

    def _emit_struct_copy(self, source_code: str, struct_type, frame) -> str:
        struct_name = struct_type.struct_name
        code = self.emit.emit_new_instance(struct_name, frame)
        for member in self.structs.get(struct_name, []):
            code += self.emit.emit_dup(frame)
            code += source_code
            code += self.emit.emit_get_field(
                struct_name + "/" + member.name, member.member_type, frame
            )
            if is_struct_type(member.member_type):
                code = self._emit_struct_copy(code, member.member_type, frame)
            code += self.emit.emit_put_field(
                struct_name + "/" + member.name, member.member_type, frame
            )
        return code

    def _copy_if_struct_value(self, code: str, value_type, frame) -> str:
        if is_struct_type(value_type):
            return self._emit_struct_copy(code, value_type, frame)
        return code

    def _infer_function_return_type(self, node: FuncDecl):
        if node.return_type is not None:
            return node.return_type

        param_syms = [
            Symbol(param.name, param.param_type, Index(index))
            for index, param in enumerate(node.params)
        ]
        access = Access(None, param_syms)

        for stmt in node.body.statements:
            if isinstance(stmt, ReturnStmt) and stmt.expr is not None:
                return self._infer_type(stmt.expr, access)
        return VoidType()

    def _always_returns(self, node: Stmt) -> bool:
        if isinstance(node, ReturnStmt):
            return True
        if isinstance(node, BlockStmt):
            return any(self._always_returns(stmt) for stmt in node.statements)
        if isinstance(node, IfStmt):
            return (
                node.else_stmt is not None
                and self._always_returns(node.then_stmt)
                and self._always_returns(node.else_stmt)
            )
        return False

    def visit_program(self, node: Program, o: Any = None):
        self.emit = Emitter(f"{self.class_name}.j")
        self.emit.print_out(self.emit.emit_prolog(self.class_name))
        self.structs = {}
        self.break_labels = []
        self.continue_labels = []

        for io_sym in IO_SYMBOL_LIST:
            self.functions[io_sym.name] = io_sym

        for decl in node.decls:
            if isinstance(decl, StructDecl):
                self.structs[decl.name] = decl.members
            if isinstance(decl, FuncDecl):
                return_type = self._infer_function_return_type(decl)
                param_types = [p.param_type for p in decl.params]
                self.functions[decl.name] = Symbol(
                    decl.name, FunctionType(param_types, return_type), CName(self.class_name)
                )

        for decl in node.decls:
            if isinstance(decl, FuncDecl):
                self.visit(decl, None)
            elif isinstance(decl, StructDecl):
                self.visit(decl, None)

        self.emit.emit_epilog()

    def visit_func_decl(self, node: FuncDecl, o: Any = None):
        self.current_return_type = self.functions[node.name].type.return_type
        frame = Frame(node.name, self.current_return_type)
        frame.enter_scope(True)

        if node.name == "main":
            mtype = FunctionType([StringArrayType()], VoidType())
        else:
            mtype = FunctionType([p.param_type for p in node.params], self.current_return_type)

        self.emit.print_out(self.emit.emit_method(node.name, mtype, True))

        start_label = frame.get_start_label()
        end_label = frame.get_end_label()
        self.emit.print_out(self.emit.emit_label(start_label, frame))

        local_syms: list[Symbol] = []
        if node.name == "main":
            args_idx = frame.get_new_index()
            self.emit.print_out(
                self.emit.emit_var(
                    args_idx, "args", StringArrayType(), start_label, end_label
                )
            )

        for param in node.params:
            idx = frame.get_new_index()
            self.emit.print_out(
                self.emit.emit_var(idx, param.name, param.param_type, start_label, end_label)
            )
            local_syms.append(Symbol(param.name, param.param_type, Index(idx)))

        sub_body = SubBody(frame, local_syms)
        self.visit(node.body, sub_body)

        if is_void_type(self.current_return_type):
            self.emit.print_out(self.emit.emit_return(VoidType(), frame))

        self.emit.print_out(self.emit.emit_label(end_label, frame))
        frame.exit_scope()
        self.emit.print_out(self.emit.emit_end_method(frame))

    def visit_block_stmt(self, node: BlockStmt, o: SubBody = None):
        local = SubBody(o.frame, list(o.sym))
        for stmt in node.statements:
            local = self.visit(stmt, local)
        return o

    def visit_var_decl(self, node: VarDecl, o: SubBody = None):
        frame = o.frame
        idx = frame.get_new_index()
        if node.var_type is None and node.init_value is None:
            o.sym.append(Symbol(node.name, None, Index(idx)))
            return o

        var_type = node.var_type if node.var_type else self._infer_type(node.init_value, Access(frame, o.sym))
        self.emit.print_out(
            self.emit.emit_var(
                idx, node.name, var_type, frame.get_start_label(), frame.get_end_label()
            )
        )
        if node.init_value is not None:
            init_access = (
                (Access(frame, o.sym), var_type)
                if isinstance(node.init_value, StructLiteral)
                else Access(frame, o.sym)
            )
            rhs_code, rhs_type = self.visit(node.init_value, init_access)
            rhs_code = self._coerce_value(rhs_code, rhs_type, var_type, frame)
            if isinstance(node.init_value, (Identifier, MemberAccess)):
                rhs_code = self._copy_if_struct_value(rhs_code, var_type, frame)
            self.emit.print_out(rhs_code)
            self.emit.print_out(self.emit.emit_write_var(node.name, var_type, idx, frame))
        else:
            self.emit.print_out(self._emit_default_value(var_type, frame))
            self.emit.print_out(self.emit.emit_write_var(node.name, var_type, idx, frame))
        o.sym.append(Symbol(node.name, var_type, Index(idx)))
        return o

    def visit_expr_stmt(self, node: ExprStmt, o: SubBody = None):
        code, expr_type = self.visit(node.expr, Access(o.frame, o.sym))
        self.emit.print_out(code)
        if not is_void_type(expr_type):
            self.emit.print_out(self.emit.emit_pop(o.frame))
        return o

    def visit_if_stmt(self, node: IfStmt, o: SubBody = None):
        frame = o.frame
        cond_code, _ = self.visit(node.condition, Access(frame, o.sym))
        else_label = frame.get_new_label()
        end_label = frame.get_new_label()
        then_returns = self._always_returns(node.then_stmt)
        else_returns = node.else_stmt is not None and self._always_returns(node.else_stmt)
        self.emit.print_out(cond_code)
        self.emit.print_out(self.emit.emit_if_false(else_label, frame))
        self.visit(node.then_stmt, o)
        if not then_returns:
            self.emit.print_out(self.emit.emit_goto(end_label, frame))
        self.emit.print_out(self.emit.emit_label(else_label, frame))
        if node.else_stmt:
            self.visit(node.else_stmt, o)
        if not (then_returns and else_returns):
            self.emit.print_out(self.emit.emit_label(end_label, frame))
        return o

    def visit_while_stmt(self, node: WhileStmt, o: SubBody = None):
        frame = o.frame
        start_label = frame.get_new_label()
        end_label = frame.get_new_label()
        self.continue_labels.append(start_label)
        self.break_labels.append(end_label)
        self.emit.print_out(self.emit.emit_label(start_label, frame))
        cond_code, _ = self.visit(node.condition, Access(frame, o.sym))
        self.emit.print_out(cond_code)
        self.emit.print_out(self.emit.emit_if_false(end_label, frame))
        self.visit(node.body, o)
        self.emit.print_out(self.emit.emit_goto(start_label, frame))
        self.emit.print_out(self.emit.emit_label(end_label, frame))
        self.continue_labels.pop()
        self.break_labels.pop()
        return o

    def visit_return_stmt(self, node: ReturnStmt, o: SubBody = None):
        if node.expr is None:
            self.emit.print_out(self.emit.emit_return(VoidType(), o.frame))
            return o
        expr_access = (
            (Access(o.frame, o.sym), self.current_return_type)
            if isinstance(node.expr, StructLiteral)
            else Access(o.frame, o.sym)
        )
        code, ret_type = self.visit(node.expr, expr_access)
        self.emit.print_out(code)
        self.emit.print_out(self.emit.emit_return(ret_type, o.frame))
        return o

    def visit_binary_op(self, node: BinaryOp, o: Access = None):
        left_code, left_type = self.visit(node.left, o)
        right_code, right_type = self.visit(node.right, o)
        frame = o.frame

        if node.operator in ["+", "-"]:
            result_type = FloatType() if is_float_type(left_type) or is_float_type(right_type) else IntType()
            if is_float_type(result_type) and is_int_type(left_type):
                left_code = left_code + self.emit.emit_i2f(frame)
            if is_float_type(result_type) and is_int_type(right_type):
                right_code = right_code + self.emit.emit_i2f(frame)
            return (
                left_code
                + right_code
                + self.emit.emit_add_op(node.operator, result_type, frame),
                result_type,
            )
        if node.operator in ["*", "/"]:
            result_type = FloatType() if is_float_type(left_type) or is_float_type(right_type) else IntType()
            if is_float_type(result_type) and is_int_type(left_type):
                left_code = left_code + self.emit.emit_i2f(frame)
            if is_float_type(result_type) and is_int_type(right_type):
                right_code = right_code + self.emit.emit_i2f(frame)
            return (
                left_code
                + right_code
                + self.emit.emit_mul_op(node.operator, result_type, frame),
                result_type,
            )
        if node.operator == "%":
            return left_code + right_code + self.emit.emit_mod(frame), IntType()
        if node.operator in ["<", "<=", ">", ">=", "==", "!="]:
            op_type = FloatType() if is_float_type(left_type) or is_float_type(right_type) else IntType()
            if is_float_type(op_type) and is_int_type(left_type):
                left_code = left_code + self.emit.emit_i2f(frame)
            if is_float_type(op_type) and is_int_type(right_type):
                right_code = right_code + self.emit.emit_i2f(frame)
            return left_code + right_code + self.emit.emit_re_op(node.operator, op_type, frame), IntType()
        if node.operator == "&&":
            false_label = frame.get_new_label()
            end_label = frame.get_new_label()
            return (
                left_code
                + self.emit.emit_if_false(false_label, frame)
                + right_code
                + self.emit.emit_if_false(false_label, frame)
                + self.emit.emit_push_iconst(1, frame)
                + self.emit.emit_goto(end_label, frame)
                + self.emit.emit_label(false_label, frame)
                + self.emit.emit_push_iconst(0, frame)
                + self.emit.emit_label(end_label, frame),
                IntType(),
            )
        if node.operator == "||":
            true_label = frame.get_new_label()
            end_label = frame.get_new_label()
            return (
                left_code
                + self.emit.emit_if_true(true_label, frame)
                + right_code
                + self.emit.emit_if_true(true_label, frame)
                + self.emit.emit_push_iconst(0, frame)
                + self.emit.emit_goto(end_label, frame)
                + self.emit.emit_label(true_label, frame)
                + self.emit.emit_push_iconst(1, frame)
                + self.emit.emit_label(end_label, frame),
                IntType(),
            )
        raise RuntimeError(f"Unsupported operator: {node.operator}")

    def visit_assign_expr(self, node: AssignExpr, o: Access = None):
        if isinstance(node.lhs, Identifier):
            lhs_sym = self._lookup_symbol(node.lhs.name, o.sym)
            rhs_access = (
                (o, lhs_sym.type)
                if isinstance(node.rhs, StructLiteral) and lhs_sym.type is not None
                else o
            )
            rhs_code, rhs_type = self.visit(node.rhs, rhs_access)
            if lhs_sym.type is None:
                lhs_sym.type = rhs_type
                self.emit.print_out(
                    self.emit.emit_var(
                        lhs_sym.value.value,
                        node.lhs.name,
                        lhs_sym.type,
                        o.frame.get_start_label(),
                        o.frame.get_end_label(),
                    )
                )
            idx = lhs_sym.value.value
            rhs_code = self._coerce_value(rhs_code, rhs_type, lhs_sym.type, o.frame)
            if isinstance(node.rhs, (Identifier, MemberAccess)):
                rhs_code = self._copy_if_struct_value(rhs_code, lhs_sym.type, o.frame)
            code = rhs_code + self.emit.emit_dup(o.frame) + self.emit.emit_write_var(
                node.lhs.name, lhs_sym.type, idx, o.frame
            )
            return code, lhs_sym.type
        if isinstance(node.lhs, MemberAccess):
            obj_code, obj_type = self.visit(node.lhs.obj, o)
            for member in self.structs.get(obj_type.struct_name, []):
                if member.name == node.lhs.member:
                    rhs_access = (
                        (o, member.member_type) if isinstance(node.rhs, StructLiteral) else o
                    )
                    rhs_code, rhs_type = self.visit(node.rhs, rhs_access)
                    rhs_code = self._coerce_value(
                        rhs_code, rhs_type, member.member_type, o.frame
                    )
                    code = (
                        obj_code
                        + rhs_code
                        + self.emit.emit_dup_x1(o.frame)
                        + self.emit.emit_put_field(
                            obj_type.struct_name + "/" + node.lhs.member,
                            member.member_type,
                            o.frame,
                        )
                    )
                    return code, member.member_type
        raise RuntimeError("Minimal codegen only supports identifier assignment")

    def visit_func_call(self, node: FuncCall, o: Access = None):
        frame = o.frame
        fn_sym = self.functions[node.name]
        fn_type = fn_sym.type
        code = ""
        for arg, param_type in zip(node.args, fn_type.param_types):
            if isinstance(arg, Identifier):
                arg_sym = self._lookup_symbol(arg.name, o.sym)
                if arg_sym.type is None:
                    arg_sym.type = param_type
                    self.emit.print_out(
                        self.emit.emit_var(
                            arg_sym.value.value,
                            arg.name,
                            arg_sym.type,
                            frame.get_start_label(),
                            frame.get_end_label(),
                        )
                    )
                    code += self._emit_default_value(arg_sym.type, frame)
                    code += self.emit.emit_write_var(
                        arg.name, arg_sym.type, arg_sym.value.value, frame
                    )
            arg_access = (o, param_type) if isinstance(arg, StructLiteral) else o
            arg_code, arg_type = self.visit(arg, arg_access)
            arg_code = self._coerce_value(arg_code, arg_type, param_type, frame)
            if isinstance(arg, (Identifier, MemberAccess)):
                arg_code = self._copy_if_struct_value(arg_code, param_type, frame)
            code += arg_code
        code += self.emit.emit_invoke_static(f"{fn_sym.value.value}/{node.name}", fn_type, frame)
        return code, fn_type.return_type

    def visit_identifier(self, node: Identifier, o: Access = None):
        if isinstance(o, tuple):
            o = o[0]
        sym = self._lookup_symbol(node.name, o.sym)
        if sym.type is None:
            raise RuntimeError(f"TypeCannotBeInferred({node})")
        return self.emit.emit_read_var(node.name, sym.type, sym.value.value, o.frame), sym.type

    def visit_int_literal(self, node: IntLiteral, o: Access = None):
        if isinstance(o, tuple):
            o = o[0]
        return self.emit.emit_push_iconst(node.value, o.frame), IntType()

    def visit_float_literal(self, node: FloatLiteral, o: Access = None):
        if isinstance(o, tuple):
            o = o[0]
        return self.emit.emit_push_fconst(str(node.value), o.frame), FloatType()

    def visit_string_literal(self, node: StringLiteral, o: Access = None):
        if isinstance(o, tuple):
            o = o[0]
        return self.emit.emit_push_const(node.value, StringType(), o.frame), StringType()

    def visit_struct_decl(self, node: StructDecl, o: Any = None):
        old_emit = self.emit
        self.emit = Emitter(node.name + ".j")
        self.emit.print_out(self.emit.emit_prolog(node.name))
        for member in node.members:
            self.emit.print_out(
                ".field public " + member.name + " " + self.emit.get_jvm_type(member.member_type) + "\n"
            )
        self.emit.print_out("\n.method public <init>()V\n")
        self.emit.print_out("\taload_0\n")
        self.emit.print_out("\tinvokespecial java/lang/Object/<init>()V\n")
        frame = Frame("<init>", VoidType())
        frame.push()
        frame.pop()
        for member in node.members:
            self.emit.print_out("\taload_0\n")
            frame.push()
            self.emit.print_out(self._emit_default_value(member.member_type, frame))
            self.emit.print_out(
                self.emit.emit_put_field(
                    node.name + "/" + member.name,
                    member.member_type,
                    frame,
                )
            )
        self.emit.print_out("\treturn\n")
        self.emit.print_out(".limit stack " + str(max(1, frame.get_max_op_stack_size())) + "\n")
        self.emit.print_out(".limit locals 1\n")
        self.emit.print_out(".end method\n")
        self.emit.emit_epilog()
        self.emit = old_emit
        return None

    def visit_member_decl(self, node: MemberDecl, o: Any = None):
        return None

    def visit_param(self, node: Param, o: Any = None):
        return None

    def visit_int_type(self, node: IntType, o: Any = None):
        return node

    def visit_float_type(self, node: FloatType, o: Any = None):
        return node

    def visit_string_type(self, node: StringType, o: Any = None):
        return node

    def visit_void_type(self, node: VoidType, o: Any = None):
        return node

    def visit_struct_type(self, node: StructType, o: Any = None):
        return node

    def visit_for_stmt(self, node: ForStmt, o: Any = None):
        frame = o.frame
        if node.init:
            o = self.visit(node.init, o)
        start_label = frame.get_new_label()
        continue_label = frame.get_new_label()
        end_label = frame.get_new_label()
        self.continue_labels.append(continue_label)
        self.break_labels.append(end_label)
        self.emit.print_out(self.emit.emit_label(start_label, frame))
        if node.condition:
            cond_code, _ = self.visit(node.condition, Access(frame, o.sym))
            self.emit.print_out(cond_code)
            self.emit.print_out(self.emit.emit_if_false(end_label, frame))
        self.visit(node.body, o)
        self.emit.print_out(self.emit.emit_label(continue_label, frame))
        if node.update:
            update_code, update_type = self.visit(node.update, Access(frame, o.sym))
            self.emit.print_out(update_code)
            if not is_void_type(update_type):
                self.emit.print_out(self.emit.emit_pop(frame))
        self.emit.print_out(self.emit.emit_goto(start_label, frame))
        self.emit.print_out(self.emit.emit_label(end_label, frame))
        self.continue_labels.pop()
        self.break_labels.pop()
        return o

    def visit_switch_stmt(self, node: SwitchStmt, o: Any = None):
        frame = o.frame
        expr_code, _ = self.visit(node.expr, Access(frame, o.sym))
        expr_index = frame.get_new_index()
        end_label = frame.get_new_label()
        default_label = frame.get_new_label() if node.default_case else end_label
        case_labels = [frame.get_new_label() for _ in node.cases]

        self.emit.print_out(expr_code)
        self.emit.print_out(self.emit.emit_write_var("$switch", IntType(), expr_index, frame))

        for case_stmt, case_label in zip(node.cases, case_labels):
            self.emit.print_out(self.emit.emit_read_var("$switch", IntType(), expr_index, frame))
            case_code, _ = self.visit(case_stmt.expr, Access(frame, o.sym))
            self.emit.print_out(case_code)
            frame.pop()
            frame.pop()
            self.emit.print_out(self.emit.jvm.emitIFICMPEQ(case_label))
        self.emit.print_out(self.emit.emit_goto(default_label, frame))

        self.break_labels.append(end_label)
        for case_stmt, case_label in zip(node.cases, case_labels):
            self.emit.print_out(self.emit.emit_label(case_label, frame))
            for stmt in case_stmt.statements:
                self.visit(stmt, o)
        if node.default_case:
            self.emit.print_out(self.emit.emit_label(default_label, frame))
            for stmt in node.default_case.statements:
                self.visit(stmt, o)
        self.break_labels.pop()
        self.emit.print_out(self.emit.emit_label(end_label, frame))
        return o

    def visit_case_stmt(self, node: CaseStmt, o: Any = None):
        return o

    def visit_default_stmt(self, node: DefaultStmt, o: Any = None):
        return o

    def visit_break_stmt(self, node: BreakStmt, o: Any = None):
        self.emit.print_out(self.emit.emit_goto(self.break_labels[-1], o.frame))
        return o

    def visit_continue_stmt(self, node: ContinueStmt, o: Any = None):
        self.emit.print_out(self.emit.emit_goto(self.continue_labels[-1], o.frame))
        return o

    def visit_prefix_op(self, node: PrefixOp, o: Any = None):
        if isinstance(o, tuple):
            o = o[0]
        frame = o.frame
        if node.operator == "+":
            return self.visit(node.operand, o)
        if node.operator == "-":
            code, in_type = self.visit(node.operand, o)
            return code + self.emit.emit_neg_op(in_type, frame), in_type
        if node.operator == "!":
            code, _ = self.visit(node.operand, o)
            true_label = frame.get_new_label()
            end_label = frame.get_new_label()
            code = (
                code
                + self.emit.emit_if_false(true_label, frame)
                + self.emit.emit_push_iconst(0, frame)
                + self.emit.emit_goto(end_label, frame)
                + self.emit.emit_label(true_label, frame)
                + self.emit.emit_push_iconst(1, frame)
                + self.emit.emit_label(end_label, frame)
            )
            return code, IntType()
        if isinstance(node.operand, Identifier):
            sym = self._lookup_symbol(node.operand.name, o.sym)
            code = (
                self.emit.emit_read_var(node.operand.name, sym.type, sym.value.value, frame)
                + self.emit.emit_push_iconst(1, frame)
                + self.emit.emit_add_op("+" if node.operator == "++" else "-", sym.type, frame)
                + self.emit.emit_dup(frame)
                + self.emit.emit_write_var(node.operand.name, sym.type, sym.value.value, frame)
            )
            return code, sym.type
        if isinstance(node.operand, MemberAccess):
            obj_code, obj_type = self.visit(node.operand.obj, o)
            for member in self.structs.get(obj_type.struct_name, []):
                if member.name == node.operand.member:
                    code = (
                        obj_code
                        + self.emit.emit_dup(frame)
                        + self.emit.emit_get_field(obj_type.struct_name + "/" + node.operand.member, member.member_type, frame)
                        + self.emit.emit_push_iconst(1, frame)
                        + self.emit.emit_add_op("+" if node.operator == "++" else "-", member.member_type, frame)
                        + self.emit.emit_dup_x1(frame)
                        + self.emit.emit_put_field(obj_type.struct_name + "/" + node.operand.member, member.member_type, frame)
                    )
                    return code, member.member_type
        raise RuntimeError("PrefixOp not supported in minimal codegen")

    def visit_postfix_op(self, node: PostfixOp, o: Any = None):
        if isinstance(o, tuple):
            o = o[0]
        frame = o.frame
        if isinstance(node.operand, Identifier):
            sym = self._lookup_symbol(node.operand.name, o.sym)
            code = (
                self.emit.emit_read_var(node.operand.name, sym.type, sym.value.value, frame)
                + self.emit.emit_dup(frame)
                + self.emit.emit_push_iconst(1, frame)
                + self.emit.emit_add_op("+" if node.operator == "++" else "-", sym.type, frame)
                + self.emit.emit_write_var(node.operand.name, sym.type, sym.value.value, frame)
            )
            return code, sym.type
        if isinstance(node.operand, MemberAccess):
            obj_code, obj_type = self.visit(node.operand.obj, o)
            for member in self.structs.get(obj_type.struct_name, []):
                if member.name == node.operand.member:
                    code = (
                        obj_code
                        + self.emit.emit_dup(frame)
                        + self.emit.emit_get_field(obj_type.struct_name + "/" + node.operand.member, member.member_type, frame)
                        + self.emit.emit_dup_x1(frame)
                        + self.emit.emit_push_iconst(1, frame)
                        + self.emit.emit_add_op("+" if node.operator == "++" else "-", member.member_type, frame)
                        + self.emit.emit_put_field(obj_type.struct_name + "/" + node.operand.member, member.member_type, frame)
                    )
                    return code, member.member_type
        raise RuntimeError("PostfixOp not supported in minimal codegen")

    def visit_member_access(self, node: MemberAccess, o: Any = None):
        if isinstance(o, tuple):
            o = o[0]
        obj_code, obj_type = self.visit(node.obj, o)
        for member in self.structs.get(obj_type.struct_name, []):
            if member.name == node.member:
                return (
                    obj_code
                    + self.emit.emit_get_field(obj_type.struct_name + "/" + node.member, member.member_type, o.frame),
                    member.member_type,
                )
        raise RuntimeError("MemberAccess not supported in minimal codegen")

    def visit_struct_literal(self, node: StructLiteral, o: Any = None):
        access = o[0] if isinstance(o, tuple) else o
        struct_type = o[1] if isinstance(o, tuple) and len(o) > 1 else None
        if struct_type is None:
            raise RuntimeError("StructLiteral not supported in minimal codegen")
        code = self.emit.emit_new_instance(struct_type.struct_name, access.frame)
        for expr, member in zip(node.values, self.structs.get(struct_type.struct_name, [])):
            expr_access = (access, member.member_type) if isinstance(expr, StructLiteral) else access
            expr_code, _ = self.visit(expr, expr_access)
            code = (
                code
                + self.emit.emit_dup(access.frame)
                + expr_code
                + self.emit.emit_put_field(struct_type.struct_name + "/" + member.name, member.member_type, access.frame)
            )
        return code, struct_type
