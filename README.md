# atom-cc

Float doesn't work with optimisation !

### /!\ Be careful, parentheses are very important, a code like 1 + 4 == 5 can have both behavior, 5 == 5 or 1 + (4==5) -> 1 because == equals to have 0 if False, everything else if True

##How to compile main.ac ?

No optimisation :
./atom-cc.sh float.ac -> ./main

With optimation :
./atom-cc.sh float.ac -01 -> ./main

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
/!\ This function forbid the use of var named $array_nameshowarr

```
showarr(array)
```

## Optimisation

The compilator has a optimisation option which improve the execution time of the generated binary.

First, immediate calculations are done during the compilation. Which means that expression such has (1+3)\*(4-2) is replace by 8 in the assembly code.

Then, variables that are assigned only once by a constant value are not stored as a variable and are replace by there value every where in the assembly code.
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

Finaly, dead code from if bloc are deleted and if bloc always true are replace by a simple bloc.
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

**All this optimisation principles work together.**
<<<<<<< HEAD
=======

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

> > > > > > > ben
