"""
Full lexer coverage test cases for TyC compiler
Exhaustive token-based testing
"""

import pytest
from tests.utils import Tokenizer


# ==================================================
# I. WHITESPACE
# ==================================================

def test_ws_valid_1():
    tokenizer = Tokenizer("   auto   ")
    assert tokenizer.get_tokens_as_string() == "auto,<EOF>"


def test_ws_valid_2():
    tokenizer = Tokenizer("\tint\tx\t;")
    assert tokenizer.get_tokens_as_string() == "int,x,;,<EOF>"


def test_ws_valid_3():
    tokenizer = Tokenizer("\nfloat\nx\n=\n3.14\n;")
    assert tokenizer.get_tokens_as_string() == "float,x,=,3.14,;,<EOF>"


def test_ws_valid_4():
    tokenizer = Tokenizer("string\f s\f=\f\"hi\";")
    assert tokenizer.get_tokens_as_string() == "string,s,=,hi,;,<EOF>"


def test_ws_valid_5():
    tokenizer = Tokenizer("auto\r\nx\r\n=\r\n10;")
    assert tokenizer.get_tokens_as_string() == "auto,x,=,10,;,<EOF>"


def test_ws_invalid_1():
    tokenizer = Tokenizer("auto\x00x")
    assert "Error" in tokenizer.get_tokens_as_string()


def test_ws_invalid_2():
    tokenizer = Tokenizer("\x07")
    assert "Error" in tokenizer.get_tokens_as_string()


def test_ws_invalid_3():
    tokenizer = Tokenizer("\x1F")
    assert "Error" in tokenizer.get_tokens_as_string()


def test_ws_invalid_4():
    tokenizer = Tokenizer("\x80")
    assert "Error" in tokenizer.get_tokens_as_string()


def test_ws_invalid_5():
    tokenizer = Tokenizer("@\n")
    assert tokenizer.get_tokens_as_string() == "Error Token @"


# ==================================================
# II. COMMENTS
# ==================================================

def test_comment_valid_1():
    tokenizer = Tokenizer("// comment")
    assert tokenizer.get_tokens_as_string() == "<EOF>"


def test_comment_valid_2():
    tokenizer = Tokenizer("auto x; // trailing")
    assert tokenizer.get_tokens_as_string() == "auto,x,;,<EOF>"


def test_comment_valid_3():
    tokenizer = Tokenizer("/* block */ auto x;")
    assert tokenizer.get_tokens_as_string() == "auto,x,;,<EOF>"


def test_comment_valid_4():
    tokenizer = Tokenizer("/* // inside block */")
    assert tokenizer.get_tokens_as_string() == "<EOF>"


def test_comment_valid_5():
    tokenizer = Tokenizer("// /* inside line */")
    assert tokenizer.get_tokens_as_string() == "<EOF>"


def test_comment_valid_6():
    tokenizer = Tokenizer("/* \x00 */")
    assert tokenizer.get_tokens_as_string() == "<EOF>" 


def test_comment_invalid_1():
    tokenizer = Tokenizer("*/")
    assert tokenizer.get_tokens_as_string() == "*,/,<EOF>"


def test_comment_invalid_2():
    tokenizer = Tokenizer("/* nested /* */ */")
    assert tokenizer.get_tokens_as_string() == "*,/,<EOF>"
    
    
# ==================================================
# III. IDENTIFIERS
# ==================================================

# ---- valid identifiers ----

def test_id_valid_lowercase():
    tokenizer = Tokenizer("a b c z")
    assert tokenizer.get_tokens_as_string() == "a,b,c,z,<EOF>"


def test_id_valid_uppercase():
    tokenizer = Tokenizer("A Z")
    assert tokenizer.get_tokens_as_string() == "A,Z,<EOF>"


def test_id_valid_mixed():
    tokenizer = Tokenizer("aBc DeF")
    assert tokenizer.get_tokens_as_string() == "aBc,DeF,<EOF>"


def test_id_valid_underscore():
    tokenizer = Tokenizer("_ __ ___")
    assert tokenizer.get_tokens_as_string() == "_,__,___,<EOF>"


def test_id_valid_digits_after():
    tokenizer = Tokenizer("a1 a123 z9")
    assert tokenizer.get_tokens_as_string() == "a1,a123,z9,<EOF>"


# ---- invalid identifiers ----

def test_id_invalid_digit_first_1():
    tokenizer = Tokenizer("1a")
    assert tokenizer.get_tokens_as_string() == "1,a,<EOF>"


def test_id_invalid_digit_first_2():
    tokenizer = Tokenizer("9abc")
    assert tokenizer.get_tokens_as_string() == "9,abc,<EOF>"


def test_id_invalid_symbol():
    tokenizer = Tokenizer("@id")
    assert tokenizer.get_tokens_as_string() == "Error Token @"


def test_id_invalid_dash():
    tokenizer = Tokenizer("a-b")
    assert tokenizer.get_tokens_as_string() == "a,-,b,<EOF>"


def test_id_invalid_space():
    tokenizer = Tokenizer("a b")
    assert tokenizer.get_tokens_as_string() == "a,b,<EOF>"


# ==================================================
# IV. KEYWORDS
# ==================================================

def test_keyword_all():
    tokenizer = Tokenizer(
        "auto break case continue default else "
        "float for if int return string struct switch void while"
    )
    assert tokenizer.get_tokens_as_string().endswith("<EOF>")


def test_keyword_vs_id_1():
    tokenizer = Tokenizer("auto1")
    assert tokenizer.get_tokens_as_string() == "auto1,<EOF>"


def test_keyword_vs_id_2():
    tokenizer = Tokenizer("Auto")
    assert tokenizer.get_tokens_as_string() == "Auto,<EOF>"


def test_keyword_vs_id_3():
    tokenizer = Tokenizer("_auto")
    assert tokenizer.get_tokens_as_string() == "_auto,<EOF>"


def test_keyword_invalid_space():
    tokenizer = Tokenizer("wh ile")
    assert tokenizer.get_tokens_as_string() == "wh,ile,<EOF>"


# ==================================================
# V. OPERATORS
# ==================================================

def test_op_valid_single():
    tokenizer = Tokenizer("+ - * / %")
    assert tokenizer.get_tokens_as_string() == "+,-,*,/,%,<EOF>"


def test_op_valid_double():
    tokenizer = Tokenizer("== != <= >= && || ++ --")
    assert tokenizer.get_tokens_as_string().endswith("<EOF>")


def test_op_valid_assign_dot():
    tokenizer = Tokenizer("= .")
    assert tokenizer.get_tokens_as_string() == "=,.,<EOF>"


def test_op_invalid_1():
    tokenizer = Tokenizer("&")
    assert tokenizer.get_tokens_as_string() == "Error Token &"


def test_op_invalid_2():
    tokenizer = Tokenizer("|")
    assert tokenizer.get_tokens_as_string() == "Error Token |"


def test_op_invalid_3():
    tokenizer = Tokenizer("===")
    assert "==" in tokenizer.get_tokens_as_string()


def test_op_invalid_4():
    tokenizer = Tokenizer("**")
    assert tokenizer.get_tokens_as_string() == "*,*,<EOF>"


def test_op_invalid_5():
    tokenizer = Tokenizer("->")
    assert tokenizer.get_tokens_as_string() == "-,>,<EOF>"


# ==================================================
# VI. SEPARATORS
# ==================================================

def test_sep_valid_all():
    tokenizer = Tokenizer("{ } ( ) ; , :")
    assert tokenizer.get_tokens_as_string() == "{,},(,),;,,,:,<EOF>"


def test_sep_invalid_1():
    tokenizer = Tokenizer("[")
    assert tokenizer.get_tokens_as_string() == "[,<EOF>"


def test_sep_invalid_2():
    tokenizer = Tokenizer("]")
    assert tokenizer.get_tokens_as_string() == "],<EOF>"


def test_sep_invalid_3():
    tokenizer = Tokenizer("::")
    assert tokenizer.get_tokens_as_string() == ":,:,<EOF>"


def test_sep_invalid_4():
    tokenizer = Tokenizer("..")
    assert tokenizer.get_tokens_as_string() == ".,.,<EOF>"


def test_sep_invalid_5():
    tokenizer = Tokenizer("?")
    assert tokenizer.get_tokens_as_string() == "Error Token ?"


# ==================================================
# VII. NUMERIC LITERALS (INTEGER + FLOAT)
# ==================================================

# ---------- VALID NUMERIC LITERALS ----------

def test_number_valid_int_basic():
    tokenizer = Tokenizer("0 1 10 999")
    assert tokenizer.get_tokens_as_string() == "0,1,10,999,<EOF>"


def test_number_valid_int_negative():
    tokenizer = Tokenizer("-1 -45 -999")
    assert tokenizer.get_tokens_as_string() == "-1,-45,-999,<EOF>"


def test_number_valid_float_decimal():
    tokenizer = Tokenizer("0.0 3.14 1. .5")
    assert tokenizer.get_tokens_as_string() == "0.0,3.14,1.,.5,<EOF>"


def test_number_valid_float_scientific():
    tokenizer = Tokenizer("1e3 2E4 5.67E-2 1.23e+4")
    assert tokenizer.get_tokens_as_string() == "1e3,2E4,5.67E-2,1.23e+4,<EOF>"


def test_number_valid_mixed():
    tokenizer = Tokenizer("10 3.14 1e2 0.5 -3")
    assert tokenizer.get_tokens_as_string() == "10,3.14,1e2,0.5,-3,<EOF>"


# ---------- INVALID FOR TYPE BUT VALID FOR LEXER ----------

def test_number_invalid_double_sign():
    tokenizer = Tokenizer("--5")
    assert tokenizer.get_tokens_as_string() == "--,5,<EOF>"


def test_number_invalid_leading_plus():
    tokenizer = Tokenizer("+5")
    assert tokenizer.get_tokens_as_string() == "+,5,<EOF>"


def test_number_invalid_trailing_dot_sequence():
    tokenizer = Tokenizer("3..14")
    assert tokenizer.get_tokens_as_string() == "3.,.14,<EOF>"


def test_number_invalid_exp_missing_digits():
    tokenizer = Tokenizer("1e")
    assert tokenizer.get_tokens_as_string() == "1,e,<EOF>"


def test_number_invalid_exp_symbol_only():
    tokenizer = Tokenizer("e10")
    assert tokenizer.get_tokens_as_string() == "e10,<EOF>"


def test_number_invalid_mixed_alpha():
    tokenizer = Tokenizer("123abc")
    assert tokenizer.get_tokens_as_string() == "123,abc,<EOF>"


# ==================================================
# VIII. FLOAT LITERALS
# ==================================================

def test_float_valid_all():
    tokenizer = Tokenizer("3.14 1. .5 1e4 2E-3")
    assert tokenizer.get_tokens_as_string().endswith("<EOF>")


def test_float_invalid_dot():
    tokenizer = Tokenizer(".")
    assert tokenizer.get_tokens_as_string() == ".,<EOF>"


def test_float_invalid_e():
    tokenizer = Tokenizer("e10")
    assert tokenizer.get_tokens_as_string() == "e10,<EOF>"


def test_float_invalid_short():
    tokenizer = Tokenizer("1e")
    assert tokenizer.get_tokens_as_string() == "1,e,<EOF>"


def test_float_invalid_double_dot():
    tokenizer = Tokenizer("3..14")
    assert tokenizer.get_tokens_as_string() == "3.,.14,<EOF>"


# ==================================================
# IX. STRING LITERALS
# ==================================================

# ---------- VALID STRING LITERALS ----------

def test_string_valid_basic():
    tokenizer = Tokenizer("\"hello\"")
    assert tokenizer.get_tokens_as_string() == "hello,<EOF>"


def test_string_valid_empty():
    tokenizer = Tokenizer("\"\"")
    assert tokenizer.get_tokens_as_string() == ",<EOF>"


def test_string_valid_escape_newline():
    tokenizer = Tokenizer("\"line\\nnext\"")
    assert tokenizer.get_tokens_as_string() == "line\\nnext,<EOF>"


def test_string_valid_escape_tab():
    tokenizer = Tokenizer("\"a\\tb\"")
    assert tokenizer.get_tokens_as_string() == "a\\tb,<EOF>"


def test_string_valid_escape_backspace():
    tokenizer = Tokenizer("\"a\\bb\"")
    assert tokenizer.get_tokens_as_string() == "a\\bb,<EOF>"


def test_string_valid_escape_formfeed():
    tokenizer = Tokenizer("\"a\\fb\"")
    assert tokenizer.get_tokens_as_string() == "a\\fb,<EOF>"


def test_string_valid_escape_carriage_return():
    tokenizer = Tokenizer("\"a\\rb\"")
    assert tokenizer.get_tokens_as_string() == "a\\rb,<EOF>"


def test_string_valid_escape_quote():
    tokenizer = Tokenizer("\"He said: \\\"Hi\\\"\"")
    assert tokenizer.get_tokens_as_string() == "He said: \\\"Hi\\\",<EOF>"


def test_string_valid_escape_backslash():
    tokenizer = Tokenizer("\"\\\\\"")
    assert tokenizer.get_tokens_as_string() == "\\\\,<EOF>"


def test_string_valid_all_escapes_combined():
    tokenizer = Tokenizer("\"\\b\\f\\n\\r\\t\\\"\\\\\"")
    assert tokenizer.get_tokens_as_string() == "\\b\\f\\n\\r\\t\\\"\\\\,<EOF>"


# ---------- INVALID STRING LITERALS ----------

def test_string_invalid_unclosed_eof():
    tokenizer = Tokenizer("\"abc")
    assert "Unclosed String" in tokenizer.get_tokens_as_string()


def test_string_invalid_unclosed_newline():
    tokenizer = Tokenizer("\"abc\n\"")
    assert "Unclosed String" in tokenizer.get_tokens_as_string()


def test_string_invalid_unclosed_carriage_return():
    tokenizer = Tokenizer("\"abc\r\"")
    assert "Unclosed String" in tokenizer.get_tokens_as_string()


def test_string_invalid_illegal_escape_x():
    tokenizer = Tokenizer("\"abs\\x01\"")
    assert "Illegal Escape In String" in tokenizer.get_tokens_as_string()


def test_string_invalid_illegal_escape_hex_like():
    tokenizer = Tokenizer("\"\\u1234\"")
    assert "Illegal Escape In String" in tokenizer.get_tokens_as_string()


def test_string_invalid_illegal_escape_unknown():
    tokenizer = Tokenizer("\"\\q\"")
    assert "Illegal Escape In String" in tokenizer.get_tokens_as_string()


def test_string_invalid_illegal_escape_digit():
    tokenizer = Tokenizer("\"\\9\"")
    assert "Illegal Escape In String" in tokenizer.get_tokens_as_string()


def test_string_invalid_dangling_backslash():
    tokenizer = Tokenizer("\"\\\"")
    assert "Unclosed String" in tokenizer.get_tokens_as_string()



# ==================================================
# X. ERROR TOKENS
# ==================================================

def test_error_token_at():
    tokenizer = Tokenizer("@")
    assert tokenizer.get_tokens_as_string() == "Error Token @"


def test_error_token_hash():
    tokenizer = Tokenizer("#")
    assert tokenizer.get_tokens_as_string() == "Error Token #"


def test_error_token_dollar():
    tokenizer = Tokenizer("$")
    assert tokenizer.get_tokens_as_string() == "Error Token $"


def test_error_token_tilde():
    tokenizer = Tokenizer("~")
    assert tokenizer.get_tokens_as_string() == "Error Token ~"


def test_error_token_backtick():
    tokenizer = Tokenizer("`")
    assert tokenizer.get_tokens_as_string() == "Error Token `"


def test_error_token_caret():
    tokenizer = Tokenizer("^")
    assert tokenizer.get_tokens_as_string() == "Error Token ^"


def test_error_token_question():
    tokenizer = Tokenizer("?")
    assert tokenizer.get_tokens_as_string() == "Error Token ?"


def test_error_token_single_pipe():
    tokenizer = Tokenizer("|")
    assert tokenizer.get_tokens_as_string() == "Error Token |"


def test_error_token_single_ampersand():
    tokenizer = Tokenizer("&")
    assert tokenizer.get_tokens_as_string() == "Error Token &"


def test_error_token_extended_ascii():
    tokenizer = Tokenizer("\x7F")
    assert "Error Token" in tokenizer.get_tokens_as_string()


# ==================================================
# XI. SUPER-LONG RANDOM MIXED TOKEN STRESS
# ==================================================

# ---------- VALID CASES ----------

def test_random_long_valid_1():
    tokenizer = Tokenizer(
        "auto x=5; int y=10; float z=3.14;"
        "x=x+y*2-3/1; printInt(x);"
    )
    assert tokenizer.get_tokens_as_string().endswith("<EOF>")


def test_random_long_valid_2():
    tokenizer = Tokenizer(
        "string s=\"hello\"; printString(s);"
        "s=\"world\"; printString(s);"
    )
    assert tokenizer.get_tokens_as_string().endswith("<EOF>")


def test_random_long_valid_3():
    tokenizer = Tokenizer(
        "for(auto i=0;i<10;i++){printInt(i);}"
    )
    assert tokenizer.get_tokens_as_string().endswith("<EOF>")


def test_random_long_valid_4():
    tokenizer = Tokenizer(
        "while(x<100){x=x+1;if(x==50){break;}}"
    )
    assert tokenizer.get_tokens_as_string().endswith("<EOF>")


def test_random_long_valid_5():
    tokenizer = Tokenizer(
        "if(a&&b||c){printInt(1);}else{printInt(0);}"
    )
    assert tokenizer.get_tokens_as_string().endswith("<EOF>")


def test_random_long_valid_6():
    tokenizer = Tokenizer(
        "switch(x){case 1:printInt(1);break;default:printInt(0);}"
    )
    assert tokenizer.get_tokens_as_string().endswith("<EOF>")


def test_random_long_valid_7():
    tokenizer = Tokenizer(
        "auto a; a=readInt(); auto b; b=readInt(); printInt(a+b);"
    )
    assert tokenizer.get_tokens_as_string().endswith("<EOF>")


def test_random_long_valid_8():
    tokenizer = Tokenizer(
        "struct Point{int x;int y;}; Point p={1,2}; printInt(p.x);"
    )
    assert tokenizer.get_tokens_as_string().endswith("<EOF>")


def test_random_long_valid_9():
    tokenizer = Tokenizer(
        "x++; --y; y=y*2+3%2;"
    )
    assert tokenizer.get_tokens_as_string().endswith("<EOF>")


def test_random_long_valid_10():
    tokenizer = Tokenizer(
        "auto s=\"a\\n\\t\\\"\\\\\"; printString(s);"
    )
    assert tokenizer.get_tokens_as_string().endswith("<EOF>")


# ---------- INVALID CASES ----------

def test_random_long_invalid_1():
    tokenizer = Tokenizer(
        "auto x=5; string s=\"bad\\q\";"
    )
    assert "Illegal Escape In String" in tokenizer.get_tokens_as_string()


def test_random_long_invalid_2():
    tokenizer = Tokenizer(
        "\"unterminated string"
    )
    assert "Unclosed String" in tokenizer.get_tokens_as_string()


def test_random_long_invalid_3():
    tokenizer = Tokenizer(
        "string s=\"abc\n\";"
    )
    assert "Unclosed String" in tokenizer.get_tokens_as_string()


def test_random_long_invalid_4():
    tokenizer = Tokenizer(
        "auto x=5; @oops;"
    )
    assert "Error Token @" in tokenizer.get_tokens_as_string()


def test_random_long_invalid_5():
    tokenizer = Tokenizer(
        "auto a=1; auto b=2; auto c=a+b*3-4/2; printInt(c);"
    )
    assert tokenizer.get_tokens_as_string().endswith("<EOF>")


def test_random_long_invalid_6():
    tokenizer = Tokenizer(
        "string s=\"\\x01\";"
    )
    assert "Illegal Escape In String" in tokenizer.get_tokens_as_string()


def test_random_long_invalid_7():
    tokenizer = Tokenizer(
        "auto y=10; string s=\"\\u1234\";"
    )
    assert "Illegal Escape In String" in tokenizer.get_tokens_as_string()


def test_random_long_invalid_8():
    tokenizer = Tokenizer(
        "\"abc\r\""
    )
    assert "Unclosed String" in tokenizer.get_tokens_as_string()


def test_random_long_invalid_9():
    tokenizer = Tokenizer(
        "x | y;"
    )
    assert "Error Token |" in tokenizer.get_tokens_as_string()


def test_random_long_invalid_10():
    tokenizer = Tokenizer(
        "a &&&& b;"
    )
    assert "&&" in tokenizer.get_tokens_as_string()
