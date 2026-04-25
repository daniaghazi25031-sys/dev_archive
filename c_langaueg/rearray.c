#include <stdio.h>
int main(){
int d[100],n,i,j=1,tam;
printf("ent num of element; ");
scanf("%d",&n);
for(i=0;i<n;i++){
   printf("num%d; ",i);
   scanf("%d",&d[i]);
}
for(i=0;i<n/2;i++){    //حت من اوصل للنص اعوفه

tam=d[i];
d[i]=d[n-1-i];         //هاي حته  ابدل وي احر رقم موبس  الي بصفه و ناقص i لين ال اي يبدي من الصفر 
d[n-1-i]=tam;


}
for(i=0;i<n;i++){
   printf("%d\n",d[i]);

}
}