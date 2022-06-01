extern printf, atoi
global main
section .data
fmt: db "%d", 10, 0
fmt_float: db "%f", 10, 0

b: dq 0
c: dq 0
a: dq 0
LC0: dq 10.0
LC1: dq 2.0

section .text
main:
push rbp
mov rbp, rsp
push rdi
push rsi


mov rbx, [rbp-0x10]
mov rdi,[rbx-0]
call atoi
mov [a],rax

mov rax,10
mov [a],rax
movsd xmm0,[LC1]
movsd [c],xmm0
movsd xmm0,[LC0]
movsd [b],xmm0
mov rax,[b]
movq xmm0, rax
mov edi, fmt_float
mov eax, 1
call printf
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
