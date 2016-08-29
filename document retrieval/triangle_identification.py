if __name__ == '__main__':
    fp = open('db/introhier.gdf')
    text=fp.read()
    pl=text.split('\n')
    #print(p1)
    flag=0
    V=[]
    flag=0
    print 'step 1'
    for each_line in pl:
        l=each_line.split(',')
        if len(l)==2:
            if flag!=0:
                V.append(l[1])
            flag=1
    A = [[0 for x in range(len(V))] for x in range(len(V))]
    flag=0
    print 'step2'
    for each_line in pl:
        l=each_line.split(',')
        if len(l)==5:
            if flag!=0:
                A[int(l[0][1:])][int(l[1][1:])]=float(l[3])
            flag=1
        else:
            continue
    print A
    for i in range(len(V)):
        for j in range(len(V)):
            if A[i][j]!=0:
                for k in range(len(V)):
                    if A[i][k]!=0 and A[k][j]!=0:
                        print '1: ',V[i],' 2: ',V[j],' 3: ',V[k]
            
        
