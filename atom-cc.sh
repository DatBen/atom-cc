python3 build/compilo.py --file $1 --moule build/moule.asm
nasm -f elf64 build/prog.asm
gcc -o build/main -no-pie -fno-pie build/prog.o
./build/main