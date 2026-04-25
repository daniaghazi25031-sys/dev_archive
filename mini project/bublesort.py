a=[10,5,8,3,59]

h=len(a)
for i in range(h):
    for j in range(0,h-i-1):
        if a[j]>a[j+1]:
           a[j],a[j+1]=a[j+1],a[j]
   
print(a)
           
        
        