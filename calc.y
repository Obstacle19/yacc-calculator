%{
#include <stdio.h>
#include <stdlib.h>

// 声明词法分析函数
int yylex(void);
void yyerror(const char *s);

// 用于存储结果的全局变量
int result;
%}

// 定义 token 类型
%token INTEGER
%left '+' '-'
%left '*' '/'
%nonassoc UMINUS

// 语法规则部分
%%
input:
    expr { result = $1; }
    ;

expr:
    expr '+' expr { $$ = $1 + $3; }
    | expr '-' expr { $$ = $1 - $3; }
    | expr '*' expr { $$ = $1 * $3; }
    | expr '/' expr { if ($3 == 0) { yyerror("Division by zero"); } else { $$ = $1 / $3; } }
    | '-' expr %prec UMINUS { $$ = -$2; }
    | '(' expr ')' { $$ = $2; }
    | INTEGER { $$ = $1; }
    ;

%%

// 错误处理函数
void yyerror(const char *s) {
    fprintf(stderr, "Error: %s\n", s);
}

// 主函数
int main(void) {
    printf("Enter an expression: ");
    if (yyparse() == 0) {
        printf("Result: %d\n", result);
    }
    return 0;
}
