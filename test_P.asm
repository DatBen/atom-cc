extern printf, atoi
global main
section .data
fmt: db "%d", 10, 0
Y : dq 0
X : dq 0

section .text
main:
push rbp
mov rbp, rsp
push rdi
push rsi

mov rbx, [rbp-0x10]
mov rdi, [rbx+8]
call atoi
mov [X], rax
mov rbx, [rbp-0x10]
mov rdi, [rbx+16]
call atoi
mov [Y], rax

mov rax, [X]
push rax
mov rax, [Y]
pop rbx
sub rax,rbx
mov rdi, fmt
mov rsi,rax
xor rax,rax
call printf
mov rax, [X]
push rax
mov rax, [Y]
pop rbx
imul rax,rbx
mov rdi, fmt
mov rsi,rax
xor rax,rax
call printf
mov rax, [Y]

mov rdi, fmt
mov rsi, rax
xor rax, rax
call printf
add rsp, 16
pop rbp
ret

