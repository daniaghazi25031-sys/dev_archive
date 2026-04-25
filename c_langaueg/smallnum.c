#include <stdio.h>
int main(){
int d[100],n,i,j=1,tam,p;
printf("ent num of element; ");
scanf("%d",&n);
for(i=0;i<n;i++){
   printf("num%d; ",i);
   scanf("%d",&d[i]);
}
p=0;
tam=d[0];
for(i=0;i<n;i++){
    if(tam>d[i])
       tam=d[i];
        p=i;  
    }
printf("%d,,%d",tam,p);
}




