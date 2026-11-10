from adjmatrix import AdjMatrix
from graph_init import initgraph
import graph_init
from bfs import BFS
import operator
import math
def rt(ip):
	print "\n ENHANCED EDGE WEIGHT BASED DOCUMENT RETRIEVAL \n"
	fkey=open("data/keywords")
	raw=fkey.read()
	keywrd=raw.split("\n")
	keywrd.remove("")
	#print keywrd
	fqkey=open("data/query.key","w")
	fquery=open("data/query.txt","w")
	qrytxt=ip
	fquery.write(ip)
	fquery.close()
	qkey=[]
	for k in keywrd:
		if k in qrytxt:
			fqkey.write(k+'\n')
	fqkey.close()
	qkey=initgraph("query.key","query.txt")
	#qkey=list(graph_init.amatrix.gmatrix['stack'].keys())
	#print qkey
	query_mat=graph_init.amatrix.gmatrix
	similarity={} 
	deg={}
	wtgraph={}
	graph = {}
	maxi=graph_init.amatrix.getMaxNumUpdate(qkey)
	#print maxi
	for k in qkey:
		deg[k]=0.0
		graph[k]=[]
		wtgraph[k]={}
		for j in qkey:
			if query_mat[k][j].weight != float('inf'):
				#print graph_init.amatrix.gmatrix[k][j].getwt(maxi)
				graph[k].append(j)
				wtgraph[k][j]=query_mat[k][j].getwt(maxi)
				deg[k]+=1
			else:
				wtgraph[k][j]=0
	sorted_deg = sorted(deg.items(), key=operator.itemgetter(1))
	sorted_deg=sorted_deg[::-1]
	#print sorted_deg[0]
	hd=0
	while len(similarity.keys())<11 and len(sorted_deg)>hd:
		max_deg=sorted_deg[hd][0]            
		qry=BFS(graph,wtgraph,max_deg)
		bfsqry=qry[0]
		lvl=qry[1]
		##root=[]
		##for i in range(3):
		##    if i<len(sorted_deg):
		##        root.append(sorted_deg[i][0])

		ffile=open("data/filekeys")
		raw=ffile.read()
		#print "\n \n"+max_deg+"\n \n"
		fkeys=raw.split("\n")
		filekeys={}
		key_int={}
		#key_no_int={}
		file_levels={}
		md=[]
		md.append(max_deg)

		for k in range(len(fkeys)):
			fkeys[k]=fkeys[k].replace("<<",",")
			x=fkeys[k].split(",")
			filekeys[x[0]]=x[1:]
			key_int[x[0]]=list(set(list(md))&set(filekeys[x[0]]))
			#print key_int[x[0]]
			#key_no_int[x[0]]=len(key_int[x[0]])
			if len(key_int[x[0]])>0:
				#print "\n \n match found\n \n"
				fp = open('data/enhanced_semantic_nets/enhanced_semantic_net_'+x[0])
				text=fp.read()
				pl=text.split('\n')
				#print(p1)
				flag=0
				V=[]
				VN={}
				docgraph={}
				wtdocgraph={}
				flag=0
				for each_line in pl:
					l=each_line.split(',')
					if len(l)==2:
						if flag!=0:
							V.append(l[0])
							VN[l[0]]=l[1]
							docgraph[VN[l[0]]]=[]
							wtdocgraph[VN[l[0]]]={}
						flag=1
				flag=0
				for each_line in pl:
					l=each_line.split(',')
					if len(l)==5:
						if flag!=0:
							#print(l[0],l[1],l[3])
							docgraph[VN[l[0]]].append(VN[l[1]])
							wtdocgraph[VN[l[0]]][VN[l[1]]]=float(l[3])
						flag=1
					else:
						continue


				dg=BFS(docgraph,wtdocgraph,max_deg)
				bfsdoc=dg[0]
				key_inter=list(set(qkey)&set(filekeys[x[0]]))
				sm=0
				for ikey in qkey:
					for jkey in qkey:
						if ikey in key_inter and jkey in key_inter:
							sm+=((bfsqry[ikey][jkey]-bfsdoc[ikey][jkey])**2)
						else:
							sm+=(bfsqry[ikey][jkey]**2)
				
				if x[0] in similarity.keys():
					if similarity[x[0]]>math.sqrt(sm):
						similarity[x[0]]=math.sqrt(sm)
				else:
					similarity[x[0]]=math.sqrt(sm)
		hd+=1
	sorted_result = sorted(similarity.items(), key=operator.itemgetter(1))            
	#print sorted_result
	a=[]
	for i in range(len(sorted_result)):
		print sorted_result[i][0]
		a.append(sorted_result[i][0])
	return a





