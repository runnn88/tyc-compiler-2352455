"""
Static Semantic Checker for TyC Programming Language

This module implements a comprehensive static semantic checker using visitor pattern
for the TyC procedural programming language. It performs type checking,
scope management, type inference, and detects all semantic errors as
specified in the TyC language specification.
"""

from functools import reduce
from typing import (
    Dict,
    List,
    Set,
    Optional,
    Any,
    Tuple,
    NamedTuple,
    Union,
    TYPE_CHECKING,
)

from ..utils.visitor import ASTVisitor
from ..utils.nodes import (
    ASTNode,
    Program,
    StructDecl,
    MemberDecl,
    FuncDecl,
    Param,
    VarDecl,
    IfStmt,
    WhileStmt,
    ForStmt,
    BreakStmt,
    ContinueStmt,
    ReturnStmt,
    BlockStmt,
    SwitchStmt,
    CaseStmt,
    DefaultStmt,
    Type,
    IntType,
    FloatType,
    StringType,
    VoidType,
    StructType,
    BinaryOp,
    PrefixOp,
    PostfixOp,
    AssignExpr,
    MemberAccess,
    FuncCall,
    Identifier,
    StructLiteral,
    IntLiteral,
    FloatLiteral,
    StringLiteral,
    ExprStmt,
    Expr,
    Stmt,
    Decl,
)
from .static_error import (
    StaticError,
    Redeclared,
    UndeclaredIdentifier,
    UndeclaredFunction,
    UndeclaredStruct,
    TypeCannotBeInferred,
    TypeMismatchInStatement,
    TypeMismatchInExpression,
    MustInLoop,
)


class StaticChecker(ASTVisitor):
    class _UnknownType:
        def __repr__(self):
            return "UnknownType()"

    class _VarInfo:
        def __init__(self, name: str, typ: Any, decl: Optional[VarDecl], auto: bool):
            self.name = name
            self.typ = typ
            self.decl = decl
            self.auto = auto

    class _FuncInfo:
        def __init__(
            self,
            name: str,
            return_type: Any,
            params: List[Tuple[str, Any]],
            decl: Optional[FuncDecl],
            inferred: bool,
            param_names: Optional[set] = None,
        ):
            self.name = name
            self.return_type = return_type
            self.params = params
            self.decl = decl
            self.inferred = inferred
            self.param_names = param_names or set()
            self.saw_value_return = False

    class _StructInfo:
        def __init__(
            self,
            name: str,
            members: List[Tuple[str, Any]],
            decl: StructDecl,
        ):
            self.name = name
            self.members = members
            self.decl = decl
            self.member_map = {
                member_name: member_type for member_name, member_type in members
            }

    class _Context:
        def __init__(
            self,
            scopes: List[Dict[str, "StaticChecker._VarInfo"]],
            functions: Dict[str, "StaticChecker._FuncInfo"],
            structs: Dict[str, "StaticChecker._StructInfo"],
            current_func: Optional["StaticChecker._FuncInfo"] = None,
            loop_depth: int = 0,
            switch_depth: int = 0,
        ):
            self.scopes = scopes
            self.functions = functions
            self.structs = structs
            self.current_func = current_func
            self.loop_depth = loop_depth
            self.switch_depth = switch_depth

    UNKNOWN = _UnknownType()

    def __init__(self):
        self._int_type = IntType()
        self._float_type = FloatType()
        self._string_type = StringType()
        self._void_type = VoidType()

    def check_program(self, ast: Program):
        return self.visit(ast, None)

    def _builtin_functions(self):
        return {
            "readInt": self._FuncInfo("readInt", self._int_type, [], None, False),
            "readFloat": self._FuncInfo("readFloat", self._float_type, [], None, False),
            "readString": self._FuncInfo("readString", self._string_type, [], None, False),
            "printInt": self._FuncInfo(
                "printInt",
                self._void_type,
                [("value", self._int_type)],
                None,
                False,
            ),
            "printFloat": self._FuncInfo(
                "printFloat",
                self._void_type,
                [("value", self._float_type)],
                None,
                False,
            ),
            "printString": self._FuncInfo(
                "printString",
                self._void_type,
                [("value", self._string_type)],
                None,
                False,
            ),
        }

    def _new_context(self):
        return self._Context([{}], self._builtin_functions(), {})

    def _visit_and_keep_ctx(self, ctx, node):
        self.visit(node, ctx)
        return ctx

    def _visit_sequence(self, nodes, ctx):
        reduce(self._visit_and_keep_ctx, nodes, ctx)
        return ctx

    def _expr_env(self, o):
        if isinstance(o, tuple) and len(o) == 2:
            return o
        return o, None

    def _same_type(self, left, right):
        if left is self.UNKNOWN or right is self.UNKNOWN:
            return True
        if left is None or right is None:
            return left is right
        if type(left) is not type(right):
            return False
        if isinstance(left, StructType):
            return left.struct_name == right.struct_name
        return True

    def _is_int(self, typ):
        return isinstance(typ, IntType)

    def _is_float(self, typ):
        return isinstance(typ, FloatType)

    def _is_string(self, typ):
        return isinstance(typ, StringType)

    def _is_void(self, typ):
        return isinstance(typ, VoidType)

    def _is_struct(self, typ):
        return isinstance(typ, StructType)

    def _is_numeric(self, typ):
        return self._is_int(typ) or self._is_float(typ)

    def _lookup_var(self, ctx: _Context, name: str):
        for scope in reversed(ctx.scopes):
            if name in scope:
                return scope[name]
        return None

    def _declare_var(self, ctx: _Context, info: _VarInfo):
        scope = ctx.scopes[-1]
        if ctx.current_func is not None and info.name in ctx.current_func.param_names:
            raise Redeclared("Variable", info.name)
        if info.name in scope:
            raise Redeclared("Variable", info.name)
        scope[info.name] = info

    def _push_scope(self, ctx: _Context):
        ctx.scopes.append({})

    def _pop_scope(self, ctx: _Context):
        ctx.scopes.pop()

    def _resolve_type(self, typ: Type, ctx: _Context, allow_void: bool = False):
        if isinstance(typ, IntType):
            return self._int_type
        if isinstance(typ, FloatType):
            return self._float_type
        if isinstance(typ, StringType):
            return self._string_type
        if isinstance(typ, VoidType):
            if allow_void:
                return self._void_type
            raise TypeMismatchInStatement(typ)
        if isinstance(typ, StructType):
            if typ.struct_name not in ctx.structs:
                raise UndeclaredStruct(typ.struct_name)
            return StructType(typ.struct_name)
        return typ

    def _ensure_expr_type(
        self,
        expr: Expr,
        ctx: _Context,
        expected: Union[IntType, FloatType, StringType, VoidType, StructType],
        stmt: Optional[Stmt] = None,
    ):
        expr_type = self.visit(expr, (ctx, expected))
        if expr_type is self.UNKNOWN:
            raise TypeCannotBeInferred(expr)
        if not self._same_type(expr_type, expected):
            if stmt is None:
                raise TypeMismatchInExpression(expr)
            raise TypeMismatchInStatement(stmt)
        return expr_type

    def _infer_identifier(self, expr: Expr, ctx: _Context, expected):
        if isinstance(expr, Identifier):
            info = self._lookup_var(ctx, expr.name)
            if info is None:
                raise UndeclaredIdentifier(expr.name)
            if info.typ is self.UNKNOWN:
                info.typ = expected
                return expected
            return info.typ
        return self.visit(expr, (ctx, expected))

    def _unknown_from_expr(self, expr: Expr):
        raise TypeCannotBeInferred(expr)

    def _is_lvalue(self, expr: Expr):
        return isinstance(expr, (Identifier, MemberAccess))

    def _infer_binary_numeric(
        self,
        node: BinaryOp,
        ctx: _Context,
        allow_float_result: bool,
    ):
        left = self.visit(node.left, (ctx, None))
        right = self.visit(node.right, (ctx, None))

        if left is self.UNKNOWN and right is self.UNKNOWN:
            raise TypeCannotBeInferred(node)

        if left is self.UNKNOWN and right is not self.UNKNOWN:
            if not self._is_numeric(right):
                raise TypeCannotBeInferred(node)
            left = self._infer_identifier(node.left, ctx, right)

        if right is self.UNKNOWN and left is not self.UNKNOWN:
            if not self._is_numeric(left):
                raise TypeCannotBeInferred(node)
            right = self._infer_identifier(node.right, ctx, left)

        if not self._is_numeric(left) or not self._is_numeric(right):
            raise TypeMismatchInExpression(node)

        if allow_float_result and (self._is_float(left) or self._is_float(right)):
            return self._float_type
        return self._int_type

    def _check_unused_auto_in_scope(self, ctx: _Context, report_node: Any):
        if any(info.auto and info.typ is self.UNKNOWN for info in ctx.scopes[-1].values()):
            raise TypeCannotBeInferred(report_node)

    def visit_program(self, node: Program, o: Any = None):
        ctx = self._new_context()
        self._visit_sequence(node.decls, ctx)
        return None

    def visit_struct_decl(self, node: StructDecl, o: Any = None):
        ctx = o
        if node.name in ctx.structs:
            raise Redeclared("Struct", node.name)

        def fold_members(acc, member):
            seen, members = acc
            if member.name in seen:
                raise Redeclared("Member", member.name)
            return (
                seen | {member.name},
                members + [(member.name, self._resolve_type(member.member_type, ctx))],
            )

        _, members = reduce(fold_members, node.members, (set(), []))

        ctx.structs[node.name] = self._StructInfo(node.name, members, node)
        return None

    def visit_member_decl(self, node: MemberDecl, o: Any = None):
        return None

    def visit_func_decl(self, node: FuncDecl, o: Any = None):
        ctx = o
        if node.name in ctx.functions:
            raise Redeclared("Function", node.name)

        return_type = (
            self._resolve_type(node.return_type, ctx, allow_void=True)
            if node.return_type
            else None
        )
        def fold_params(acc, param):
            seen, params, param_scope = acc
            if param.name in seen:
                raise Redeclared("Parameter", param.name)
            param_type = self._resolve_type(param.param_type, ctx)
            return (
                seen | {param.name},
                params + [(param.name, param_type)],
                {
                    **param_scope,
                    param.name: self._VarInfo(param.name, param_type, None, False),
                },
            )

        param_names, params, param_scope = reduce(fold_params, node.params, (set(), [], {}))

        func_info = self._FuncInfo(
            node.name,
            return_type,
            params,
            node,
            node.return_type is None,
            param_names,
        )
        ctx.functions[node.name] = func_info

        func_ctx = self._Context([param_scope], ctx.functions, ctx.structs, func_info, 0, 0)
        self._visit_sequence(node.body.statements, func_ctx)
        self._check_unused_auto_in_scope(func_ctx, node.body)

        if func_info.inferred and func_info.return_type is None:
            func_info.return_type = self._void_type
        return None

    def visit_param(self, node: Param, o: Any = None):
        return None

    def visit_int_type(self, node: IntType, o: Any = None):
        return self._int_type

    def visit_float_type(self, node: FloatType, o: Any = None):
        return self._float_type

    def visit_string_type(self, node: StringType, o: Any = None):
        return self._string_type

    def visit_void_type(self, node: VoidType, o: Any = None):
        return self._void_type

    def visit_struct_type(self, node: StructType, o: Any = None):
        return node

    def visit_block_stmt(self, node: BlockStmt, o: Any = None):
        ctx = o
        self._push_scope(ctx)
        try:
            self._visit_sequence(node.statements, ctx)
            self._check_unused_auto_in_scope(ctx, node)
        finally:
            self._pop_scope(ctx)
        return None

    def visit_var_decl(self, node: VarDecl, o: Any = None):
        ctx = o

        if node.var_type is None:
            inferred_type = self.UNKNOWN
            if node.init_value is not None:
                inferred_type = self.visit(node.init_value, (ctx, None))
                if inferred_type is self.UNKNOWN:
                    raise TypeCannotBeInferred(node)
                if self._is_void(inferred_type):
                    raise TypeMismatchInStatement(node)
            self._declare_var(ctx, self._VarInfo(node.name, inferred_type, node, True))
            return None

        declared_type = self._resolve_type(node.var_type, ctx)
        if self._is_void(declared_type):
            raise TypeMismatchInStatement(node)

        if node.init_value is not None:
            self._ensure_expr_type(node.init_value, ctx, declared_type, node)

        self._declare_var(ctx, self._VarInfo(node.name, declared_type, node, False))
        return None

    def visit_if_stmt(self, node: IfStmt, o: Any = None):
        ctx = o
        self._ensure_expr_type(node.condition, ctx, self._int_type, node)
        self.visit(node.then_stmt, ctx)
        if node.else_stmt:
            self.visit(node.else_stmt, ctx)
        return None

    def visit_while_stmt(self, node: WhileStmt, o: Any = None):
        ctx = o
        self._ensure_expr_type(node.condition, ctx, self._int_type, node)
        ctx.loop_depth += 1
        try:
            self.visit(node.body, ctx)
        finally:
            ctx.loop_depth -= 1
        return None

    def visit_for_stmt(self, node: ForStmt, o: Any = None):
        ctx = o
        if node.init is not None:
            try:
                self.visit(node.init, ctx)
            except TypeMismatchInExpression as exc:
                if isinstance(node.init, AssignExpr) and exc.expr is node.init:
                    raise TypeMismatchInStatement(node)
                raise
        if node.condition is not None:
            self._ensure_expr_type(node.condition, ctx, self._int_type, node)
        if node.update is not None:
            try:
                self.visit(node.update, (ctx, None))
            except TypeMismatchInExpression as exc:
                if isinstance(node.update, AssignExpr) and exc.expr is node.update:
                    raise TypeMismatchInStatement(node)
                raise

        body_ctx = self._Context(
            ctx.scopes + [{}],
            ctx.functions,
            ctx.structs,
            ctx.current_func,
            ctx.loop_depth + 1,
            ctx.switch_depth,
        )
        if isinstance(node.body, BlockStmt):
            self.visit(node.body, body_ctx)
        else:
            self.visit(node.body, body_ctx)
            self._check_unused_auto_in_scope(body_ctx, BlockStmt([node.body]))
        return None

    def visit_switch_stmt(self, node: SwitchStmt, o: Any = None):
        ctx = o
        self._ensure_expr_type(node.expr, ctx, self._int_type, node)
        ctx.switch_depth += 1
        try:
            self._visit_sequence(node.cases, ctx)
            if node.default_case:
                self.visit(node.default_case, ctx)
        finally:
            ctx.switch_depth -= 1
        return None

    def visit_case_stmt(self, node: CaseStmt, o: Any = None):
        ctx = o
        self._ensure_expr_type(node.expr, ctx, self._int_type)
        self._visit_sequence(node.statements, ctx)
        return None

    def visit_default_stmt(self, node: DefaultStmt, o: Any = None):
        ctx = o
        self._visit_sequence(node.statements, ctx)
        return None

    def visit_break_stmt(self, node: BreakStmt, o: Any = None):
        ctx = o
        if ctx.loop_depth <= 0 and ctx.switch_depth <= 0:
            raise MustInLoop(node)
        return None

    def visit_continue_stmt(self, node: ContinueStmt, o: Any = None):
        ctx = o
        if ctx.loop_depth <= 0:
            raise MustInLoop(node)
        return None

    def visit_return_stmt(self, node: ReturnStmt, o: Any = None):
        ctx = o
        func = ctx.current_func
        if func is None:
            raise TypeMismatchInStatement(node)

        if node.expr is None:
            if func.return_type is None and func.inferred:
                func.return_type = self._void_type
                return None
            if func.return_type is not None and not self._is_void(func.return_type):
                raise TypeMismatchInStatement(node)
            return None

        expr_type = self.visit(node.expr, (ctx, func.return_type))
        if expr_type is self.UNKNOWN:
            raise TypeCannotBeInferred(node)

        if func.return_type is None:
            func.return_type = expr_type
            func.saw_value_return = True
            return None

        if not self._same_type(func.return_type, expr_type):
            raise TypeMismatchInStatement(node)

        func.saw_value_return = True
        return None

    def visit_expr_stmt(self, node: ExprStmt, o: Any = None):
        ctx = o
        try:
            self.visit(node.expr, (ctx, None))
        except TypeMismatchInExpression as exc:
            if isinstance(node.expr, AssignExpr) and exc.expr is node.expr:
                raise TypeMismatchInStatement(node.expr)
            raise
        return None

    def visit_binary_op(self, node: BinaryOp, o: Any = None):
        ctx, expected = self._expr_env(o)
        op = node.operator

        if op in ["+", "-", "*", "/"]:
            return self._infer_binary_numeric(node, ctx, True)

        if op == "%":
            left = self.visit(node.left, (ctx, None))
            right = self.visit(node.right, (ctx, None))
            if left is self.UNKNOWN and right is self.UNKNOWN:
                raise TypeCannotBeInferred(node)
            if left is self.UNKNOWN and not self._is_int(right):
                raise TypeCannotBeInferred(node)
            if right is self.UNKNOWN and not self._is_int(left):
                raise TypeCannotBeInferred(node)
            try:
                self._ensure_expr_type(node.left, ctx, self._int_type)
                self._ensure_expr_type(node.right, ctx, self._int_type)
            except TypeMismatchInExpression:
                raise TypeMismatchInExpression(node)
            return self._int_type

        if op in ["<", "<=", ">", ">=", "==", "!="]:
            left = self.visit(node.left, (ctx, None))
            right = self.visit(node.right, (ctx, None))
            if left is self.UNKNOWN and right is self.UNKNOWN:
                raise TypeCannotBeInferred(node)
            if left is self.UNKNOWN:
                left = self._infer_identifier(node.left, ctx, right)
            if right is self.UNKNOWN:
                right = self._infer_identifier(node.right, ctx, left)
            if not self._is_numeric(left) or not self._is_numeric(right):
                raise TypeMismatchInExpression(node)
            return self._int_type

        if op in ["&&", "||"]:
            left = self.visit(node.left, (ctx, None))
            right = self.visit(node.right, (ctx, None))
            if left is self.UNKNOWN and right is self.UNKNOWN:
                raise TypeCannotBeInferred(node)
            if left is self.UNKNOWN and not self._is_int(right):
                raise TypeCannotBeInferred(node)
            if right is self.UNKNOWN and not self._is_int(left):
                raise TypeCannotBeInferred(node)
            try:
                self._ensure_expr_type(node.left, ctx, self._int_type)
                self._ensure_expr_type(node.right, ctx, self._int_type)
            except TypeMismatchInExpression:
                raise TypeMismatchInExpression(node)
            return self._int_type

        raise TypeMismatchInExpression(node)

    def visit_prefix_op(self, node: PrefixOp, o: Any = None):
        ctx, expected = self._expr_env(o)
        if node.operator in ["++", "--"]:
            if not self._is_lvalue(node.operand):
                raise TypeMismatchInExpression(node)
            try:
                self._ensure_expr_type(node.operand, ctx, self._int_type)
            except TypeMismatchInExpression:
                raise TypeMismatchInExpression(node)
            return self._int_type

        if node.operator == "!":
            try:
                self._ensure_expr_type(node.operand, ctx, self._int_type)
            except TypeMismatchInExpression:
                raise TypeMismatchInExpression(node)
            return self._int_type

        operand_type = self.visit(node.operand, (ctx, expected))
        if operand_type is self.UNKNOWN:
            if expected is not None and self._is_numeric(expected):
                operand_type = self._infer_identifier(node.operand, ctx, expected)
            else:
                self._unknown_from_expr(node.operand)
        if not self._is_numeric(operand_type):
            raise TypeMismatchInExpression(node)
        return operand_type

    def visit_postfix_op(self, node: PostfixOp, o: Any = None):
        ctx, expected = self._expr_env(o)
        if not self._is_lvalue(node.operand):
            raise TypeMismatchInExpression(node)
        try:
            self._ensure_expr_type(node.operand, ctx, self._int_type)
        except TypeMismatchInExpression:
            raise TypeMismatchInExpression(node)
        return self._int_type

    def visit_assign_expr(self, node: AssignExpr, o: Any = None):
        ctx, expected = self._expr_env(o)
        if not self._is_lvalue(node.lhs):
            raise TypeMismatchInExpression(node)

        lhs_type = self.visit(node.lhs, (ctx, expected))
        rhs_type = self.visit(
            node.rhs,
            (ctx, lhs_type if lhs_type is not self.UNKNOWN else expected),
        )

        if lhs_type is self.UNKNOWN and rhs_type is self.UNKNOWN:
            raise TypeCannotBeInferred(node)

        if lhs_type is self.UNKNOWN:
            lhs_type = self._infer_identifier(node.lhs, ctx, rhs_type)
        if rhs_type is self.UNKNOWN:
            rhs_type = self._infer_identifier(node.rhs, ctx, lhs_type)

        if rhs_type is self.UNKNOWN or lhs_type is self.UNKNOWN:
            raise TypeCannotBeInferred(node)

        if not self._same_type(lhs_type, rhs_type):
            raise TypeMismatchInExpression(node)

        return lhs_type

    def visit_member_access(self, node: MemberAccess, o: Any = None):
        ctx, expected = self._expr_env(o)
        obj_type = self.visit(node.obj, (ctx, None))
        if obj_type is self.UNKNOWN:
            raise TypeCannotBeInferred(node)
        if not isinstance(obj_type, StructType):
            raise TypeMismatchInExpression(node)
        if obj_type.struct_name not in ctx.structs:
            raise UndeclaredStruct(obj_type.struct_name)
        struct_info = ctx.structs[obj_type.struct_name]
        if node.member not in struct_info.member_map:
            raise TypeMismatchInExpression(node)
        return struct_info.member_map[node.member]

    def visit_func_call(self, node: FuncCall, o: Any = None):
        ctx, expected = self._expr_env(o)
        if node.name not in ctx.functions:
            raise UndeclaredFunction(node.name)

        func = ctx.functions[node.name]
        if len(node.args) != len(func.params):
            raise TypeMismatchInExpression(node)

        for arg, (_, param_type) in zip(node.args, func.params):
            try:
                self._ensure_expr_type(arg, ctx, param_type)
            except TypeMismatchInExpression:
                raise TypeMismatchInExpression(node)

        if func.return_type is None:
            if expected is not None:
                func.return_type = expected
            else:
                return self.UNKNOWN
        return func.return_type

    def visit_identifier(self, node: Identifier, o: Any = None):
        ctx, expected = self._expr_env(o)
        info = self._lookup_var(ctx, node.name)
        if info is None:
            raise UndeclaredIdentifier(node.name)
        if info.typ is self.UNKNOWN and expected is not None:
            info.typ = expected
        return info.typ

    def visit_struct_literal(self, node: StructLiteral, o: Any = None):
        ctx, expected = self._expr_env(o)
        if not isinstance(expected, StructType):
            return self.UNKNOWN

        if expected.struct_name not in ctx.structs:
            raise UndeclaredStruct(expected.struct_name)

        struct_info = ctx.structs[expected.struct_name]
        if len(node.values) != len(struct_info.members):
            raise TypeMismatchInExpression(node)

        for expr, (_, member_type) in zip(node.values, struct_info.members):
            self._ensure_expr_type(expr, ctx, member_type)

        return expected

    def visit_int_literal(self, node: IntLiteral, o: Any = None):
        return self._int_type

    def visit_float_literal(self, node: FloatLiteral, o: Any = None):
        return self._float_type

    def visit_string_literal(self, node: StringLiteral, o: Any = None):
        return self._string_type
