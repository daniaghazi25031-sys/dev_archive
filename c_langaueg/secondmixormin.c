#include <stdio.h>

int main() {
    int arr[50], n,i,p1,p2;
    int min;

    printf("Input the size of the array: ");
    scanf("%d", &n);

    printf("Input %d elements in the array:\n", n);
    for(i=0;i<=n;i++){
       printf("enter element-%d:",i);
       scanf("%d",&arr[i]);
    }
for(i=0;i<=n;i++){
   printf("%d ",arr[i]);
   arr[p1]=arr[i+1];
      arr[p2]=arr[i];
       min=p2;
       if (arr[p1]>arr[p2])
         printf("%d ",min);
    
}






}     
 