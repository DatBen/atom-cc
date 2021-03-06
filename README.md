# atom-cc

- **/!\ The main branch of this repository is the branch named "Ben" not "Main"**

- **/!\ Float implementation doesn't work with optimisation !**

- **/!\ Be careful, parentheses are very important, a code like 1 + 4 == 5 can have both behavior, 5 == 5 or 1 + (4==5) -> 1 because == equals to have 0 if False, everything else if True**

## How to compile main.ac ?

No optimisation :

```
./atom-cc.sh name_of_my_code_file.ac
./main --args
```

With optimisation :

```
./atom-cc.sh name_of_my_code_file.ac -01
./main --args
```

## Array

Create array:

```
array = new int[len_of_array]
```

Modify array:

```
array[index]=expr
```

Access array:

```
access=array[index]
```

Length of array:

```
len_array=len(array)
```

Print array:
/!\ This function forbid the use of var named $(array_name)showarr

```
showarr(array)
```

Exemple de code :

```
main(a)
{   u=1;
    a=new int[u+25+25];
    i=0;
    while(i!=len(a)){
        a[i]=i;
        i=i+1;

    }
    showarr(a);
    return (len(a));
}

```

## Optimisation

The compiler has an optimisation option which improve the execution time of the generated binary code after compilation.

First, immediate calculations are done during the compilation. Which means that expression such has (1+3)\*(4-2) are replace by their value (8 in this example) in the assembly code.

Then, variables that are assigned only once by a constant value are not stored as a variable and are also replace by their value everywhere in the assembly code.
For instance a code like this :

```
A=5+6;
B=A*2;
printf(B);
```

is compiled like if it was written like that :

```
printf(22)
```

This way we gain in memory usage and in execution time.

Finaly, the optimised pretty printer can recognize dead code. Dead code from "if" blocs are deleted and "if" blocs always true are replaced by a simple bloc.
For instance, this code :

```
if(1 == 1){
    A = A+1
}
if (A == A-1){
    A = 0
}
```

is replace by :

```
A = A+1
```

**All this optimisation principles work together. The pretty printer and the compiler do these optimisations (exept for the dead code recognition). Which means that a code do not need to be pre-processed by the pretty printer to be optimized by the compilator.**

To run an example which show all this principles and print the code optimized you can run :

```
./atom-cc.sh exemple_opt.ac -01
./main --arg
```

where --arg is an integer.

Here is exemple_opt.ac :

```
main(X)
{   A=1+4;
    U = A*2;
    if(0){
        U = 200;
    }
    if((1+4)==5){
        U = 1;
    }
    if((A+X)==5){
        U = 2;
    }
    if(A == 5){
        U = U+X;
    }
    return (U);
}
```

It will be compiled like if it were written like this :

```
main (X) {
 U = 10;
 U = 1;
 if((5 + X) == 5){
 U = 2; }
 U = U + X;
 return(U);
}
```

So finaly, the algorithm return X + 1 exept if X = 0, then it return 2.

## Float

Define a float :

```
x=2.5f
```

If you want copy a float in another variable, set this variable to a float first :

```
z=0.0f
z=x
```

Once the variable has been seen as a float, it can't be assigned to an int

Operation with float :

```
z=0.0f
x=1.0f
y=2.0f
z=x+y
z=x/y
z=x-y
z=x*y
```

You can cast an int to a float :

```
x=1
z=(float) x
```
