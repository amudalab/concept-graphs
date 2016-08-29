import sys

class Vertex:
    def __init__(self, node):
        self.id = node
        self.adjacent = {}
        # Set distance to infinity for all nodes
        self.distance = sys.maxsize
        # Mark all nodes unvisited        
        self.visited = False  
        # Predecessor
        self.previous = None

    def add_neighbor(self, neighbor, weight=0):
        self.adjacent[neighbor] = weight

    def get_connections(self):
        return self.adjacent.keys()  

    def get_id(self):
        return self.id

    def get_weight(self, neighbor):
        return self.adjacent[neighbor]

    def set_distance(self, dist):
        self.distance = dist

    def get_distance(self):
        return self.distance

    def set_previous(self, prev):
        self.previous = prev

    def set_visited(self):
        self.visited = True

    def __str__(self):
        return str(self.id) + ' adjacent: ' + str([x.id for x in self.adjacent])

class Graph:
    def __init__(self):
        self.vert_dict = {}
        self.num_vertices = 0

    def __iter__(self):
        return iter(self.vert_dict.values())

    def add_vertex(self, node):
        self.num_vertices = self.num_vertices + 1
        new_vertex = Vertex(node)
        self.vert_dict[node] = new_vertex
        return new_vertex

    def get_vertex(self, n):
        if n in self.vert_dict:
            return self.vert_dict[n]
        else:
            return None

    def add_edge(self, frm, to, cost = 0):
        if frm not in self.vert_dict:
            self.add_vertex(frm)
        if to not in self.vert_dict:
            self.add_vertex(to)

        self.vert_dict[frm].add_neighbor(self.vert_dict[to], cost)
        self.vert_dict[to].add_neighbor(self.vert_dict[frm], cost)

    def get_vertices(self):
        return self.vert_dict.keys()

    def set_previous(self, current):
        self.previous = current

    def get_previous(self, current):
        return self.previous

def shortest(v, path):
    ''' make shortest path from v.previous'''
    if v.previous:
        path.append(v.previous.get_id())
        shortest(v.previous, path)
    return

import heapq

def dijkstra(aGraph, start):
    print ('''Dijkstra's shortest path''')
    # Set the distance for the start node to zero 
    start.set_distance(0)

    # Put tuple pair into the priority queue
    unvisited_queue = [(v.get_distance(),v) for v in aGraph]
    heapq.heapify(unvisited_queue)

    while len(unvisited_queue):
        # Pops a vertex with the smallest distance 
        uv = heapq.heappop(unvisited_queue)
        current = uv[1]
        current.set_visited()

        #for next in v.adjacent:
        for next in current.adjacent:
            # if visited, skip
            if next.visited:
                continue
            new_dist = current.get_distance() + current.get_weight(next)
            
            if new_dist < next.get_distance():
                next.set_distance(new_dist)
                next.set_previous(current)
                print ('updated : current = %s next = %s new_dist = %s' \
                        %(current.get_id(), next.get_id(), next.get_distance()))
            else:
                print ('not updated : current = %s next = %s new_dist = %s' \
                        %(current.get_id(), next.get_id(), next.get_distance()))

        # Rebuild heap
        # 1. Pop every item
        while len(unvisited_queue):
            heapq.heappop(unvisited_queue)
        # 2. Put all vertices not visited into the queue
        unvisited_queue = [(v.get_distance(),v) for v in aGraph if not v.visited]
        heapq.heapify(unvisited_queue)


if __name__ == '__main__':

    

    fp = open('db/introhier.gdf')
    fil_fin=open("spanning_tree/comp_shortest_path_tree.gdf","w")
    text=fp.read()
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
                VN[l[0]]=l[1]
            flag=1
    vert='v54'
    g = Graph()
    flag=0
    for each_line in pl:
        l=each_line.split(',')
        if len(l)==2:
            if flag!=0:
                #print(l[0])
                g.add_vertex(l[0])
            flag=1
        else:
            break
    A = [[0 for x in range(len(V))] for x in range(len(V))]
    flag=0
    for each_line in pl:
        l=each_line.split(',')
        if len(l)==5:
            if flag!=0:
                #print(l[0],l[1],l[3])
                g.add_edge(l[0], l[1], float(l[3]))
                A[int(l[0][1:])][int(l[1][1:])]=float(l[3])
            flag=1
        else:
            continue
        
##    g.add_vertex('a')
##    g.add_vertex('b')
##    g.add_vertex('c')
##    g.add_vertex('d')
##    g.add_vertex('e')
##    g.add_vertex('f')
##
##    g.add_edge('a', 'b', 7)  
##    g.add_edge('a', 'c', 9)
##    g.add_edge('a', 'f', 14)
##    g.add_edge('b', 'c', 10)
##    g.add_edge('b', 'd', 15)
##    g.add_edge('c', 'd', 11)
##    g.add_edge('c', 'f', 2)
##    g.add_edge('d', 'e', 6)
##    g.add_edge('e', 'f', 9)

    print ('Graph data:')
##    for v in g:
##        for w in v.get_connections():
##            vid = v.get_id()
##            wid = w.get_id()
##            print ('( %s , %s, %3d)'  % ( vid, wid, v.get_weight(w)))
    #print V
    
    dijkstra(g, g.get_vertex(vert)) 
    edge = [[0 for x in range(len(V))] for x in range(len(V))]
    for t in V:
        target = g.get_vertex(t)
        path = [t]
        shortest(target, path)
        print ('The shortest path for %s : %s' %(t, path[::-1]))
        for i in range(len(path)-1):
            edge[int(path[i][1:])][int(path[i+1][1:])]+=1
            edge[int(path[i+1][1:])][int(path[i][1:])]+=1
    print 'creating gdf'
    fil_out=open("comp_shortest_path_tree_from_"+VN[vert]+".gdf","w")
    for each_line in pl:
        l=each_line.split(',')
        if len(l)==2:
            fil_out.write(each_line+'\n')

    fil_out.write("\nedgedef>node1,node2,directed,weight,labelvisible\n")

    for i in range(len(V)):
        for j in range(len(V)):
            if edge[i][j]>0:
                str1="v"+str(i)+","+"v"+str(j)+","+"false"+","+str(edge[i][j])+","+"true\n"
                fil_out.write(str1)
    fil_out.close()

