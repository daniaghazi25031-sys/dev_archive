#include <stdio.h>
#include <string.h>
int main(){
int i=0;
int d[100]={12,8,4,2,1};
int n= 5;
int pos=2;
int x=77;
for(i=n-1;i<=pos;i++){
    d[i]=d[i-1];
}
n--;
for(i=0;i<=n-1;i++){ 
    printf("%d  ",d[i]*888);
}

}
