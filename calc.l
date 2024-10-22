%{
#include "calc.tab.h"
%}

%%

[0-9]+  { yylval = atoi(yytext); return INTEGER; }
[ \t\n]  { /* 忽略空白字符 */ }
"+"     { return '+'; }
"-"     { return '-'; }
"*"     { return '*'; }
"/"     { return '/'; }
"("     { return '('; }
")"     { return ')'; }

.       { return yytext[0]; }

%%

int yywrap(void) {
    return 1;
}
