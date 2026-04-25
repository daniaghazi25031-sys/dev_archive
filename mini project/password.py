import random
num=[1,2,3,4,5,6,7,8,9,0]
c=[]
for i in range(65,91):
    c.append(chr(i))
l=[]
for j in range(97,123):
    l.append(chr(j))
s=['#','@','%','&','$']

all_passwords = []

for n in range(100):
    p=[]
    o=random.choice(c)
    p.append(o)
    for x in range(6):
        d=random.choice(num+l+s+c)
        p.append(d)
    
    wordpass="".join(map(str,p))
    all_passwords.append(wordpass)
    print(wordpass)

with open("passwords.txt", "w") as f:
    for line in all_passwords:
        f.write(line + "\n")