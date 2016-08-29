# prim - minimum spanning tree
# Tim Wilson, 2-25-2002

#A = adjacency matrix, u = vertex u, v = vertex v
def weight(A, u, v):
    return A[u][v]

#A = adjacency matrix, u = vertex u
def adjacent(A, u):
    L = []
    for x in range(len(A)):
        if A[u][x] > 0 and x != u:
            L.insert(0,x)
    return L

#Q = min queue
def extractMin(Q):
    q = Q[0]
    Q.remove(Q[0])
    return q

#Q = min queue, V = vertex list
def decreaseKey(Q, K):
    for i in range(len(Q)):
        for j in range(len(Q)):
            if K[Q[i]] < K[Q[j]]:
                s = Q[i]
                Q[i] = Q[j]
                Q[j] = s

#V = vertex list, A = adjacency list, r = root
def prim(V, A, r):
    u = 0
    v = 0

    # initialize and set each value of the array P (pi) to none
    # pi holds the parent of u, so P(v)=u means u is the parent of v
    P=[None]*len(V)

    # initialize and set each value of the array K (key) to some large number (simulate infinity)
    K = [999999]*len(V)

    # initialize the min queue and fill it with all vertices in V
    Q=[0]*len(V)
    for u in range(len(Q)):
        Q[u] = V[u]

    # set the key of the root to 0
    K[r] = 0
    decreaseKey(Q, K)    # maintain the min queue

    # loop while the min queue is not empty
    while len(Q) > 0:
        u = extractMin(Q)    # pop the first vertex off the min queue

        # loop through the vertices adjacent to u
        Adj = adjacent(A, u)
        for v in Adj:
            w = weight(A, u, v)    # get the weight of the edge uv

            # proceed if v is in Q and the weight of uv is less than v's key
            if Q.count(v)>0 and w < K[v]:
                # set v's parent to u
                P[v] = u
                # v's key to the weight of uv
                K[v] = w
                decreaseKey(Q, K)    # maintain the min queue
    return P
f = open('output/comp_introhier.gdf')
text=f.read()
p1=text.split('\n')
#print(p1)
flag=0
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
##A = [ [0,  4,  0,  0,  0,  0,   0,  8,  0],
##      [4,  0,  8,  0,  0,  0,   0, 11,  0],
##      [0,  8,  0,  7,  0,  4,   0,  0,  2],
##      [0,  0,  7,  0,  9, 14,   0,  0,  0],
##      [0,  0,  0,  9,  0, 10,   0,  0,  0],
##      [0,  0,  4, 14, 10,  0,   2,  0,  0],
##      [0,  0,  0,  0,  0,  2,   0,  1,  6],
##      [8, 11,  0,  0,  0,  0,   1,  0,  7],
##      [0,  0,  2,  0,  0,  0,   6,  7,  0]]
##V = [ 0, 1, 2, 3, 4, 5, 6, 7, 8 ]
root=17
P = prim(V, A, root)
print (P)
for i in range(len(P)):
    if P[i]==None:
        print(i)
fil_out=open("minimum_spanning.gdf",'w')
fil_out.write("nodedef> name,label\n")
for i in range(0,len(P)):
    if P[i]!=None or i==root:
        fil_out.write(p1[i+1]+'\n')

fil_out.write("\nedgedef>node1,node2,directed,weight,labelvisible\n")

for i in range(0,len(P)):
    if P[i]!=None:
        str1="v"+str(i)+","+"v"+str(P[i])+","+"false"+","+str(A[i][P[i]])+","+"true\n"
        fil_out.write(str1)
        
##for i in range(0,len(P)):
##    for j in range(i+1,len(key)):
##        if ind_mat[i][j]!=0:
##            str1="v"+str(i)+","+"v"+str(j)+","+"false"+","+str(ind_mat[i][j])+","+"true\n"
##            fil_out.write(str1)          
fil_out.close()
#[None, 0, 5, 2, 3, 6, 7, 0, 2]
