extern printf, atoi
global main
section .data
fmt: db "%d", 10, 0
U: dq 0
X: dq 0
Z: dq 0
Y: dq 0

section .text
main:
push rbp
mov rbp, rsp
push rdi
push rsi


mov rbx, [rbp-0x10]
mov rdi,[rbx-0]
call atoi
mov [X],rax
mov rbx, [rbp-0x10]
mov rdi,[rbx-8]
call atoi
mov [Y],rax

mov rax,[Y]
push rax

mov rax,[X]
pop rbx
add rax,rbx
mov [Z],rax5
mov [U],rax
mov rax,[U]
push rax

mov rax,[Z]
pop rbx
add rax,rbx
mov rdi,fmt
mov rsi,rax
xor rax,rax
call printf
-4

mov rdi, fmt
mov rsi, rax
xor rax, rax
call printf
add rsp, 16
pop rbp
ret
