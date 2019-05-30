grammar task_2_1;

NEWLINE :(' '|'\r'|'\n')+ -> skip;
COMMAND : ( 'ADD' | 'AAA' | 'INC' );
REG : ('AX'|'BX'|'CX'|'DX');
IMMEDIATE : ( [0-9]+ | ( '0' | '1' )+'b' );
MEMORY: '[' REG ']';
COMMA: ',' -> skip;

Instruction: COMMAND REG COMMA REG
    | COMMAND
    | COMMAND REG COMMA IMMEDIATE
    | COMMAND REG COMMA MEMORY;
 
start: (Instruction NEWLINE)* ;







