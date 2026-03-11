grammar TyC;

@lexer::header {
from lexererr import *
}

@lexer::members {
def emit(self):
    tk = self.type
    if tk == self.UNCLOSE_STRING:       
        result = super().emit();
        raise UncloseString(result.text);
    elif tk == self.ILLEGAL_ESCAPE:
        result = super().emit();
        raise IllegalEscape(result.text);
    elif tk == self.ERROR_CHAR:
        result = super().emit();
        raise ErrorToken(result.text); 
    else:
        return super().emit();
}

options{
	language=Python3;
}


LINE_COMMENT  : '//' ~[\r\n]* -> skip ;
BLOCK_COMMENT : '/*' .*? '*/' -> skip ;

//Operators
// Increment / decrement
INC: '++';
DEC: '--';

// Arithmetic
ADD: '+';
SUB: '-';
MUL: '*';
DIV: '/';
MOD: '%';

EQ   : '==';
NEQ  : '!=';
LE   : '<=';
GE   : '>=';
LT   : '<';
GT   : '>';

LAND : '&&';
LOR  : '||';
LNOT : '!';

ASSIGN: '=';
DOT: '.';

//Separators

LB: '{';
RB: '}';

LP: '(';
RP: ')';

SM: ';';
CM: ',';    
COLON: ':';

// LITERALS
// =====================
// INT LITERALS
// =====================
fragment DIGIT: [0-9];

INTLIT: (DIGIT+);

// =====================
// FLOAT LITERALS
// =====================
fragment SCIENTIFIC: [eE] [+-]? DIGIT+;
FLOATLIT: ( ( '.'DIGIT+ SCIENTIFIC?) 
        | ( DIGIT+'.'DIGIT*SCIENTIFIC? ) 
        | ( DIGIT+ SCIENTIFIC) );


// =====================
// STRING LITERALS
// =====================

//Escape sequences
fragment ESC_SEQ: '\\' [bfrnt"\\];

// Characters allowed inside a string (excluding quotes, backslash, newline)
fragment STR_CHAR: ESC_SEQ
                | ~["\\\r\n];

//Valid string literal
STRINGLIT: '"' STR_CHAR* '"'
        {
            # strip opening and closing quotes
            self.text = self.text[1:-1]
        };

// Illegal escape (must be detected FIRST)
ILLEGAL_ESCAPE: '"' STR_CHAR* '\\' ~[bfrnt"\\\r\n]
        {
                self.text = self.text[1:]
        };

UNCLOSE_STRING: '"' STR_CHAR* '\\'? EOF
    {
        self.text = self.text[1:]
    }
    | '"' STR_CHAR* '\\'? '\n'
    {
        self.text = self.text[1:-1]
    }
    | '"' STR_CHAR* '\\'? '\r'
    {
        self.text = self.text[1:-1]
    };




//Types
INT: 'int';
FLOAT: 'float';
STRING: 'string';
VOID: 'void';
STRUCT: 'struct';
AUTO: 'auto';

//Keywords
IF: 'if';
ELSE: 'else';
FOR: 'for';
WHILE: 'while';
SWITCH: 'switch';
CASE: 'case';
DEFAULT: 'default';
BREAK: 'break';
CONTINUE: 'continue';
RETURN: 'return';

fragment ALPHA: [a-zA-Z];
ID: (ALPHA|'_')(ALPHA|DIGIT|'_')*;



// TODO: Define grammar rules here

// =====================
// FUNCTION
// =====================
func_decl: func_decl_typed | func_decl_infer;
func_decl_typed: func_typ ID LP param_list? RP block;
func_decl_infer: ID LP param_list? RP block;
param_list: param (CM param)*;
param: typ ID;
func_typ: INT
        | FLOAT
        | STRING
        | VOID
        | ID;

typ: INT
    | FLOAT
    | STRING
    | ID;

// =====================
// STRUCT
// =====================
//DECLARE
struct_decl: STRUCT ID struct_body SM;
struct_body: LB struct_vardecl_lst RB;
struct_vardecl_lst: struct_vardecl*;
struct_vardecl: typ ID SM;

//INITIALIZE
var_structdecl: var_structdecl_init;
var_structdecl_init: ID ID ASSIGN LB expr_lst RB SM;

//STRUCT LITERAL
struct_literal: LB expr_lst? RB;


// =====================
// VARIABLE DECLARE + INIT
// =====================

vardecl: vardecl_core SM;

vardecl_core: var_explicit_core
                | var_auto_core;

var_explicit_core: typ ID (ASSIGN expr)?;

var_auto_core: AUTO ID (ASSIGN expr)?;



// =====================
// EXPRESSIONS
// =====================

expr: exp0;

// assignment (right)
exp0: assign_lhs ASSIGN exp0 | exp1;
assign_lhs: ID
        | member_lhs;

member_lhs: primary member_suffix* DOT ID;
member_suffix: DOT ID
            | LP expr_lst? RP
            | INC
            | DEC;

// logical OR (left)
exp1: exp1 LOR exp2 | exp2;

// logical AND (left)
exp2: exp2 LAND exp3 | exp3;

// equality (left)
exp3: exp3 (EQ | NEQ) exp4 | exp4;

// relational (left)
exp4: exp4 (LT | LE | GT | GE) exp5 | exp5;

// additive (left)
exp5: exp5 (ADD | SUB) exp6 | exp6;

// multiplicative (left)
exp6: exp6 (MUL | DIV | MOD) prefix | prefix;

// prefix: unary ! + - (right)  prefix ++ -- (right, higher precedence)
prefix: (LNOT | ADD | SUB | INC | DEC) prefix 
        | postfix;

// postfix expressions chain left-to-right
postfix: primary postfix_suffix*;
postfix_suffix: DOT ID
              | LP expr_lst? RP
              | INC
              | DEC;

// primary
primary: ID
        | literal
        | LP expr RP
        | struct_literal;

literal: INTLIT | FLOATLIT | STRINGLIT;
expr_lst: expr (CM expr)*;




// =====================
// STATEMENTS
// =====================
stmt: simple_stmt SM
    | block
    | if_stmt
    | while_stmt
    | for_stmt
    | switch_stmt
    | vardecl;

simple_stmt: break_stmt
           | continue_stmt
           | return_stmt
           | expr_stmt;

block: LB stmt_lst RB;
stmt_lst: stmt*;

if_stmt: IF LP expr RP stmt 
        | IF LP expr RP stmt ELSE stmt;

while_stmt: WHILE LP expr RP stmt;

for_stmt: FOR LP for_init? SM for_cond? SM for_update? RP stmt;

for_init: vardecl_core
        | assign_lhs ASSIGN expr;

for_cond: expr;
for_update: assign_lhs ASSIGN expr
            | incdec_expr;

incdec_expr: INC expr
        | DEC expr
        | expr INC
        | expr DEC;


switch_stmt: SWITCH LP expr RP LB switch_body RB;
switch_body: case_stmt*                           
        | case_stmt* default_case case_stmt*;

case_lst: case_stmt*;
case_stmt: CASE expr COLON stmt_lst;
default_case: DEFAULT COLON stmt_lst;

break_stmt: BREAK;
continue_stmt: CONTINUE;
return_stmt: RETURN expr?;
expr_stmt: expr;

program: (struct_decl | func_decl)* EOF;


WS : [ \t\r\n\f]+ -> skip ; // skip spaces, tabs

ERROR_CHAR: .;
