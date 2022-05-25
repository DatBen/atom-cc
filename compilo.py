from logging import exception
import lark

import argparse


parser = argparse.ArgumentParser(description="Compile a program")
parser.add_argument("--file", help="the file to compile")
args = parser.parse_args()


grammaire = lark.Lark(
    """ variables: IDENTIFIANT ("," IDENTIFIANT)*
    expr: IDENTIFIANT -> variable | NUMBER -> nombre | expr OP expr -> binexpr | "("expr")" -> parenexpr
    NUMBER : /[0-9]+/
    cmd : IDENTIFIANT "=" expr ";" -> assignement | "while" "("expr")" "{" bloc "}" -> while | "if" "("expr")" "{" bloc "}" -> if | "printf" "("expr")" ";" -> printf
    bloc : (cmd)*
    prog: "main" "(" variables ")" "{" bloc "return" "(" expr ")" ";" "}"
    OP : "+" | "-" | "*" | ">" | "<" | "==" | "!="
    IDENTIFIANT : /[a-zA-Z][a-zA-Z0-9]*/
    %import common.WS
    %ignore WS
     """,
    start="prog",
)


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


def pp_expr(expr):
    if expr.data == "binexpr":
        # print(expr)
        op = expr.children[1].value
        if (
            expr.children[0].data == "nombre"
            and expr.children[2].data == "nombre"
        ):
            e1 = int(expr.children[0].children[0].value)
            e2 = int(expr.children[2].children[0].value)
            return f"{operation(op,e1,e2)}"

        e1 = pp_expr(expr.children[0])
        e2 = pp_expr(expr.children[2])

        return f"({e1} {op} {e2})"
    elif expr.data == "parenexpr":
        return f"({pp_expr(expr.children[0])})"
    elif expr.data in {"variable", "nombre"}:
        return expr.children[0].value

    else:
        return expr.data  # not implemented


def pp_cmd(cmd):
    if cmd.data == "assignement":
        lhs = cmd.children[0].value
        rhs = pp_expr(cmd.children[1])
        return f"{lhs} = {rhs};"
    elif cmd.data == "printf":
        return f"printf({pp_expr(cmd.children[0])});"
    elif cmd.data in {"if", "while"}:
        e = pp_expr(cmd.children[0])
        b = pp_bloc(cmd.children[1])
        return f"{cmd.data}({e}){{\n {b} }}"

    else:
        raise NotImplementedError(cmd.data)


def pp_bloc(bloc):
    return "\n ".join(pp_cmd(cmd) for cmd in bloc.children)


def pp_variables(variables):
    return ",".join(variables.children)


def pp_prg(prog):
    vars = pp_variables(prog.children[0])
    bloc = pp_bloc(prog.children[1])
    ret = pp_expr(prog.children[2])
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


def compile_expr(expr):
    if expr.data == "binexpr":
        op = expr.children[1].value
        if (
            expr.children[0].data == "nombre"
            and expr.children[2].data == "nombre"
        ):
            e1 = int(expr.children[0].children[0].value)
            e2 = int(expr.children[2].children[0].value)
            return f"\nmov rax, {operation(op,e1,e2)}"
        e1 = compile_expr(expr.children[0])
        e2 = compile_expr(expr.children[2])
        if op == "+":
            return f"{e2}\npush rax\n{e1}\npop rbx\nadd rax,rbx"
        if op == "-":
            return f"{e2}\npush rax\n{e1}\npop rbx\nsub rax,rbx"
        if op == "*":
            return f"{e2}\npush rax\n{e1}\npop rbx\nmul rax,rbx"
        if op == "!=":
            return f"{e2}\npush rax\n{e1}\npop rbx\nsub rax,rbx"
        if op == "==":
            return f"{e2}\npush rax\n{e1}\npop rbx\nsub rax,rbx\ncmp rax,0\nje finrax\nmov rax 1\njmp finrax\nfin:mov rax, 0\n"

    if expr.data == "parenexpr":
        return compile_expr(expr.children[0])
    if expr.data == "variable":
        e = expr.children[0].value
        return f"\nmov rax,[{e}]"
    if expr.data == "nombre":
        e = expr.children[0].value
        return f"\nmov rax,{e}"


def compile_cmd(cmd):
    global nb_while
    global nb_if
    if cmd.data == "assignement":
        lhs = cmd.children[0].value
        rhs = compile_expr(cmd.children[1])
        return f"{rhs}\nmov [{lhs}],rax"
    if cmd.data == "printf":
        return f"{compile_expr(cmd.children[0])}\nmov rdi,fmt\nmov rsi,rax\nxor rax,rax\ncall printf"
    if cmd.data == "if":
        nb_if += 1
        e = compile_expr(cmd.children[0])
        b = compile_bloc(cmd.children[1])
        return f"{e}\ncmp rax,0\njz end_if{nb_if}\n{b}\nend_if{nb_if}:"
    if cmd.data == "while":
        nb_while += 1
        e = compile_expr(cmd.children[0])
        b = compile_bloc(cmd.children[1])
        return f"\ndeb_while{nb_while}:\n{e}\ncmp rax,0\njz end_while{nb_while}\n{b}\njmp deb_while{nb_while}\nend_while{nb_while}:"


def compile_bloc(bloc):
    res = ""
    for cmd in bloc.children:
        res += compile_cmd(cmd)
    return res


def compile_prg(prog):
    vars = prog.children[0]
    bloc = prog.children[1]
    ret = prog.children[2]
    return compile_bloc(bloc)


def compile_vars(ast):
    s = ""
    for i in range(len(ast.children)):
        s += f"\nmov rbx, [rbp-0x10]\nmov rdi, [rbx+{8*(i+1)}]\ncall atoi\n\
mov [{ast.children[i].value}], rax\n"
    return s


def compile(prg):
    with open("moule.asm") as f:
        code = f.read()
        vars_decl = "\n".join([f"{x}: dq 0" for x in var_list(prg)])
        prog = compile_prg(prg)
        code = code.replace("VAR_DECL", vars_decl)
        code = code.replace("RETURN", compile_expr(prg.children[2]))
        code = code.replace("BODY", prog)
        code = code.replace("VAR_INIT", compile_vars(prg.children[0]))
        return code


# print(compile_prg(grammaire.parse(program)))

# program = "".join(open(args.file).readlines())
program = """main(X){
    X=3;
    U=4+3;
    printf(2+6);
    return(U+X);
    }"""

print(compile(grammaire.parse(program)))
# print("\n")
# with open("prog.asm", "w") as f:
#     f.write(compile(grammaire.parse(program)))
