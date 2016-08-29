import operator
if __name__ == '__main__':

    

    fp = open('db/introhier.gdf')
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
                VN[l[0]]=l[1].replace("\n","").replace("\r","")
            flag=1
    A = [['inf' for x in range(len(V))] for x in range(len(V))]
    flag=0
    maxi=0
    for each_line in pl:
        l=each_line.split(',')
        if len(l)==5:
            if flag!=0:
                #print(l[0],l[1],l[3])
                A[int(l[0][1:])][int(l[1][1:])]=float(l[3])
                if float(l[3])>maxi:
                    maxi=float(l[3])
            flag=1
        else:
            continue
    percent = 1.0
    while (percent > 0.0):
        cut_off=maxi*percent
        f1=open("cluster/lessthan"+str(int(percent*100))+".gdf","w")
        f2=open("cluster/greaterthan"+str(int(percent*100))+".gdf","w")
        for each_line in pl:
            l=each_line.split(',')
            if len(l)==2:
                f1.write(each_line+"\n")
                f2.write(each_line+"\n")

        f1.write("edgedef> node1,node2,directed,weight,labelvisible"+"\n")
        f2.write("edgedef> node1,node2,directed,weight,labelvisible"+"\n")
        for i in range(len(V)):
            for j in range(len(V)):
                if A[i][j] != 'inf':
                    if A[i][j]<=cut_off:
                        f1.write("v"+str(i)+","+"v"+str(j)+","+"false"+","+str(A[i][j])+","+"true"+"\n")
                    elif A[i][j]>=cut_off:
                        f2.write("v"+str(i)+","+"v"+str(j)+","+"false"+","+str(A[i][j])+","+"true"+"\n")
                    else:
                        continue
        percent -= 0.1
        f1.close()
        f2.close()
