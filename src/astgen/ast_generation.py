"""
AST Generation module for TyC programming language.
This module contains the ASTGeneration class that converts parse trees
into Abstract Syntax Trees using the visitor pattern.
"""

from build.TyCVisitor import TyCVisitor
from build.TyCParser import TyCParser
from src.utils.nodes import *


class ASTGeneration(TyCVisitor):

    # ==========================================================
    # PROGRAM
    # ==========================================================

    def visitProgram(self, ctx: TyCParser.ProgramContext):
        decls = []
        for child in ctx.children:
            if isinstance(child, TyCParser.Struct_declContext) or \
               isinstance(child, TyCParser.Func_declContext):
                decls.append(self.visit(child))
        return Program(decls)

    # ==========================================================
    # STRUCT DECLARATION
    # ==========================================================

    def visitStruct_decl(self, ctx):
        name = ctx.ID().getText()
        members = self.visit(ctx.struct_body())
        return StructDecl(name, members)

    def visitStruct_body(self, ctx):
        return self.visit(ctx.struct_vardecl_lst())

    def visitStruct_vardecl_lst(self, ctx):
        return [self.visit(x) for x in ctx.struct_vardecl()]

    def visitStruct_vardecl(self, ctx):
        return MemberDecl(self.visit(ctx.typ()), ctx.ID().getText())

    # ==========================================================
    # FUNCTION DECLARATION
    # ==========================================================

    def visitFunc_decl(self, ctx):
        return self.visitChildren(ctx)

    def visitFunc_decl_typed(self, ctx):
        return FuncDecl(
            self.visit(ctx.func_typ()),
            ctx.ID().getText(),
            self.visit(ctx.param_list()) if ctx.param_list() else [],
            self.visit(ctx.block())
        )

    def visitFunc_decl_infer(self, ctx):
        return FuncDecl(
            None,
            ctx.ID().getText(),
            self.visit(ctx.param_list()) if ctx.param_list() else [],
            self.visit(ctx.block())
        )

    def visitParam_list(self, ctx):
        return [self.visit(p) for p in ctx.param()]

    def visitParam(self, ctx):
        return Param(self.visit(ctx.typ()), ctx.ID().getText())

    # ==========================================================
    # TYPES
    # ==========================================================

    def visitFunc_typ(self, ctx):
        text = ctx.getText()
        if text == "int":
            return IntType()
        if text == "float":
            return FloatType()
        if text == "string":
            return StringType()
        if text == "void":
            return VoidType()
        return StructType(text)

    def visitTyp(self, ctx):
        text = ctx.getText()
        if text == "int":
            return IntType()
        if text == "float":
            return FloatType()
        if text == "string":
            return StringType()
        return StructType(text)

    # ==========================================================
    # BLOCK & STATEMENTS
    # ==========================================================

    def visitBlock(self, ctx):
        return BlockStmt(self.visit(ctx.stmt_lst()))

    def visitStmt_lst(self, ctx):
        return [self.visit(s) for s in ctx.stmt()]

    def visitStmt(self, ctx):
        # simple_stmt SM
        if ctx.simple_stmt():
            return self.visit(ctx.simple_stmt())

        if ctx.block():
            return self.visit(ctx.block())

        if ctx.if_stmt():
            return self.visit(ctx.if_stmt())

        if ctx.while_stmt():
            return self.visit(ctx.while_stmt())

        if ctx.for_stmt():
            return self.visit(ctx.for_stmt())

        if ctx.switch_stmt():
            return self.visit(ctx.switch_stmt())

        if ctx.vardecl():
            return self.visit(ctx.vardecl())

        return None

   # ---------------- Variable Declaration ----------------

    def visitVardecl(self, ctx):
        return self.visit(ctx.vardecl_core())

    def visitVardecl_core(self, ctx):
        return self.visit(ctx.getChild(0))

    def visitVar_explicit_core(self, ctx):
        typ = self.visit(ctx.typ())
        name = ctx.ID().getText()
        init = self.visit(ctx.expr()) if ctx.expr() else None
        return VarDecl(typ, name, init)

    def visitVar_auto_core(self, ctx):
        name = ctx.ID().getText()
        init = self.visit(ctx.expr()) if ctx.expr() else None
        return VarDecl(None, name, init)

    # ---------------- If ----------------

    def visitIf_stmt(self, ctx):
        return IfStmt(
            self.visit(ctx.expr()),
            self.visit(ctx.stmt(0)),
            self.visit(ctx.stmt(1)) if ctx.ELSE() else None
        )

    # ---------------- While ----------------

    def visitWhile_stmt(self, ctx):
        return WhileStmt(
            self.visit(ctx.expr()),
            self.visit(ctx.stmt())
        )

    # ---------------- For ----------------

    def visitFor_stmt(self, ctx):
        return ForStmt(
            self.visit(ctx.for_init()) if ctx.for_init() else None,
            self.visit(ctx.for_cond()) if ctx.for_cond() else None,
            self.visit(ctx.for_update()) if ctx.for_update() else None,
            self.visit(ctx.stmt())
        )

    def visitFor_init(self, ctx):
        if ctx.vardecl_core():
            return self.visit(ctx.vardecl_core())
        return ExprStmt(
            AssignExpr(
                self.visit(ctx.assign_lhs()),
                self.visit(ctx.expr())
            )
        )

    def visitFor_cond(self, ctx):
        return self.visit(ctx.expr())

    def visitFor_update(self, ctx):
        if ctx.assign_lhs():
            return AssignExpr(
                self.visit(ctx.assign_lhs()),
                self.visit(ctx.expr())
            )
        return self.visit(ctx.incdec_expr())

    def visitIncdec_expr(self, ctx):
        # prefix ++x or --x
        if ctx.getChild(0).getText() in ["++", "--"]:
            return PrefixOp(
                ctx.getChild(0).getText(),
                self.visit(ctx.expr())
            )

        # postfix x++ or x--
        return PostfixOp(
            ctx.getChild(1).getText(),
            self.visit(ctx.expr())
        )
    
    # ---------------- Switch ----------------

    def visitSwitch_stmt(self, ctx):
        expr = self.visit(ctx.expr())
        cases = []
        default_case = None

        body = ctx.switch_body()
        if body is None or body.children is None:
            return SwitchStmt(expr, cases, default_case)

        for child in body.children:
            if isinstance(child, TyCParser.Case_stmtContext):
                cases.append(self.visit(child))
            if isinstance(child, TyCParser.Default_caseContext):
                default_case = self.visit(child)

        return SwitchStmt(expr, cases, default_case)

    def visitCase_stmt(self, ctx):
        return CaseStmt(
            self.visit(ctx.expr()),
            self.visit(ctx.stmt_lst())
        )

    def visitDefault_case(self, ctx):
        return DefaultStmt(self.visit(ctx.stmt_lst()))

    # ---------------- Simple Statements ----------------

    def visitBreak_stmt(self, ctx):
        return BreakStmt()

    def visitContinue_stmt(self, ctx):
        return ContinueStmt()

    def visitReturn_stmt(self, ctx):
        return ReturnStmt(self.visit(ctx.expr()) if ctx.expr() else None)

    def visitExpr_stmt(self, ctx):
        return ExprStmt(self.visit(ctx.expr()))

    # ==========================================================
    # EXPRESSIONS
    # ==========================================================

    def _apply_call(self, func, args):
        if isinstance(func, Identifier):
            return FuncCall(func.name, args)
        raise ValueError("Function call target must be an identifier")

    def _apply_postfix_suffixes(self, expr, suffixes):
        for suffix in suffixes:
            token = suffix.getChild(0).getText()
            if token == ".":
                expr = MemberAccess(expr, suffix.ID().getText())
            elif token == "(":
                args = self.visit(suffix.expr_lst()) if suffix.expr_lst() else []
                expr = self._apply_call(expr, args)
            else:
                expr = PostfixOp(token, expr)
        return expr

    # Assignment (right associative)
    def visitAssign_lhs(self, ctx):
        if ctx.ID():
            return Identifier(ctx.ID().getText())
        return self.visit(ctx.member_lhs())

    def visitMember_lhs(self, ctx):
        expr = self.visit(ctx.primary())
        expr = self._apply_postfix_suffixes(expr, ctx.member_suffix())
        return MemberAccess(expr, ctx.ID().getText())
        
    def visitExp0(self, ctx):
        if ctx.ASSIGN():
            return AssignExpr(
                self.visit(ctx.assign_lhs()),
                self.visit(ctx.exp0())
            )
        return self.visit(ctx.exp1())

    # ----- Binary Layers -----

    def visitExp1(self, ctx):
        if ctx.getChildCount() == 3:
            return BinaryOp(
                self.visit(ctx.exp1()),
                ctx.getChild(1).getText(),
                self.visit(ctx.exp2())
            )
        return self.visit(ctx.exp2())

    def visitExp2(self, ctx):
        if ctx.getChildCount() == 3:
            return BinaryOp(
                self.visit(ctx.exp2()),
                ctx.getChild(1).getText(),
                self.visit(ctx.exp3())
            )
        return self.visit(ctx.exp3())

    def visitExp3(self, ctx):
        if ctx.getChildCount() == 3:
            return BinaryOp(
                self.visit(ctx.exp3()),
                ctx.getChild(1).getText(),
                self.visit(ctx.exp4())
            )
        return self.visit(ctx.exp4())

    def visitExp4(self, ctx):
        if ctx.getChildCount() == 3:
            return BinaryOp(
                self.visit(ctx.exp4()),
                ctx.getChild(1).getText(),
                self.visit(ctx.exp5())
            )
        return self.visit(ctx.exp5())

    def visitExp5(self, ctx):
        if ctx.getChildCount() == 3:
            return BinaryOp(
                self.visit(ctx.exp5()),
                ctx.getChild(1).getText(),
                self.visit(ctx.exp6())
            )
        return self.visit(ctx.exp6())

    def visitExp6(self, ctx):
        if ctx.getChildCount() == 3:
            return BinaryOp(
                self.visit(ctx.exp6()),
                ctx.getChild(1).getText(),
                self.visit(ctx.prefix())
            )
        return self.visit(ctx.prefix())

    # ----- Prefix -----

    def visitPrefix(self, ctx):
        if ctx.getChildCount() == 2:
            return PrefixOp(
                ctx.getChild(0).getText(),
                self.visit(ctx.prefix())
            )
        return self.visit(ctx.postfix())

    # ----- Postfix -----

    def visitPostfix(self, ctx):
        expr = self.visit(ctx.primary())
        return self._apply_postfix_suffixes(expr, ctx.postfix_suffix())

    # ----- Primary -----

    def visitPrimary(self, ctx):
        if ctx.ID():
            return Identifier(ctx.ID().getText())
        if ctx.literal():
            return self.visit(ctx.literal())
        if ctx.expr():
            return self.visit(ctx.expr())
        return self.visit(ctx.struct_literal())

    # ----- Literals -----

    def visitLiteral(self, ctx):
        if ctx.INTLIT():
            return IntLiteral(int(ctx.INTLIT().getText()))
        if ctx.FLOATLIT():
            return FloatLiteral(float(ctx.FLOATLIT().getText()))
        return StringLiteral(ctx.STRINGLIT().getText())

    # ----- Struct Literal -----

    def visitStruct_literal(self, ctx):
        return StructLiteral(
            self.visit(ctx.expr_lst()) if ctx.expr_lst() else []
        )

    def visitExpr_lst(self, ctx):
        return [self.visit(e) for e in ctx.expr()]
