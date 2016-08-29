import sys
import xlrd

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
                #print ('updated : current = %s next = %s new_dist = %s' \
                #        %(current.get_id(), next.get_id(), next.get_distance()))
            #else:
                #print ('not updated : current = %s next = %s new_dist = %s' \
                #        %(current.get_id(), next.get_id(), next.get_distance()))

        # Rebuild heap
        # 1. Pop every item
        while len(unvisited_queue):
            heapq.heappop(unvisited_queue)
        # 2. Put all vertices not visited into the queue
        unvisited_queue = [(v.get_distance(),v) for v in aGraph if not v.visited]
        heapq.heapify(unvisited_queue)


if __name__ == '__main__':

    

    fp = open('db/introhier.gdf')
    #fil_fin=open("shortest_path_tree1/comp_shortest_path_tree.gdf","w")
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
    glob_edge = [['nil' for x in range(len(V))] for x in range(len(V))]
    tax = [['nil' for x in range(len(V))] for x in range(len(V))]
    #Open a workbook
    od={}
    od["40"]=[1,0,2,3]
    od["41"]=[3,2,1,0]
    od["42"]=[1,3,2,0]
    od["43"]=[0,1]
    od["44"]=[0,3,1,2]
    od["45"]=[1,0,2,3]
    #od["46"]=[0]
    od["47"]=[3,0,1,2]
    od["48"]=[0,2,1,3]
    od["49"]=[1,2,3,0]
    od["410"]=[3,2,0,1]
    od["411"]=[2,0,1,3]
    od["412"]=[2,3,1,0]
    od["413"]=[0,2,1]
    for clu in od.keys():
        workbook = xlrd.open_workbook("C:/Users/Romauld/Desktop/EM4/KEM"+clu+".xlsx")
        order=od[clu]
        clust=[[] for i in range(len(order))]
        #Get a sheet by index
        sheet = workbook.sheet_by_index(0)
         
        #Access the cell value at (2,2)
        print sheet.cell_value(0,1)

        for sheet_name in workbook.sheet_names(): 
           sheet = workbook.sheet_by_name(sheet_name)
           j=len(sheet.row_values(0))-1
           print "j:",j
           print "clu:",clu
           for i in range(len(sheet.col_values(0))):
               s=[]
               s.append(str(sheet.row_values(i)[1]))
               s.append(str(sheet.row_values(i)[2]).replace("'",""))
               #print s
               clust[int(str(sheet.row_values(i)[j]).replace("cluster",""))].append(s)
           #print clust
           #topic = clust[0][1]
           #print topic
        for k in range(len(clust)):
           print clust[k]
           print "\n"
        for i in range(len(order)-1):
            root=[]
            targ=[]
            for j in range(len(clust[order[i]])):
                root.append(clust[order[i]][j][0])
            for k in range(len(clust[order[i+1]])):
                targ.append(clust[order[i+1]][k][0])
            print root
            for vert in root:
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
                for t in targ:
                    dist=0
                    target = g.get_vertex(t)
                    path = [t]
                    shortest(target, path)
                    print "path",path
                    print ('The shortest path for %s : %s' %(t, path[::-1]))
                    for m in range(len(path)-1):
                        if dist != 'nil':
                            dist=dist+A[int(path[m][1:])][int(path[m+1][1:])]
                        else:
                            dist=A[int(path[m][1:])][int(path[m+1][1:])]
                    print t,vert   
                    glob_edge[int(t[1:])][int(vert[1:])]=dist
    ##                glob_edge[int(path[vert][1:])][int(path[t][1:])]+=dist

        for k in range(len(V)):
            mini='nil'
            for l in range(len(V)):
                if glob_edge[k][l]!='nil':
                    if mini!='nil':
                        if glob_edge[k][l]<glob_edge[k][mini]:
                            mini=l
                    else:
                        mini=l
            print k, mini
            if mini=="nil":
                print "nil:",VN[V[k]]
            else:
                tax[k][mini]=glob_edge[k][mini]
                print "hi"
        ri=[]
        for c in clust[order[0]]:
            print "r:",c[0]
            xy=0
            flag=0
            print tax[4][63]
            for xy in range(len(V)):
                if tax[xy][int(c[0][1:])]!='nil':
                    flag=1
                    break
            if flag==0:
                ri.append(c[0])
        for k in clust[order[0]]:
            if k[0] not in ri:
                targ.append(k[0])
        for r in ri:
            vert=r
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


    
            
            dijkstra(g, g.get_vertex(vert)) 
            edge = [[0 for x in range(len(V))] for x in range(len(V))]
            for t in targ:
                dist=0
                target = g.get_vertex(t)
                path = [t]
                shortest(target, path)
                print "path",path
                print ('The shortest path for %s : %s' %(t, path[::-1]))
                for m in range(len(path)-1):
                    if dist != 'nil':
                        dist=dist+A[int(path[m][1:])][int(path[m+1][1:])]
                    else:
                        dist=A[int(path[m][1:])][int(path[m+1][1:])]
                print t,vert   
                glob_edge[int(vert[1:])][int(t[1:])]=dist
##                glob_edge[int(path[vert][1:])][int(path[t][1:])]+=dist
            mini='nil'

            for k in range(len(V)):
                
                if glob_edge[int(r[1:])][k]!='nil':
                    if mini!='nil':
                        if glob_edge[int(r[1:])][k]<glob_edge[int(r[1:])][mini]:
                            mini=k
                    else:
                        mini=k
                print k, mini
            print tax[4][63]
            tax[int(r[1:])][mini]=glob_edge[int(r[1:])][mini]

                
                
        
    print 'creating gdf'
    fil_out=open("taxKEM.gdf","w")
    for each_line in pl:
        l=each_line.split(',')
        if len(l)==2:
            fil_out.write(each_line+'\n')
    fil_out.write("edgedef>node1,node2,directed,weight,labelvisible\n")

    for i in range(len(V)):
        for j in range(len(V)):
            if tax[i][j]!='nil':
                str1="v"+str(i)+","+"v"+str(j)+","+"false"+","+str(tax[i][j])+","+"true\n"
                fil_out.write(str1)
    fil_out.close()
    fp.close()

