extern printf, atoi
global main
section .data
fmt: db "%d", 10, 0
fmt_float: db "%f", 10, 0

b: dq 0
x: dq 0
y: dq 0
c: dq 0
a: dq 0
z: dq 0
LC0: dq 50.0
LC1: dq 10.0

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

movsd xmm0,[LC1]
movsd [x],xmm0
movsd xmm0,[LC0]
movsd [y],xmm0
mov rax,[x]
push rax

mov rax,[x]
movq xmm0, rax
pop rax
movq xmm1, rax
mulsd xmm0,xmm1
movsd [x],xmm0
mov rax,[x]
movq xmm0, rax
mov edi, fmt_float
mov eax, 1
call printf
mov rax,[y]
push rax

mov rax,[x]
movq xmm0, rax
pop rax
movq xmm1, rax
subsd xmm0,xmm1
movsd [z],xmm0
mov rax,1
mov [a],rax
mov rax,2
mov [b],rax
mov rax,[b]
push rax

mov rax,[a]
pop rbx
add rax,rbx
mov [c],rax
mov rax,[b]
push rax

mov rax,[a]
pop rbx
add rax,rbx
mov rdi,fmt
mov rsi,rax
xor rax,rax
call printf
mov rax,5
cvtsi2ss xmm0, rax
unpcklps xmm0, xmm0
cvtps2pd xmm0, xmm0
movq rax, xmm0
mov edi, fmt_float
mov eax, 1
call printf

mov rax,[x]

mov rdi, fmt
mov rsi, rax
xor rax, rax
call printf
add rsp, 16
pop rbp
ret
