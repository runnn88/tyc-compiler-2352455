"""
AST Generation test cases for TyC compiler.
TODO: Implement 100 test cases for AST generation
"""

import pytest
from tests.utils import ASTGenerator



# ==========================================================
# Program + Top-level Declarations
# ==========================================================

def test_empty_program():
    source = ""
    expected = "Program([])"
    assert str(ASTGenerator(source).generate()) == expected


def test_void_main_function():
    source = "void main(){}"
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([]))])"
    assert str(ASTGenerator(source).generate()) == expected


def test_int_main_returns_zero():
    source = "int main(){ return 0; }"
    expected = "Program([FuncDecl(IntType(), main, [], BlockStmt([ReturnStmt(return IntLiteral(0))]))])"
    assert str(ASTGenerator(source).generate()) == expected


def test_auto_function_without_declared_return_type():
    source = "f(){}"
    expected = "Program([FuncDecl(auto, f, [], BlockStmt([]))])"
    assert str(ASTGenerator(source).generate()) == expected


def test_auto_function_with_typed_parameters():
    source = "sum(int a, int b){ return a+b; }"
    expected = "Program([FuncDecl(auto, sum, [Param(IntType(), a), Param(IntType(), b)], BlockStmt([ReturnStmt(return BinaryOp(Identifier(a), +, Identifier(b)))]))])"
    assert str(ASTGenerator(source).generate()) == expected


def test_int_local_variable_declaration():
    source = "void main(){ int x; }"
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(IntType(), x)]))])"
    assert str(ASTGenerator(source).generate()) == expected


def test_float_local_variable_declaration():
    source = "void main(){ float x; }"
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(FloatType(), x)]))])"
    assert str(ASTGenerator(source).generate()) == expected


def test_string_local_variable_declaration():
    source = "void main(){ string s; }"
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(StringType(), s)]))])"
    assert str(ASTGenerator(source).generate()) == expected


def test_auto_local_variable_declaration():
    source = "void main(){ auto x; }"
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(auto, x)]))])"
    assert str(ASTGenerator(source).generate()) == expected


def test_auto_local_variable_with_initializer():
    source = "void main(){ auto x = 1; }"
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(auto, x = IntLiteral(1))]))])"
    assert str(ASTGenerator(source).generate()) == expected


def test_typed_int_local_variable_with_initializer():
    source = "void main(){ int x = 1; }"
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(IntType(), x = IntLiteral(1))]))])"
    assert str(ASTGenerator(source).generate()) == expected


def test_typed_float_local_variable_with_initializer():
    source = "void main(){ float x = 1.0; }"
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(FloatType(), x = FloatLiteral(1.0))]))])"
    assert str(ASTGenerator(source).generate()) == expected


def test_typed_string_local_variable_with_initializer():
    source = 'void main(){ string s = "ok"; }'
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(StringType(), s = StringLiteral('ok'))]))])"
    assert str(ASTGenerator(source).generate()) == expected


def test_struct_typed_local_variable_declaration():
    source = "void main(){ Point p; }"
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(StructType(Point), p)]))])"
    assert str(ASTGenerator(source).generate()) == expected


def test_multiple_top_level_functions():
    source = "void f(){} void main(){}"
    expected = "Program([FuncDecl(VoidType(), f, [], BlockStmt([])), FuncDecl(VoidType(), main, [], BlockStmt([]))])"
    assert str(ASTGenerator(source).generate()) == expected


def test_struct_then_main_function():
    source = "struct A{}; void main(){}"
    expected = "Program([StructDecl(A, []), FuncDecl(VoidType(), main, [], BlockStmt([]))])"
    assert str(ASTGenerator(source).generate()) == expected


def test_two_struct_declarations():
    source = "struct A{ int x; }; struct B{ float y; };"
    expected = "Program([StructDecl(A, [MemberDecl(IntType(), x)]), StructDecl(B, [MemberDecl(FloatType(), y)])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_program_with_interleaved_structs_and_functions():
    source = """
        struct Vec2{ float x; float y; };
        length(int dx, int dy){ return dx * dx + dy * dy; }
        struct Line{ Vec2 start; Vec2 end; };
        void main(){
            Vec2 origin = {0.0, 0.0};
            Line line = {{1.0, 2.0}, {3.0, 4.0}};
            auto len = length(1, 2);
        }
        """
    expected_parts = [
            "StructDecl(Vec2, [MemberDecl(FloatType(), x), MemberDecl(FloatType(), y)])",
            "FuncDecl(auto, length, [Param(IntType(), dx), Param(IntType(), dy)]",
            "ReturnStmt(return BinaryOp(BinaryOp(Identifier(dx), *, Identifier(dx)), +, BinaryOp(Identifier(dy), *, Identifier(dy))))",
            "StructDecl(Line, [MemberDecl(StructType(Vec2), start), MemberDecl(StructType(Vec2), end)])",
            "VarDecl(StructType(Line), line = StructLiteral({StructLiteral({FloatLiteral(1.0), FloatLiteral(2.0)}), StructLiteral({FloatLiteral(3.0), FloatLiteral(4.0)})}))",
        ]
    result = str(ASTGenerator(source).generate())
    assert "AST Generation Error" not in result
    for expected_part in expected_parts:
        assert expected_part in result


def test_program_with_multiple_function_signatures_and_calls():
    source = """
        struct Pair{ int left; int right; };
        int add(int a, int b){ return a + b; }
        Pair makePair(int x, int y){ return {x, y}; }
        void main(){
            Pair p = makePair(add(1, 2), add(3, 4));
        }
        """
    expected_parts = [
            "StructDecl(Pair, [MemberDecl(IntType(), left), MemberDecl(IntType(), right)])",
            "FuncDecl(IntType(), add, [Param(IntType(), a), Param(IntType(), b)]",
            "FuncDecl(StructType(Pair), makePair, [Param(IntType(), x), Param(IntType(), y)]",
            "ReturnStmt(return StructLiteral({Identifier(x), Identifier(y)}))",
            "VarDecl(StructType(Pair), p = FuncCall(makePair, [FuncCall(add, [IntLiteral(1), IntLiteral(2)]), FuncCall(add, [IntLiteral(3), IntLiteral(4)])]))",
        ]
    result = str(ASTGenerator(source).generate())
    assert "AST Generation Error" not in result
    for expected_part in expected_parts:
        assert expected_part in result


def test_program_with_nested_blocks_and_mixed_local_declarations():
    source = """
        void helper(int x, string msg){
            {
                int count = x;
                {
                    string inner = msg;
                    float scale = 1.5;
                }
            }
        }
        void main(){}
        """
    expected_parts = [
            "FuncDecl(VoidType(), helper, [Param(IntType(), x), Param(StringType(), msg)]",
            "VarDecl(IntType(), count = Identifier(x))",
            "VarDecl(StringType(), inner = Identifier(msg))",
            "VarDecl(FloatType(), scale = FloatLiteral(1.5))",
            "FuncDecl(VoidType(), main, [], BlockStmt([]))",
        ]
    result = str(ASTGenerator(source).generate())
    assert "AST Generation Error" not in result
    for expected_part in expected_parts:
        assert expected_part in result


def test_program_with_struct_members_using_multiple_declared_types():
    source = """
        struct Config{
            int retries;
            float timeout;
            string label;
        };
        void main(){
            Config cfg = {3, 2.5, "core"};
        }
        """
    expected_parts = [
            "StructDecl(Config, [MemberDecl(IntType(), retries), MemberDecl(FloatType(), timeout), MemberDecl(StringType(), label)])",
            "VarDecl(StructType(Config), cfg = StructLiteral({IntLiteral(3), FloatLiteral(2.5), StringLiteral('core')}))",
        ]
    result = str(ASTGenerator(source).generate())
    assert "AST Generation Error" not in result
    for expected_part in expected_parts:
        assert expected_part in result


def test_program_with_inferred_function_returning_complex_expression():
    source = """
        compute(int a, int b, int c){
            return (a + b) * c - (a = b = 1);
        }
        void main(){}
        """
    expected_parts = [
            "FuncDecl(auto, compute, [Param(IntType(), a), Param(IntType(), b), Param(IntType(), c)]",
            "ReturnStmt(return BinaryOp(BinaryOp(BinaryOp(Identifier(a), +, Identifier(b)), *, Identifier(c)), -, AssignExpr(Identifier(a) = AssignExpr(Identifier(b) = IntLiteral(1)))))",
        ]
    result = str(ASTGenerator(source).generate())
    assert "AST Generation Error" not in result
    for expected_part in expected_parts:
        assert expected_part in result


# ==========================================================
# Expressions + Precedence + Associativity
# ==========================================================

def test_simple_assignment_expression():
    source = "void main(){ x = 1; }"
    expected_part = "AssignExpr(Identifier(x) = IntLiteral(1))"
    result = str(ASTGenerator(source).generate())
    assert "AST Generation Error" not in result
    assert expected_part in result


def test_chained_assignment_is_right_associative():
    source = "void main(){ x = y = 5; }"
    expected_part = "AssignExpr(Identifier(x) = AssignExpr(Identifier(y) = IntLiteral(5)))"
    result = str(ASTGenerator(source).generate())
    assert "AST Generation Error" not in result
    assert expected_part in result


def test_multiplication_has_higher_precedence_than_addition():
    source = "void main(){ auto x = 1 + 2 * 3; }"
    expected_part = "BinaryOp(IntLiteral(1), +, BinaryOp(IntLiteral(2), *, IntLiteral(3)))"
    result = str(ASTGenerator(source).generate())
    assert "AST Generation Error" not in result
    assert expected_part in result


def test_parentheses_override_arithmetic_precedence():
    source = "void main(){ auto x = (1 + 2) * 3; }"
    expected_part = "BinaryOp(BinaryOp(IntLiteral(1), +, IntLiteral(2)), *, IntLiteral(3))"
    result = str(ASTGenerator(source).generate())
    assert "AST Generation Error" not in result
    assert expected_part in result


def test_logical_and_has_higher_precedence_than_or():
    source = "void main(){ auto x = 1 || 2 && 3; }"
    expected_part = "BinaryOp(IntLiteral(1), ||, BinaryOp(IntLiteral(2), &&, IntLiteral(3)))"
    result = str(ASTGenerator(source).generate())
    assert "AST Generation Error" not in result
    assert expected_part in result


def test_relational_expressions_bind_before_equality():
    source = "void main(){ auto x = a < b == c < d; }"
    expected_part = "BinaryOp(BinaryOp(Identifier(a), <, Identifier(b)), ==, BinaryOp(Identifier(c), <, Identifier(d)))"
    result = str(ASTGenerator(source).generate())
    assert "AST Generation Error" not in result
    assert expected_part in result


def test_prefix_increment_expression():
    source = "void main(){ ++x; }"
    expected_part = "PrefixOp(++Identifier(x))"
    result = str(ASTGenerator(source).generate())
    assert "AST Generation Error" not in result
    assert expected_part in result


def test_prefix_decrement_expression():
    source = "void main(){ --x; }"
    expected_part = "PrefixOp(--Identifier(x))"
    result = str(ASTGenerator(source).generate())
    assert "AST Generation Error" not in result
    assert expected_part in result


def test_postfix_increment_expression():
    source = "void main(){ x++; }"
    expected_part = "PostfixOp(Identifier(x)++)"
    result = str(ASTGenerator(source).generate())
    assert "AST Generation Error" not in result
    assert expected_part in result


def test_postfix_decrement_expression():
    source = "void main(){ x--; }"
    expected_part = "PostfixOp(Identifier(x)--)"
    result = str(ASTGenerator(source).generate())
    assert "AST Generation Error" not in result
    assert expected_part in result


def test_chained_unary_prefix_expression():
    source = "void main(){ auto x = !-+a; }"
    expected_part = "PrefixOp(!PrefixOp(-PrefixOp(+Identifier(a))))"
    result = str(ASTGenerator(source).generate())
    assert "AST Generation Error" not in result
    assert expected_part in result


def test_simple_member_access_expression():
    source = "void main(){ auto x = a.b; }"
    expected_part = "MemberAccess(Identifier(a).b)"
    result = str(ASTGenerator(source).generate())
    assert "AST Generation Error" not in result
    assert expected_part in result


def test_chained_member_access_expression():
    source = "void main(){ auto x = a.b.c; }"
    expected_part = "MemberAccess(MemberAccess(Identifier(a).b).c)"
    result = str(ASTGenerator(source).generate())
    assert "AST Generation Error" not in result
    assert expected_part in result


def test_function_call_without_arguments():
    source = "void main(){ f(); }"
    expected_part = "FuncCall(f, [])"
    result = str(ASTGenerator(source).generate())
    assert "AST Generation Error" not in result
    assert expected_part in result


def test_function_call_with_multiple_arguments():
    source = "void main(){ f(1,2,3); }"
    expected_part = "FuncCall(f, [IntLiteral(1), IntLiteral(2), IntLiteral(3)])"
    result = str(ASTGenerator(source).generate())
    assert "AST Generation Error" not in result
    assert expected_part in result


def test_nested_function_call_argument():
    source = "void main(){ auto x = g(f(1)); }"
    expected_part = "FuncCall(g, [FuncCall(f, [IntLiteral(1)])])"
    result = str(ASTGenerator(source).generate())
    assert "AST Generation Error" not in result
    assert expected_part in result


def test_simple_struct_literal_expression():
    source = "void main(){ auto x = {1,2}; }"
    expected_part = "StructLiteral({IntLiteral(1), IntLiteral(2)})"
    result = str(ASTGenerator(source).generate())
    assert "AST Generation Error" not in result
    assert expected_part in result


def test_nested_struct_literal_expression():
    source = "void main(){ auto x = {{1,2},3}; }"
    expected_part = "StructLiteral({StructLiteral({IntLiteral(1), IntLiteral(2)}), IntLiteral(3)})"
    result = str(ASTGenerator(source).generate())
    assert "AST Generation Error" not in result
    assert expected_part in result


def test_complex_expression_with_member_access_function_call_and_unary_ops():
    source = "void main(){ auto x = a.b.c + foo(1, bar(2), {3,{4,5}}) * -(d.e); }"
    expected_parts = [
            "MemberAccess(MemberAccess(Identifier(a).b).c)",
            "FuncCall(foo, [IntLiteral(1), FuncCall(bar, [IntLiteral(2)]), StructLiteral({IntLiteral(3), StructLiteral({IntLiteral(4), IntLiteral(5)})})])",
            "PrefixOp(-MemberAccess(Identifier(d).e))",
            "BinaryOp(MemberAccess(MemberAccess(Identifier(a).b).c), +, BinaryOp(FuncCall(foo, [IntLiteral(1), FuncCall(bar, [IntLiteral(2)]), StructLiteral({IntLiteral(3), StructLiteral({IntLiteral(4), IntLiteral(5)})})]), *, PrefixOp(-MemberAccess(Identifier(d).e))))",
        ]
    result = str(ASTGenerator(source).generate())
    assert "AST Generation Error" not in result
    for expected_part in expected_parts:
        assert expected_part in result


def test_complex_assignment_expression_with_nested_parentheses():
    source = "void main(){ x = y = (a + b * (c - d)) / e % f; }"
    expected_part = "AssignExpr(Identifier(x) = AssignExpr(Identifier(y) = BinaryOp(BinaryOp(BinaryOp(Identifier(a), +, BinaryOp(Identifier(b), *, BinaryOp(Identifier(c), -, Identifier(d)))), /, Identifier(e)), %, Identifier(f))))"
    result = str(ASTGenerator(source).generate())
    assert "AST Generation Error" not in result
    assert expected_part in result


def test_complex_logical_expression_with_embedded_assignments():
    source = "void main(){ auto flag = (a = 1) && (b = 2) || !c && d < e + f; }"
    expected_part = "BinaryOp(BinaryOp(AssignExpr(Identifier(a) = IntLiteral(1)), &&, AssignExpr(Identifier(b) = IntLiteral(2))), ||, BinaryOp(PrefixOp(!Identifier(c)), &&, BinaryOp(Identifier(d), <, BinaryOp(Identifier(e), +, Identifier(f)))))"
    result = str(ASTGenerator(source).generate())
    assert "AST Generation Error" not in result
    assert expected_part in result


def test_complex_expression_with_prefix_and_postfix_on_member_access():
    source = "void main(){ auto value = ++p.left + q.right-- * -r.mid.end; }"
    expected_part = "BinaryOp(PrefixOp(++MemberAccess(Identifier(p).left)), +, BinaryOp(PostfixOp(MemberAccess(Identifier(q).right)--), *, PrefixOp(-MemberAccess(MemberAccess(Identifier(r).mid).end))))"
    result = str(ASTGenerator(source).generate())
    assert "AST Generation Error" not in result
    assert expected_part in result


def test_complex_struct_literal_expression_inside_binary_expression():
    source = "void main(){ auto shape = {1, {2, 3}, foo(4)} == {1, {2, 3}, foo(4)}; }"
    expected_part = "BinaryOp(StructLiteral({IntLiteral(1), StructLiteral({IntLiteral(2), IntLiteral(3)}), FuncCall(foo, [IntLiteral(4)])}), ==, StructLiteral({IntLiteral(1), StructLiteral({IntLiteral(2), IntLiteral(3)}), FuncCall(foo, [IntLiteral(4)])}))"
    result = str(ASTGenerator(source).generate())
    assert "AST Generation Error" not in result
    assert expected_part in result


# ==========================================================
# Statements + Control Flow
# ==========================================================

def test_if_statement_without_else():
    source = "void main(){ if(1) x=1; }"
    expected_part = "IfStmt(if IntLiteral(1) then ExprStmt(AssignExpr(Identifier(x) = IntLiteral(1))))"
    result = str(ASTGenerator(source).generate())
    assert "AST Generation Error" not in result
    assert expected_part in result


def test_if_statement_with_else():
    source = "void main(){ if(1) x=1; else x=2; }"
    expected_part = "else ExprStmt(AssignExpr(Identifier(x) = IntLiteral(2)))"
    result = str(ASTGenerator(source).generate())
    assert "AST Generation Error" not in result
    assert expected_part in result


def test_while_statement_with_postfix_increment():
    source = "void main(){ while(1) x++; }"
    expected_part = "WhileStmt(while IntLiteral(1) do ExprStmt(PostfixOp(Identifier(x)++)))"
    result = str(ASTGenerator(source).generate())
    assert "AST Generation Error" not in result
    assert expected_part in result


def test_for_statement_with_variable_declaration_initializer():
    source = "void main(){ for(auto i=0;i<5;i++) x=1; }"
    expected_part = "ForStmt(for VarDecl(auto, i = IntLiteral(0)); BinaryOp(Identifier(i), <, IntLiteral(5)); PostfixOp(Identifier(i)++)"
    result = str(ASTGenerator(source).generate())
    assert "AST Generation Error" not in result
    assert expected_part in result


def test_for_statement_with_expression_initializer():
    source = "void main(){ for(i=0;i<5;++i) x=1; }"
    expected_part = "ForStmt(for ExprStmt(AssignExpr(Identifier(i) = IntLiteral(0))); BinaryOp(Identifier(i), <, IntLiteral(5)); PrefixOp(++Identifier(i))"
    result = str(ASTGenerator(source).generate())
    assert "AST Generation Error" not in result
    assert expected_part in result


def test_for_statement_with_all_clauses_empty():
    source = "void main(){ for(;;) break; }"
    expected_part = "ForStmt(for None; None; None do BreakStmt())"
    result = str(ASTGenerator(source).generate())
    assert "AST Generation Error" not in result
    assert expected_part in result


def test_break_statement():
    source = "void main(){ break; }"
    expected_part = "BreakStmt()"
    result = str(ASTGenerator(source).generate())
    assert "AST Generation Error" not in result
    assert expected_part in result


def test_continue_statement():
    source = "void main(){ continue; }"
    expected_part = "ContinueStmt()"
    result = str(ASTGenerator(source).generate())
    assert "AST Generation Error" not in result
    assert expected_part in result


def test_return_statement_without_value():
    source = "void main(){ return; }"
    expected_part = "ReturnStmt(return)"
    result = str(ASTGenerator(source).generate())
    assert "AST Generation Error" not in result
    assert expected_part in result


def test_return_statement_with_value():
    source = "int f(){ return 1; }"
    expected_part = "ReturnStmt(return IntLiteral(1))"
    result = str(ASTGenerator(source).generate())
    assert "AST Generation Error" not in result
    assert expected_part in result


def test_multiple_expression_statements_in_block():
    source = "void main(){ x=1; y=2; }"
    expected_part = "ExprStmt(AssignExpr(Identifier(y) = IntLiteral(2)))"
    result = str(ASTGenerator(source).generate())
    assert "AST Generation Error" not in result
    assert expected_part in result


def test_switch_statement_with_single_case():
    source = "void main(){ switch(x){ case 1: break; } }"
    expected_part = "CaseStmt(case IntLiteral(1): [BreakStmt()])"
    result = str(ASTGenerator(source).generate())
    assert "AST Generation Error" not in result
    assert expected_part in result


def test_switch_statement_with_default_case():
    source = "void main(){ switch(x){ default: break; } }"
    expected_part = "DefaultStmt(default: [BreakStmt()])"
    result = str(ASTGenerator(source).generate())
    assert "AST Generation Error" not in result
    assert expected_part in result


def test_switch_statement_with_case_and_default():
    source = "void main(){ switch(x){ case 1: x=1; default: x=2; } }"
    expected_part = "DefaultStmt(default: [ExprStmt(AssignExpr(Identifier(x) = IntLiteral(2)))])"
    result = str(ASTGenerator(source).generate())
    assert "AST Generation Error" not in result
    assert expected_part in result


def test_empty_switch_statement():
    source = "void main(){ switch(1){} }"
    expected_part = "SwitchStmt(switch IntLiteral(1) cases [])"
    result = str(ASTGenerator(source).generate())
    assert "AST Generation Error" not in result
    assert expected_part in result


def test_nested_block_statement():
    source = "void main(){ { x=1; } }"
    expected_part = "BlockStmt([ExprStmt(AssignExpr(Identifier(x) = IntLiteral(1)))])"
    result = str(ASTGenerator(source).generate())
    assert "AST Generation Error" not in result
    assert expected_part in result


def test_if_else_with_block_bodies():
    source = "void main(){ if(1){x=1;} else {x=2;} }"
    expected_part = "BlockStmt([ExprStmt(AssignExpr(Identifier(x) = IntLiteral(2)))])"
    result = str(ASTGenerator(source).generate())
    assert "AST Generation Error" not in result
    assert expected_part in result


def test_while_statement_with_block_body():
    source = "void main(){ while(1){break;} }"
    expected_part = "WhileStmt(while IntLiteral(1) do BlockStmt([BreakStmt()]))"
    result = str(ASTGenerator(source).generate())
    assert "AST Generation Error" not in result
    assert expected_part in result


def test_for_statement_with_only_condition_clause():
    source = "void main(){ for(;i<10;) i=i+1; }"
    expected_part = "ForStmt(for None; BinaryOp(Identifier(i), <, IntLiteral(10)); None"
    result = str(ASTGenerator(source).generate())
    assert "AST Generation Error" not in result
    assert expected_part in result


def test_switch_statement_with_fallthrough_cases():
    source = "void main(){ switch(x){ case 1: case 2: break; } }"
    expected_part = "CaseStmt(case IntLiteral(2): [BreakStmt()])"
    result = str(ASTGenerator(source).generate())
    assert "AST Generation Error" not in result
    assert expected_part in result


def test_nested_for_if_switch_statement_combination():
    source = """
        void main(){
            for(auto i=0; i<10 && ready; ++i){
                if(i<3) continue;
                else {
                    total = total + i;
                    switch(i){
                        case 5:
                            break;
                        default:
                            total = total + 1;
                    }
                }
            }
        }
        """
    expected_parts = [
            "ForStmt(for VarDecl(auto, i = IntLiteral(0)); BinaryOp(BinaryOp(Identifier(i), <, IntLiteral(10)), &&, Identifier(ready)); PrefixOp(++Identifier(i))",
            "IfStmt(if BinaryOp(Identifier(i), <, IntLiteral(3)) then ContinueStmt()",
            "CaseStmt(case IntLiteral(5): [BreakStmt()])",
            "DefaultStmt(default: [ExprStmt(AssignExpr(Identifier(total) = BinaryOp(Identifier(total), +, IntLiteral(1))))])",
        ]
    result = str(ASTGenerator(source).generate())
    assert "AST Generation Error" not in result
    for expected_part in expected_parts:
        assert expected_part in result


def test_while_statement_with_nested_if_else_blocks_and_returns():
    source = """
        int process(){
            while(a < b + c){
                if(flag){
                    a = a + 1;
                } else {
                    return a;
                }
            }
            return b;
        }
        """
    expected_parts = [
            "WhileStmt(while BinaryOp(Identifier(a), <, BinaryOp(Identifier(b), +, Identifier(c))) do BlockStmt([IfStmt(",
            "ExprStmt(AssignExpr(Identifier(a) = BinaryOp(Identifier(a), +, IntLiteral(1))))",
            "ReturnStmt(return Identifier(a))",
            "ReturnStmt(return Identifier(b))",
        ]
    result = str(ASTGenerator(source).generate())
    assert "AST Generation Error" not in result
    for expected_part in expected_parts:
        assert expected_part in result


def test_switch_statement_with_complex_case_bodies():
    source = """
        void main(){
            switch(x){
                case 1 + 2 * 3:
                    if(a) b = c;
                case -4:
                    while(d) { e = e + 1; }
                default:
                    { f = g = 0; }
            }
        }
        """
    expected_parts = [
            "CaseStmt(case BinaryOp(IntLiteral(1), +, BinaryOp(IntLiteral(2), *, IntLiteral(3))): [IfStmt(",
            "CaseStmt(case PrefixOp(-IntLiteral(4)): [WhileStmt(",
            "DefaultStmt(default: [BlockStmt([ExprStmt(AssignExpr(Identifier(f) = AssignExpr(Identifier(g) = IntLiteral(0))))])])",
        ]
    result = str(ASTGenerator(source).generate())
    assert "AST Generation Error" not in result
    for expected_part in expected_parts:
        assert expected_part in result


def test_for_statement_with_assignment_update_and_block_body():
    source = """
        void main(){
            for(i = start; i < limit; i = i + step){
                current = current + i;
                if(current > max) break;
            }
        }
        """
    expected_parts = [
            "ForStmt(for ExprStmt(AssignExpr(Identifier(i) = Identifier(start))); BinaryOp(Identifier(i), <, Identifier(limit)); AssignExpr(Identifier(i) = BinaryOp(Identifier(i), +, Identifier(step)))",
            "ExprStmt(AssignExpr(Identifier(current) = BinaryOp(Identifier(current), +, Identifier(i))))",
            "IfStmt(if BinaryOp(Identifier(current), >, Identifier(max)) then BreakStmt())",
        ]
    result = str(ASTGenerator(source).generate())
    assert "AST Generation Error" not in result
    for expected_part in expected_parts:
        assert expected_part in result


def test_if_else_chain_with_nested_blocks_and_calls():
    source = """
        void main(){
            if(check(1, 2, 3))
                { log(1); log(2); }
            else
                if(other)
                    result = compute(4, 5);
                else
                    { result = 0; }
        }
        """
    expected_parts = [
            "FuncCall(check, [IntLiteral(1), IntLiteral(2), IntLiteral(3)])",
            "BlockStmt([ExprStmt(FuncCall(log, [IntLiteral(1)])), ExprStmt(FuncCall(log, [IntLiteral(2)]))])",
            "IfStmt(if Identifier(other) then ExprStmt(AssignExpr(Identifier(result) = FuncCall(compute, [IntLiteral(4), IntLiteral(5)])))",
            "BlockStmt([ExprStmt(AssignExpr(Identifier(result) = IntLiteral(0)))])",
        ]
    result = str(ASTGenerator(source).generate())
    assert "AST Generation Error" not in result
    for expected_part in expected_parts:
        assert expected_part in result


# ==========================================================
# Struct-related Cases
# ==========================================================

def test_empty_struct_declaration():
    source = "struct S{};"
    expected_part = "StructDecl(S, [])"
    result = str(ASTGenerator(source).generate())
    assert "AST Generation Error" not in result
    assert expected_part in result


def test_struct_member_declared_as_int():
    source = "struct S{ int x; };"
    expected_part = "MemberDecl(IntType(), x)"
    result = str(ASTGenerator(source).generate())
    assert "AST Generation Error" not in result
    assert expected_part in result


def test_struct_member_declared_as_float():
    source = "struct S{ float x; };"
    expected_part = "MemberDecl(FloatType(), x)"
    result = str(ASTGenerator(source).generate())
    assert "AST Generation Error" not in result
    assert expected_part in result


def test_struct_member_declared_as_string():
    source = "struct S{ string x; };"
    expected_part = "MemberDecl(StringType(), x)"
    result = str(ASTGenerator(source).generate())
    assert "AST Generation Error" not in result
    assert expected_part in result


def test_struct_member_declared_as_struct_type():
    source = "struct A{ int x; }; struct B{ A a; };"
    expected_part = "StructDecl(B, [MemberDecl(StructType(A), a)])"
    result = str(ASTGenerator(source).generate())
    assert "AST Generation Error" not in result
    assert expected_part in result


def test_struct_typed_variable_declaration():
    source = "void main(){ A a; }"
    expected_part = "VarDecl(StructType(A), a)"
    result = str(ASTGenerator(source).generate())
    assert "AST Generation Error" not in result
    assert expected_part in result


def test_struct_typed_variable_initialized_with_empty_literal():
    source = "void main(){ A a = {}; }"
    expected_part = "VarDecl(StructType(A), a = StructLiteral({}))"
    result = str(ASTGenerator(source).generate())
    assert "AST Generation Error" not in result
    assert expected_part in result


def test_struct_typed_variable_initialized_with_single_value_literal():
    source = "void main(){ A a = {1}; }"
    expected_part = "StructLiteral({IntLiteral(1)})"
    result = str(ASTGenerator(source).generate())
    assert "AST Generation Error" not in result
    assert expected_part in result


def test_struct_typed_variable_initialized_with_nested_literal():
    source = "void main(){ A a = {{1},2}; }"
    expected_part = "StructLiteral({StructLiteral({IntLiteral(1)}), IntLiteral(2)})"
    result = str(ASTGenerator(source).generate())
    assert "AST Generation Error" not in result
    assert expected_part in result


def test_member_access_used_as_statement():
    source = "void main(){ p.x; }"
    expected_part = "ExprStmt(MemberAccess(Identifier(p).x))"
    result = str(ASTGenerator(source).generate())
    assert "AST Generation Error" not in result
    assert expected_part in result


def test_chained_member_access_used_as_statement():
    source = "void main(){ p.x.y; }"
    expected_part = "MemberAccess(MemberAccess(Identifier(p).x).y)"
    result = str(ASTGenerator(source).generate())
    assert "AST Generation Error" not in result
    assert expected_part in result


def test_assign_literal_to_struct_member():
    source = "void main(){ p.x = 1; }"
    expected_part = "AssignExpr(MemberAccess(Identifier(p).x) = IntLiteral(1))"
    result = str(ASTGenerator(source).generate())
    assert "AST Generation Error" not in result
    assert expected_part in result


def test_assign_member_access_to_struct_member():
    source = "void main(){ p.x = q.y; }"
    expected_part = "AssignExpr(MemberAccess(Identifier(p).x) = MemberAccess(Identifier(q).y))"
    result = str(ASTGenerator(source).generate())
    assert "AST Generation Error" not in result
    assert expected_part in result


def test_auto_variable_initialized_from_member_access():
    source = "void main(){ auto v = p.x; }"
    expected_part = "VarDecl(auto, v = MemberAccess(Identifier(p).x))"
    result = str(ASTGenerator(source).generate())
    assert "AST Generation Error" not in result
    assert expected_part in result


def test_member_access_inside_binary_expression():
    source = "void main(){ auto v = p.x + 1; }"
    expected_part = "BinaryOp(MemberAccess(Identifier(p).x), +, IntLiteral(1))"
    result = str(ASTGenerator(source).generate())
    assert "AST Generation Error" not in result
    assert expected_part in result


def test_deep_member_access_chain():
    source = "void main(){ p.a.b.c.d; }"
    expected_part = "MemberAccess(MemberAccess(MemberAccess(MemberAccess(Identifier(p).a).b).c).d)"
    result = str(ASTGenerator(source).generate())
    assert "AST Generation Error" not in result
    assert expected_part in result


def test_nested_struct_literal_with_mixed_values():
    source = "void main(){ auto s = {1,{2,3}}; }"
    expected_part = "StructLiteral({IntLiteral(1), StructLiteral({IntLiteral(2), IntLiteral(3)})})"
    result = str(ASTGenerator(source).generate())
    assert "AST Generation Error" not in result
    assert expected_part in result


def test_struct_literal_passed_as_function_argument():
    source = "void main(){ f({1,2}); }"
    expected_part = "FuncCall(f, [StructLiteral({IntLiteral(1), IntLiteral(2)})])"
    result = str(ASTGenerator(source).generate())
    assert "AST Generation Error" not in result
    assert expected_part in result


def test_member_access_on_function_call_result():
    source = "void main(){ auto x = getP().x; }"
    expected_part = "MemberAccess(FuncCall(getP, []).x)"
    result = str(ASTGenerator(source).generate())
    assert "AST Generation Error" not in result
    assert expected_part in result


def test_struct_declaration_with_multiple_nested_struct_members():
    source = """
        struct Point{ int x; int y; };
        struct Segment{ Point start; Point end; string name; };
        void main(){
            Segment s = {{1, 2}, {3, 4}, "edge"};
        }
        """
    expected_parts = [
            "StructDecl(Point, [MemberDecl(IntType(), x), MemberDecl(IntType(), y)])",
            "StructDecl(Segment, [MemberDecl(StructType(Point), start), MemberDecl(StructType(Point), end), MemberDecl(StringType(), name)])",
            "VarDecl(StructType(Segment), s = StructLiteral({StructLiteral({IntLiteral(1), IntLiteral(2)}), StructLiteral({IntLiteral(3), IntLiteral(4)}), StringLiteral('edge')}))",
        ]
    result = str(ASTGenerator(source).generate())
    assert "AST Generation Error" not in result
    for expected_part in expected_parts:
        assert expected_part in result


def test_nested_struct_literals_inside_function_arguments_and_assignment():
    source = """
        void main(){
            Matrix m = {{{1, 2}, {3, 4}}, {{5, 6}, {7, 8}}};
            apply(m, {{9, 10}, {11, 12}});
        }
        """
    expected_parts = [
            "VarDecl(StructType(Matrix), m = StructLiteral({StructLiteral({StructLiteral({IntLiteral(1), IntLiteral(2)}), StructLiteral({IntLiteral(3), IntLiteral(4)})}), StructLiteral({StructLiteral({IntLiteral(5), IntLiteral(6)}), StructLiteral({IntLiteral(7), IntLiteral(8)})})}))",
            "FuncCall(apply, [Identifier(m), StructLiteral({StructLiteral({IntLiteral(9), IntLiteral(10)}), StructLiteral({IntLiteral(11), IntLiteral(12)})})])",
        ]
    result = str(ASTGenerator(source).generate())
    assert "AST Generation Error" not in result
    for expected_part in expected_parts:
        assert expected_part in result


def test_deep_member_access_assignment_with_binary_expression():
    source = """
        void main(){
            world.region.city.center.x = world.region.city.center.x + offset.value;
        }
        """
    expected_parts = [
            "AssignExpr(MemberAccess(MemberAccess(MemberAccess(MemberAccess(Identifier(world).region).city).center).x) = BinaryOp(MemberAccess(MemberAccess(MemberAccess(MemberAccess(Identifier(world).region).city).center).x), +, MemberAccess(Identifier(offset).value)))",
        ]
    result = str(ASTGenerator(source).generate())
    assert "AST Generation Error" not in result
    for expected_part in expected_parts:
        assert expected_part in result


def test_struct_member_access_combined_with_prefix_postfix_and_calls():
    source = """
        void main(){
            auto score = ++player.stats.level + enemy.stats.hp-- + bonus(multiplier.value, player.stats.level);
        }
        """
    expected_parts = [
            "PrefixOp(++MemberAccess(MemberAccess(Identifier(player).stats).level))",
            "PostfixOp(MemberAccess(MemberAccess(Identifier(enemy).stats).hp)--)",
            "FuncCall(bonus, [MemberAccess(Identifier(multiplier).value), MemberAccess(MemberAccess(Identifier(player).stats).level)])",
        ]
    result = str(ASTGenerator(source).generate())
    assert "AST Generation Error" not in result
    for expected_part in expected_parts:
        assert expected_part in result


def test_member_access_on_function_result_followed_by_deeper_access():
    source = """
        void main(){
            auto code = getState().current.mode.level;
        }
        """
    expected_parts = [
            "MemberAccess(MemberAccess(MemberAccess(FuncCall(getState, []).current).mode).level)",
        ]
    result = str(ASTGenerator(source).generate())
    assert "AST Generation Error" not in result
    for expected_part in expected_parts:
        assert expected_part in result


# ==========================================================
# Invalid Cases
# ==========================================================

def test_invalid_function_header_missing_parenthesis():
    source = "void main( { }"
    expected_part = "AST Generation Error"
    result = str(ASTGenerator(source).generate())
    assert expected_part in result


def test_invalid_variable_declaration_missing_semicolon():
    source = "void main(){ int x }"
    expected_part = "AST Generation Error"
    result = str(ASTGenerator(source).generate())
    assert expected_part in result


def test_invalid_auto_declaration_missing_identifier():
    source = "void main(){ auto = 1; }"
    expected_part = "AST Generation Error"
    result = str(ASTGenerator(source).generate())
    assert expected_part in result


def test_invalid_auto_declaration_missing_initializer_expression():
    source = "void main(){ auto x = ; }"
    expected_part = "AST Generation Error"
    result = str(ASTGenerator(source).generate())
    assert expected_part in result


def test_invalid_if_statement_missing_then_branch():
    source = "void main(){ if(1) else x=2; }"
    expected_part = "AST Generation Error"
    result = str(ASTGenerator(source).generate())
    assert expected_part in result


def test_invalid_while_statement_missing_open_parenthesis():
    source = "void main(){ while 1) x++; }"
    expected_part = "AST Generation Error"
    result = str(ASTGenerator(source).generate())
    assert expected_part in result


def test_invalid_for_statement_missing_first_semicolon():
    source = "void main(){ for(auto i=0 i<5; i++) x=1; }"
    expected_part = "AST Generation Error"
    result = str(ASTGenerator(source).generate())
    assert expected_part in result


def test_invalid_for_statement_missing_second_semicolon():
    source = "void main(){ for(auto i=0;i<5 i++) x=1; }"
    expected_part = "AST Generation Error"
    result = str(ASTGenerator(source).generate())
    assert expected_part in result


def test_invalid_for_statement_with_extra_semicolon():
    source = "void main(){ for(;;;) x=1; }"
    expected_part = "AST Generation Error"
    result = str(ASTGenerator(source).generate())
    assert expected_part in result


def test_invalid_switch_case_missing_colon():
    source = "void main(){ switch(x){ case 1 x=1; } }"
    expected_part = "AST Generation Error"
    result = str(ASTGenerator(source).generate())
    assert expected_part in result


def test_invalid_switch_with_duplicate_default():
    source = "void main(){ switch(x){ default: break; default: break; } }"
    expected_part = "AST Generation Error"
    result = str(ASTGenerator(source).generate())
    assert expected_part in result


def test_invalid_struct_declaration_missing_trailing_semicolon():
    source = "struct A{ int x; }"
    expected_part = "AST Generation Error"
    result = str(ASTGenerator(source).generate())
    assert expected_part in result


def test_invalid_struct_declaration_missing_open_brace():
    source = "struct A int x; };"
    expected_part = "AST Generation Error"
    result = str(ASTGenerator(source).generate())
    assert expected_part in result


def test_invalid_struct_literal_with_trailing_comma():
    source = "void main(){ Point p = {1,}; }"
    expected_part = "AST Generation Error"
    result = str(ASTGenerator(source).generate())
    assert expected_part in result


def test_invalid_struct_literal_with_leading_comma():
    source = "void main(){ Point p = {,1}; }"
    expected_part = "AST Generation Error"
    result = str(ASTGenerator(source).generate())
    assert expected_part in result


def test_invalid_member_access_with_double_dot():
    source = "void main(){ p..x = 1; }"
    expected_part = "AST Generation Error"
    result = str(ASTGenerator(source).generate())
    assert expected_part in result


def test_invalid_call_on_member_access_target():
    source = "void main(){ a.b(1); }"
    expected_part = "Function call target must be an identifier"
    result = str(ASTGenerator(source).generate())
    assert expected_part in result


def test_invalid_call_on_parenthesized_member_access_target():
    source = "void main(){ (a.b)(1); }"
    expected_part = "Function call target must be an identifier"
    result = str(ASTGenerator(source).generate())
    assert expected_part in result


def test_invalid_call_on_nested_parenthesized_member_access_target():
    source = "void main(){ ((a.b.c))(1,2); }"
    expected_part = "Function call target must be an identifier"
    result = str(ASTGenerator(source).generate())
    assert expected_part in result


def test_invalid_call_on_member_of_function_result():
    source = "void main(){ foo().bar(1); }"
    expected_part = "Function call target must be an identifier"
    result = str(ASTGenerator(source).generate())
    assert expected_part in result


def test_invalid_program_missing_struct_semicolon_after_complex_body():
    source = """
        struct Config{
            int retries;
            float timeout;
            string label;
        }
        void main(){ Config c = {1, 2.0, "x"}; }
        """
    expected_part = "AST Generation Error"
    result = str(ASTGenerator(source).generate())
    assert expected_part in result


def test_invalid_for_statement_missing_separator_in_complex_header():
    source = """
        void main(){
            for(auto i = 0; i < 10 && ready ++i){
                total = total + i;
            }
        }
        """
    expected_part = "AST Generation Error"
    result = str(ASTGenerator(source).generate())
    assert expected_part in result


def test_invalid_switch_with_duplicate_default_in_long_body():
    source = """
        void main(){
            switch(x){
                case 1:
                    total = total + 1;
                default:
                    total = 0;
                case 2:
                    total = total + 2;
                default:
                    total = total + 3;
            }
        }
        """
    expected_part = "AST Generation Error"
    result = str(ASTGenerator(source).generate())
    assert expected_part in result


def test_invalid_struct_literal_with_deep_trailing_comma():
    source = """
        void main(){
            Matrix m = {{{1, 2}, {3, 4}}, {{5, 6}, {7, 8}},};
        }
        """
    expected_part = "AST Generation Error"
    result = str(ASTGenerator(source).generate())
    assert expected_part in result


def test_invalid_function_call_target_on_deep_member_chain():
    source = """
        void main(){
            engine.current.mode.run(1, 2, 3);
        }
        """
    expected_part = "Function call target must be an identifier"
    result = str(ASTGenerator(source).generate())
    assert expected_part in result


# ==========================================================
# Random Mixed Cases
# ==========================================================

def test_random_assignment_after_auto_declaration():
    source = "void main(){ auto x = 1; x = x + 1; }"
    expected_part = "AssignExpr(Identifier(x) = BinaryOp(Identifier(x), +, IntLiteral(1)))"
    result = str(ASTGenerator(source).generate())
    assert "AST Generation Error" not in result
    assert expected_part in result


def test_random_nested_unary_negation_expression():
    source = "void main(){ auto x = -(-1); }"
    expected_part = "PrefixOp(-PrefixOp(-IntLiteral(1)))"
    result = str(ASTGenerator(source).generate())
    assert "AST Generation Error" not in result
    assert expected_part in result


def test_random_deeply_parenthesized_addition_expression():
    source = "void main(){ auto x = ((1+2)); }"
    expected_part = "BinaryOp(IntLiteral(1), +, IntLiteral(2))"
    result = str(ASTGenerator(source).generate())
    assert "AST Generation Error" not in result
    assert expected_part in result


def test_random_deeply_nested_blocks():
    source = "void main(){ { { { x=1; } } } }"
    expected_part = "BlockStmt([BlockStmt([BlockStmt([ExprStmt(AssignExpr(Identifier(x) = IntLiteral(1)))])])])"
    result = str(ASTGenerator(source).generate())
    assert "AST Generation Error" not in result
    assert expected_part in result


def test_random_triple_assignment_chain():
    source = "void main(){ x = y = z = 0; }"
    expected_part = "AssignExpr(Identifier(x) = AssignExpr(Identifier(y) = AssignExpr(Identifier(z) = IntLiteral(0))))"
    result = str(ASTGenerator(source).generate())
    assert "AST Generation Error" not in result
    assert expected_part in result


def test_random_nested_if_else_binds_to_nearest_if():
    source = "void main(){ if(1) if(2) x=1; else x=2; }"
    expected_part = "IfStmt(if IntLiteral(1) then IfStmt(if IntLiteral(2) then"
    result = str(ASTGenerator(source).generate())
    assert "AST Generation Error" not in result
    assert expected_part in result


def test_random_long_mixed_nested_loops_and_assignments():
    source = """
        void main(){
            auto total = 0;
            while(i < 10){
                for(j = 0; j < 3; ++j){
                    total = total + i + j;
                }
                i = i + 1;
            }
        }
        """
    expected_parts = [
            "VarDecl(auto, total = IntLiteral(0))",
            "WhileStmt(while BinaryOp(Identifier(i), <, IntLiteral(10)) do BlockStmt([ForStmt(",
            "AssignExpr(Identifier(total) = BinaryOp(BinaryOp(Identifier(total), +, Identifier(i)), +, Identifier(j)))",
        ]
    result = str(ASTGenerator(source).generate())
    assert "AST Generation Error" not in result
    for expected_part in expected_parts:
        assert expected_part in result


def test_random_long_mixed_switch_with_nested_blocks():
    source = """
        void main(){
            switch(kind){
                case 1:
                    { x = 1; y = 2; }
                case 2:
                    { if(flag) y = y + 1; }
                default:
                    { z = z + 1; }
            }
        }
        """
    expected_parts = [
            "CaseStmt(case IntLiteral(1): [BlockStmt([ExprStmt(AssignExpr(Identifier(x) = IntLiteral(1))), ExprStmt(AssignExpr(Identifier(y) = IntLiteral(2)))])])",
            "CaseStmt(case IntLiteral(2): [BlockStmt([IfStmt(",
            "DefaultStmt(default: [BlockStmt([ExprStmt(AssignExpr(Identifier(z) = BinaryOp(Identifier(z), +, IntLiteral(1))))])])",
        ]
    result = str(ASTGenerator(source).generate())
    assert "AST Generation Error" not in result
    for expected_part in expected_parts:
        assert expected_part in result


def test_random_long_mixed_structs_calls_and_member_access():
    source = """
        void main(){
            Node n = {{1, 2}, {3, 4}};
            auto value = combine(n.left.x, n.right.y, {5, 6});
        }
        """
    expected_parts = [
            "VarDecl(StructType(Node), n = StructLiteral({StructLiteral({IntLiteral(1), IntLiteral(2)}), StructLiteral({IntLiteral(3), IntLiteral(4)})}))",
            "FuncCall(combine, [MemberAccess(MemberAccess(Identifier(n).left).x), MemberAccess(MemberAccess(Identifier(n).right).y), StructLiteral({IntLiteral(5), IntLiteral(6)})])",
        ]
    result = str(ASTGenerator(source).generate())
    assert "AST Generation Error" not in result
    for expected_part in expected_parts:
        assert expected_part in result


def test_random_long_mixed_returning_complex_expression():
    source = """
        int score(int a, int b, int c){
            return (a + b) * (c - 1) + adjust(a, b);
        }
        """
    expected_parts = [
            "ReturnStmt(return BinaryOp(BinaryOp(BinaryOp(Identifier(a), +, Identifier(b)), *, BinaryOp(Identifier(c), -, IntLiteral(1))), +, FuncCall(adjust, [Identifier(a), Identifier(b)])))",
        ]
    result = str(ASTGenerator(source).generate())
    assert "AST Generation Error" not in result
    for expected_part in expected_parts:
        assert expected_part in result


def test_random_long_invalid_missing_brace_in_nested_construct():
    source = """
        void main(){
            if(flag){
                while(count){
                    total = total + 1;
            }
        }
        """
    expected_part = "AST Generation Error"
    result = str(ASTGenerator(source).generate())
    assert expected_part in result
