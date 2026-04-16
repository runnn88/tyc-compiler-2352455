"""
Test cases for TyC Static Semantic Checker

This module contains test cases for the static semantic checker.
100 test cases covering all error types and comprehensive scenarios.
"""

from tests.utils import Checker
from src.utils.nodes import (
    Program,
    FuncDecl,
    BlockStmt,
    VarDecl,
    AssignExpr,
    ExprStmt,
    IntType,
    FloatType,
    StringType,
    VoidType,
    StructType,
    IntLiteral,
    FloatLiteral,
    StringLiteral,
    Identifier,
    BinaryOp,
    MemberAccess,
    FuncCall,
    StructDecl,
    MemberDecl,
    Param,
    ReturnStmt,
)


# ============================================================================
# SECTION 1: VALID PROGRAMS
# ============================================================================

def test_valid01():
    source = """
int add(int a, int b){
    return a + b;
}
void main(){
    int x = 1;
    int y = 2;
    int z = add(x, y);
}
"""
    assert Checker(source).check_from_source() == "Static checking passed"


def test_valid02():
    source = """
struct Point {
    int x;
    int y;
};
void main(){
    Point p;
    p.x = 10;
    p.y = 20;
    int sum = p.x + p.y;
}
"""
    assert Checker(source).check_from_source() == "Static checking passed"


def test_valid03():
    source = """
void main(){
    auto x = 1;
    auto y = x + 2;
    {
        auto z = y + x;
        x = z;
    }
}
"""
    assert Checker(source).check_from_source() == "Static checking passed"


def test_valid04():
    source = """
void main(){
    int x = 0;
    while(x < 5){
        if(x == 3){
            break;
        }
        x = x + 1;
    }
}
"""
    assert Checker(source).check_from_source() == "Static checking passed"


def test_valid05():
    source = """
int f(int x){
    if(x) return 1;
    return 0;
}
void main(){
    int a = f(10);
}
"""
    assert Checker(source).check_from_source() == "Static checking passed"


def test_valid06():
    source = """
void main(){
    int x = 1;
    {
        int x = 2;
        {
            int x = 3;
            int y = x;
        }
    }
}
"""
    assert Checker(source).check_from_source() == "Static checking passed"


def test_valid07():
    source = """
void main(){
    auto x = readInt();
    auto y = x + 10;
    auto z = y + x;
}
"""
    assert Checker(source).check_from_source() == "Static checking passed"


def test_valid08():
    source = """
struct A { int x; };
int inc(int a){
    return a + 1;
}
void main(){
    A a;
    a.x = inc(10);
}
"""
    assert Checker(source).check_from_source() == "Static checking passed"


def test_valid09():
    source = """
void main(){
    int x = 1;
    int y = 2;
    int z = (x + y) * (x + y);
}
"""
    assert Checker(source).check_from_source() == "Static checking passed"


def test_valid10():
    source = """
void main(){
    for(int i = 0; i < 5; i = i + 1){
        int x = i;
        while(x){
            x = x - 1;
        }
    }
}
"""
    assert Checker(source).check_from_source() == "Static checking passed"


def test_valid11():
    source = """
int f(int x){
    return x + 1;
}
int g(int y){
    return f(y) + f(y + 1);
}
void main(){
    int z = g(5);
}
"""
    assert Checker(source).check_from_source() == "Static checking passed"


def test_valid12():
    source = """
void main(){
    auto x = 1;
    auto y = 2;
    auto z = x + y;
    z = z + x;
}
"""
    assert Checker(source).check_from_source() == "Static checking passed"


def test_valid13():
    source = """
struct A { int x; };
struct B { A a; };
void main(){
    B b;
    b.a.x = 5;
}
"""
    assert Checker(source).check_from_source() == "Static checking passed"


def test_valid14():
    source = """
void main(){
    int x = 1;
    if(x){
        int y = x + 1;
        x = y;
    }
}
"""
    assert Checker(source).check_from_source() == "Static checking passed"


def test_valid15():
    source = """
void main(){
    int x = 1;
    int y = 2;
    if(x < y){
        x = x + y;
    } else {
        y = y + x;
    }
}
"""
    assert Checker(source).check_from_source() == "Static checking passed"
    
# ============================================================================
# SECTION 2: REDECLARED ERRORS
# ============================================================================

def test_redeclared01():
    source = """
void main(){
    int x = 1;
    int x = 2;
}
"""
    assert Checker(source).check_from_source() == "Redeclared(Variable, x)"


def test_redeclared02():
    source = """
void main(){
    int x = 1;
    {
        int y = 2;
        int y = 3;
    }
}
"""
    assert Checker(source).check_from_source() == "Redeclared(Variable, y)"


def test_redeclared03():
    source = """
void main(){
    int x = 1;
    {
        int x = 2;
        int x = 3;
    }
}
"""
    assert Checker(source).check_from_source() == "Redeclared(Variable, x)"


def test_redeclared04():
    source = """
int f(int x, int x){
    return x;
}
"""
    assert Checker(source).check_from_source() == "Redeclared(Parameter, x)"


def test_redeclared05():
    source = """
int f(int x){
    int x = 2;
    return x;
}
"""
    assert Checker(source).check_from_source() == "Redeclared(Variable, x)"


def test_redeclared06():
    source = """
int f(int a, int b){
    int c = a + b;
    int c = a - b;
    return c;
}
"""
    assert Checker(source).check_from_source() == "Redeclared(Variable, c)"


def test_redeclared07():
    source = """
struct A { int x; };
struct A { float y; };
"""
    assert Checker(source).check_from_source() == "Redeclared(Struct, A)"


def test_redeclared08():
    source = """
struct A { int x; };
struct B { int y; };
struct A { int z; };
"""
    assert Checker(source).check_from_source() == "Redeclared(Struct, A)"


def test_redeclared09():
    source = """
int f(int x){
    return x;
}
int f(int y){
    return y;
}
"""
    assert Checker(source).check_from_source() == "Redeclared(Function, f)"


def test_redeclared10():
    source = """
int f(int x){
    return x;
}
int g(int x){
    return x;
}
int f(int y){
    return y;
}
"""
    assert Checker(source).check_from_source() == "Redeclared(Function, f)"


def test_redeclared11():
    source = """
void main(){
    for(int i = 0; i < 5; i = i + 1){
        int i = 10;
    }
}
"""
    assert Checker(source).check_from_source() == "Static checking passed"


def test_redeclared12():
    source = """
void main(){
    int x = 1;
    {
        int y = 2;
        {
            int y = 3;
            int y = 4;
        }
    }
}
"""
    assert Checker(source).check_from_source() == "Redeclared(Variable, y)"


def test_redeclared13():
    source = """
void main(){
    int x = 1;
    int y = 2;
    int x = y;
}
"""
    assert Checker(source).check_from_source() == "Redeclared(Variable, x)"


def test_redeclared14():
    source = """
int f(int x){
    return x;
}
void main(){
    int f = 10;
    int f = 20;
}
"""
    assert Checker(source).check_from_source() == "Redeclared(Variable, f)"


def test_redeclared15():
    source = """
void main(){
    auto x = 1;
    auto x = 2;
}
"""
    assert Checker(source).check_from_source() == "Redeclared(Variable, x)"


def test_redeclared16():
    source = """
int f(int x){
    {
        int x = 2;
    }
    return x;
}
"""
    assert Checker(source).check_from_source() == "Redeclared(Variable, x)"


def test_redeclared17():
    source = """
void f(int x){
    for(int x = 0; x < 2; x = x + 1){
    }
}
"""
    assert Checker(source).check_from_source() == "Redeclared(Variable, x)"
    
# ============================================================================
# SECTION 3: UNDECLARED ERRORS
# ============================================================================

def test_undeclared01():
    source = """
void main(){
    x = 1;
}
"""
    assert Checker(source).check_from_source() == "UndeclaredIdentifier(x)"


def test_undeclared02():
    source = """
void main(){
    int x = y + 1;
}
"""
    assert Checker(source).check_from_source() == "UndeclaredIdentifier(y)"


def test_undeclared03():
    source = """
void main(){
    int x = 1;
    {
        int y = x;
    }
    y = 2;
}
"""
    assert Checker(source).check_from_source() == "UndeclaredIdentifier(y)"


def test_undeclared04():
    source = """
void main(){
    int x = 1;
    {
        int y = x + z;
    }
}
"""
    assert Checker(source).check_from_source() == "UndeclaredIdentifier(z)"


def test_undeclared05():
    source = """
int f(int x){
    return y;
}
"""
    assert Checker(source).check_from_source() == "UndeclaredIdentifier(y)"


def test_undeclared06():
    source = """
void main(){
    int x = 1;
    int y = x + f(1);
}
"""
    assert Checker(source).check_from_source() == "UndeclaredFunction(f)"


def test_undeclared07():
    source = """
void main(){
    f(1);
}
"""
    assert Checker(source).check_from_source() == "UndeclaredFunction(f)"


def test_undeclared08():
    source = """
int f(int x){
    return g(x);
}
"""
    assert Checker(source).check_from_source() == "UndeclaredFunction(g)"


def test_undeclared09():
    source = """
void main(){
    int x = foo(bar);
}
"""
    assert Checker(source).check_from_source() == "UndeclaredFunction(foo)"


def test_undeclared10():
    source = """
struct A { int x; };
void main(){
    B b;
}
"""
    assert Checker(source).check_from_source() == "UndeclaredStruct(B)"


def test_undeclared11():
    source = """
void main(){
    A a;
}
"""
    assert Checker(source).check_from_source() == "UndeclaredStruct(A)"


def test_undeclared12():
    source = """
struct A { int x; };
void main(){
    A a;
    a.y = 10;
}
"""
    # accessing non-existent field behaves like invalid member → expression error
    assert "TypeMismatchInExpression" in Checker(source).check_from_source()


def test_undeclared13():
    source = """
void main(){
    int x = 1;
    if(x){
        int y = x + 1;
    }
    int z = y + 2;
}
"""
    assert Checker(source).check_from_source() == "UndeclaredIdentifier(y)"


def test_undeclared14():
    source = """
void main(){
    int x = 1;
    for(int i = 0; i < 5; i = i + 1){
        int y = i;
    }
    int z = i;
}
"""
    assert Checker(source).check_from_source() == "Static checking passed"


def test_undeclared15():
    source = """
void main(){
    int x = 1;
    while(x){
        int y = x;
        x = x - 1;
    }
    y = 2;
}
"""
    assert Checker(source).check_from_source() == "UndeclaredIdentifier(y)"
    
# ============================================================================
# SECTION 4: TYPE MISMATCH IN STATEMENT
# ============================================================================

def test_typemismatch_stmt01():
    source = """
void main(){
    int x = 1.5;
}
"""
    assert "TypeMismatchInStatement" in Checker(source).check_from_source()


def test_typemismatch_stmt02():
    source = """
void main(){
    float x = "hello";
}
"""
    assert "TypeMismatchInStatement" in Checker(source).check_from_source()


def test_typemismatch_stmt03():
    source = """
void main(){
    string s = 10;
}
"""
    assert "TypeMismatchInStatement" in Checker(source).check_from_source()


def test_typemismatch_stmt04():
    source = """
void main(){
    int x = 1;
    x = "abc";
}
"""
    assert "TypeMismatchInStatement" in Checker(source).check_from_source()


def test_typemismatch_stmt05():
    source = """
void main(){
    float x = 1.2;
    x = 10;
}
"""
    # depending spec: int → float may or may not be allowed
    assert "TypeMismatchInStatement" in Checker(source).check_from_source()


def test_typemismatch_stmt06():
    source = """
int f(){
    return "hello";
}
"""
    assert "TypeMismatchInStatement" in Checker(source).check_from_source()


def test_typemismatch_stmt07():
    source = """
float f(){
    return 10;
}
"""
    assert "TypeMismatchInStatement" in Checker(source).check_from_source()


def test_typemismatch_stmt08():
    source = """
void main(){
    int x = 1;
    if("abc"){
        x = 2;
    }
}
"""
    assert "TypeMismatchInStatement" in Checker(source).check_from_source()


def test_typemismatch_stmt09():
    source = """
void main(){
    while("abc"){
        int x = 1;
    }
}
"""
    assert "TypeMismatchInStatement" in Checker(source).check_from_source()


def test_typemismatch_stmt10():
    source = """
void main(){
    for(int i = 0; "abc"; i = i + 1){
        int x = i;
    }
}
"""
    assert "TypeMismatchInStatement" in Checker(source).check_from_source()


def test_typemismatch_stmt11():
    source = """
void main(){
    auto x = 1;
    x = "hello";
}
"""
    assert "TypeMismatchInStatement" in Checker(source).check_from_source()


def test_typemismatch_stmt12():
    source = """
void main(){
    auto x = "hello";
    x = 1;
}
"""
    assert "TypeMismatchInStatement" in Checker(source).check_from_source()


def test_typemismatch_stmt13():
    source = """
int f(int x){
    if(x){
        return 1;
    }
    return "abc";
}
"""
    assert "TypeMismatchInStatement" in Checker(source).check_from_source()


def test_typemismatch_stmt14():
    source = """
struct A { int x; };
void main(){
    A a;
    a = 10;
}
"""
    assert "TypeMismatchInStatement" in Checker(source).check_from_source()


def test_typemismatch_stmt15():
    source = """
void main(){
    int x = 1;
    {
        x = "nested error";
    }
}
"""
    assert "TypeMismatchInStatement" in Checker(source).check_from_source()


def test_typemismatch_stmt16():
    source = """
void main(){
    int a;
    float b;
    a = b;
}
"""
    assert Checker(source).check_from_source() == "TypeMismatchInStatement(AssignExpr(Identifier(a) = Identifier(b)))"


def test_typemismatch_stmt17():
    source = """
f(){
    return;
    return 1;
}
"""
    assert Checker(source).check_from_source() == "TypeMismatchInStatement(ReturnStmt(return IntLiteral(1)))"


def test_typemismatch_stmt18():
    source = """
void main(){
    auto x = printInt(1);
}
"""
    assert Checker(source).check_from_source() == "TypeMismatchInStatement(VarDecl(auto, x = FuncCall(printInt, [IntLiteral(1)])))"

# ============================================================================
# SECTION 5: TYPE MISMATCH IN EXPRESSION
# ============================================================================

def test_typemismatch_expr01():
    source = """
void main(){
    int x = 1 + "a";
}
"""
    assert "TypeMismatchInExpression" in Checker(source).check_from_source()


def test_typemismatch_expr02():
    source = """
void main(){
    int x = "a" + "b";
}
"""
    assert "TypeMismatchInExpression" in Checker(source).check_from_source()


def test_typemismatch_expr03():
    source = """
void main(){
    int x = 1 * "a";
}
"""
    assert "TypeMismatchInExpression" in Checker(source).check_from_source()


def test_typemismatch_expr04():
    source = """
void main(){
    int x = 1 < "a";
}
"""
    assert "TypeMismatchInExpression" in Checker(source).check_from_source()


def test_typemismatch_expr05():
    source = """
void main(){
    int x = 1 == "a";
}
"""
    assert "TypeMismatchInExpression" in Checker(source).check_from_source()


def test_typemismatch_expr06():
    source = """
void main(){
    int x = 1 && 2;
}
"""
    assert Checker(source).check_from_source() == "Static checking passed"


def test_typemismatch_expr07():
    source = """
void main(){
    int x = "a" || "b";
}
"""
    assert "TypeMismatchInExpression" in Checker(source).check_from_source()


def test_typemismatch_expr08():
    source = """
void main(){
    int x = !1;
}
"""
    assert Checker(source).check_from_source() == "Static checking passed"


def test_typemismatch_expr09():
    source = """
void main(){
    int x = !"abc";
}
"""
    assert "TypeMismatchInExpression" in Checker(source).check_from_source()


def test_typemismatch_expr10():
    source = """
void main(){
    int x = -"abc";
}
"""
    assert "TypeMismatchInExpression" in Checker(source).check_from_source()


def test_typemismatch_expr11():
    source = """
int f(int x){
    return x;
}
void main(){
    int y = f("abc");
}
"""
    assert "TypeMismatchInExpression" in Checker(source).check_from_source()


def test_typemismatch_expr12():
    source = """
int f(int x){
    return x;
}
void main(){
    int y = f(1.5);
}
"""
    assert "TypeMismatchInExpression" in Checker(source).check_from_source()


def test_typemismatch_expr13():
    source = """
struct A { int x; };
void main(){
    A a;
    int y = a.y;
}
"""
    assert "TypeMismatchInExpression" in Checker(source).check_from_source()


def test_typemismatch_expr14():
    source = """
struct A { int x; };
void main(){
    int y = a.x;
}
"""
    assert "UndeclaredIdentifier(a)" == Checker(source).check_from_source()


def test_typemismatch_expr15():
    source = """
void main(){
    int x = (1 + 2) * ("a" + 3);
}
"""
    assert "TypeMismatchInExpression" in Checker(source).check_from_source()


def test_typemismatch_expr16():
    source = """
void main(){
    int x = (1 < 2) + 3;
}
"""
    assert Checker(source).check_from_source() == "Static checking passed"


def test_typemismatch_expr17():
    source = """
void main(){
    int x = (1 + 2) && 3;
}
"""
    assert Checker(source).check_from_source() == "Static checking passed"


def test_typemismatch_expr18():
    source = """
void main(){
    int x = (1 + (2 * (3 + "a")));
}
"""
    assert "TypeMismatchInExpression" in Checker(source).check_from_source()


def test_typemismatch_expr19():
    source = """
void main(){
    int x = (1 + (2 * (3 + (4 * "a"))));
}
"""
    assert "TypeMismatchInExpression" in Checker(source).check_from_source()


def test_typemismatch_expr20():
    source = """
void main(){
    int x = (1 + (2 * (3 + (4 * (5 + "a")))));
}
"""
    assert "TypeMismatchInExpression" in Checker(source).check_from_source()


def test_typemismatch_expr21():
    source = """
void main(){
    int a;
    float b;
    a = (a = b);
}
"""
    assert Checker(source).check_from_source() == "TypeMismatchInExpression(AssignExpr(Identifier(a) = Identifier(b)))"
    
# ============================================================================
# SECTION 6: TYPE INFERENCE (AUTO)
# ============================================================================

def test_infer01():
    source = """
void main(){
    auto x;
}
"""
    assert Checker(source).check_from_source() == "TypeCannotBeInferred(BlockStmt([VarDecl(auto, x)]))"


def test_infer02():
    source = """
void main(){
    auto x;
    auto y = x;
}
"""
    assert "TypeCannotBeInferred" in Checker(source).check_from_source()


def test_infer03():
    source = """
void main(){
    auto x;
    x = x;
}
"""
    assert "TypeCannotBeInferred" in Checker(source).check_from_source()


def test_infer04():
    source = """
void main(){
    auto x;
    auto y;
    x = y;
}
"""
    assert "TypeCannotBeInferred" in Checker(source).check_from_source()


def test_infer05():
    source = """
void main(){
    auto x = x;
}
"""
    assert Checker(source).check_from_source() == "UndeclaredIdentifier(x)"


def test_infer06():
    source = """
void main(){
    auto x = 1;
    auto y = x;
    auto z = y;
}
"""
    assert Checker(source).check_from_source() == "Static checking passed"


def test_infer07():
    source = """
void main(){
    auto x = 1;
    auto y = x + 2;
    auto z = y + x;
}
"""
    assert Checker(source).check_from_source() == "Static checking passed"


def test_infer08():
    source = """
void main(){
    auto x = 1;
    auto y = x;
    y = "abc";
}
"""
    assert "TypeMismatchInStatement" in Checker(source).check_from_source()


def test_infer09():
    source = """
void main(){
    auto x;
    x = 1;
}
"""
    assert Checker(source).check_from_source() == "Static checking passed"


def test_infer10():
    source = """
void main(){
    auto x;
    x = 1;
    x = 2;
}
"""
    assert Checker(source).check_from_source() == "Static checking passed"


def test_infer11():
    source = """
void main(){
    auto x;
    x = 1;
    x = "abc";
}
"""
    assert "TypeMismatchInStatement" in Checker(source).check_from_source()


def test_infer12():
    source = """
void main(){
    auto x;
    auto y;
    x = 1;
    y = x;
}
"""
    assert Checker(source).check_from_source() == "Static checking passed"


def test_infer13():
    source = """
void main(){
    auto x;
    auto y;
    y = x;
    x = 1;
}
"""
    assert "TypeCannotBeInferred" in Checker(source).check_from_source()


def test_infer14():
    source = """
void main(){
    auto x;
    auto y;
    x = y;
    y = x;
}
"""
    assert "TypeCannotBeInferred" in Checker(source).check_from_source()


def test_infer15():
    source = """
int f(int a){
    return a;
}
void main(){
    auto x = f(1);
}
"""
    assert Checker(source).check_from_source() == "Static checking passed"


def test_infer16():
    source = """
int f(int a){
    return a;
}
void main(){
    auto x = f(1);
    x = "abc";
}
"""
    assert "TypeMismatchInStatement" in Checker(source).check_from_source()


def test_infer17():
    source = """
void main(){
    auto x;
    x = readInt();
}
"""
    assert Checker(source).check_from_source() == "Static checking passed"


def test_infer18():
    source = """
void main(){
    auto x;
    auto y = x + 1;
}
"""
    assert Checker(source).check_from_source() == "Static checking passed"


def test_infer19():
    source = """
void main(){
    auto x;
    x = 1 + 2;
}
"""
    assert Checker(source).check_from_source() == "Static checking passed"


def test_infer20():
    source = """
void main(){
    auto x;
    auto y;
    x = 1;
    y = x + 2;
}
"""
    assert Checker(source).check_from_source() == "Static checking passed"


def test_infer21():
    source = """
void main(){
    auto x;
    auto y;
    auto z = x + y;
}
"""
    assert Checker(source).check_from_source() == "TypeCannotBeInferred(BinaryOp(Identifier(x), +, Identifier(y)))"
    
# ============================================================================
# SECTION 7: LOOP ERRORS (MustInLoop)
# ============================================================================

def test_loop01():
    source = """
void main(){
    break;
}
"""
    assert "MustInLoop" in Checker(source).check_from_source()


def test_loop02():
    source = """
void main(){
    continue;
}
"""
    assert "MustInLoop" in Checker(source).check_from_source()


def test_loop03():
    source = """
void main(){
    if(1){
        break;
    }
}
"""
    assert "MustInLoop" in Checker(source).check_from_source()


def test_loop04():
    source = """
void main(){
    if(1){
        continue;
    }
}
"""
    assert "MustInLoop" in Checker(source).check_from_source()


def test_loop05():
    source = """
void main(){
    while(1){
        break;
    }
}
"""
    assert Checker(source).check_from_source() == "Static checking passed"


def test_loop06():
    source = """
void main(){
    while(1){
        continue;
    }
}
"""
    assert Checker(source).check_from_source() == "Static checking passed"


def test_loop07():
    source = """
void main(){
    for(int i = 0; i < 5; i = i + 1){
        break;
    }
}
"""
    assert Checker(source).check_from_source() == "Static checking passed"


def test_loop08():
    source = """
void main(){
    for(int i = 0; i < 5; i = i + 1){
        continue;
    }
}
"""
    assert Checker(source).check_from_source() == "Static checking passed"


def test_loop15():
    source = """
void main(){
    {
        break;
    }
}
"""
    assert "MustInLoop" in Checker(source).check_from_source()
    
# ============================================================================
# SECTION 8: FUNCTION SEMANTICS
# ============================================================================

def test_func01():
    source = """
int add(int a, int b){
    return a + b;
}
void main(){
    int x = add(1, 2);
}
"""
    assert Checker(source).check_from_source() == "Static checking passed"


def test_func02():
    source = """
int add(int a, int b){
    return a + b;
}
void main(){
    int x = add(1);
}
"""
    assert "TypeMismatchInExpression" in Checker(source).check_from_source()


def test_func03():
    source = """
int add(int a, int b){
    return a + b;
}
void main(){
    int x = add(1, "a");
}
"""
    assert "TypeMismatchInExpression" in Checker(source).check_from_source()


def test_func04():
    source = """
int f(int x){
    return x + 1;
}
int g(int y){
    return f(y) + f(y + 1);
}
void main(){
    int z = g(5);
}
"""
    assert Checker(source).check_from_source() == "Static checking passed"


def test_func05():
    source = """
int f(int x){
    return x + 1;
}
void main(){
    int z = f(f(f(1)));
}
"""
    assert Checker(source).check_from_source() == "Static checking passed"


def test_func06():
    source = """
int f(int x){
    return x;
}
void main(){
    int z = f(f("a"));
}
"""
    assert "TypeMismatchInExpression" in Checker(source).check_from_source()


def test_func07():
    source = """
int f(int x){
    if(x) return 1;
    return 2;
}
"""
    assert Checker(source).check_from_source() == "Static checking passed"


def test_func08():
    source = """
int f(int x){
    if(x) return 1;
    return "a";
}
"""
    assert "TypeMismatchInStatement" in Checker(source).check_from_source()


def test_func09():
    source = """
void f(){
    return 1;
}
"""
    assert "TypeMismatchInStatement" in Checker(source).check_from_source()


def test_func10():
    source = """
int f(int x){
    return x;
}
void main(){
    int a = 1;
    int b = f(a) + f(a + 1);
}
"""
    assert Checker(source).check_from_source() == "Static checking passed"


def test_func11():
    source = """
int f(int x){
    return x;
}
void main(){
    int a = f(1) + f("a");
}
"""
    assert "TypeMismatchInExpression" in Checker(source).check_from_source()


def test_func12():
    source = """
int f(int x){
    return x;
}
int g(int y){
    return f(y) + y;
}
void main(){
    int z = g(10);
}
"""
    assert Checker(source).check_from_source() == "Static checking passed"


def test_func13():
    source = """
int f(int x){
    return x;
}
int g(int y){
    return f(y) + f("a");
}
"""
    assert "TypeMismatchInExpression" in Checker(source).check_from_source()


def test_func14():
    source = """
int f(int x){
    return x;
}
void main(){
    int x = 1;
    int y = f(x);
    int z = f(y);
}
"""
    assert Checker(source).check_from_source() == "Static checking passed"


def test_func15():
    source = """
int f(int x){
    return x;
}
void main(){
    auto x = f(1);
    x = "a";
}
"""
    assert "TypeMismatchInStatement" in Checker(source).check_from_source()
    
# ============================================================================
# SECTION 9: STRUCT SEMANTICS
# ============================================================================

def test_struct01():
    source = """
struct A { int x; int y; };
void main(){
    A a;
    a.x = 10;
    a.y = 20;
}
"""
    assert Checker(source).check_from_source() == "Static checking passed"


def test_struct02():
    source = """
struct A { int x; };
void main(){
    A a;
    int y = a.x;
}
"""
    assert Checker(source).check_from_source() == "Static checking passed"


def test_struct03():
    source = """
struct A { int x; };
void main(){
    A a;
    int y = a.y;
}
"""
    assert "TypeMismatchInExpression" in Checker(source).check_from_source()


def test_struct04():
    source = """
struct A { int x; };
void main(){
    int y = a.x;
}
"""
    assert Checker(source).check_from_source() == "UndeclaredIdentifier(a)"


def test_struct05():
    source = """
struct A { int x; };
void main(){
    A a;
    a = 10;
}
"""
    assert "TypeMismatchInStatement" in Checker(source).check_from_source()


def test_struct06():
    source = """
struct A { int x; };
struct B { A a; };
void main(){
    B b;
    b.a.x = 5;
}
"""
    assert Checker(source).check_from_source() == "Static checking passed"


def test_struct07():
    source = """
struct A { int x; };
struct B { A a; };
void main(){
    B b;
    int y = b.a.x;
}
"""
    assert Checker(source).check_from_source() == "Static checking passed"


def test_struct08():
    source = """
struct A { int x; };
struct B { A a; };
void main(){
    B b;
    int y = b.a.y;
}
"""
    assert "TypeMismatchInExpression" in Checker(source).check_from_source()


def test_struct09():
    source = """
struct A { int x; };
void main(){
    A a;
    a.x = "hello";
}
"""
    assert "TypeMismatchInStatement" in Checker(source).check_from_source()


def test_struct10():
    source = """
struct A { int x; };
void main(){
    A a;
    int y = a.x + "abc";
}
"""
    assert "TypeMismatchInExpression" in Checker(source).check_from_source()


def test_struct11():
    source = """
struct A { int x; };
struct B { int y; };
void main(){
    A a;
    B b;
    a = b;
}
"""
    assert "TypeMismatchInStatement" in Checker(source).check_from_source()


def test_struct12():
    source = """
struct A { int x; };
void main(){
    A a;
    if(a){
        int x = 1;
    }
}
"""
    assert "TypeMismatchInStatement" in Checker(source).check_from_source()


def test_struct13():
    source = """
struct A { int x; };
void main(){
    A a;
    while(a){
        int x = 1;
    }
}
"""
    assert "TypeMismatchInStatement" in Checker(source).check_from_source()


def test_struct14():
    source = """
struct A { int x; };
void main(){
    A a;
    int y = (a.x + 1) * (a.x + 2);
}
"""
    assert Checker(source).check_from_source() == "Static checking passed"


def test_struct15():
    source = """
struct A { int x; };
struct B { A a; };
struct C { B b; };
void main(){
    C c;
    c.b.a.x = 10;
}
"""
    assert Checker(source).check_from_source() == "Static checking passed"


def test_struct16():
    source = """
struct A { int x; int x; };
"""
    assert Checker(source).check_from_source() == "Redeclared(Member, x)"
    
# ============================================================================
# SECTION 10: SCOPE & BLOCK HANDLING
# ============================================================================

def test_scope01():
    source = """
void main(){
    int x = 1;
    {
        int y = x + 1;
    }
}
"""
    assert Checker(source).check_from_source() == "Static checking passed"


def test_scope02():
    source = """
void main(){
    int x = 1;
    {
        int x = 2;
        int y = x;
    }
}
"""
    assert Checker(source).check_from_source() == "Static checking passed"


def test_scope03():
    source = """
void main(){
    int x = 1;
    {
        int y = x;
    }
    y = 2;
}
"""
    assert Checker(source).check_from_source() == "UndeclaredIdentifier(y)"


def test_scope04():
    source = """
void main(){
    int x = 1;
    if(x){
        int y = x + 1;
    }
    int z = y;
}
"""
    assert Checker(source).check_from_source() == "UndeclaredIdentifier(y)"


def test_scope05():
    source = """
void main(){
    for(int i = 0; i < 5; i = i + 1){
        int x = i;
    }
    int y = i;
}
"""
    assert Checker(source).check_from_source() == "Static checking passed"


def test_scope06():
    source = """
void main(){
    int x = 1;
    while(x){
        int y = x;
        x = x - 1;
    }
    y = 2;
}
"""
    assert Checker(source).check_from_source() == "UndeclaredIdentifier(y)"


def test_scope07():
    source = """
void main(){
    int x = 1;
    {
        int y = x;
        {
            int z = y;
        }
    }
}
"""
    assert Checker(source).check_from_source() == "Static checking passed"


def test_scope08():
    source = """
void main(){
    int x = 1;
    {
        int y = x;
        {
            int z = y;
        }
        z = 2;
    }
}
"""
    assert Checker(source).check_from_source() == "UndeclaredIdentifier(z)"


def test_scope09():
    source = """
void main(){
    int x = 1;
    {
        int x = 2;
        {
            int x = 3;
        }
    }
}
"""
    assert Checker(source).check_from_source() == "Static checking passed"


def test_scope10():
    source = """
void main(){
    int x = 1;
    {
        int x = 2;
        int x = 3;
    }
}
"""
    assert Checker(source).check_from_source() == "Redeclared(Variable, x)"


def test_scope11():
    source = """
int f(int x){
    {
        int y = x;
    }
    return y;
}
"""
    assert Checker(source).check_from_source() == "UndeclaredIdentifier(y)"


def test_scope12():
    source = """
int f(int x){
    int y = x;
    {
        int y = 2;
    }
    return y;
}
"""
    assert Checker(source).check_from_source() == "Static checking passed"


def test_scope13():
    source = """
void main(){
    int x = 1;
    {
        int y = x;
    }
    {
        int y = 2;
    }
}
"""
    assert Checker(source).check_from_source() == "Static checking passed"


def test_scope14():
    source = """
void main(){
    int x = 1;
    {
        int y = x;
    }
    {
        int y = 2;
        int y = 3;
    }
}
"""
    assert Checker(source).check_from_source() == "Redeclared(Variable, y)"


def test_scope15():
    source = """
void main(){
    int x = 1;
    {
        int y = x;
        {
            int x = y;
        }
    }
}
"""
    assert Checker(source).check_from_source() == "Static checking passed"

# ============================================================================
# SECTION 11: COMPLEX MIXED PROGRAMS (STRESS TEST)
# ============================================================================

def test_complex01():
    source = """
struct A { int x; };
struct B { A a; };

int f(int x){
    if(x){
        return x + 1;
    }
    return x;
}

void main(){
    B b;
    b.a.x = f(10);
    int y = b.a.x + f(b.a.x);
}
"""
    assert Checker(source).check_from_source() == "Static checking passed"


def test_complex02():
    source = """
int f(int x){
    return x + 1;
}

int g(int y){
    int z = f(y) + f(y + 1);
    return z;
}

void main(){
    int x = 1;
    int y = g(x);
    int z = g(y + f(x));
}
"""
    assert Checker(source).check_from_source() == "Static checking passed"


def test_complex03():
    source = """
void main(){
    auto x = 1;
    auto y = x + 2;
    auto z = y + x;

    for(int i = 0; i < 5; i = i + 1){
        int t = z + i;
        while(t){
            t = t - 1;
        }
    }
}
"""
    assert Checker(source).check_from_source() == "Static checking passed"


def test_complex04():
    source = """
struct A { int x; };
void main(){
    A a;
    a.x = 1;

    if(a.x){
        int y = a.x + 2;
        while(y){
            y = y - 1;
        }
    }
}
"""
    assert Checker(source).check_from_source() == "Static checking passed"


def test_complex05():
    source = """
int f(int x){
    return x;
}

void main(){
    int x = 1;
    int y = f(f(f(f(x))));
    int z = (x + y) * (f(x) + f(y));
}
"""
    assert Checker(source).check_from_source() == "Static checking passed"


# ---------------------- INVALID / STRESS ----------------------

def test_complex06():
    source = """
struct A { int x; };
void main(){
    A a;
    a.x = 1;

    int y = a.x + "hello";

    if(y){
        int z = f(y);
    }

    y = z;
}
"""
    # multiple possible errors → mismatch + undeclared + function
    assert 'TypeMismatchInExpression(BinaryOp(MemberAccess(Identifier(a).x), +, StringLiteral(\'hello\')))' == Checker(source).check_from_source()


def test_complex07():
    source = """
int f(int x){
    if(x){
        return x;
    }
    return "hello";
}

void main(){
    int y = f(1);
    int z = f("abc");
}
"""
    assert 'TypeMismatchInStatement(ReturnStmt(return StringLiteral(\'hello\')))' == Checker(source).check_from_source()


def test_complex08():
    source = """
void main(){
    auto x;
    auto y;
    auto z;

    x = y;
    y = z;
    z = x;

    int a = x + 1;
}
"""
    assert Checker(source).check_from_source() == "TypeCannotBeInferred(AssignExpr(Identifier(x) = Identifier(y)))"


def test_complex09():
    source = """
struct A { int x; };
struct B { A a; };

void main(){
    B b;
    int x = b.a.y;

    while(x){
        break;
    }
}
"""
    assert "TypeMismatchInExpression" in Checker(source).check_from_source()


def test_complex10():
    source = """
void main(){
    int x = 1;

    for(int i = 0; i < 5; i = i + 1){
        int y = x + i;

        if(y){
            int z = y + f(i);
        }
    }

    int k = y + z;
}
"""
    assert Checker(source).check_from_source() == "UndeclaredFunction(f)"


def test_complex11():
    source = """
int f(int x){
    return x;
}

void main(){
    int x = 1;
    int y = f(x);

    {
        int x = "hello";
        int z = x + y;
    }

    y = x + z;
}
"""
    assert 'TypeMismatchInStatement(VarDecl(IntType(), x = StringLiteral(\'hello\')))' == Checker(source).check_from_source()


def test_complex12():
    source = """
void main(){
    auto x = 1;
    auto y = x + 2;

    {
        auto z;
        z = y + x;
        x = z;
    }

    y = x + z;
}
"""
    assert Checker(source).check_from_source() == "UndeclaredIdentifier(z)"


def test_complex13():
    source = """
struct A { int x; };
struct B { int y; };

void main(){
    A a;
    B b;

    a = b;

    int x = a.x + b.y;
}
"""
    assert 'TypeMismatchInStatement(AssignExpr(Identifier(a) = Identifier(b)))' == Checker(source).check_from_source()


def test_complex14():
    source = """
void main(){
    int x = 1;

    while(x){
        int y = x;
        break;
    }

    continue;
}
"""
    assert Checker(source).check_from_source() == "MustInLoop(ContinueStmt())"


def test_complex15():
    source = """
int f(int x){
    return x + 1;
}

void main(){
    int x = 1;

    int y = f(f(f("hello")));

    for(int i = 0; i < 5; i = i + 1){
        int z = y + i;
        while(z){
            z = z - 1;
        }
    }
}
"""
    assert 'TypeMismatchInExpression(FuncCall(f, [FuncCall(f, [FuncCall(f, [StringLiteral(\'hello\')])])]))' == Checker(source).check_from_source()
