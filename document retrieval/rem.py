from os import listdir
import os
lis1 = [f for f in listdir("keys/intro/old")]
lis2 = [f for f in listdir("keys/intro/comp")]
#print (lis1)
for i in lis2:
        if i not in lis1:
                print(i)
                os.remove("keys/intro/comp/"+i)
