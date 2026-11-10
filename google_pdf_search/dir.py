import sys
import os
import pdfminer

pypath=os.getcwd()
path=sys.argv[1] if len(sys.argv) > 1 else "data/"
val=0
compkey=[]

def updatekeycount(x):
    fkey=open("data/pdf2txtcount.txt","w")
    fkey.write(str(x))
    fkey.close()
    
def pdfcount():
    fkey=open("data/pdf2txtcount.txt")
    keyval=fkey.read()
    keyval=int(keyval)
    fkey.close()
    return keyval

def keycount():
    fkey=open("data/keycount.txt")
    keyval=fkey.read()
    keyval=int(keyval)
    fkey.close()
    return keyval


def readcompkey():
    f=open("compkey.txt")
    txt=f.read().lower()
    key=txt.split("\n")
    c=0
    for i in key:
        ni=i.split("\t")
        compkey.append(ni[0])
        c+=1
'''
for f in os.listdir(path):
    print(f+"\n")
'''
readcompkey()
kval=keycount()
pval=pdfcount()
for i in range(kval):
    fpath=path+"\\"+compkey[pval]
    for f in os.listdir(fpath):
        k=f.split(".")
        k="\\transcript\\"+k[0]+".txt"
        print(f)
        command="python \""+pypath+"\\pdf2txt.py\" -o \""+pypath+k+"\" \""+fpath+"\\"+f+"\""
        #print(command)
        os.system(command)
    print("FOLDER :"+compkey[pval]+" done....")
    pval+=1
    updatekeycount(pval)
    
