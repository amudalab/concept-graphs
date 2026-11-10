import sys
import os

path=sys.argv[1] if len(sys.argv) > 1 else "data/"
txt=[]

def updatekey(x):
    fkey=open("data/txt2keyphrase.txt","w")
    for t in x:
        fkey.write(str(t)+"\n")
    fkey.close()

def readtxtfile():
    tkey=open("data/txt2keyphrase.txt")
    key=tkey.read()
    txt=key.split("\n")
    return txt
    
def callshell():
    for f in os.listdir(path):
        if f not in txt:
            command="sh ss2.sh \""+os.path.join(path,f)+"\""
            os.system(command)
            print(command)
            txt.append(f)
            updatekey(txt)
        else:
            print("FILE: "+f+" keyphrase already extracted")

txt=readtxtfile()
callshell()
