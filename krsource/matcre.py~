import nltk
fw = open("cooc.gdf","w")
fn=open("filewords(om)3")


fd=open("nwdb")
key=[]
for each_line in fd:
	x=each_line.strip('\n')
	key.append(x)

mat = [[0 for x in xrange(len(key))] for x in xrange(len(key))]

for each_line in fn:
	st=each_line.strip("\n")
	l=st.split(">")
	l=l[1].split(",")
	
	for w1 in l:
		for w2 in l:
			if(w1!=w2):
				mat[key.index(w1)][key.index(w2)]=mat[key.index(w1)][key.index(w2)]+1
				
fm=open("matrix","w")

for i in range(0,len(key)):
	for j in range(0,len(key)):
		fm.write(str(mat[i][j])+"  ")
	fm.write("\n")


#GDF generation


fw.write("nodedef> name,label\n")
for i in range(0,len(key)):
	str1="v"+str(i)+","+key[i]+"\n"
	fw.write(str1)

fw.write("\nedgedef>node1,node2,directed,weight,labelvisible\n")
	
for i in range(0,len(key)):
	for j in range(i+1,len(key)):
		if mat[i][j]!=0:
			str1="v"+str(i)+","+"v"+str(j)+","+"false"+","+str(mat[i][j])+","+"true\n"
			fw.write(str1)
			print " "

print "done"

 


