# yacc-calculator

## **安装工具**

- 首先需要安装 `bison`（GNU Yacc）和 `flex`（Lex 的实现）以生成词法和语法分析器：
  ```bash
  sudo apt-get install bison flex
  ```

## **编写词法分析器（Lex 文件）**

- `calc.l` 文件定义了如何从输入中提取整数和运算符。
- `[0-9]+` 匹配整数，将其转换为 `int` 类型并返回 `INTEGER` token。
- 运算符如 `+`, `-`, `*`, `/`, `(`, `)` 直接返回对应的字符。

## **编写语法分析器（Yacc 文件）**

- `calc.y` 文件定义四则运算的语法规则。
- 这部分代码使用了左递归来处理加减法和乘除法的优先级。
- 使用 `%left` 和 `%right` 来指定运算符的优先级，并且定义了 `UMINUS` 来处理一元减号。

## 编译和执行

- 使用以下命令生成词法和语法分析器：
  ```bash
  bison -d calc.y
  flex calc.l
  gcc lex.yy.c calc.tab.c -o calc -lm
  ```

- 然后执行程序：
  ```bash
  ./calc
  ```

- 输入类似 `3 + 5 * (2 - 4)` 这样的表达式，`Ctrl + D` 停止输入，程序将输出计算结果。

## **生成 LR(1) 分析表**

使用 `bison` 生成输出文件：

- 可以通过 `bison` 的 `-v` 选项生成详细的 LALR(1) 分析表：

  ```shell
  bison -v calc.y
  ```

- 这会生成一个 `calc.output` 文件，其中包含了语法分析器的状态、项集、转移等信息。

生成 LR(1) 分析表：

```shell
python3 lr1_table.py
```

将会生成如下图所示的分析表：

```shell
State         +         -         *         /         (         )      INTEGER      $     |  input      expr   
0                       s2                            s3                  s1       acc    |    4         5     
1                                                     r8        r8                  r8    |                    
2                       s2                            s3                  s1              |              6     
3                       s2                            s3                  s1              |              7     
4                                                                                   s8    |                    
5             s9       s10       s11       s12        r1        r1                  r1    |                    
6                                                     r6        r6                  r6    |                    
7             s9       s10       s11       s12                 s13                        |                    
8                                                                                  acc    |                    
9                       s2                            s3                  s1              |              14    
10                      s2                            s3                  s1              |              15    
11                      s2                            s3                  s1              |              16    
12                      s2                            s3                  s1              |              17    
13                                                    r7        r7                  r7    |                    
14                               s11       s12        r2        r2                  r2    |                    
15                               s11       s12        r3        r3                  r3    |                    
16                                                    r4        r4                  r4    |                    
17                                                    r5        r5                  r5    |                    
```

