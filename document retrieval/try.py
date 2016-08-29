from os import listdir
##fn=open("Corpus/intro/ds11.txt")
##raw=fn.read()
##raw2=raw.replace('subtree','sub tree')
##fn.close()
##fn=open("Corpus/intro/ds11.txt","w")
##fn.write(raw2)
##fn.close()
##fp = open('db/introhier.gdf')
##text=fp.read()
##pl=text.split('\n')
###print(p1)
##flag=0
##V=[]
##VN={}
##flag=0
##for each_line in pl:
##    l=each_line.split(',')
##    if len(l)==2:
##        if flag!=0:
##            V.append(l[1].replace("\n","").replace("\r",""))
##            VN[l[0]]=l[1].replace("\n","").replace("\r","")
##        flag=1
##
##print V
##lis1 = [f for f in listdir("C:/Users/Romauld/Desktop/final version 3/new_data_struct/Keys/intro/comp")]
##for j in lis1:
##    f = open("Keys/intro/comp/"+j)
##    raw=f.read().lower()
##    w=raw.split("\n")
##    f.close()
##    f = open("Keys/intro/comp/"+j,"w")
##    print w
##    for x in w:
##        print x
##        if x in V:
##            f.write(str(x)+"\n")
##    f.close()
##    
for i in range(5):
    for j in range(i,5):
        print i, j
