import lark
import argparse


parser = argparse.ArgumentParser(description="Compile a program")
parser.add_argument("--file", help="the file to compile")
args = parser.parse_args()


grammaire = lark.Lark(
    """ variables: IDENTIFIANT ("," IDENTIFIANT)*
    expr: IDENTIFIANT -> variable | NUMBER -> nombre | expr OP expr -> binexpr | "("expr")" -> parenexpr | "new"  "int" "[" expr "]" -> new_array | IDENTIFIANT "[" expr "]" -> array_access | "len(" IDENTIFIANT ")" -> len_array 
    NUMBER : /[0-9]+/
    cmd : IDENTIFIANT "=" expr ";" -> assignement | IDENTIFIANT "[" expr "]" "=" expr ";" -> array_assignement | "while" "("expr")" "{" bloc "}" -> while | "if" "("expr")" "{" bloc "}" -> if | "printf" "("expr")" ";" -> printf | "showarr" "("expr")" ";" -> showarr 
    bloc : (cmd)*
    prog: "main" "(" variables ")" "{" bloc "return" "(" expr ")" ";" "}"
    OP : "+" | "-" | "*" | ">" | "<" | "==" | "!="
    IDENTIFIANT : /[a-zA-Z][a-zA-Z0-9]*/
    %import common.WS
    %ignore WS
     """,
    start="prog",
)


def create_dict(prg, vars):
    vars = var_list(prg)
    repetition = dict.fromkeys(vars, 0)
    values = dict.fromkeys(vars, 0)
    return repetition, values


def find_assignement(prg, rep):

    if prg.data == "assignement":
        rep[prg.children[0]] += 1

    else:
        for c in prg.children:
            if isinstance(c, lark.Tree):
                rep = find_assignement(c, rep)
    return rep


def find_values(prg, rep, values):

    if prg.data == "assignement" and rep[prg.children[0]] < 2:
        flag, res = rec_isImmediat(prg.children[1])
        if flag:
            values[prg.children[0]] = res
        # if isImmediat(prg.children[1]):
        #     op = prg.children[1].children[1]
        #     e1 = int(prg.children[1].children[0].children[0].value)
        #     e2 = int(prg.children[1].children[2].children[0].value)
        #     values[prg.children[0]] = operation(op, e1, e2)
        elif prg.children[1].data == "nombre":
            values[prg.children[0]] = prg.children[1].children[0].value
        else:
            pass

    else:
        for c in prg.children:
            if isinstance(c, lark.Tree):
                values = find_values(c, rep, values)
    return values


def isImmediat(expr):
    return (
        expr.data == "binexpr"
        and expr.children[0].data == "nombre"
        and expr.children[2].data == "nombre"
    )


def rec_isImmediat(expr):
    if expr.data == "nombre":
        return True, int(expr.children[0].value)
    elif expr.data == "binexpr":
        flag1, res1 = rec_isImmediat(expr.children[0])
        flag2, res2 = rec_isImmediat(expr.children[2])
        if flag1 and flag2:
            return True, operation(expr.children[1].value, res1, res2)
        else:
            return False, None
    elif expr.data == "parenexpr":
        return rec_isImmediat(expr.children[0])
    else:
        return False, None


def operation(op, nb1, nb2):
    if op == "+":
        return nb1 + nb2
    elif op == "-":
        return nb1 - nb2
    elif op == "*":
        return nb1 * nb2
    elif op == "==":
        if nb1 == nb2:
            return 1
        else:
            return 0
    elif op == "!=":
        if nb1 == nb2:
            return 0
        else:
            return 1
    else:
        raise Exception("Not Implemented")


def pp_expr(expr, values, opti):
    if opti:
        flag, res = rec_isImmediat(expr)
        if flag:
            return f"{res}"
        elif expr.data == "binexpr":
            op = expr.children[1].value
            e1 = pp_expr(expr.children[0], values, opti)
            e2 = pp_expr(expr.children[2], values, opti)
            if str.isdigit(e1) and str.isdigit(e2):
                return f"{operation(op,int(e1),int(e2))}"
            return f"{e1} {op} {e2}"
        elif expr.data == "variable":
            if values[expr.children[0].value] is not None:
                return f"{values[expr.children[0].value]}"
            else:
                return f"{expr.children[0].value}"
    else:

        if expr.data == "binexpr":
            op = expr.children[1].value
            e1 = pp_expr(expr.children[0], values, opti)
            e2 = pp_expr(expr.children[2], values, opti)
            return f"{e1} {op} {e2}"

        elif expr.data == "variable":
            return f"{expr.children[0].value}"

    if expr.data == "nombre":
        return f"{expr.children[0].value}"
    elif expr.data == "parenexpr":
        return f"({pp_expr(expr.children[0],values,opti)})"
    elif expr.data == "array_access":
        return (
            f"{expr.children[0].value}[{pp_expr(expr.children[1],values,opti)}]"
        )
    elif expr.data == "new_array":
        return f"new int[{pp_expr(expr.children[0],values,opti)}]"
    elif expr.data == "len_array":
        return f"len({expr.children[0].value})"
    else:
        return expr.data  # not implemented


def pp_cmd(cmd, values, opti):
    if cmd.data == "assignement":
        if values[cmd.children[0].value] is not None and opti:
            return ""
        lhs = cmd.children[0].value
        rhs = pp_expr(cmd.children[1], values, opti)
        return f"{lhs} = {rhs};"
    elif cmd.data == "array_assignement":
        lhs = (
            cmd.children[0].value
            + "["
            + pp_expr(cmd.children[1], values, opti)
            + "]"
        )
        rhs = pp_expr(cmd.children[2], values, opti)
        return f"{lhs} = {rhs};"
    elif cmd.data == "printf":
        return f"printf({pp_expr(cmd.children[0],values,opti)});"

    elif cmd.data in {"if", "while"}:
        e = pp_expr(cmd.children[0], values, opti)
        b = pp_bloc(cmd.children[1], values, opti)
        return f"{cmd.data}({e}){{\n {b} }}"

    elif cmd.data == "showarr":
        tab = pp_expr(cmd.children[0], values, opti)
        return tab+"showarr=0;\nwhile("+tab+"showarr!=len("+tab+")){\nprintf("+tab+"["+tab+"showarr]);\n"+tab+"showarr="+tab+"showarr+1;\n}\n"

    else:
        raise NotImplementedError(cmd.data)


def pp_bloc(bloc, values, opti):
    return "\n ".join(pp_cmd(cmd, values, opti) for cmd in bloc.children)


def pp_variables(variables):
    return ",".join(variables.children)


def pp_prg(prog, opti=False):
    vars_list = var_list(prog)

    dict_assignement = find_assignement(prog, dict.fromkeys(vars_list, 0))
    dict_values = find_values(
        prog, dict_assignement, dict.fromkeys(vars_list, None)
    )
    vars = pp_variables(prog.children[0])
    bloc = pp_bloc(prog.children[1], dict_values, opti)
    ret = pp_expr(prog.children[2], dict_values, opti)
    return f"main ({vars}) {{\n {bloc} \n return({ret});\n}}"


def var_list(ast):
    if isinstance(ast, lark.Token):
        if ast.type == "IDENTIFIANT":
            return {ast.value}
        else:
            return set()
    s = set()
    for c in ast.children:
        s.update(var_list(c))
    return s


nb_while = 0
nb_if = 0
nb_de = 0


def comp_op(op, e1, e2):
    global nb_de
    if op == "+":
        return f"{e2}\npush rax\n{e1}\npop rbx\nadd rax,rbx"
    if op == "-":
        return f"{e2}\npush rax\n{e1}\npop rbx\nsub rax,rbx"
    if op == "*":
        return f"{e2}\npush rax\n{e1}\npop rbx\nimul rax,rbx"
    if op == "!=":
        return f"{e2}\npush rax\n{e1}\npop rbx\nsub rax,rbx"
    if op == "==":
        nb_de += 1
        return f"{e2}\npush rax\n{e1}\npop rbx\nsub rax,rbx\ncmp rax,0\nje fin_de{nb_de}\nmov rax,0\njmp fin_de{nb_de}_2\nfin_de{nb_de}:\nmov rax, 1\nfin_de{nb_de}_2:\n"


def compile_expr(expr, values, opti):
    if opti:
        flag, res = rec_isImmediat(expr)
        if flag:
            return f"\nmov rax, {res}"
        elif expr.data == "binexpr":
            op = expr.children[1].value
            e1 = compile_expr(expr.children[0], values, opti)
            e2 = compile_expr(expr.children[2], values, opti)
            if str.isdigit(e1) and str.isdigit(e2):

                return f"{operation(op,int(e1),int(e2))}"
            return comp_op(op, e1, e2)
        if expr.data == "variable":
            if values[expr.children[0].value] is not None:
                return f"\nmov rax, {values[expr.children[0].value]}"
            else:
                return f"\nmov rax,[{expr.children[0].value}]"
    else:
        if expr.data == "binexpr":
            op = expr.children[1].value
            e1 = compile_expr(expr.children[0], values, opti)
            e2 = compile_expr(expr.children[2], values, opti)
            return comp_op(op, e1, e2)
        if expr.data == "variable":
            return f"\nmov rax,[{expr.children[0].value}]"

    if expr.data == "parenexpr":
        return compile_expr(expr.children[0], values, opti)
    if expr.data == "variable":

        return f"\nmov rax,[{expr.children[0].value}]"
    if expr.data == "nombre":
        e = f"{expr.children[0].value}"
        return f"\nmov rax,{e}"
    if expr.data == "new_array":
        e = compile_expr(expr.children[0], values, opti)
        res = f"{e}\npush rax\npop rbx\nimul rbx,8\nadd rbx,8\nmov rdi, rbx\ncall malloc\npush rax\n{e}\npop rbx\npush rax\nmov rax,rbx\npop rbx\nmov [rax], rbx\n"
        return res
    if expr.data == "len_array":
        e = expr.children[0].value
        return f"\nmov rax,  [{e}]\nmov rax,[rax]"
    if expr.data == "array_access":
        id = expr.children[0].value
        e = compile_expr(expr.children[1], values, opti)
        return f"{e}\npush rax\nmov rax,  [{id}]\npop rbx\nimul rbx,8\nadd rbx,8\nadd rax,rbx\nmov rax,  [rax]"


def compile_cmd(cmd, values, opti):
    global nb_while
    global nb_if
    if cmd.data == "assignement":
        if values[cmd.children[0].value] is not None and opti:
            return ""
        lhs = cmd.children[0].value
        rhs = compile_expr(cmd.children[1], values, opti)
        return f"{rhs}\nmov [{lhs}],rax"
    if cmd.data == "printf":
        return f"{compile_expr(cmd.children[0],values,opti)}\nmov rdi,fmt\nmov rsi,rax\nxor rax,rax\ncall printf"
    if cmd.data == "if":
        nb_if += 1
        e = compile_expr(cmd.children[0], values, opti)
        b = compile_bloc(cmd.children[1], values, opti)
        return f"{e}\ncmp rax,0\njz end_if{nb_if}\n{b}\nend_if{nb_if}:"
    if cmd.data == "while":
        nb_while += 1
        e = compile_expr(cmd.children[0], values, opti)
        b = compile_bloc(cmd.children[1], values, opti)
        return f"\ndeb_while{nb_while}:\n{e}\ncmp rax,0\njz end_while{nb_while}\n{b}\njmp deb_while{nb_while}\nend_while{nb_while}:"
    if cmd.data == "array_assignement":
        lhs = cmd.children[0].value
        e = compile_expr(cmd.children[1], values, opti)
        rhs = compile_expr(cmd.children[2], values, opti)
        return f"{e}\npush rax\nmov rax, [{lhs}]\npop rbx\nimul rbx,8\nadd rbx,8\nadd rax,rbx\npush rax\n{rhs}\npop rbx\nmov [rbx],rax"


def compile_bloc(bloc, values, opti):
    res = ""
    for cmd in bloc.children:
        res += compile_cmd(cmd, values, opti)
    return res


def compile_vars(ast):
    s = ""
    for i in range(len(ast.children)):
        s += f"\nmov rbx, [rbp-0x10]\nmov rdi, [rbx+{8*(i+1)}]\ncall atoi\n\
mov [{ast.children[i].value}], rax\n"

    return s


def compile(prg, opti=False):
    vars_list = var_list(prg)

    dict_assignement = find_assignement(prg, dict.fromkeys(vars_list, 0))
    dict_values = find_values(
        prg, dict_assignement, dict.fromkeys(vars_list, None)
    )

    with open("moule.asm") as f:
        code = f.read()
        vars_decl = "\n".join([f"{x}: dq 0" for x in var_list(prg)])
        code = code.replace("VAR_DECL", vars_decl)
        code = code.replace(
            "RETURN", compile_expr(prg.children[2], dict_values, opti)
        )
        code = code.replace(
            "BODY", compile_bloc(prg.children[1], dict_values, opti)
        )
        code = code.replace("VAR_INIT", compile_vars(prg.children[0]))
        return code


# print(compile_prg(grammaire.parse(program)))


# program = """main(X,Y){

#     U=4+3;
#     printf(Y-X);
#     printf(3+8);
#     return(U+X);
#     }"""


# print(pp_prg(grammaire.parse(program)))
# print("\n")
program = grammaire.parse("".join(open(args.file).readlines()))
program = pp_prg(program)
with open("prog.pac", "w") as f:
    f.write(program)
program = grammaire.parse(program)

with open("prog.asm", "w") as f:
    f.write(compile(program, True))


print(pp_prg(program))
