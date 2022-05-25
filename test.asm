extern printf
global main
section .data
hello :
    db 'Hello World! %d', 10,0;

section .text

main :
push rsi
mov rsi,12;
mov rdi,hello;
xor rax,rax
call printf
pop rsi
ret
