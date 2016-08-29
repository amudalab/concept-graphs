from adjmatrix import AdjMatrix
from test import initgraph
import test
import operator
import math
def rt(ip):
	print "\n BAG OF WORDS BASED DOCUMENT RETRIEVAL \n"
	fkey=open("keywords")
	raw=fkey.read()
	keywrd=raw.split("\n")
	keywrd.remove("")
	#print keywrd
	fqkey=open("query.key","w")
	fquery=open("query.txt","w")
	qrytxt=ip
	fquery.write(ip)
	fquery.close()
	qkey=[]
	for k in keywrd:
		if k in qrytxt:
			fqkey.write(k+'\n')
	fqkey.close()
	qkey=initgraph("query.key","query.txt")
	#qkey=list(test.amatrix.gmatrix['stack'].keys())
	#print qkey

	#print freq
	ffile=open("filekeys")
	raw=ffile.read()

	fkeys=raw.split("\n")
	filekeys={}
	key_int={}
	key_no_int={}
	file_levels={}
	for k in range(len(fkeys)):
		y=fkeys[k].split("<<")
		file_levels[y[0]]=y[1:]
		fkeys[k]=fkeys[k].replace("<<",",")
		x=fkeys[k].split(",")
		filekeys[x[0]]=x[1:]
		key_int[x[0]]=list(set(qkey)&set(filekeys[x[0]]))
		key_no_int[x[0]]=len(key_int[x[0]])
	sorted_key_int = sorted(key_no_int.items(), key=operator.itemgetter(1))
	sorted_key_int= sorted_key_int[::-1]
	a=[]			
	for i in range(10):
		print sorted_key_int[i][0]
		a.append(sorted_key_int[i][0])
	return a
		
