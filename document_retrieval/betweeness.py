import operator
if __name__ == '__main__':

    

    fp = open('shortest_path_tree1/comp_shortest_path_tree.gdf')
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
    print V
    A = [[0 for x in range(len(V))] for x in range(len(V))]
    flag=0
    for each_line in pl:
        l=each_line.split(',')
        if len(l)==5:
            if flag!=0:
                #print l[0],l[1],l[3]
                A[int(l[0][1:])][int(l[1][1:])]=float(l[3])
            flag=1
        else:
            continue
    bet={}
    fil_out=open('betweeness1.txt','w')
    for i in range(len(V)):
        bet[V[i]]=A[i][0]
        j=1
        for j in range(1,len(V)):
            bet[V[i]]+=A[i][j]
        bet[V[i]]=(((bet[V[i]]-(2*(len(V)-1)))/2)+(2*(len(V)-1)))/(len(V)*len(V))
    srt = sorted(bet.items(), key=operator.itemgetter(1), reverse=True)
    maxi=srt[0][1]
    fil_out.write("linedef>node,label,betweeness\n")
    for i in srt:
        fil_out.write(i[0]+","+VN[i[0]]+","+str(i[1]/maxi)+'\n')
    #print srt
    fil_out.close()
    fp.close()
            
            
            
