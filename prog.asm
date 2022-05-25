extern printf, atoi
global main
section .data
fmt: db "%d", 10, 0
a: dq 0

section .text
main:
push rbp
mov rbp, rsp
push rdi
push rsi


mov rbx, [rbp-0x10]
mov rdi, [rbx+8]
call atoi
mov [a], rax


deb_while1:

mov rax,8
push rax

mov rax,[a]
pop rbx
sub rax,rbx
cmp rax,0
jz end_while1

mov rax,1
push rax

mov rax,[a]
pop rbx
sub rax,rbx
mov [a],rax
mov rax,[a]
mov rdi,fmt
mov rsi,rax
xor rax,rax
call printf
jmp deb_while1
end_while1:

mov rax,[a]

mov rdi, fmt
mov rsi, rax
xor rax, rax
call printf
add rsp, 16
pop rbp
ret
