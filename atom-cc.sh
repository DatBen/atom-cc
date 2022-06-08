rm -f build/main build/prog.o build/prog.asm

if [ $# = 1 ]
then
    python3 build/compilo.py --file $1 --moule build/moule.asm
    nasm -f elf64 build/prog.asm
    gcc -o main -no-pie -fno-pie build/prog.o
fi



if [ $# = 2 ]
then
    python3 build/compilo-opti.py --file $1 --moule build/moule.asm
    nasm -f elf64 build/prog.asm
    gcc -o main -no-pie -fno-pie build/prog.o
fi

