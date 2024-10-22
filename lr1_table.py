import re

# 定义正则表达式
state_pattern = re.compile(r"State (\d+)")
shift_pattern = re.compile(r"shift, and go to state (\d+)")
reduce_pattern = re.compile(r"reduce using rule (\d+)")
goto_pattern = re.compile(r"go to state (\d+)")
accept_pattern = re.compile(r"accept")

# 终结符和非终结符列表
terminals = ['+', '-', '*', '/', '(', ')', 'INTEGER', '$']
non_terminals = ['input', 'expr']

# 用于存储 Action 和 Goto 表
action_table = {}
goto_table = {}

# 解析 y.output 文件
def parse_y_output(file_path):
    with open(file_path, "r") as file:
        current_state = None
        for line in file:
            # 匹配状态
            state_match = state_pattern.search(line)
            if state_match:
                current_state = int(state_match.group(1))
                action_table[current_state] = {}
                goto_table[current_state] = {}
                continue

            # 如果当前状态未定义，跳过处理
            if current_state is None:
                continue

            # 匹配移入 (shift)
            for terminal in terminals:
                if terminal in line and "shift" in line:
                    shift_match = shift_pattern.search(line)
                    if shift_match:
                        action_table[current_state][terminal] = f"s{shift_match.group(1)}"

            # 匹配规约 (reduce)
            for terminal in terminals:
                if terminal in line and "reduce" in line:
                    reduce_match = reduce_pattern.search(line)
                    if reduce_match:
                        action_table[current_state][terminal] = f"r{reduce_match.group(1)}"

            # 匹配 goto
            for non_terminal in non_terminals:
                if non_terminal in line and "go to state" in line:
                    goto_match = goto_pattern.search(line)
                    if goto_match:
                        goto_table[current_state][non_terminal] = goto_match.group(1)

            # 匹配接受 (accept)
            if accept_pattern.search(line):
                action_table[current_state]['$'] = "acc"


# 打印 LR(1) 分析表
def print_lr1_table():
    # 打印表头
    print("State".ljust(10), end="")
    for terminal in terminals:
        print(terminal.center(10), end="")
    print("|", end="")
    for non_terminal in non_terminals:
        print(non_terminal.center(10), end="")
    print()

    # 打印表格内容
    for state in sorted(action_table.keys()):
        print(str(state).ljust(10), end="")
        for terminal in terminals:
            action = action_table[state].get(terminal, "")
            print(action.center(10), end="")
        print("|", end="")
        for non_terminal in non_terminals:
            goto = goto_table[state].get(non_terminal, "")
            print(goto.center(10), end="")
        print()


# 解析 y.output 文件
parse_y_output("calc.output")

# 打印 LR(1) 分析表
print_lr1_table()