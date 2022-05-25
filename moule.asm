extern printf, atoi
global main
section .data
fmt: db "%d", 10, 0
fmt_float: db "%lf", 10, 0

VAR_DECL
FLOAT_DECL

section .text
main:
push rbp
mov rbp, rsp
push rdi
push rsi

VAR_INIT
BODY
RETURN

mov rdi, fmt
mov rsi, rax
xor rax, rax
call printf
add rsp, 16
pop rbp
ret
