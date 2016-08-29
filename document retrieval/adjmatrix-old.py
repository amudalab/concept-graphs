#import gv,pygraph, edge
#from pygraph.classes.graph import graph
#from pygraph.classes.digraph import digraph
#from pygraph.algorithms.searching import breadth_first_search
#from pygraph.readwrite.dot import write
#import pygraphviz as pgv
import math

class AdjMatrix(object):
    """
        A class defined for the nodes in the word graph. Here nodes include
        node name, node id etc, and any other information needed. The methods
        facilitate the processing specific to text graph
    """

    def __init__(self):
        self.gmatrix = list()
        
    
    def createMatrix(self,wordlist, poslist, directed):
        print len(wordlist)
        from edge import Edge
        for i in range(len(wordlist)):
            tmatrix = list()
            for j in range(len(wordlist)):
                if i<len(wordlist) and j < len(wordlist):
                    temp = Edge()
                    #temp.fromnode = wordlist[i]
                    #temp.tonode = wordlist[j]
                    tmatrix.insert(j,temp)
            self.gmatrix.insert(i,tmatrix)

        i=0
        while i < (len(poslist)-1):
            if poslist[i+1][0] != poslist[i][0]:
                dist = float(poslist[i+1][1]-poslist[i][1])
                #print (poslist[i][0],poslist[i+1][0], dist)
                """
                    need to map the word to position in matrix!!
                """
                #fnode = poslist[i][0]
                #tnode = poslist[i+1][0]
                
                row = wordlist.index(poslist[i][0])
                #print poslist[i+1][0]
                col = wordlist.index(poslist[i+1][0])
                #gmatrix[row][col].fromnode = fnode
                #gmatrix[row][col].tonode = tnode
                if self.gmatrix[row][col].numupdate == 0:
                    self.gmatrix[row][col].weight = dist
                else:
                    #print ("updating",gmatrix[row][col].weight, dist)
                    self.gmatrix[row][col].updatewt(dist)
                    #print ("updated",gmatrix[row][col].weight, dist)
                self.gmatrix[row][col].updatenumber()
                #if poslist[i][0]=='stack full exception' or poslist[i+1][0]=='stack full exception':
                #    print dist , "......", poslist[i][0], poslist[i+1][0], row, col, self.gmatrix[row][col].weight
                #    print len(self.gmatrix)
                if directed == False:
                    if self.gmatrix[col][row].numupdate == 0:
                        self.gmatrix[col][row].weight = dist
                    else:
                        self.gmatrix[col][row].updatewt(dist)
                    self.gmatrix[col][row].updatenumber()
            i += 1
        return self.gmatrix

    """
        Given the current matrix and a new matrix with new values, the matrix must be updated
    """
    def updateMatrix(self, wordlist, poslist, directed):
        from edge import Edge
        #print ("matrix initial size", len(wordlist), len(self.gmatrix), len(self.gmatrix[0]))
        initsize = len(self.gmatrix)
        i=0
        #print wordlist
        while (i<len(wordlist)):
            tmatrix = list()
            if i>= initsize:
                j=0
                while j < len(wordlist):
                    temp = Edge()
                    tmatrix.insert(j,temp)
                    j+=1
                self.gmatrix.insert(i,tmatrix)
            else:
                j = initsize
                while j < len(wordlist):
                    temp = Edge()
                    self.gmatrix[i].insert(j,temp)
                    j+=1
            i+=1
            
        i=0
        #print ("matrix later size", len(self.gmatrix), len(self.gmatrix[0]))
        #print wordlist
        while i < (len(poslist)-1):
##            if (poslist[i][0] == 'executable'):
           ## print "found", poslist[i][0]
            if poslist[i+1][0] != poslist[i][0]:
                dist = poslist[i+1][1]-poslist[i][1]
                #print "found", poslist[i][0], i
                row = wordlist.index(poslist[i][0])
                col = wordlist.index(poslist[i+1][0])
                #print (self.gmatrix[row][col].weight, poslist[i][0], poslist[i+1][0])
                if self.gmatrix[row][col].numupdate == 0:
                    self.gmatrix[row][col].weight = dist
                else:
                    self.gmatrix[row][col].updatewt(dist)
                self.gmatrix[row][col].updatenumber()
##                if poslist[i][0]=='executable' or poslist[i+1][0]=='executable':
##                   print dist , "......", poslist[i][0], poslist[i+1][0], row, col, self.gmatrix[row][col].weight
                if directed == False:
                    if self.gmatrix[col][row].numupdate == 0:
                        self.gmatrix[col][row].weight = dist
                    else:
                        self.gmatrix[col][row].updatewt(dist)
                    self.gmatrix[col][row].updatenumber()
            i += 1
        
    def Floyd_Warshall(self):
        paths = AdjMatrix()
        for i in range(len(self.gmatrix[0])):
            tmatrix = list()
            for j in range(len(self.gmatrix[0])):
                dist = self.gmatrix[i][j].weight
                tmatrix.insert(j,dist)
            paths.gmatrix.insert(i,tmatrix)

        n = len(self.gmatrix[0])
        print n
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    #print paths.gmatrix[i][j]
                    #paths.gmatrix[i][j] = min(paths.gmatrix[i][j], paths.gmatrix[i][k]+paths.gmatrix[k][j])
                    if paths.gmatrix[i][j] > paths.gmatrix[i][k]+paths.gmatrix[k][j]:
                       paths.gmatrix[i][j] = paths.gmatrix[i][k]+paths.gmatrix[k][j]

        return paths           
            
    def draw_png(self, text):
        #gr = digraph()
        #print text
        #f = open("db/ds2a.gdf","w")
        f = open("db/full.gdf","w")
        f.write("nodedef> name,label"+"\n")
        #G=pgv.AGraph(strict=False,directed=True)

        for x in range(len(text)):
##            if gr.has_node((text[x])) == False:
##                gr.add_node(text[x])
            f.write("v"+str(x)+","+text[x]+"\n")
                
        f.write("edgedef> node1,node2,directed,weight,labelvisible"+"\n")        

        i = j = 0
        for i in range(len(text)):
            for j in range(len(text)):
                #print (text[i],i, text[j],j, self.gmatrix[i][j].weight, len(self.gmatrix), len(self.gmatrix[0]))
                if self.gmatrix[i][j].weight != float('inf'):
                #if self.gmatrix[i][j].weight < 10.0:
			wt1= self.gmatrix[i][j].weight
                        if wt1 ==0:
                            wt1 = 0.5
			#if self.gmatrix[i][j].weight ==0:
				#print (text[i],i, text[j],j, wt1)
	                 #gr.add_edge((text[i],text[j]),wt = wt1, label = str(wt1))
        	        f.write("v"+str(i)+","+"v"+str(j)+","+"false"+","+str(wt1)+","+"true"+"\n")
                	if (i == 1081 or j==1081):
                        	print self.gmatrix[i][j].weight
        
##        dot = write(gr)
##        gvv = gv.readstring(dot)
##        gv.layout(gvv,'dot')
##        gv.render(gvv,'png','textgraph.png')
##        gr.clear()

    def draw_paths(self, text):
        #gr = digraph()
        f = open("test.gdf","w")
        f.write("nodedef> name,label"+"\n")
        #G=pgv.AGraph(strict=False,directed=True)

        for x in range(len(text)):
            #if gr.has_node((text[x])) == False:
                #gr.add_node(text[x])
            f.write("v"+str(x)+","+text[x]+"\n")
                
        f.write("edgedef> node1,node2,directed,weight,labelvisible"+"\n")
        i = j = 0
        for i in range(len(text)):
            for j in range(len(text)):
                #if self.gmatrix[i][j]!= float('inf'):
                if self.gmatrix[i][j] < 10.0:
                    wt1= self.gmatrix[i][j]
                    #print (text[i],i, text[j],j, wt1)
                    #gr.add_edge((text[i],text[j]),label = str(wt1))
                    f.write("v"+str(i)+","+"v"+str(j)+","+"true"+","+str(wt1)+","+"true"+"\n")
                    
                
        print "done"
        #dot = write(gr)
        print "done1"
##        gvv = gv.readstring(dot)
##        print "done2"
##        gv.layout(gvv,'nop1')
##        print "done3"
##        gv.render(gvv,'png','pathgraph.png')

        #G=pgv.AGraph(dot)
        #G.write("test.xml")
        # G.layout(prog='dot')
       #G.layout(prog = 'dot')
        #G.draw('pathgraph.png')
        
