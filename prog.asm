extern printf, atoi, malloc
global main
section .data
fmt: db "%d", 10, 0
fmt_float: db "%f", 10, 0

i: dq 0
u: dq 0
ashowarr: dq 0
a: dq 0
FLOAT_DECL

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


mov rax, 51
push rax
pop rbx
imul rbx,8
add rbx,8
mov rdi, rbx
call malloc
push rax

mov rax, 51
pop rbx
push rax
mov rax,rbx
pop rbx
mov [rax], rbx

mov [a],rax
mov rax, 0
mov [i],rax
deb_while1:

mov rax,  [a]
mov rax,[rax]
push rax

mov rax,[i]
pop rbx
sub rax,rbx
cmp rax,0
jz end_while1

mov rax,[i]
push rax
mov rax, [a]
pop rbx
imul rbx,8
add rbx,8
add rax,rbx
push rax

mov rax,[i]
pop rbx
mov [rbx],rax
mov rax, 1
push rax

mov rax,[i]
pop rbx
add rax,rbx
mov [i],rax
jmp deb_while1
end_while1:
mov rax, 0
mov [ashowarr],rax
deb_while2:

mov rax,  [a]
mov rax,[rax]
push rax

mov rax,[ashowarr]
pop rbx
sub rax,rbx
cmp rax,0
jz end_while2

mov rax,[ashowarr]
push rax
mov rax,  [a]
pop rbx
imul rbx,8
add rbx,8
add rax,rbx
mov rax,  [rax]
mov rdi,fmt
mov rsi,rax
xor rax,rax
call printf
mov rax, 1
push rax

mov rax,[ashowarr]
pop rbx
add rax,rbx
mov [ashowarr],rax
jmp deb_while2
end_while2:
mov rax, 2
push rax
mov rax,  [a]
pop rbx
imul rbx,8
add rbx,8
add rax,rbx
mov rax,  [rax]
mov rdi,fmt
mov rsi,rax
xor rax,rax
call printf

mov rax,  [a]
mov rax,[rax]

mov rdi, fmt
mov rsi, rax
xor rax, rax
call printf
add rsp, 16
pop rbp
ret
