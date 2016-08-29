def BFS(graph,root,p1,max1):
    checked = []
    visited=[]
    energy=[]
    level=[]
    l=[]
    l.append(root)
    level.append(l)
    checked.append(root)
    inienergy=14600
    threshold=10
    l1=0
    flag=0
    energy.append(inienergy)
    while(len(checked)>0):
        l1=l1+1
        #print "level"+str(l1)
        v=checked.pop(0)
        e1=energy.pop(0)
        while v in visited:
            #print "ll"
            if(len(checked)>0):
                v=checked.pop(0)
        
            if len(checked)==0:
                 flag=1
                 break
        if(flag==1):
            break
       # print "kk"
        visited.append(v)
        l=[]
        #print str(v)+"-->"
        if(float(e1)/float(len(graph[v])) >= float(threshold)):
            for edge in graph[v]:
                #print edge
                if edge not in checked:
                    checked.append(edge)
                energy.append(float(e1*A[v][edge]/(len(graph[v])*max1)))
                str1="v"+str(v)+","+"v"+str(edge)+","+"false"+","+str(A[v][edge])+","+"true\n"
                fil_out.write(str1)
            for edge in level[(len(level)-1)]:
                               
                l=list(set(graph[edge])|set(l))
                #print "l "+str(l)
            for i in range(len(level)):
                for j in level[i]:
                    if j in l:
                        l.remove(j)
            if len(l)>0:
                level.append(l)

                
f = open('dsfull1.gdf')
text=f.read()
p1=text.split('\n')
V=[]
flag=0
for each_line in p1:
    l=each_line.split(',')
    if len(l)==2:
        if flag!=0:
            #print(l[0])
            V.append(int(l[0][1:]))
        flag=1
    else:
        break
A = [[0 for x in range(len(V))] for x in range(len(V))]
flag=0
max1=-1
for each_line in p1:
    l=each_line.split(',')
    if len(l)==5:
        if flag!=0:
            #print(l[0],l[1],l[3])
            A[int(l[0][1:])][int(l[1][1:])]=float(l[3])
            #if(float(l[3]>max)):
             #  max1=float(l[3])
        flag=1
    else:
        continue
#print max1
graph = [[] for x in range(len(V))]
flag=0
i=0
x=0
for each_line in p1:
    l=each_line.split(',')
    if len(l)==5:
        if flag!=0:
            #print(l[0],l[1],l[3])
            #A[int(l[0][1:])][int(l[1][1:])]=float(l[3])
            graph[int(l[0][1:])].append(int(l[1][1:]))
        flag=1
    else:
        continue

root=154
#print(len(graph[root]))
fil_out=open("sub5.gdf",'w')
fil_out1=open("ds2.txt","w")
fil_out.write("nodedef> name,label\n")
for i in range(0,len(V)):
    fil_out.write(p1[i+1]+'\n')
fil_out.write("edgedef>node1,node2,directed,weight,labelvisible\n")
h=p1[root+1].split(',')
fil_out1.write(str(h[1])+",")
BFS(graph,root,p1,max1)
fil_out.close()
f.close()







        
        
        
        
