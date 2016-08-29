import nltk
import re

def stem(word):
    regexp = r'^(.*?)(es|s)?$'
    stem, suffix = re.findall(regexp, word)[0]
    #print(stem)
    return stem

def indxes(a,item):
    l=[]
    wlist=item.split(" ")
   # print wlist
    if len(wlist)>1:
        c1=a.count(stem(wlist[0]))
        c2=a.count(stem(wlist[1]))
        #print c1,c2
        if c1>c2:
                c=c2
        else:
                c=c1
        ini=0
        fin=len(a)-1
        while (c1>0 and c2>0):
                
                ind1=a[ini:fin].index(stem(wlist[0]))+ini
                if flist[ind1+1]==stem(wlist[1]):
                    l.append(ind1)
                ini=ind1+1
                c1=c1-1
                
    else:
            ini=0
            fin=len(a)
            c=a.count(stem(wlist[0]))           
            while c>0:
                ind=a[ini:fin].index(stem(item))+ini
                ini=ind+1
                c=c-1
                l.append(ind)
   # print l
    return l

        

fd=open("nwdb1.txt")
key=[]
for each_line in fd:
        x=each_line.strip('\n')
        key.append(x)
        


print("KEYWORDS: ")
print(key)
x=input()

fw=open("fileomkey","w")

for tword in key:
        
        fil="all/"+tword
        print("FILENAME: ",fil)
        fo=open(fil)
        tx=(fo.read()).lower()
        tx=tx.replace("\n"," ")
        tx=tx.replace("\t"," ")
        tx=tx.replace("("," ")
        tx=tx.replace(")"," ")
        tx=tx.replace("\\"," ")
        tx=tx.replace("/"," ")
        tx=tx.replace("."," ")
        tx=tx.replace("["," ")
        tx=tx.replace("]"," ")
        tx=tx.replace(":"," ")
        tx=tx.replace(","," ")
        
        flist=tx.split(" ")
        print(flist)
        #z=input()
        for i in range(0,len(flist)):
            if len(flist[i])>1:
                flist[i]=stem(flist[i])                 
        lis=[]
        for w in key:
            
            w=w.strip("\n")
            w=w.strip(",")
            ind=indxes(flist,w.lower())
            if len(ind)!=0:
                print(w.lower(),tword)
                lis.append(w)
        print("OUTPUT: \n",lis)
        if len(lis)!=0:
            fw.write(tword+">"+lis[0])
            for i in range(1,len(lis)):
                fw.write(","+lis[i])
            fw.write("\n")
             
        
fo.close()        
fw.close()

