### a sample graph
##graph = {'A': ['B', 'C','E'],
##             'B': ['A','C', 'D'],
##             'C': ['D'],
##             'D': ['C'],
##             'E': ['D'],
##             'F': []}
fp = open('taxem.gdf')
text=fp.read()
pl=text.split('\n')
#print(p1)
flag=0
V=[]
graph={}
flag=0
for each_line in pl:
    l=each_line.split(',')
    if len(l)==2:
        if flag!=0:
            V.append(l[0])
            graph[l[0]]=[]
        flag=1
flag=0
for each_line in pl:
    l=each_line.split(',')
    if len(l)==5:
        if flag!=0:
            #print(l[0],l[1],l[3])
            graph[l[0]].append(l[1])
        flag=1
    else:
        continue
class MyQUEUE: # just an implementation of a queue

    def __init__(self):
        self.holder = []

    def enqueue(self,val):
        self.holder.append(val)

    def dequeue(self):
        val = None
        try:
            val = self.holder[0]
            if len(self.holder) == 1:
                self.holder = []
            else:
                self.holder = self.holder[1:]   
        except:
            pass

        return val  

    def IsEmpty(self):
        result = False
        if len(self.holder) == 0:
            result = True
        return result


path_queue = MyQUEUE() # now we make a queue


def BFS(graph,start,end,q):

    temp_path = [start]
    path_len='inf'

    q.enqueue(temp_path)

    while q.IsEmpty() == False:
        tmp_path = q.dequeue()
        last_node = tmp_path[len(tmp_path)-1]
        print tmp_path
        if last_node == end:
            print "VALID_PATH : ",tmp_path
            if path_len=='inf':
                    path_len=len(tmp_path)-1
            else:
                if path_len>len(tmp_path)-1:
                    path_len=len(tmp_path)-1
                        
        else:
            print "0"
        for link_node in graph[last_node]:
            if link_node not in tmp_path:
                #new_path = []
                new_path = tmp_path + [link_node]
                q.enqueue(new_path)
    print path_len
    return path_len

fp = open('db/introhier.gdf')
text=fp.read()
pl=text.split('\n')
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
for x in range(len(V)):
    for y in range(len(V)):
        if A[x][y]!='inf':
            path_len=BFS(graph,"v"+str(x),"v"+str(y),path_queue)
            if A[x][y] != 'inf' and path_len!='inf':
                A[x][y]=(A[x][y]*path_len)/6

fil_out=open("enhanced_semantic_net.gdf","w")
for each_line in pl:
    l=each_line.split(',')
    if len(l)==2:
        fil_out.write(each_line+'\n')
fil_out.write("edgedef>node1,node2,directed,weight,labelvisible\n")
for i in range(len(V)):
    for j in range(len(V)):
        if A[i][j]!='inf':
            str1="v"+str(i)+","+"v"+str(j)+","+"false"+","+str(A[i][j])+","+"true\n"
            fil_out.write(str1)
fil_out.close()
