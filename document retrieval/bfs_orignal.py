def BFS(graph,root):
    checked = []
    visited=[]
    level=[]
    l=[]
    l.append(root)
    level.append(l)
    checked.append(root)
    while len(checked)>0:
        v = checked.pop(0)
        visited.append(v)
        l=[]
        for edge in graph[v]:
            #l=list(set(graph[v])|set(l))
            if edge not in checked and edge not in visited:
                checked.append(edge)
                str1="v"+str(v)+","+"v"+str(edge)+","+"false"+","+str(A[v][edge])+","+"true\n"
                fil_out.write(str1)
        for edge in level[(len(level)-1)]:
            l=list(set(graph[edge])|set(l))
        for i in range(len(level)):
            for j in level[i]:
                if j in l:
                    l.remove(j)
        if len(l)>0:
            level.append(l)
    print(level)
    print(len(level))
f = open('db/introhier.gdf')
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
for each_line in p1:
    l=each_line.split(',')
    if len(l)==5:
        if flag!=0:
            #print(l[0],l[1],l[3])
            A[int(l[0][1:])][int(l[1][1:])]=float(l[3])
        flag=1
    else:
        continue
graph = [[] for x in range(len(V))]
flag=0
i=0
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
#print(graph)
root=43

fil_out=open("bfs.gdf",'w')
fil_out.write("nodedef> name,label\n")
for i in range(0,len(V)):
    fil_out.write(p1[i+1]+'\n')
fil_out.write("\nedgedef>node1,node2,directed,weight,labelvisible\n")
BFS(graph,root)
fil_out.close()

