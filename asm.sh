nasm -f elf64 prog.asm
gcc -o main -no-pie -fno-pie  prog.o
./main 10 5