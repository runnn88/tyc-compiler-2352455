import pytest
from tests.utils import Parser

# =========================================================
# SECTION 1: PROGRAM STRUCTURE
# =========================================================

def test_empty_program():
    source = ""
    assert Parser(source).parse() == "success"


def test_only_main_function():
    source = "void main() {}"
    assert Parser(source).parse() == "success"


def test_only_struct_declaration():
    source = "struct A { int x; };"
    assert Parser(source).parse() == "success"


def test_struct_then_function():
    source = """
    struct A { int x; };
    void main() {}
    """
    assert Parser(source).parse() == "success"


def test_multiple_functions():
    source = """
    int f() { return 1; }
    void g() {}
    """
    assert Parser(source).parse() == "success"


def test_invalid_struct_missing_name():
    source = "struct { int x; };"
    assert Parser(source).parse() != "success"


def test_invalid_function_missing_name():
    source = "void () {}"
    assert Parser(source).parse() != "success"


def test_invalid_function_missing_body():
    source = "void main();"
    assert Parser(source).parse() != "success"


def test_invalid_top_level_block():
    source = "{ int x; }"
    assert Parser(source).parse() != "success"


def test_invalid_struct_missing_semicolon():
    source = "struct A { int x; }"
    assert Parser(source).parse() != "success"


# =========================================================
# SECTION 2: IDENTIFIERS & KEYWORDS (SYNTAX ONLY)
# =========================================================

def test_identifier_simple():
    source = "void main() { int x; }"
    assert Parser(source).parse() == "success"


def test_identifier_with_underscore():
    source = "void main() { int _x; }"
    assert Parser(source).parse() == "success"


def test_identifier_with_digits():
    source = "void main() { int x1; }"
    assert Parser(source).parse() == "success"


def test_identifier_case_sensitive():
    source = "void main() { int X; int x; }"
    assert Parser(source).parse() == "success"


def test_identifier_long():
    source = "void main() { int very_long_identifier_123; }"
    assert Parser(source).parse() == "success"


def test_invalid_identifier_start_digit():
    source = "void main() { int 1x; }"
    assert Parser(source).parse() != "success"


def test_invalid_identifier_keyword():
    source = "void main() { int if; }"
    assert Parser(source).parse() != "success"


def test_invalid_identifier_symbol():
    source = "void main() { int x-y; }"
    assert Parser(source).parse() != "success"


def test_invalid_identifier_space():
    source = "void main() { int x y; }"
    assert Parser(source).parse() != "success"


def test_invalid_identifier_empty():
    source = "void main() { int ; }"
    assert Parser(source).parse() != "success"


# =========================================================
# SECTION 3: LITERALS (PARSE-LEVEL ONLY)
# =========================================================

def test_integer_literal():
    source = "void main() { auto x = 10; }"
    assert Parser(source).parse() == "success"


def test_negative_integer_literal():
    source = "void main() { auto x = -5; }"
    assert Parser(source).parse() == "success"


def test_float_literal():
    source = "void main() { auto x = 3.14; }"
    assert Parser(source).parse() == "success"


def test_float_leading_dot():
    source = "void main() { auto x = .5; }"
    assert Parser(source).parse() == "success"


def test_string_literal():
    source = 'void main() { auto s = "hello"; }'
    assert Parser(source).parse() == "success"


def test_invalid_unclosed_string():
    source = 'void main() { auto s = "hello; }'
    assert Parser(source).parse() != "success"


def test_invalid_string_newline():
    source = 'void main() { auto s = "hello\n"; }'
    assert Parser(source).parse() != "success"


def test_invalid_char_literal():
    source = "void main() { auto c = 'a'; }"
    assert Parser(source).parse() != "success"


def test_invalid_float_double_dot():
    source = "void main() { auto x = 1..2; }"
    assert Parser(source).parse() != "success"


def test_invalid_exponent_literal():
    source = "void main() { auto x = 1e; }"
    assert Parser(source).parse() != "success"


# =========================================================
# SECTION 4: TYPES & VARIABLE DECLARATIONS (SYNTAX ONLY)
# =========================================================

def test_auto_without_init():
    source = "void main() { auto x; }"
    assert Parser(source).parse() == "success"


def test_auto_with_init():
    source = "void main() { auto x = 1; }"
    assert Parser(source).parse() == "success"


def test_explicit_int_decl():
    source = "void main() { int x; }"
    assert Parser(source).parse() == "success"


def test_explicit_float_decl():
    source = "void main() { float y = 1.2; }"
    assert Parser(source).parse() == "success"


def test_struct_type_decl_syntax_only():
    source = "void main() { Point p; }"
    assert Parser(source).parse() == "success"


def test_invalid_auto_missing_identifier():
    source = "void main() { auto = 1; }"
    assert Parser(source).parse() != "success"


def test_invalid_decl_missing_identifier():
    source = "void main() { int ; }"
    assert Parser(source).parse() != "success"


def test_invalid_missing_semicolon():
    source = "void main() { int x }"
    assert Parser(source).parse() != "success"


def test_invalid_auto_missing_expr():
    source = "void main() { auto x = ; }"
    assert Parser(source).parse() != "success"


def test_invalid_multiple_identifiers():
    source = "void main() { int x y; }"
    assert Parser(source).parse() != "success"


# =========================================================
# SECTION 5: EXPRESSIONS (HEAVY CHAINING / STRESS TESTS)
# =========================================================

def test_postfix_then_binary_then_prefix():
    source = "void main() { ++x + y++ * -z; }"
    assert Parser(source).parse() == "success"


def test_multiple_prefix_chain():
    source = "void main() { !!!++--x; }"
    assert Parser(source).parse() == "success"


def test_multiple_postfix_chain():
    source = "void main() { x+++++y; }"
    assert Parser(source).parse() == "success"


def test_assignment_chain_deep():
    source = "void main() { a = b = c = d = e = 1; }"
    assert Parser(source).parse() == "success"


def test_assignment_inside_expression_chain():
    source = "void main() { (a = b = c = 1) + (d = 2); }"
    assert Parser(source).parse() == "success"


def test_member_access_chain():
    source = "void main() { a.b.c.d.e; }"
    assert Parser(source).parse() == "success"


def test_member_access_with_prefix_postfix():
    source = "void main() { ++a.b--.c; }"
    assert Parser(source).parse() == "success"


def test_call_chain_simple():
    source = "void main() { f()(); }"
    assert Parser(source).parse() == "success"


def test_call_then_member_then_call():
    source = "void main() { f().g().h(1, 2, x); }"
    assert Parser(source).parse() == "success"


def test_call_with_complex_args():
    source = "void main() { f(a = b = 1, ++x, y++ * (z + 1)); }"
    assert Parser(source).parse() == "success"


def test_postfix_on_call_result():
    source = "void main() { f(x)++; }"
    assert Parser(source).parse() == "success"


def test_nested_parentheses_everywhere():
    source = "void main() { (((x))) = (((y))); }"
    assert Parser(source).parse() == "success"


def test_logical_chain_with_assignments():
    source = "void main() { a = b && c || d && (e = f); }"
    assert Parser(source).parse() == "success"


def test_relational_chain_with_arithmetic():
    source = "void main() { (a + b * c) < (d - e / f); }"
    assert Parser(source).parse() == "success"


def test_extreme_mixed_expression():
    source = """
    void main() {
        a = ++b.c--.d.e(f(1, g(2)), h()) * -(i + j++)
            && k || l = m = n++;
    }
    """
    assert Parser(source).parse() == "success"


# ---------------- INVALID EXPRESSIONS ----------------

def test_invalid_double_binary_op():
    source = "void main() { a + * b; }"
    assert Parser(source).parse() != "success"


def test_invalid_missing_operand_chain():
    source = "void main() { a = b + ; }"
    assert Parser(source).parse() != "success"


def test_invalid_unbalanced_parens_complex():
    source = "void main() { ((a + b) * (c - d); }"
    assert Parser(source).parse() != "success"


# =========================================================
# SECTION 6: STATEMENTS (COMPLEX FORMS)
# =========================================================

def test_expression_statement_complex():
    source = "void main() { ++a.b--.c(d = e = 1, f()) * g++; }"
    assert Parser(source).parse() == "success"


def test_nested_blocks_with_exprs():
    source = "void main() { { { x = y = z++; } } }"
    assert Parser(source).parse() == "success"


def test_multiple_statements_sequence():
    source = """
    void main() {
        a = b = 1;
        ++a;
        b++;
        (a + b) * c;
    }
    """
    assert Parser(source).parse() == "success"


def test_statement_with_call_assignment_mix():
    source = "void main() { f(a = b++, c = ++d); }"
    assert Parser(source).parse() == "success"


def test_block_with_only_complex_exprs():
    source = "void main() { { a = b = c = d++; } }"
    assert Parser(source).parse() == "success"


def test_invalid_statement_missing_semicolon_complex():
    source = "void main() { a = b = c++ }"
    assert Parser(source).parse() != "success"


def test_invalid_statement_only_prefix_chain():
    source = "void main() { ++++; }"
    assert Parser(source).parse() != "success"


def test_invalid_block_expression_leak():
    source = "void main() { { a = b } }"
    assert Parser(source).parse() != "success"


# =========================================================
# SECTION 7: CONTROL FLOW (COMPLEX CONDITIONS & BODIES)
# =========================================================

def test_if_with_extreme_condition():
    source = """
    void main() {
        if (++a.b--.c(d()) * e < f && g || h + i++)
            j = k = l++;
    }
    """
    assert Parser(source).parse() == "success"


def test_if_else_nested_complex():
    source = """
    void main() {
        if (a)
            if (b = c++)
                d++;
            else
                e = f(g());
    }
    """
    assert Parser(source).parse() == "success"


def test_while_with_assignment_condition():
    source = "void main() { while (x = y = z++) a++; }"
    assert Parser(source).parse() == "success"


def test_while_block_heavy():
    source = """
    void main() {
        while ((a + b) * c < d) {
            ++x;
            y = z++;
        }
    }
    """
    assert Parser(source).parse() == "success"


def test_for_all_parts_complex():
    source = """
    void main() {
        for (a = b = 0; (c = d++) < e; ++f.g)
            h = i(j++);
    }
    """
    assert Parser(source).parse() == "success"


def test_for_empty_cond_complex_body():
    source = "void main() { for (;; ++i) { a = b++; } }"
    assert Parser(source).parse() == "success"


# ---------------- INVALID CONTROL FLOW ----------------

def test_invalid_if_missing_condition_complex():
    source = "void main() { if () a = b++; }"
    assert Parser(source).parse() != "success"


def test_invalid_while_missing_parens():
    source = "void main() { while a = b++ c++; }"
    assert Parser(source).parse() != "success"


def test_invalid_for_broken_structure():
    source = "void main() { for (a = 1 b = 2; c++) d++; }"
    assert Parser(source).parse() != "success"


def test_invalid_else_without_if_complex():
    source = "void main() { else a = b = c++; }"
    assert Parser(source).parse() != "success"


# =========================================================
# SECTION 8: SWITCH / CASE / DEFAULT / BREAK
# =========================================================

def test_switch_empty():
    source = "void main() { switch (x) { } }"
    assert Parser(source).parse() == "success"


def test_switch_single_case_simple():
    source = "void main() { switch (x) { case 1: x++; } }"
    assert Parser(source).parse() == "success"


def test_switch_multiple_cases_fallthrough():
    source = """
    void main() {
        switch (x) {
            case 1:
            case 2:
            case 3:
                x++;
        }
    }
    """
    assert Parser(source).parse() == "success"


def test_switch_case_complex_expression():
    source = """
    void main() {
        switch (x) {
            case (1 + 2 * 3):
                y = z++;
        }
    }
    """
    assert Parser(source).parse() == "success"


def test_switch_case_unary_expression():
    source = """
    void main() {
        switch (x) {
            case -1:
            case +2:
                y++;
        }
    }
    """
    assert Parser(source).parse() == "success"


def test_switch_default_only():
    source = """
    void main() {
        switch (x) {
            default:
                y = 1;
        }
    }
    """
    assert Parser(source).parse() == "success"


def test_switch_default_middle():
    source = """
    void main() {
        switch (x) {
            case 1:
                y = 1;
            default:
                y = 0;
            case 2:
                y = 2;
        }
    }
    """
    assert Parser(source).parse() == "success"


def test_switch_with_blocks():
    source = """
    void main() {
        switch (x) {
            case 1: { a = b++; }
            case 2: { c = d++; }
            default: { e = f++; }
        }
    }
    """
    assert Parser(source).parse() == "success"


def test_switch_with_nested_statements():
    source = """
    void main() {
        switch (x) {
            case 1:
                if (a) b++;
            case 2:
                while (c) d++;
        }
    }
    """
    assert Parser(source).parse() == "success"


# ---------------- INVALID SWITCH ----------------

def test_invalid_switch_missing_parens():
    source = "void main() { switch x { case 1: x++; } }"
    assert Parser(source).parse() != "success"


def test_invalid_case_missing_expression():
    source = "void main() { switch (x) { case : x++; } }"
    assert Parser(source).parse() != "success"


def test_invalid_case_missing_colon():
    source = "void main() { switch (x) { case 1 x++; } }"
    assert Parser(source).parse() != "success"


def test_invalid_default_missing_colon():
    source = "void main() { switch (x) { default x++; } }"
    assert Parser(source).parse() != "success"


def test_invalid_switch_no_block():
    source = "void main() { switch (x) case 1: x++; }"
    assert Parser(source).parse() != "success"


# =========================================================
# SECTION 9: STRUCT DECLARATION / LITERALS / MEMBER ACCESS
# =========================================================

def test_struct_declaration_simple():
    source = "struct A { int x; };"
    assert Parser(source).parse() == "success"


def test_struct_multiple_members():
    source = "struct A { int x; float y; string z; };"
    assert Parser(source).parse() == "success"


def test_struct_empty():
    source = "struct Empty { };"
    assert Parser(source).parse() == "success"


def test_struct_variable_decl():
    source = "void main() { A a; }"
    assert Parser(source).parse() == "success"


def test_struct_literal_simple():
    source = "void main() { A a = {1, 2}; }"
    assert Parser(source).parse() == "success"


def test_struct_literal_nested():
    source = "void main() { A a = {{1, 2}, 3}; }"
    assert Parser(source).parse() == "success"


def test_struct_member_access_chain():
    source = "void main() { a.b.c.d; }"
    assert Parser(source).parse() == "success"


def test_struct_member_with_assignment():
    source = "void main() { a.b.c = d.e++; }"
    assert Parser(source).parse() == "success"


def test_struct_member_with_call_and_postfix():
    source = "void main() { f().a.b(c).d++; }"
    assert Parser(source).parse() == "success"


def test_struct_literal_in_call():
    source = "void main() { f({1, 2, 3}); }"
    assert Parser(source).parse() == "success"


# ---------------- INVALID STRUCT ----------------

def test_invalid_struct_missing_semicolon():
    source = "struct A { int x; }"
    assert Parser(source).parse() != "success"


def test_invalid_struct_missing_member_name():
    source = "struct A { int ; };"
    assert Parser(source).parse() != "success"


def test_invalid_struct_missing_brace():
    source = "struct A { int x; ;"
    assert Parser(source).parse() != "success"


def test_invalid_struct_literal_missing_brace():
    source = "void main() { A a = {1, 2; }"
    assert Parser(source).parse() != "success"


def test_invalid_member_access_trailing_dot():
    source = "void main() { a.b.; }"
    assert Parser(source).parse() != "success"


# =========================================================
# SECTION 10: FUNCTIONS & FUNCTION CALLS
# =========================================================

def test_function_no_params_no_return():
    source = "void f() { }"
    assert Parser(source).parse() == "success"


def test_function_with_params():
    source = "int f(int x, float y, string z) { return x; }"
    assert Parser(source).parse() == "success"


def test_function_inferred_return():
    source = "f(int x) { return x + 1; }"
    assert Parser(source).parse() == "success"


def test_function_multiple_returns():
    source = """
    int f(int x) {
        if (x) return 1;
        return 0;
    }
    """
    assert Parser(source).parse() == "success"


def test_function_call_no_args():
    source = "void main() { f(); }"
    assert Parser(source).parse() == "success"


def test_function_call_with_args():
    source = "void main() { f(1, x + y, g()); }"
    assert Parser(source).parse() == "success"


def test_nested_function_calls():
    source = "void main() { f(g(h(1))); }"
    assert Parser(source).parse() == "success"


def test_call_chaining():
    source = "void main() { f()()()(x); }"
    assert Parser(source).parse() == "success"


def test_function_call_with_assignment_expr():
    source = "void main() { f(a = b = c++); }"
    assert Parser(source).parse() == "success"


def test_function_call_member_mix():
    source = "void main() { f().a(b).c(d++); }"
    assert Parser(source).parse() == "success"


# ---------------- INVALID FUNCTIONS ----------------

def test_invalid_function_missing_body():
    source = "int f(int x);"
    assert Parser(source).parse() != "success"


def test_invalid_param_missing_name():
    source = "int f(int, int y) { return y; }"
    assert Parser(source).parse() != "success"


def test_invalid_param_trailing_comma():
    source = "int f(int x,) { return x; }"
    assert Parser(source).parse() != "success"


def test_invalid_call_trailing_comma():
    source = "void main() { f(1, 2,); }"
    assert Parser(source).parse() != "success"


def test_invalid_call_missing_paren():
    source = "void main() { f(1, 2; }"
    assert Parser(source).parse() != "success"
