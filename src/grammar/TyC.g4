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

//Operators
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

INC: '++';
DEC: '--';

ASSIGN: '=';
DOT: '.';

//Separators

LSB: '[';
RSB: ']';

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

INTLIT: ('-'?)(DIGIT+);

// =====================
// FLOAT LITERALS
// =====================
fragment SCIENTIFIC: [eE] '-'? DIGIT+;
FLOATLIT: '-'?
            ( ( '.'DIGIT+ SCIENTIFIC?) 
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
STRINGLIT: '"' STR_CHAR* '"';

ILLEGAL_ESCAPE: '"' STR_CHAR* '\\' ~[bfrnt"\\];

UNCLOSE_STRING: '"' STR_CHAR* ('\r' | '\n' | EOF);




//Primitive types
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
func_decl_typed: typ ID LP param_list? RP block;
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
//var_structdecl_noinit: ID ID SM;
var_structdecl_init: ID ID ASSIGN LB expr_lst RB SM;


// =====================
// VARIABLE DECLARE + INIT
// =====================
vardecl: var_explicit_decl | var_auto_decl;
var_explicit_decl: var_explicit_noinit | var_explicit_init;
var_explicit_noinit: typ ID SM;
var_explicit_init: typ ID ASSIGN expr SM;

var_auto_decl: var_auto_noinit | var_auto_init;
var_auto_noinit: AUTO ID SM;
var_auto_init: AUTO ID ASSIGN expr SM;


// =====================
// EXPRESSIONS
// =====================

expr: exp0;

// assignment (right)
exp0: exp1 ASSIGN exp0 | exp1;

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
exp6: exp6 (MUL | DIV | MOD) exp7 | exp7;

// unary ! + - (right)
exp7: (LNOT | ADD | SUB) exp7 | exp8;

// prefix ++ -- (right)
exp8: (INC | DEC) exp8 | exp9;


// postfix ++ --
exp9: exp9 INC
    | exp9 DEC
    | exp10;

// member access + function call (higher precedence)
exp10: exp10 DOT ID
    | exp10 LP expr_lst? RP
    | exp11;

// primary
exp11: ID | literal | LP expr RP;

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
    | switch_stmt;

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
for_init: vardecl 
        | assign;
for_cond: expr;
for_update: assign 
            | incdec_expr;

incdec_expr: INC ID
            | DEC ID
            | ID INC
            | ID DEC;

switch_stmt: SWITCH LP expr RP LB case_lst default_case? RB;
case_lst: case_stmt*;
case_stmt: CASE INTLIT COLON stmt_lst;
default_case: DEFAULT COLON stmt_lst;

break_stmt: BREAK;
continue_stmt: CONTINUE;
return_stmt: RETURN expr?;
expr_stmt: expr;

program: (struct_decl | func_decl)+ EOF;

LINE_COMMENT  : '//' ~[\r\n]* -> skip ;
BLOCK_COMMENT : '/*' .*? '*/' -> skip ;
WS : [ \t\r\n]+ -> skip ; // skip spaces, tabs

ERROR_CHAR: .;