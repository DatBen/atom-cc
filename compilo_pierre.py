import lark
from numpy import var

grammaire = lark.Lark(
    """
variables : IDENTIFIANT (","  IDENTIFIANT)*
expr : IDENTIFIANT -> variable | NUMBER -> nombre
| expr OP expr -> binexpr | "(" expr ")" -> parenexpr
cmd : IDENTIFIANT "=" expr ";"-> assignment|"while" "(" expr ")" "{" bloc "}" -> while
    | "if" "(" expr ")" "{" bloc "}" -> if | "printf" "(" expr ")" ";"-> printf
bloc : (cmd)*
prog : "main" "(" variables ")" "{" bloc "return" "(" expr ")" ";" "}"
NUMBER : /[0-9]+/
OP : /[+\*\/>-]/
IDENTIFIANT : /[a-zA-Z][a-zA-Z0-9]*/
%import common.WS
%ignore WS
""",
    start="prog",
)

compteur = iter(range(10000))


def pp_variables(vars):
    return ", ".join([t.value for t in vars.children])


def pp_expr(expr):
    if expr.data in {"variable", "nombre"}:
        return expr.children[0].value
    elif expr.data == "binexpr":
        e1 = pp_expr(expr.children[0])
        e2 = pp_expr(expr.children[2])
        op = expr.children[1].value
        return f"{e1} {op} {e2}"
    elif expr.data == "parenexpr":
        return f"({pp_expr(expr.children[0])})"
    else:
        raise Exception("Not implemented")


def pp_cmd(cmd):
    if cmd.data == "assignment":
        lhs = cmd.children[0].value
        rhs = pp_expr(cmd.children[1])
        return f"{lhs} = {rhs};"
    elif cmd.data == "printf":
        return f"printf( {pp_expr(cmd.children[0])} );"
    elif cmd.data in {"while", "if"}:
        e = pp_expr(cmd.children[0])
        b = pp_bloc(cmd.children[1])
        return f"{cmd.data} ({e}) {{ {b}}}"
    else:
        raise Exception("Not implemented")


def pp_bloc(bloc):
    return "\n".join([pp_cmd(t) for t in bloc.children])


def pp_prg(prog):
    vars = pp_variables(prog.children[0])
    bloc = pp_bloc(prog.children[1])
    ret = pp_expr(prog.children[2])
    return f"main ({vars}){{ {bloc} return ({ret});}}"


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


def compile_vars(ast):
    s = ""
    for i in range(len(ast.children)):
        s += f"mov rbx, [rbp-0x10]\nmov rdi, [rbx+{8*(i+1)}]\ncall atoi\n\
mov [{ast.children[i].value}], rax\n"
    return s


def compile(prg):
    with open("moule.asm") as f:
        code = f.read()
        var_decl = "\n".join([f"{x} : dq 0" for x in var_list(prg)])
        code = code.replace("VAR_DECL", var_decl)
        code = code.replace("RETURN", compile_expr(prg.children[2]))
        code = code.replace("BODY", compile_bloc(prg.children[1]))
        code = code.replace("VAR_INIT", compile_vars(prg.children[0]))
    return code


def compile_expr(expr):
    op2asm = {
        "+": "add rax,rbx",
        "-": "sub rax,rbx",
        "*": "imul rax,rbx",
        "/": "div rax,rbx",
    }
    if expr.data == "variable":
        return f"mov rax, [{expr.children[0].value}]"
    elif expr.data == "nombre":
        return f"mov rax, {expr.children[0].value}"
    elif expr.data == "binexpr":
        e1 = compile_expr(expr.children[0])
        e2 = compile_expr(expr.children[2])
        op = expr.children[1].value
        return f"{e2}\npush rax\n{e1}\npop rbx\n{op2asm[op]}"
        # if op == "+":
        #     return f"{e2}\npush rax\n{e1}\npop rbx\nadd rax,rbx"
        # if op == "-":
        #     return f"{e2}\npush rax\n{e1}\npop rbx\nsub rax,rbx"
        # if op == "*":
        #     return f"{e2}\npush rax\n{e1}\npop rbx\nimul rax,rbx"
        # if op == "/":
        #     return f"{e2}\npush rax\n{e1}\npop rbx\ndiv rax,rbx"
        # if op == "%":
        #     return f"{e2}\npush rax\n{e1}\npop rbx\nmod rax,rbx"
    elif expr.data == "parenexpr":
        return compile_expr(compile_expr(expr.children[0]))
    else:
        raise Exception("Not implemented")


def compile_bloc(bloc):
    return "\n".join([compile_cmd(cmd) for cmd in bloc.children])


def compile_cmd(cmd):
    global compteur
    if cmd.data == "assignment":
        lhs = cmd.children[0].value
        rhs = compile_expr(cmd.children[1])
        return f"{rhs}\nmov [{lhs}], rax"
    elif cmd.data == "printf":
        return f"{compile_expr(cmd.children[0])}\nmov rdi, fmt\nmov rsi,rax\nxor rax,rax\ncall printf"
    elif cmd.data == "if":
        e = compile_expr(cmd.children[0])
        b = compile_bloc(cmd.children[1])
        index = next(compteur)
        return f"{e}cmp rax,0\njz fin{index}\n{b}\nfin{index}"
    elif cmd.data == "while":
        e = compile_expr(cmd.children[0])
        b = compile_bloc(cmd.children[1])
        index = next(compteur)
        return f"debut{index}:\n{e}\ncmp rax,0\njz fin{index}\n{b}\njmp debut{index}\nfin{index}:"

    else:
        print("la")
        print(cmd.data)
        raise Exception("Not Implemented")


prg = grammaire.parse(
    """main(X,Y) {
while(X){
    Z=3;
    X = X - 1; Y = Y+1;
}
printf(Y+1);
return(Y);}"""
)

prg2 = grammaire.parse(
    """main(X,Y) {
printf(Y-X);
printf(Y*X);

return(Y);}"""
)
# printf(X);

# print(prg.children[0])

print(compile(prg2))
# prg2 = grammaire.parse(pp_prg(prg))
# print(prg2 == prg)
# print(var_list(prg))
