from adjmatrix import AdjMatrix
from test import initgraph
import test
import operator
import math
fkey=open("keywords")
raw=fkey.read()
keywrd=raw.split("\n")
keywrd.remove("")
#print keywrd
fqkey=open("query.key","w")
fquery=open("query.txt")
qrytxt=fquery.read().lower()
qkey=[]
for k in keywrd:
    if k in qrytxt:
        fqkey.write(k+'\n')
fqkey.close()
qkey=initgraph("query.key","query.txt")
#qkey=list(test.amatrix.gmatrix['stack'].keys())
#print qkey
deg={}
maxi=test.amatrix.getMaxNumUpdate(qkey)
#print maxi
for k in qkey:
    deg[k]=0.0
    for j in qkey:
        if test.amatrix.gmatrix[k][j].weight != float('inf'):
            #print test.amatrix.gmatrix[k][j].getwt(maxi)
            deg[k]+=1
sorted_deg = sorted(deg.items(), key=operator.itemgetter(1))
sorted_deg=sorted_deg[::-1]
#print sorted_deg[0][1]
max_deg=sorted_deg[0][1]
for i in deg.keys():
    deg[i]/=max_deg

#print deg
ffile=open("filekeys")
raw=ffile.read()

fkeys=raw.split("\n")
filekeys={}
key_int={}
key_no_int={}
file_levels={}
for k in range(len(fkeys)):
    y=fkeys[k].split("<<")
    file_levels[y[0]]=y[1:]
    fkeys[k]=fkeys[k].replace("<<",",")
    x=fkeys[k].split(",")
    filekeys[x[0]]=x[1:]
    key_int[x[0]]=list(set(qkey)&set(filekeys[x[0]]))
    key_no_int[x[0]]=len(key_int[x[0]])
sorted_key_int = sorted(key_no_int.items(), key=operator.itemgetter(1))
sorted_key_int= sorted_key_int[::-1]
#print sorted_key_int
result={}
for i in range(10):
    similarity={}
    for j in key_int[sorted_key_int[i][0]]:
        if j in file_levels[sorted_key_int[i][0]][0]:
            similarity[j]=1
        elif j in file_levels[sorted_key_int[i][0]][1]:
            similarity[j]=0.75
        elif j in file_levels[sorted_key_int[i][0]][2]:
            similarity[j]=0.5
        elif j in file_levels[sorted_key_int[i][0]][3]:
            similarity[j]=0.25
        else:
            similarity[j]=0
    s=0
    for k in deg.keys():
        if k in similarity.keys():
            s+=(deg[k]-similarity[k])**2
        else:
            s+=(deg[k])**2
    result[sorted_key_int[i][0]]=math.sqrt(s)
sorted_result = sorted(result.items(), key=operator.itemgetter(1))            
for i in range(len(sorted_result)):
    print sorted_result[i][0]
