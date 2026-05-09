from src.utils.nodes import *
from tests.utils import CodeGenerator
import pytest

# =========================
# SECTION 1: BASIC IO (5)
# =========================

def test_io_001():
    ast = Program([FuncDecl(VoidType(),"main",[],BlockStmt([
        ExprStmt(FuncCall("printString",[StringLiteral("A")]))
    ]))])
    assert CodeGenerator().generate_and_run(ast) == "A"

def test_io_002():
    ast = Program([FuncDecl(VoidType(),"main",[],BlockStmt([
        ExprStmt(FuncCall("printInt",[IntLiteral(1)]))
    ]))])
    assert CodeGenerator().generate_and_run(ast) == "1"

def test_io_003():
    ast = Program([FuncDecl(VoidType(),"main",[],BlockStmt([
        ExprStmt(FuncCall("printFloat",[FloatLiteral(2.5)]))
    ]))])
    assert CodeGenerator().generate_and_run(ast) == "2.5"

def test_io_004():
    ast = Program([FuncDecl(VoidType(),"main",[],BlockStmt([
        ExprStmt(FuncCall("printInt",[IntLiteral(1)])),
        ExprStmt(FuncCall("printInt",[IntLiteral(2)]))
    ]))])
    assert CodeGenerator().generate_and_run(ast) == "12"

def test_io_005():
    ast = Program([FuncDecl(VoidType(),"main",[],BlockStmt([
        ExprStmt(FuncCall("printString",[StringLiteral("Hi")])),
        ExprStmt(FuncCall("printString",[StringLiteral("!")]))
    ]))])
    assert CodeGenerator().generate_and_run(ast) == "Hi!"


# =========================
# SECTION 2: LITERAL (6)
# =========================

def test_lit_001():
    ast = Program([FuncDecl(VoidType(),"main",[],BlockStmt([
        ExprStmt(FuncCall("printInt",[BinaryOp(IntLiteral(2),"+",IntLiteral(3))]))
    ]))])
    assert CodeGenerator().generate_and_run(ast) == "5"

def test_lit_002():
    ast = Program([FuncDecl(VoidType(),"main",[],BlockStmt([
        ExprStmt(FuncCall("printInt",[BinaryOp(IntLiteral(10),"-",IntLiteral(7))]))
    ]))])
    assert CodeGenerator().generate_and_run(ast) == "3"

def test_lit_003():
    ast = Program([FuncDecl(VoidType(),"main",[],BlockStmt([
        ExprStmt(FuncCall("printInt",[BinaryOp(IntLiteral(3),"*",IntLiteral(5))]))
    ]))])
    assert CodeGenerator().generate_and_run(ast) == "15"

def test_lit_004():
    ast = Program([FuncDecl(VoidType(),"main",[],BlockStmt([
        ExprStmt(FuncCall("printInt",[BinaryOp(IntLiteral(8),"/",IntLiteral(2))]))
    ]))])
    assert CodeGenerator().generate_and_run(ast) == "4"

def test_lit_005():
    ast = Program([FuncDecl(VoidType(),"main",[],BlockStmt([
        ExprStmt(FuncCall("printInt",[BinaryOp(IntLiteral(9),"%",IntLiteral(4))]))
    ]))])
    assert CodeGenerator().generate_and_run(ast) == "1"

def test_lit_006():
    ast = Program([FuncDecl(VoidType(),"main",[],BlockStmt([
        ExprStmt(FuncCall("printInt",[
            BinaryOp(IntLiteral(1),"+",BinaryOp(IntLiteral(2),"*",IntLiteral(3)))
        ]))
    ]))])
    assert CodeGenerator().generate_and_run(ast) == "7"


# =========================
# SECTION 3: VARIABLES (6)
# =========================

def test_var_001():
    ast = Program([FuncDecl(VoidType(),"main",[],BlockStmt([
        VarDecl(IntType(),"x",IntLiteral(5)),
        ExprStmt(FuncCall("printInt",[Identifier("x")]))
    ]))])
    assert CodeGenerator().generate_and_run(ast) == "5"

def test_var_002():
    ast = Program([FuncDecl(VoidType(),"main",[],BlockStmt([
        VarDecl(IntType(),"x",IntLiteral(2)),
        VarDecl(IntType(),"y",IntLiteral(3)),
        ExprStmt(FuncCall("printInt",[BinaryOp(Identifier("x"),"+",Identifier("y"))]))
    ]))])
    assert CodeGenerator().generate_and_run(ast) == "5"

def test_var_003():
    ast = Program([FuncDecl(VoidType(),"main",[],BlockStmt([
        VarDecl(FloatType(),"x",FloatLiteral(2.5)),
        ExprStmt(FuncCall("printFloat",[Identifier("x")]))
    ]))])
    assert CodeGenerator().generate_and_run(ast) == "2.5"

def test_var_004():
    ast = Program([FuncDecl(VoidType(),"main",[],BlockStmt([
        VarDecl(IntType(),"x",None),
        ExprStmt(AssignExpr(Identifier("x"),IntLiteral(9))),
        ExprStmt(FuncCall("printInt",[Identifier("x")]))
    ]))])
    assert CodeGenerator().generate_and_run(ast) == "9"

def test_var_005():
    ast = Program([FuncDecl(VoidType(),"main",[],BlockStmt([
        VarDecl(IntType(),"a",IntLiteral(1)),
        VarDecl(IntType(),"b",IntLiteral(2)),
        VarDecl(IntType(),"c",BinaryOp(Identifier("a"),"+",Identifier("b"))),
        ExprStmt(FuncCall("printInt",[Identifier("c")]))
    ]))])
    assert CodeGenerator().generate_and_run(ast) == "3"

def test_var_006():
    ast = Program([FuncDecl(VoidType(),"main",[],BlockStmt([
        VarDecl(IntType(),"x",IntLiteral(10)),
        ExprStmt(AssignExpr(Identifier("x"),BinaryOp(Identifier("x"),"+",IntLiteral(5)))),
        ExprStmt(FuncCall("printInt",[Identifier("x")]))
    ]))])
    assert CodeGenerator().generate_and_run(ast) == "15"


# =========================
# SECTION 4: ASSIGNMENT (6)
# =========================

def test_assign_001():
    ast = Program([FuncDecl(VoidType(),"main",[],BlockStmt([
        VarDecl(IntType(),"x",None),
        ExprStmt(AssignExpr(Identifier("x"),IntLiteral(3))),
        ExprStmt(FuncCall("printInt",[Identifier("x")]))
    ]))])
    assert CodeGenerator().generate_and_run(ast) == "3"

def test_assign_002():
    ast = Program([FuncDecl(VoidType(),"main",[],BlockStmt([
        VarDecl(IntType(),"x",None),
        VarDecl(IntType(),"y",
            BinaryOp(AssignExpr(Identifier("x"),IntLiteral(5)),"+",IntLiteral(2))
        ),
        ExprStmt(FuncCall("printInt",[Identifier("y")]))
    ]))])
    assert CodeGenerator().generate_and_run(ast) == "7"

def test_assign_003():
    ast = Program([FuncDecl(VoidType(),"main",[],BlockStmt([
        VarDecl(IntType(),"a",None),
        VarDecl(IntType(),"b",None),
        ExprStmt(AssignExpr(Identifier("a"),AssignExpr(Identifier("b"),IntLiteral(4)))),
        ExprStmt(FuncCall("printInt",[Identifier("a")]))
    ]))])
    assert CodeGenerator().generate_and_run(ast) == "4"

def test_assign_004():
    ast = Program([FuncDecl(VoidType(),"main",[],BlockStmt([
        VarDecl(IntType(),"x",IntLiteral(1)),
        ExprStmt(AssignExpr(Identifier("x"),
            BinaryOp(Identifier("x"),"+",IntLiteral(1))
        )),
        ExprStmt(FuncCall("printInt",[Identifier("x")]))
    ]))])
    assert CodeGenerator().generate_and_run(ast) == "2"

def test_assign_005():
    ast = Program([FuncDecl(VoidType(),"main",[],BlockStmt([
        VarDecl(IntType(),"x",IntLiteral(5)),
        VarDecl(IntType(),"y",IntLiteral(2)),
        ExprStmt(AssignExpr(Identifier("x"),BinaryOp(Identifier("x"),"*",Identifier("y")))),
        ExprStmt(FuncCall("printInt",[Identifier("x")]))
    ]))])
    assert CodeGenerator().generate_and_run(ast) == "10"

def test_assign_006():
    ast = Program([FuncDecl(VoidType(),"main",[],BlockStmt([
        VarDecl(IntType(),"x",None),
        ExprStmt(FuncCall("printInt",[
            AssignExpr(Identifier("x"),IntLiteral(8))
        ]))
    ]))])
    assert CodeGenerator().generate_and_run(ast) == "8"


# =========================
# SECTION 5: ARITHMETIC (8)
# =========================

def test_arith_001():
    ast = Program([FuncDecl(VoidType(),"main",[],BlockStmt([
        ExprStmt(FuncCall("printInt",[BinaryOp(IntLiteral(3),"+",IntLiteral(4))]))
    ]))])
    assert CodeGenerator().generate_and_run(ast) == "7"

def test_arith_002():
    ast = Program([FuncDecl(VoidType(),"main",[],BlockStmt([
        ExprStmt(FuncCall("printInt",[BinaryOp(IntLiteral(10),"-",IntLiteral(6))]))
    ]))])
    assert CodeGenerator().generate_and_run(ast) == "4"

def test_arith_003():
    ast = Program([FuncDecl(VoidType(),"main",[],BlockStmt([
        ExprStmt(FuncCall("printInt",[BinaryOp(IntLiteral(5),"*",IntLiteral(5))]))
    ]))])
    assert CodeGenerator().generate_and_run(ast) == "25"

def test_arith_004():
    ast = Program([FuncDecl(VoidType(),"main",[],BlockStmt([
        ExprStmt(FuncCall("printInt",[BinaryOp(IntLiteral(20),"/",IntLiteral(4))]))
    ]))])
    assert CodeGenerator().generate_and_run(ast) == "5"

def test_arith_005():
    ast = Program([FuncDecl(VoidType(),"main",[],BlockStmt([
        ExprStmt(FuncCall("printInt",[BinaryOp(IntLiteral(9),"%",IntLiteral(5))]))
    ]))])
    assert CodeGenerator().generate_and_run(ast) == "4"

def test_arith_006():
    ast = Program([FuncDecl(VoidType(),"main",[],BlockStmt([
        ExprStmt(FuncCall("printInt",[
            BinaryOp(
                BinaryOp(IntLiteral(2),"+",IntLiteral(3)),
                "*",
                IntLiteral(4)
            )
        ]))
    ]))])
    assert CodeGenerator().generate_and_run(ast) == "20"

def test_arith_007():
    ast = Program([FuncDecl(VoidType(),"main",[],BlockStmt([
        ExprStmt(FuncCall("printInt",[
            BinaryOp(IntLiteral(100),"/",
                BinaryOp(IntLiteral(5),"+",IntLiteral(5))
            )
        ]))
    ]))])
    assert CodeGenerator().generate_and_run(ast) == "10"

def test_arith_008():
    ast = Program([FuncDecl(VoidType(),"main",[],BlockStmt([
        ExprStmt(FuncCall("printInt",[
            BinaryOp(
                BinaryOp(IntLiteral(1),"+",IntLiteral(2)),
                "+",
                BinaryOp(IntLiteral(3),"+",IntLiteral(4))
            )
        ]))
    ]))])
    assert CodeGenerator().generate_and_run(ast) == "10"
    
# =========================
# SECTION 6: LOGIC (8)
# =========================

def test_logic_001():
    ast = Program([FuncDecl(VoidType(),"main",[],BlockStmt([
        ExprStmt(FuncCall("printInt",[BinaryOp(IntLiteral(1),"<",IntLiteral(2))]))
    ]))])
    assert CodeGenerator().generate_and_run(ast) == "1"

def test_logic_002():
    ast = Program([FuncDecl(VoidType(),"main",[],BlockStmt([
        ExprStmt(FuncCall("printInt",[BinaryOp(IntLiteral(5),">",IntLiteral(10))]))
    ]))])
    assert CodeGenerator().generate_and_run(ast) == "0"

def test_logic_003():
    ast = Program([FuncDecl(VoidType(),"main",[],BlockStmt([
        ExprStmt(FuncCall("printInt",[BinaryOp(IntLiteral(5),"==",IntLiteral(5))]))
    ]))])
    assert CodeGenerator().generate_and_run(ast) == "1"

def test_logic_004():
    ast = Program([FuncDecl(VoidType(),"main",[],BlockStmt([
        ExprStmt(FuncCall("printInt",[BinaryOp(IntLiteral(3),"!=",IntLiteral(4))]))
    ]))])
    assert CodeGenerator().generate_and_run(ast) == "1"

def test_logic_005():
    ast = Program([FuncDecl(VoidType(),"main",[],BlockStmt([
        ExprStmt(FuncCall("printInt",[BinaryOp(IntLiteral(1),"&&",IntLiteral(0))]))
    ]))])
    assert CodeGenerator().generate_and_run(ast) == "0"

def test_logic_006():
    ast = Program([FuncDecl(VoidType(),"main",[],BlockStmt([
        ExprStmt(FuncCall("printInt",[BinaryOp(IntLiteral(1),"||",IntLiteral(0))]))
    ]))])
    assert CodeGenerator().generate_and_run(ast) == "1"

def test_logic_007():
    ast = Program([FuncDecl(VoidType(),"main",[],BlockStmt([
        ExprStmt(FuncCall("printInt",[
            BinaryOp(
                BinaryOp(IntLiteral(3),"<",IntLiteral(5)),
                "&&",
                IntLiteral(1)
            )
        ]))
    ]))])
    assert CodeGenerator().generate_and_run(ast) == "1"

def test_logic_008():
    ast = Program([FuncDecl(VoidType(),"main",[],BlockStmt([
        ExprStmt(FuncCall("printInt",[
            BinaryOp(
                BinaryOp(IntLiteral(2),">",IntLiteral(5)),
                "||",
                IntLiteral(1)
            )
        ]))
    ]))])
    assert CodeGenerator().generate_and_run(ast) == "1"


# =========================
# SECTION 7: IF (8)
# =========================

def test_if_001():
    ast = Program([FuncDecl(VoidType(),"main",[],BlockStmt([
        IfStmt(IntLiteral(1),
            ExprStmt(FuncCall("printString",[StringLiteral("T")])),
            None)
    ]))])
    assert CodeGenerator().generate_and_run(ast) == "T"

def test_if_002():
    ast = Program([FuncDecl(VoidType(),"main",[],BlockStmt([
        IfStmt(IntLiteral(0),
            ExprStmt(FuncCall("printString",[StringLiteral("T")])),
            ExprStmt(FuncCall("printString",[StringLiteral("F")]))
        )
    ]))])
    assert CodeGenerator().generate_and_run(ast) == "F"

def test_if_003():
    ast = Program([FuncDecl(VoidType(),"main",[],BlockStmt([
        IfStmt(BinaryOp(IntLiteral(3),"<",IntLiteral(5)),
            ExprStmt(FuncCall("printString",[StringLiteral("OK")])),
            None)
    ]))])
    assert CodeGenerator().generate_and_run(ast) == "OK"

def test_if_004():
    ast = Program([FuncDecl(VoidType(),"main",[],BlockStmt([
        IfStmt(BinaryOp(IntLiteral(5),">",IntLiteral(10)),
            ExprStmt(FuncCall("printString",[StringLiteral("A")])),
            ExprStmt(FuncCall("printString",[StringLiteral("B")]))
        )
    ]))])
    assert CodeGenerator().generate_and_run(ast) == "B"

def test_if_005():
    ast = Program([FuncDecl(VoidType(),"main",[],BlockStmt([
        IfStmt(IntLiteral(1),
            BlockStmt([
                ExprStmt(FuncCall("printString",[StringLiteral("A")])),
                ExprStmt(FuncCall("printString",[StringLiteral("B")]))
            ]),
            None)
    ]))])
    assert CodeGenerator().generate_and_run(ast) == "AB"

def test_if_006():
    ast = Program([FuncDecl(VoidType(),"main",[],BlockStmt([
        IfStmt(IntLiteral(0),
            BlockStmt([ExprStmt(FuncCall("printString",[StringLiteral("X")]))]),
            BlockStmt([ExprStmt(FuncCall("printString",[StringLiteral("Y")]))])
        )
    ]))])
    assert CodeGenerator().generate_and_run(ast) == "Y"

def test_if_007():
    ast = Program([FuncDecl(VoidType(),"main",[],BlockStmt([
        IfStmt(IntLiteral(1),
            IfStmt(IntLiteral(1),
                ExprStmt(FuncCall("printString",[StringLiteral("N")])),
                None),
            None)
    ]))])
    assert CodeGenerator().generate_and_run(ast) == "N"

def test_if_008():
    ast = Program([FuncDecl(VoidType(),"main",[],BlockStmt([
        IfStmt(IntLiteral(1),
            IfStmt(IntLiteral(0),
                ExprStmt(FuncCall("printString",[StringLiteral("X")])),
                ExprStmt(FuncCall("printString",[StringLiteral("Y")]))
            ),
            None)
    ]))])
    assert CodeGenerator().generate_and_run(ast) == "Y"
    
# =========================
# SECTION 8: WHILE (10)
# =========================

def test_while_001():
    ast = Program([FuncDecl(VoidType(),"main",[],BlockStmt([
        VarDecl(IntType(),"i",IntLiteral(0)),
        WhileStmt(BinaryOp(Identifier("i"),"<",IntLiteral(3)),
            BlockStmt([
                ExprStmt(FuncCall("printInt",[Identifier("i")])),
                ExprStmt(AssignExpr(Identifier("i"),
                    BinaryOp(Identifier("i"),"+",IntLiteral(1))))
            ])
        )
    ]))])
    assert CodeGenerator().generate_and_run(ast) == "012"


def test_while_002():
    ast = Program([FuncDecl(VoidType(),"main",[],BlockStmt([
        VarDecl(IntType(),"i",IntLiteral(5)),
        WhileStmt(BinaryOp(Identifier("i"),"<",IntLiteral(5)),
            BlockStmt([
                ExprStmt(FuncCall("printInt",[Identifier("i")]))
            ])
        )
    ]))])
    assert CodeGenerator().generate_and_run(ast) == ""


def test_while_003():
    ast = Program([FuncDecl(VoidType(),"main",[],BlockStmt([
        VarDecl(IntType(),"i",IntLiteral(0)),
        WhileStmt(BinaryOp(Identifier("i"),"<",IntLiteral(1)),
            BlockStmt([
                ExprStmt(FuncCall("printInt",[IntLiteral(9)])),
                ExprStmt(AssignExpr(Identifier("i"),IntLiteral(1)))
            ])
        )
    ]))])
    assert CodeGenerator().generate_and_run(ast) == "9"


def test_while_004():
    ast = Program([FuncDecl(VoidType(),"main",[],BlockStmt([
        VarDecl(IntType(),"i",IntLiteral(0)),
        WhileStmt(IntLiteral(0),
            BlockStmt([
                ExprStmt(FuncCall("printInt",[IntLiteral(1)]))
            ])
        )
    ]))])
    assert CodeGenerator().generate_and_run(ast) == ""


def test_while_005():
    ast = Program([FuncDecl(VoidType(),"main",[],BlockStmt([
        VarDecl(IntType(),"i",IntLiteral(1)),
        WhileStmt(BinaryOp(Identifier("i"),">",IntLiteral(0)),
            BlockStmt([
                ExprStmt(FuncCall("printInt",[Identifier("i")])),
                ExprStmt(AssignExpr(Identifier("i"),IntLiteral(0)))
            ])
        )
    ]))])
    assert CodeGenerator().generate_and_run(ast) == "1"


# -------- Nested loops --------

def test_while_006():
    ast = Program([FuncDecl(VoidType(),"main",[],BlockStmt([
        VarDecl(IntType(),"i",IntLiteral(0)),
        WhileStmt(BinaryOp(Identifier("i"),"<",IntLiteral(2)),
            BlockStmt([
                VarDecl(IntType(),"j",IntLiteral(0)),
                WhileStmt(BinaryOp(Identifier("j"),"<",IntLiteral(2)),
                    BlockStmt([
                        ExprStmt(FuncCall("printInt",[Identifier("j")])),
                        ExprStmt(AssignExpr(Identifier("j"),
                            BinaryOp(Identifier("j"),"+",IntLiteral(1))))
                    ])
                ),
                ExprStmt(AssignExpr(Identifier("i"),
                    BinaryOp(Identifier("i"),"+",IntLiteral(1))))
            ])
        )
    ]))])
    assert CodeGenerator().generate_and_run(ast) == "0101"


def test_while_007():
    ast = Program([FuncDecl(VoidType(),"main",[],BlockStmt([
        VarDecl(IntType(),"i",IntLiteral(0)),
        WhileStmt(BinaryOp(Identifier("i"),"<",IntLiteral(2)),
            BlockStmt([
                ExprStmt(FuncCall("printInt",[Identifier("i")])),
                WhileStmt(IntLiteral(0), BlockStmt([
                    ExprStmt(FuncCall("printInt",[IntLiteral(9)]))
                ])),
                ExprStmt(AssignExpr(Identifier("i"),
                    BinaryOp(Identifier("i"),"+",IntLiteral(1))))
            ])
        )
    ]))])
    assert CodeGenerator().generate_and_run(ast) == "01"


# -------- Complex conditions --------

def test_while_008():
    ast = Program([FuncDecl(VoidType(),"main",[],BlockStmt([
        VarDecl(IntType(),"i",IntLiteral(0)),
        WhileStmt(
            BinaryOp(
                BinaryOp(Identifier("i"),"<",IntLiteral(3)),
                "&&",
                IntLiteral(1)
            ),
            BlockStmt([
                ExprStmt(FuncCall("printInt",[Identifier("i")])),
                ExprStmt(AssignExpr(Identifier("i"),
                    BinaryOp(Identifier("i"),"+",IntLiteral(1))))
            ])
        )
    ]))])
    assert CodeGenerator().generate_and_run(ast) == "012"


# -------- Long loop --------

def test_while_009():
    ast = Program([FuncDecl(VoidType(),"main",[],BlockStmt([
        VarDecl(IntType(),"i",IntLiteral(0)),
        WhileStmt(BinaryOp(Identifier("i"),"<",IntLiteral(5)),
            BlockStmt([
                ExprStmt(FuncCall("printInt",[Identifier("i")])),
                ExprStmt(AssignExpr(Identifier("i"),
                    BinaryOp(Identifier("i"),"+",IntLiteral(1))))
            ])
        )
    ]))])
    assert CodeGenerator().generate_and_run(ast) == "01234"


# -------- Complex update --------

def test_while_010():
    ast = Program([FuncDecl(VoidType(),"main",[],BlockStmt([
        VarDecl(IntType(),"i",IntLiteral(1)),
        WhileStmt(BinaryOp(Identifier("i"),"<",IntLiteral(10)),
            BlockStmt([
                ExprStmt(FuncCall("printInt",[Identifier("i")])),
                ExprStmt(AssignExpr(Identifier("i"),
                    BinaryOp(Identifier("i"),"*",IntLiteral(2))))
            ])
        )
    ]))])
    assert CodeGenerator().generate_and_run(ast) == "1248"
    
# =========================
# SECTION 9: FUNCTIONS (10)
# =========================

def test_func_001():
    ast = Program([
        FuncDecl(IntType(),"f",[Param(IntType(),"x")],
            BlockStmt([
                ReturnStmt(BinaryOp(Identifier("x"),"+",IntLiteral(1)))
            ])
        ),
        FuncDecl(VoidType(),"main",[],BlockStmt([
            ExprStmt(FuncCall("printInt",[FuncCall("f",[IntLiteral(5)])]))
        ]))
    ])
    assert CodeGenerator().generate_and_run(ast) == "6"


def test_func_002():
    ast = Program([
        FuncDecl(IntType(),"add",[Param(IntType(),"a"),Param(IntType(),"b")],
            BlockStmt([
                ReturnStmt(BinaryOp(Identifier("a"),"+",Identifier("b")))
            ])
        ),
        FuncDecl(VoidType(),"main",[],BlockStmt([
            ExprStmt(FuncCall("printInt",[FuncCall("add",[IntLiteral(3),IntLiteral(4)])]))
        ]))
    ])
    assert CodeGenerator().generate_and_run(ast) == "7"


def test_func_003():
    ast = Program([
        FuncDecl(IntType(),"square",[Param(IntType(),"x")],
            BlockStmt([
                ReturnStmt(BinaryOp(Identifier("x"),"*",Identifier("x")))
            ])
        ),
        FuncDecl(VoidType(),"main",[],BlockStmt([
            ExprStmt(FuncCall("printInt",[FuncCall("square",[IntLiteral(6)])]))
        ]))
    ])
    assert CodeGenerator().generate_and_run(ast) == "36"


def test_func_004():
    ast = Program([
        FuncDecl(IntType(),"inc",[Param(IntType(),"x")],
            BlockStmt([
                ReturnStmt(BinaryOp(Identifier("x"),"+",IntLiteral(1)))
            ])
        ),
        FuncDecl(IntType(),"double",[Param(IntType(),"x")],
            BlockStmt([
                ReturnStmt(BinaryOp(Identifier("x"),"*",IntLiteral(2)))
            ])
        ),
        FuncDecl(VoidType(),"main",[],BlockStmt([
            ExprStmt(FuncCall("printInt",[
                FuncCall("double",[FuncCall("inc",[IntLiteral(3)])])
            ]))
        ]))
    ])
    assert CodeGenerator().generate_and_run(ast) == "8"


def test_func_005():
    ast = Program([
        FuncDecl(IntType(),"f",[Param(IntType(),"x")],
            BlockStmt([
                ReturnStmt(Identifier("x"))
            ])
        ),
        FuncDecl(VoidType(),"main",[],BlockStmt([
            ExprStmt(FuncCall("printInt",[FuncCall("f",[IntLiteral(10)])]))
        ]))
    ])
    assert CodeGenerator().generate_and_run(ast) == "10"


def test_func_006():
    ast = Program([
        FuncDecl(IntType(),"sum3",[Param(IntType(),"a"),Param(IntType(),"b"),Param(IntType(),"c")],
            BlockStmt([
                ReturnStmt(BinaryOp(
                    BinaryOp(Identifier("a"),"+",Identifier("b")),
                    "+",
                    Identifier("c")
                ))
            ])
        ),
        FuncDecl(VoidType(),"main",[],BlockStmt([
            ExprStmt(FuncCall("printInt",[FuncCall("sum3",[IntLiteral(1),IntLiteral(2),IntLiteral(3)])]))
        ]))
    ])
    assert CodeGenerator().generate_and_run(ast) == "6"


def test_func_007():
    ast = Program([
        FuncDecl(IntType(),"f",[Param(IntType(),"x")],
            BlockStmt([
                ReturnStmt(BinaryOp(Identifier("x"),"+",IntLiteral(2)))
            ])
        ),
        FuncDecl(VoidType(),"main",[],BlockStmt([
            VarDecl(IntType(),"a",IntLiteral(5)),
            ExprStmt(FuncCall("printInt",[FuncCall("f",[Identifier("a")])]))
        ]))
    ])
    assert CodeGenerator().generate_and_run(ast) == "7"


def test_func_008():
    ast = Program([
        FuncDecl(IntType(),"f",[Param(IntType(),"x")],
            BlockStmt([
                ReturnStmt(BinaryOp(Identifier("x"),"*",IntLiteral(2)))
            ])
        ),
        FuncDecl(IntType(),"g",[Param(IntType(),"y")],
            BlockStmt([
                ReturnStmt(BinaryOp(FuncCall("f",[Identifier("y")]),"+",IntLiteral(3)))
            ])
        ),
        FuncDecl(VoidType(),"main",[],BlockStmt([
            ExprStmt(FuncCall("printInt",[FuncCall("g",[IntLiteral(4)])]))
        ]))
    ])
    assert CodeGenerator().generate_and_run(ast) == "11"


def test_func_009():
    ast = Program([
        FuncDecl(IntType(),"f",[Param(IntType(),"x")],
            BlockStmt([
                ReturnStmt(BinaryOp(
                    BinaryOp(Identifier("x"),"+",IntLiteral(1)),
                    "*",
                    IntLiteral(2)
                ))
            ])
        ),
        FuncDecl(VoidType(),"main",[],BlockStmt([
            ExprStmt(FuncCall("printInt",[FuncCall("f",[IntLiteral(3)])]))
        ]))
    ])
    assert CodeGenerator().generate_and_run(ast) == "8"


def test_func_010():
    ast = Program([
        FuncDecl(IntType(),"id",[Param(IntType(),"x")],
            BlockStmt([
                ReturnStmt(Identifier("x"))
            ])
        ),
        FuncDecl(VoidType(),"main",[],BlockStmt([
            ExprStmt(FuncCall("printInt",[
                BinaryOp(FuncCall("id",[IntLiteral(5)]),"+",IntLiteral(5))
            ]))
        ]))
    ])
    assert CodeGenerator().generate_and_run(ast) == "10"
    
# =========================
# SECTION 10: BLOCKS (5)
# =========================

def test_block_001():
    ast = Program([FuncDecl(VoidType(),"main",[],BlockStmt([
        VarDecl(IntType(),"a",IntLiteral(1)),
        VarDecl(IntType(),"b",IntLiteral(2)),
        ExprStmt(FuncCall("printInt",[BinaryOp(Identifier("a"),"+",Identifier("b"))]))
    ]))])
    assert CodeGenerator().generate_and_run(ast) == "3"


def test_block_002():
    ast = Program([FuncDecl(VoidType(),"main",[],BlockStmt([
        VarDecl(IntType(),"x",IntLiteral(5)),
        ExprStmt(FuncCall("printInt",[Identifier("x")])),
        ExprStmt(FuncCall("printInt",[Identifier("x")]))
    ]))])
    assert CodeGenerator().generate_and_run(ast) == "55"


def test_block_003():
    ast = Program([FuncDecl(VoidType(),"main",[],BlockStmt([
        VarDecl(IntType(),"x",IntLiteral(1)),
        BlockStmt([
            VarDecl(IntType(),"y",IntLiteral(2)),
            ExprStmt(FuncCall("printInt",[BinaryOp(Identifier("x"),"+",Identifier("y"))]))
        ])
    ]))])
    assert CodeGenerator().generate_and_run(ast) == "3"


def test_block_004():
    ast = Program([FuncDecl(VoidType(),"main",[],BlockStmt([
        VarDecl(IntType(),"x",IntLiteral(2)),
        BlockStmt([
            VarDecl(IntType(),"x",IntLiteral(3)),  # shadowing allowed
            ExprStmt(FuncCall("printInt",[Identifier("x")]))
        ]),
        ExprStmt(FuncCall("printInt",[Identifier("x")]))
    ]))])
    assert CodeGenerator().generate_and_run(ast) == "32"


def test_block_005():
    ast = Program([FuncDecl(VoidType(),"main",[],BlockStmt([
        VarDecl(IntType(),"a",IntLiteral(1)),
        VarDecl(IntType(),"b",IntLiteral(2)),
        BlockStmt([
            VarDecl(IntType(),"c",BinaryOp(Identifier("a"),"+",Identifier("b"))),
            ExprStmt(FuncCall("printInt",[Identifier("c")]))
        ]),
        ExprStmt(FuncCall("printInt",[Identifier("a")]))
    ]))])
    assert CodeGenerator().generate_and_run(ast) == "31"
    
# =========================
# SECTION 11: NESTED EXPR (5)
# =========================

def test_nested_001():
    ast = Program([FuncDecl(VoidType(),"main",[],BlockStmt([
        ExprStmt(FuncCall("printInt",[
            BinaryOp(
                BinaryOp(IntLiteral(2),"+",IntLiteral(3)),
                "*",
                IntLiteral(4)
            )
        ]))
    ]))])
    assert CodeGenerator().generate_and_run(ast) == "20"


def test_nested_002():
    ast = Program([FuncDecl(VoidType(),"main",[],BlockStmt([
        ExprStmt(FuncCall("printInt",[
            BinaryOp(
                IntLiteral(10),
                "/",
                BinaryOp(IntLiteral(2),"+",IntLiteral(3))
            )
        ]))
    ]))])
    assert CodeGenerator().generate_and_run(ast) == "2"


def test_nested_003():
    ast = Program([FuncDecl(VoidType(),"main",[],BlockStmt([
        ExprStmt(FuncCall("printInt",[
            BinaryOp(
                BinaryOp(IntLiteral(1),"+",
                    BinaryOp(IntLiteral(2),"*",IntLiteral(3))
                ),
                "+",
                IntLiteral(4)
            )
        ]))
    ]))])
    assert CodeGenerator().generate_and_run(ast) == "11"


def test_nested_004():
    ast = Program([FuncDecl(VoidType(),"main",[],BlockStmt([
        ExprStmt(FuncCall("printInt",[
            BinaryOp(
                BinaryOp(
                    BinaryOp(IntLiteral(1),"+",IntLiteral(2)),
                    "+",
                    BinaryOp(IntLiteral(3),"+",IntLiteral(4))
                ),
                "*",
                IntLiteral(2)
            )
        ]))
    ]))])
    assert CodeGenerator().generate_and_run(ast) == "20"


def test_nested_005():
    ast = Program([FuncDecl(VoidType(),"main",[],BlockStmt([
        ExprStmt(FuncCall("printInt",[
            BinaryOp(
                BinaryOp(IntLiteral(100),"/",IntLiteral(5)),
                "+",
                BinaryOp(IntLiteral(6),"*",IntLiteral(7))
            )
        ]))
    ]))])
    assert CodeGenerator().generate_and_run(ast) == "62"
    
# =========================
# SECTION 12: MIXED FLOW (8)
# =========================

def test_mix_001():
    ast = Program([FuncDecl(VoidType(),"main",[],BlockStmt([
        VarDecl(IntType(),"i",IntLiteral(0)),
        WhileStmt(BinaryOp(Identifier("i"),"<",IntLiteral(3)),
            BlockStmt([
                IfStmt(BinaryOp(Identifier("i"),"==",IntLiteral(1)),
                    ExprStmt(FuncCall("printString",[StringLiteral("A")])),
                    ExprStmt(FuncCall("printString",[StringLiteral("B")]))
                ),
                ExprStmt(AssignExpr(Identifier("i"),
                    BinaryOp(Identifier("i"),"+",IntLiteral(1))))
            ])
        )
    ]))])
    assert CodeGenerator().generate_and_run(ast) == "BAB"


def test_mix_002():
    ast = Program([FuncDecl(VoidType(),"main",[],BlockStmt([
        VarDecl(IntType(),"i",IntLiteral(0)),
        WhileStmt(BinaryOp(Identifier("i"),"<",IntLiteral(4)),
            BlockStmt([
                IfStmt(BinaryOp(
                    BinaryOp(Identifier("i"),"%",IntLiteral(2)),
                    "==",
                    IntLiteral(0)
                ),
                    ExprStmt(FuncCall("printInt",[Identifier("i")])),
                    None
                ),
                ExprStmt(AssignExpr(Identifier("i"),
                    BinaryOp(Identifier("i"),"+",IntLiteral(1))))
            ])
        )
    ]))])
    assert CodeGenerator().generate_and_run(ast) == "02"


def test_mix_003():
    ast = Program([FuncDecl(VoidType(),"main",[],BlockStmt([
        VarDecl(IntType(),"i",IntLiteral(1)),
        WhileStmt(BinaryOp(Identifier("i"),"<",IntLiteral(10)),
            BlockStmt([
                ExprStmt(FuncCall("printInt",[Identifier("i")])),
                ExprStmt(AssignExpr(Identifier("i"),
                    BinaryOp(Identifier("i"),"*",IntLiteral(2))))
            ])
        )
    ]))])
    assert CodeGenerator().generate_and_run(ast) == "1248"


def test_mix_004():
    ast = Program([FuncDecl(VoidType(),"main",[],BlockStmt([
        VarDecl(IntType(),"i",IntLiteral(0)),
        WhileStmt(BinaryOp(Identifier("i"),"<",IntLiteral(3)),
            BlockStmt([
                IfStmt(BinaryOp(Identifier("i"),"<",IntLiteral(2)),
                    ExprStmt(FuncCall("printString",[StringLiteral("X")])),
                    ExprStmt(FuncCall("printString",[StringLiteral("Y")]))
                ),
                ExprStmt(AssignExpr(Identifier("i"),
                    BinaryOp(Identifier("i"),"+",IntLiteral(1))))
            ])
        )
    ]))])
    assert CodeGenerator().generate_and_run(ast) == "XXY"


def test_mix_005():
    ast = Program([FuncDecl(VoidType(),"main",[],BlockStmt([
        VarDecl(IntType(),"i",IntLiteral(0)),
        WhileStmt(BinaryOp(Identifier("i"),"<",IntLiteral(5)),
            BlockStmt([
                IfStmt(BinaryOp(Identifier("i"),"==",IntLiteral(3)),
                    ExprStmt(FuncCall("printString",[StringLiteral("Z")])),
                    None
                ),
                ExprStmt(AssignExpr(Identifier("i"),
                    BinaryOp(Identifier("i"),"+",IntLiteral(1))))
            ])
        )
    ]))])
    assert CodeGenerator().generate_and_run(ast) == "Z"


# -------- nested loop + if --------

def test_mix_006():
    ast = Program([FuncDecl(VoidType(),"main",[],BlockStmt([
        VarDecl(IntType(),"i",IntLiteral(0)),
        WhileStmt(BinaryOp(Identifier("i"),"<",IntLiteral(2)),
            BlockStmt([
                VarDecl(IntType(),"j",IntLiteral(0)),
                WhileStmt(BinaryOp(Identifier("j"),"<",IntLiteral(2)),
                    BlockStmt([
                        IfStmt(BinaryOp(Identifier("j"),"==",IntLiteral(1)),
                            ExprStmt(FuncCall("printString",[StringLiteral("A")])),
                            ExprStmt(FuncCall("printString",[StringLiteral("B")]))
                        ),
                        ExprStmt(AssignExpr(Identifier("j"),
                            BinaryOp(Identifier("j"),"+",IntLiteral(1))))
                    ])
                ),
                ExprStmt(AssignExpr(Identifier("i"),
                    BinaryOp(Identifier("i"),"+",IntLiteral(1))))
            ])
        )
    ]))])
    assert CodeGenerator().generate_and_run(ast) == "BABA"


# -------- complex condition --------

def test_mix_007():
    ast = Program([FuncDecl(VoidType(),"main",[],BlockStmt([
        VarDecl(IntType(),"i",IntLiteral(0)),
        WhileStmt(
            BinaryOp(
                BinaryOp(Identifier("i"),"<",IntLiteral(3)),
                "&&",
                IntLiteral(1)
            ),
            BlockStmt([
                IfStmt(BinaryOp(Identifier("i"),"!=",IntLiteral(2)),
                    ExprStmt(FuncCall("printString",[StringLiteral("X")])),
                    ExprStmt(FuncCall("printString",[StringLiteral("Y")]))
                ),
                ExprStmt(AssignExpr(Identifier("i"),
                    BinaryOp(Identifier("i"),"+",IntLiteral(1))))
            ])
        )
    ]))])
    assert CodeGenerator().generate_and_run(ast) == "XXY"


# -------- deeper nesting --------

def test_mix_008():
    ast = Program([FuncDecl(VoidType(),"main",[],BlockStmt([
        VarDecl(IntType(),"i",IntLiteral(0)),
        WhileStmt(BinaryOp(Identifier("i"),"<",IntLiteral(2)),
            BlockStmt([
                IfStmt(IntLiteral(1),
                    WhileStmt(BinaryOp(Identifier("i"),"<",IntLiteral(2)),
                        BlockStmt([
                            ExprStmt(FuncCall("printInt",[Identifier("i")])),
                            ExprStmt(AssignExpr(Identifier("i"),
                                BinaryOp(Identifier("i"),"+",IntLiteral(1))))
                        ])
                    ),
                    None
                )
            ])
        )
    ]))])
    assert CodeGenerator().generate_and_run(ast) == "01"
    
# =========================
# SECTION 13: EDGE CASES (5)
# =========================

def test_edge_001():
    # empty main
    ast = Program([
        FuncDecl(VoidType(),"main",[],BlockStmt([]))
    ])
    assert CodeGenerator().generate_and_run(ast) == ""


def test_edge_002():
    # while never executes
    ast = Program([
        FuncDecl(VoidType(),"main",[],BlockStmt([
            WhileStmt(IntLiteral(0),
                BlockStmt([
                    ExprStmt(FuncCall("printInt",[IntLiteral(1)]))
                ])
            )
        ]))
    ])
    assert CodeGenerator().generate_and_run(ast) == ""


def test_edge_003():
    # if without else, false condition
    ast = Program([
        FuncDecl(VoidType(),"main",[],BlockStmt([
            IfStmt(IntLiteral(0),
                ExprStmt(FuncCall("printString",[StringLiteral("X")])),
                None
            )
        ]))
    ])
    assert CodeGenerator().generate_and_run(ast) == ""


def test_edge_004():
    # single statement block
    ast = Program([
        FuncDecl(VoidType(),"main",[],BlockStmt([
            BlockStmt([
                ExprStmt(FuncCall("printInt",[IntLiteral(5)]))
            ])
        ]))
    ])
    assert CodeGenerator().generate_and_run(ast) == "5"


def test_edge_005():
    # deeply nested empty blocks
    ast = Program([
        FuncDecl(VoidType(),"main",[],BlockStmt([
            BlockStmt([
                BlockStmt([
                    BlockStmt([])
                ])
            ])
        ]))
    ])
    assert CodeGenerator().generate_and_run(ast) == ""
    
# =========================
# SECTION 14: EVAL ORDER (5)
# =========================

def test_order_001():
    # simple function order
    ast = Program([
        FuncDecl(IntType(),"f",[Param(IntType(),"x")],
            BlockStmt([
                ExprStmt(FuncCall("printInt",[Identifier("x")])),
                ReturnStmt(Identifier("x"))
            ])
        ),
        FuncDecl(VoidType(),"main",[],BlockStmt([
            ExprStmt(FuncCall("f",[IntLiteral(1)])),
            ExprStmt(FuncCall("f",[IntLiteral(2)]))
        ]))
    ])
    assert CodeGenerator().generate_and_run(ast) == "12"


def test_order_002():
    # binary op evaluation order
    ast = Program([
        FuncDecl(IntType(),"f",[Param(IntType(),"x")],
            BlockStmt([
                ExprStmt(FuncCall("printInt",[Identifier("x")])),
                ReturnStmt(Identifier("x"))
            ])
        ),
        FuncDecl(VoidType(),"main",[],BlockStmt([
            ExprStmt(FuncCall("printInt",[
                BinaryOp(
                    FuncCall("f",[IntLiteral(1)]),
                    "+",
                    FuncCall("f",[IntLiteral(2)])
                )
            ]))
        ]))
    ])
    # left first → prints 1 then 2 → result 3
    assert CodeGenerator().generate_and_run(ast) == "123"


def test_order_003():
    # nested binary
    ast = Program([
        FuncDecl(IntType(),"f",[Param(IntType(),"x")],
            BlockStmt([
                ExprStmt(FuncCall("printInt",[Identifier("x")])),
                ReturnStmt(Identifier("x"))
            ])
        ),
        FuncDecl(VoidType(),"main",[],BlockStmt([
            ExprStmt(FuncCall("printInt",[
                BinaryOp(
                    FuncCall("f",[IntLiteral(1)]),
                    "+",
                    BinaryOp(
                        FuncCall("f",[IntLiteral(2)]),
                        "+",
                        FuncCall("f",[IntLiteral(3)])
                    )
                )
            ]))
        ]))
    ])
    # order: 1 → 2 → 3
    assert CodeGenerator().generate_and_run(ast) == "1236"


def test_order_004():
    # assignment inside expression (right side evaluated first)
    ast = Program([
        FuncDecl(VoidType(),"main",[],BlockStmt([
            VarDecl(IntType(),"x",None),
            ExprStmt(FuncCall("printInt",[
                BinaryOp(
                    AssignExpr(Identifier("x"),IntLiteral(5)),
                    "+",
                    IntLiteral(2)
                )
            ]))
        ]))
    ])
    assert CodeGenerator().generate_and_run(ast) == "7"


def test_order_005():
    # multiple nested calls
    ast = Program([
        FuncDecl(IntType(),"f",[Param(IntType(),"x")],
            BlockStmt([
                ExprStmt(FuncCall("printInt",[Identifier("x")])),
                ReturnStmt(Identifier("x"))
            ])
        ),
        FuncDecl(VoidType(),"main",[],BlockStmt([
            ExprStmt(FuncCall("printInt",[
                BinaryOp(
                    BinaryOp(
                        FuncCall("f",[IntLiteral(1)]),
                        "+",
                        FuncCall("f",[IntLiteral(2)])
                    ),
                    "+",
                    FuncCall("f",[IntLiteral(3)])
                )
            ]))
        ]))
    ])
    # order must be: 1 → 2 → 3
    assert CodeGenerator().generate_and_run(ast) == "1236"

# =========================
# SECTION 15: STACK STRESS (5)
# =========================

def test_stack_001():
    # long linear chain
    expr = IntLiteral(1)
    for i in range(2, 20):
        expr = BinaryOp(expr, "+", IntLiteral(i))

    ast = Program([
        FuncDecl(VoidType(),"main",[],BlockStmt([
            ExprStmt(FuncCall("printInt",[expr]))
        ]))
    ])

    assert CodeGenerator().generate_and_run(ast) == str(sum(range(1,20)))


def test_stack_002():
    # deep nested binary tree
    expr = BinaryOp(
        BinaryOp(
            BinaryOp(IntLiteral(1),"+",IntLiteral(2)),
            "+",
            BinaryOp(IntLiteral(3),"+",IntLiteral(4))
        ),
        "+",
        BinaryOp(
            BinaryOp(IntLiteral(5),"+",IntLiteral(6)),
            "+",
            BinaryOp(IntLiteral(7),"+",IntLiteral(8))
        )
    )

    ast = Program([
        FuncDecl(VoidType(),"main",[],BlockStmt([
            ExprStmt(FuncCall("printInt",[expr]))
        ]))
    ])

    assert CodeGenerator().generate_and_run(ast) == "36"


def test_stack_003():
    # nested assignments
    ast = Program([
        FuncDecl(VoidType(),"main",[],BlockStmt([
            VarDecl(IntType(),"a",None),
            VarDecl(IntType(),"b",None),
            VarDecl(IntType(),"c",None),
            ExprStmt(FuncCall("printInt",[
                AssignExpr(Identifier("a"),
                    AssignExpr(Identifier("b"),
                        AssignExpr(Identifier("c"),IntLiteral(5))
                    )
                )
            ]))
        ]))
    ])

    assert CodeGenerator().generate_and_run(ast) == "5"


def test_stack_004():
    # deep mixed expression
    expr = BinaryOp(
        BinaryOp(
            BinaryOp(IntLiteral(10),"*",IntLiteral(2)),
            "+",
            BinaryOp(IntLiteral(3),"*",IntLiteral(4))
        ),
        "+",
        BinaryOp(
            BinaryOp(IntLiteral(5),"+",IntLiteral(6)),
            "*",
            BinaryOp(IntLiteral(2),"+",IntLiteral(3))
        )
    )

    ast = Program([
        FuncDecl(VoidType(),"main",[],BlockStmt([
            ExprStmt(FuncCall("printInt",[expr]))
        ]))
    ])

    assert CodeGenerator().generate_and_run(ast) == "87"


def test_stack_005():
    # very deep recursion-like expression builder
    def build(n):
        if n == 0:
            return IntLiteral(1)
        return BinaryOp(build(n-1), "+", IntLiteral(1))

    ast = Program([
        FuncDecl(VoidType(),"main",[],BlockStmt([
            ExprStmt(FuncCall("printInt",[build(30)]))
        ]))
    ])

    assert CodeGenerator().generate_and_run(ast) == "31"
    
    
# =========================
# SECTION 16: SAFE STRESS (5)
# =========================

def test_stress_001():
    # large loop (50 iterations)
    ast = Program([
        FuncDecl(VoidType(),"main",[],BlockStmt([
            VarDecl(IntType(),"i",IntLiteral(0)),
            WhileStmt(BinaryOp(Identifier("i"),"<",IntLiteral(50)),
                BlockStmt([
                    ExprStmt(AssignExpr(Identifier("i"),
                        BinaryOp(Identifier("i"),"+",IntLiteral(1))))
                ])
            ),
            ExprStmt(FuncCall("printInt",[Identifier("i")]))
        ]))
    ])
    assert CodeGenerator().generate_and_run(ast) == "50"


def test_stress_002():
    # long arithmetic chain
    expr = IntLiteral(1)
    for i in range(2, 100):
        expr = BinaryOp(expr, "+", IntLiteral(i))

    ast = Program([
        FuncDecl(VoidType(),"main",[],BlockStmt([
            ExprStmt(FuncCall("printInt",[expr]))
        ]))
    ])
    assert CodeGenerator().generate_and_run(ast) == str(sum(range(1,100)))


def test_stress_003():
    # nested loops (3 x 4 iterations)
    ast = Program([
        FuncDecl(VoidType(),"main",[],BlockStmt([
            VarDecl(IntType(),"i",IntLiteral(0)),
            WhileStmt(BinaryOp(Identifier("i"),"<",IntLiteral(3)),
                BlockStmt([
                    VarDecl(IntType(),"j",IntLiteral(0)),
                    WhileStmt(BinaryOp(Identifier("j"),"<",IntLiteral(4)),
                        BlockStmt([
                            ExprStmt(FuncCall("printInt",[Identifier("j")])),
                            ExprStmt(AssignExpr(Identifier("j"),
                                BinaryOp(Identifier("j"),"+",IntLiteral(1))))
                        ])
                    ),
                    ExprStmt(AssignExpr(Identifier("i"),
                        BinaryOp(Identifier("i"),"+",IntLiteral(1))))
                ])
            )
        ]))
    ])
    assert CodeGenerator().generate_and_run(ast) == "012301230123"


def test_stress_004():
    # deep nested expressions + assignment
    expr = BinaryOp(
        BinaryOp(
            BinaryOp(IntLiteral(1),"+",IntLiteral(2)),
            "+",
            BinaryOp(IntLiteral(3),"+",IntLiteral(4))
        ),
        "+",
        BinaryOp(
            BinaryOp(IntLiteral(5),"+",IntLiteral(6)),
            "+",
            BinaryOp(IntLiteral(7),"+",IntLiteral(8))
        )
    )

    ast = Program([
        FuncDecl(VoidType(),"main",[],BlockStmt([
            VarDecl(IntType(),"x",None),
            ExprStmt(AssignExpr(Identifier("x"),expr)),
            ExprStmt(FuncCall("printInt",[Identifier("x")]))
        ]))
    ])
    assert CodeGenerator().generate_and_run(ast) == "36"


def test_stress_005():
    # functions + loops + accumulation
    ast = Program([
        FuncDecl(IntType(),"add",[Param(IntType(),"a"),Param(IntType(),"b")],
            BlockStmt([
                ReturnStmt(BinaryOp(Identifier("a"),"+",Identifier("b")))
            ])
        ),
        FuncDecl(VoidType(),"main",[],BlockStmt([
            VarDecl(IntType(),"i",IntLiteral(0)),
            VarDecl(IntType(),"sum",IntLiteral(0)),
            WhileStmt(BinaryOp(Identifier("i"),"<",IntLiteral(10)),
                BlockStmt([
                    ExprStmt(AssignExpr(Identifier("sum"),
                        FuncCall("add",[Identifier("sum"),Identifier("i")])
                    )),
                    ExprStmt(AssignExpr(Identifier("i"),
                        BinaryOp(Identifier("i"),"+",IntLiteral(1))))
                ])
            ),
            ExprStmt(FuncCall("printInt",[Identifier("sum")]))
        ]))
    ])
    assert CodeGenerator().generate_and_run(ast) == "45"


# =========================
# SECTION 17: AUTO / MEMBER / DEFAULT EDGE CASES
# =========================

def test_edge_auto_float_parameter_infers_default():
    ast = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            VarDecl(None, "x", None),
            ExprStmt(FuncCall("printFloat", [Identifier("x")]))
        ]))
    ])
    assert CodeGenerator().generate_and_run(ast) == "0.0"


def test_edge_auto_function_parameter_infers_struct_copy():
    ast = Program([
        StructDecl("Box", [MemberDecl(IntType(), "value")]),
        FuncDecl(VoidType(), "touch", [Param(StructType("Box"), "b")], BlockStmt([
            ExprStmt(AssignExpr(MemberAccess(Identifier("b"), "value"), IntLiteral(8)))
        ])),
        FuncDecl(VoidType(), "main", [], BlockStmt([
            VarDecl(StructType("Box"), "box", StructLiteral([IntLiteral(4)])),
            VarDecl(None, "alias", None),
            ExprStmt(AssignExpr(Identifier("alias"), Identifier("box"))),
            ExprStmt(FuncCall("touch", [Identifier("alias")])),
            ExprStmt(FuncCall("printInt", [MemberAccess(Identifier("box"), "value")])),
            ExprStmt(FuncCall("printInt", [MemberAccess(Identifier("alias"), "value")]))
        ]))
    ])
    assert CodeGenerator().generate_and_run(ast) == "44"


def test_edge_auto_assignment_inside_if_infers_float():
    ast = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            VarDecl(None, "x", None),
            IfStmt(
                IntLiteral(1),
                BlockStmt([ExprStmt(AssignExpr(Identifier("x"), FloatLiteral(6.25)))]),
                BlockStmt([ExprStmt(AssignExpr(Identifier("x"), FloatLiteral(1.25)))])
            ),
            ExprStmt(FuncCall("printFloat", [Identifier("x")]))
        ]))
    ])
    assert CodeGenerator().generate_and_run(ast) == "6.25"


def test_edge_uninitialized_nested_struct_member_defaults():
    ast = Program([
        StructDecl("Point", [MemberDecl(IntType(), "x"), MemberDecl(FloatType(), "y")]),
        StructDecl("Line", [MemberDecl(StructType("Point"), "start"), MemberDecl(StructType("Point"), "end")]),
        FuncDecl(VoidType(), "main", [], BlockStmt([
            VarDecl(StructType("Line"), "line", None),
            ExprStmt(FuncCall("printInt", [MemberAccess(MemberAccess(Identifier("line"), "start"), "x")])),
            ExprStmt(FuncCall("printFloat", [MemberAccess(MemberAccess(Identifier("line"), "end"), "y")]))
        ]))
    ])
    assert CodeGenerator().generate_and_run(ast) == "00.0"


def test_edge_nested_member_assignment_int_to_float():
    ast = Program([
        StructDecl("Point", [MemberDecl(FloatType(), "x")]),
        StructDecl("Holder", [MemberDecl(StructType("Point"), "p")]),
        FuncDecl(VoidType(), "main", [], BlockStmt([
            VarDecl(StructType("Holder"), "h", None),
            ExprStmt(AssignExpr(MemberAccess(MemberAccess(Identifier("h"), "p"), "x"), IntLiteral(7))),
            ExprStmt(FuncCall("printFloat", [MemberAccess(MemberAccess(Identifier("h"), "p"), "x")]))
        ]))
    ])
    assert CodeGenerator().generate_and_run(ast) == "7.0"


def test_edge_function_returns_uninitialized_nested_member():
    ast = Program([
        StructDecl("Point", [MemberDecl(IntType(), "x")]),
        StructDecl("Holder", [MemberDecl(StructType("Point"), "p")]),
        FuncDecl(IntType(), "get", [], BlockStmt([
            VarDecl(StructType("Holder"), "h", None),
            ReturnStmt(MemberAccess(MemberAccess(Identifier("h"), "p"), "x"))
        ])),
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ExprStmt(FuncCall("printInt", [FuncCall("get", [])]))
        ]))
    ])
    assert CodeGenerator().generate_and_run(ast) == "0"


def test_edge_struct_copy_from_member_access_is_independent():
    ast = Program([
        StructDecl("Point", [MemberDecl(IntType(), "x")]),
        StructDecl("Holder", [MemberDecl(StructType("Point"), "p")]),
        FuncDecl(VoidType(), "main", [], BlockStmt([
            VarDecl(StructType("Holder"), "h", StructLiteral([StructLiteral([IntLiteral(2)])])),
            VarDecl(StructType("Point"), "p2", MemberAccess(Identifier("h"), "p")),
            ExprStmt(AssignExpr(MemberAccess(Identifier("p2"), "x"), IntLiteral(9))),
            ExprStmt(FuncCall("printInt", [MemberAccess(MemberAccess(Identifier("h"), "p"), "x")])),
            ExprStmt(FuncCall("printInt", [MemberAccess(Identifier("p2"), "x")]))
        ]))
    ])
    assert CodeGenerator().generate_and_run(ast) == "29"


def test_edge_auto_initialized_from_nested_member():
    ast = Program([
        StructDecl("Point", [MemberDecl(IntType(), "x")]),
        StructDecl("Holder", [MemberDecl(StructType("Point"), "p")]),
        FuncDecl(VoidType(), "main", [], BlockStmt([
            VarDecl(StructType("Holder"), "h", StructLiteral([StructLiteral([IntLiteral(11)])])),
            VarDecl(None, "value", MemberAccess(MemberAccess(Identifier("h"), "p"), "x")),
            ExprStmt(FuncCall("printInt", [Identifier("value")]))
        ]))
    ])
    assert CodeGenerator().generate_and_run(ast) == "11"
