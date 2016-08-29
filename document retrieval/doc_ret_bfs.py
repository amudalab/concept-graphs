def BFS(graph,root,k):
    checked = []
    visited=[]
    level=[]
    l=[]
    l.append(root)
    level.append(l)
    count =0
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
##                if count<k:
##                    str1="v"+str(v)+","+"v"+str(edge)+","+"false"+","+str(A[v][edge])+","+"true\n"
##                    fil.write(str1)
        for edge in level[(len(level)-1)]:
            l=list(set(graph[edge])|set(l))
        for i in range(len(level)):
            for j in level[i]:
                if j in l:
                    l.remove(j)
        if len(l)>0:
            level.append(l)
    print len(level)
    for i in range(k-1):
        visit=[]
        for each_node in level[i]:
            inter=list(set(graph[each_node])&set(level[i+1]))
            for each_inter in inter:
                if each_inter not in visit:
                    str1="v"+str(each_node)+","+"v"+str(each_inter)+","+"false"+","+str(A[each_node][each_inter])+","+"true\n"
                    fil.write(str1)
                    visit.append(each_inter)

    print(level)
    print(len(level))
