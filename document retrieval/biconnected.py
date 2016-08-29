import networkx as nx
#import Biconnected
import operator
from Biconnect import _biconnected_dfs
from os import listdir
import xlwt
if __name__ == '__main__':
    lis1 = [f for f in listdir("C:/Users/Romauld/Desktop/final year project/update 4.3/cluster")]
    for each_file in lis1:
        fp = open('cluster/'+each_file)
        book = xlwt.Workbook(encoding="utf-8")
        sheet = book.add_sheet(each_file[:-4])
        text=fp.read()
        pl=text.split('\n')
        #print(p1)
        flag=0
        V=[]
        VN={}
        flag=0
        G=nx.Graph()
        for each_line in pl:
            l=each_line.split(',')
            if len(l)==2:
                if flag!=0:
                    V.append(l[0])
                    VN[l[0]]=l[1].replace("\n","").replace("\r","")
                    G.add_node(VN[l[0]])
                flag=1
        A = [[0 for x in range(len(V))] for x in range(len(V))]
        flag=0
        for each_line in pl:
            l=each_line.split(',')
            if len(l)==5:
                if flag!=0:
                    #print(l[0],l[1],l[3])
                    A[int(l[0][1:])][int(l[1][1:])]=float(l[3])
                    edge=(VN[l[0]],VN[l[1]])
                    G.add_edge(*edge)
                flag=1
            else:
                continue
        print nx.is_biconnected(G)
        
        comp=list(nx.biconnected_components(G))
        print (len(comp))
                  
                  
        for i in range(len(comp)):
            k=0
            for j in list(comp[i]):
                sheet.write(k, i, j)
                k+=1
        book.save("biconnectedness/"+each_file[:-4]+".xls")
        fp.close()

