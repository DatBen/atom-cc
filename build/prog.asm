extern printf, atoi, malloc
global main
section .data
fmt: db "%d", 10, 0
fmt_float: db "%f", 10, 0

u: dq 0
ushowarr: dq 0
b: dq 0
x: dq 0
y: dq 0
a: dq 0
c: dq 0
z: dq 0
LC0: dq 0.0
LC1: dq 10.0
LC2: dq 50.0

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


movsd xmm0,[LC1]
movsd [x],xmm0
movsd xmm0,[LC2]
movsd [y],xmm0
mov rax,[y]
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
movsd [x],xmm0
mov rax,[x]
movq xmm0, rax
mov edi, fmt_float
mov eax, 1
call printf
movsd xmm0,[LC0]
movsd [z],xmm0
mov rax,[x]
mov [z],rax
mov rax,[z]
movq xmm0, rax
mov edi, fmt_float
mov eax, 1
call printf
mov rax,1
mov [a],rax
mov rax,2
mov [b],rax
mov rax,[b]
push rax

mov rax,[a]
pop rbx
add rax,rbx
mov rdi,fmt
mov rsi,rax
xor rax,rax
call printf
mov rax,[a]
cvtsi2ss xmm0, rax
unpcklps xmm0, xmm0
cvtps2pd xmm0, xmm0
movq rax, xmm0
movsd [c],xmm0
mov rax,[y]
push rax

mov rax,[c]
movq xmm0, rax
pop rax
movq xmm1, rax
addsd xmm0,xmm1
movsd [c],xmm0
mov rax,[c]
movq xmm0, rax
mov edi, fmt_float
mov eax, 1
call printf
mov rax,5
push rax
pop rbx
imul rbx,8
add rbx,8
mov rdi, rbx
call malloc
push rax

mov rax,5
pop rbx
push rax
mov rax,rbx
pop rbx
mov [rax], rbx

mov [u],rax
mov rax,0
push rax
mov rax, [u]
pop rbx
imul rbx,8
add rbx,8
add rax,rbx
push rax

mov rax,1
pop rbx
mov [rbx],rax
mov rax,4
push rax
mov rax, [u]
pop rbx
imul rbx,8
add rbx,8
add rax,rbx
push rax

mov rax,8
pop rbx
mov [rbx],rax
mov rax,0
mov [ushowarr],rax
deb_while1:

mov rax,  [u]
mov rax,[rax]
push rax

mov rax,[ushowarr]
pop rbx
sub rax,rbx
cmp rax,0
jz end_while1

mov rax,[ushowarr]
push rax
mov rax,  [u]
pop rbx
imul rbx,8
add rbx,8
add rax,rbx
mov rax,  [rax]
mov rdi,fmt
mov rsi,rax
xor rax,rax
call printf
mov rax,1
push rax

mov rax,[ushowarr]
pop rbx
add rax,rbx
mov [ushowarr],rax
jmp deb_while1
end_while1:

mov rax,[x]

mov rdi, fmt
mov rsi, rax
xor rax, rax
call printf
add rsp, 16
pop rbp
ret
