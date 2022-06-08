main (a) {
 u = 1;
 a = new int[u + 25 + 25];
 i = 0;
 while(i != len(a)){
 a[i] = i;
 i = i + 1; }
 ashowarr=0;
while(ashowarr!=len(a)){
printf(a[ashowarr]);
ashowarr=ashowarr+1;
}

 printf(a[2]); 
 return(len(a));
}