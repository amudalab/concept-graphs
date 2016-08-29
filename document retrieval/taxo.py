#import xlrd
import xlrd


f = open('db/introhier.gdf')
text=f.read()
p1=text.split('\n')
V=[]
VN=[]
flag=0
for each_line in p1:
    l=each_line.split(',')
    if len(l)==2:
        if flag!=0:
            #print(l[0])
            V.append(int(l[0][1:]))
            VN.append(l[1].strip("\n"))
        flag=1
    else:
        break
A={}

for i in VN:
   tmatrix = {}
   for j in VN:
       tmatrix[j]='nil'
   A[i]=tmatrix

parent = {}

for i in VN:
   parent[i]='nil'
   


#A = [['nil' for x in range(len(V))] for x in range(len(V))]
flag=0
for each_line in p1:
    l=each_line.split(',')
    if len(l)==5:
        if flag!=0:
            #print(l[0],l[1],l[3])
            A[VN[int(l[0][1:])]][VN[int(l[1][1:])]]=float(l[3])
        flag=1
    else:
        continue


#Open a workbook
workbook = xlrd.open_workbook("data_st.xlsx")
order=[0,1,3,2]
clust=[[] for i in range(len(order))]
#Get a sheet by index
sheet = workbook.sheet_by_index(0)
 
#Access the cell value at (2,2)
print sheet.cell_value(0,1)

for sheet_name in workbook.sheet_names(): 
   sheet = workbook.sheet_by_name(sheet_name)
   j=len(sheet.row_values(0))-1
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
        
##for i in range(len(order)-1):
##   x=order[i]
##   for j in range(len(clust[x])):
##      for m in range((len(order)-1)-i):
##         y=order[i+1+m]
##         for k in range(len(clust[y])):
##            if A[clust[x][j][1]][clust[y][k][1]]!= 'nil':
##               if parent[clust[y][k][1]]!='nil':
##                  if A[clust[x][j][1]][clust[y][k][1]]<A[parent[clust[y][k][1]]][clust[y][k][1]]:
##                     parent[clust[y][k][1]] = clust[x][j][1]
##                     if clust[y][k][1]=="algorithms":
##                        print "found 1",x,j,k
##               else:
##                  parent[clust[y][k][1]] = clust[x][j][1]
##                  if clust[y][k][1]=="algorithms":
##                        print "found 2",x,j,k


for i in range(len(order)-1):
   x=order[i]
   for j in range(len(clust[x])):
      #for m in range((len(order)-1)-i):
         y=order[i+1]
         for k in range(len(clust[y])):
            if A[clust[x][j][1]][clust[y][k][1]]!= 'nil':
               if parent[clust[y][k][1]]!='nil':
                  if A[clust[x][j][1]][clust[y][k][1]]<A[parent[clust[y][k][1]]][clust[y][k][1]]:
                     parent[clust[y][k][1]] = clust[x][j][1]
               else:
                  parent[clust[y][k][1]] = clust[x][j][1]

               
##for i in range(len(order)):
##   for j in range(len(clust[i])):
##      for k in range(len(clust[i])):
##         if A[j][k]!= 'nil':
##            if parent[k]!='nil':
##               if A[j][k]<A[parent[k]][k]:
##                  parent[k] = int(j)
##                  #print j
##               else:
##                  print j
##            else:
##               parent[k] = int(j)
##for i in clust[order[0]]:
##   if parent[i[1]] == 'nil':
##      parent[i[1]] = i[1]
##      print i,parent[i[1]]
##   else:
##      print "present:",i,parent[i[1]]
##   

for i in VN:
   print "parent of "+str(i)+"    "+str(parent[i])
ftax=open("taxonomy2.gdf","w")
for each_line in p1:
    l=each_line.split(',')
    if len(l)==2:
        ftax.write(each_line+"\n")
    else:
        ftax.write(each_line+"\n")
        break

for i in range(len(VN)):
    if parent[VN[i]]!='nil':
        print "v"+str(i)+","+"v"+str(VN.index(parent[VN[i]]))+",false,"+str(A[VN[i]][parent[VN[i]]])+",true"+"\n"
        ftax.write("v"+str(i)+","+"v"+str(VN.index(parent[VN[i]]))+",false,"+str(A[VN[i]][parent[VN[i]]])+",true"+"\n")

print clust[order[0]]
ftax.close()
