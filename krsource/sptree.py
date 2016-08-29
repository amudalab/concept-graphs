fg=open("spfinal.gdf","w")
fr=open("sptreedata")

flist=(fr.read()).split("\n")

fd=open("nwdb")
key=[]
for each_line in fd:
	x=each_line.strip('\n')
	key.append(x)

class node:
        node1=""
        node2=""
        weight=0

ndls=[]
flist.pop(len(flist)-1)
for l in flist:
        l=l.split(",")
        x=node()
        x.node1=l[0]
        x.node2=l[1]
        x.weight=float(l[3])
        ndls.append(x)

ndls.sort(key=lambda x: float(x.weight), reverse=False)


nds=[]
edls=[]
edls.append(ndls[0])
nds.append(ndls[0].node1)
nds.append(ndls[0].node2)
p=0
while(p<len(ndls)):
        if (nds.count(ndls[p].node1)==0 and nds.count(ndls[p].node2)!=0) or (nds.count(ndls[p].node1)!=0 and nds.count(ndls[p].node2)==0):
                edls.append(ndls[p])
                if nds.count(ndls[p].node1)==0:
                        nds.append(ndls[p].node1)
                if nds.count(ndls[p].node2)==0:
                        nds.append(ndls[p].node2)
                if len(nds)>len(key):
                        break
		p=0
	else:
		p=p+1

print len(edls)
#GDF generation

fg.write("nodedef> name,label\n")
for i in range(0,len(key)):
	str1="v"+str(i)+","+key[i]+"\n"
	fg.write(str1)

fg.write("\nedgedef>node1,node2,directed,weight,labelvisible\n")
	
for j in range(0,len(edls)):
	str1=edls[j].node1+","+edls[j].node2+","+"false"+","+str(edls[j].weight)+","+"true\n"
	fg.write(str1)		

                
print "done"
