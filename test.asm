extern printf, atoi
global main
section .data
fmt: db "%d", 10, 0
U: dq 0
X: dq 0

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

mov rax,3
mov [X],rax
mov rax, 7
mov [U],rax
mov rax, 8
mov rdi,fmt
mov rsi,rax
xor rax,rax
call printf

mov rax,[X]
push rax

mov rax,[U]
pop rbx
add rax,rbx

mov rdi, fmt
mov rsi, rax
xor rax, rax
call printf
add rsp, 16
pop rbp
ret

