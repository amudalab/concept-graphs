import operator
fil_in = open('db/introhier2.gdf')
fil=open("degree2.txt","w")
text=fil_in.read()
pl=text.split('\n')
#print(p1)
flag=0
V=[]
VN={}
flag=0
for each_line in pl:
    l=each_line.split(',')
    if len(l)==2:
        if flag!=0:
            V.append(l[0])
            VN[l[0]]=l[1].replace("\r","")
        flag=1
A = [['inf' for x in range(len(V))] for x in range(len(V))]
flag=0
for each_line in pl:
    l=each_line.split(',')
    if len(l)==5:
        if flag!=0:
            #print(l[0],l[1],l[3])
            A[int(l[0][1:])][int(l[1][1:])]=float(l[3])
        flag=1
    else:
        continue
degree={}
for i in range(len(V)):
    count = 0.0
    for j in range(len(V)):
        if A[i][j]!='inf':
            count +=1
    degree[V[i]]=count
fil.write("linedef>node,label,degree\n")
degree = sorted(degree.items(), key=operator.itemgetter(1), reverse=True)
maxi=degree[0][1]
for r in range(len(V)):
    fil.write(str(degree[r][0])+','+str(VN[degree[r][0]])+','+str(degree[r][1]/maxi)+'\n')
fil_in.close()
fil.close()
