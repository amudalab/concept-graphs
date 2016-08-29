import nltk
fw = open("coc2.txt","w")
fn=open("keyfinal.txt")


fd=open("keyword.txt")
key=[]
words=[]

for word in fn:
        x=word.rstrip(" \n")
        words.append(x)
        
print(words)

print("\nKEYWORDS: ")        
for each_line in fd:
	x=each_line.strip('\n')
	key.append(x)
print (key)

print("\nCHECKING")
for i in words:
        for j in key:
                if(i==j):
                        print(i," ",j," ",key.index(i),"\n")

mat = [[0 for x in range(len(key))] for x in range(len(key))]

for i in range(len(words)-1):
        if(words[i]!=words[i+1]):
                mat[key.index(words[i])][key.index(words[i+1])]+=1
                mat[key.index(words[i+1])][key.index(words[i])]+=1
'''
for each_line in fn:
	l=each_line.strip(" \n")
	
	#print("N: ",l)
	
	#l=l[1].split(",")
	#print("N1: ",l)
	#z=read()
	for w1 in l:
		for w2 in l:
			if(w1!=w2):
				mat[key.index(w1)][key.index(w2)]=mat[key.index(w1)][key.index(w2)]+1
'''				
fm=open("matrix","w")

for i in range(0,len(key)):
	for j in range(0,len(key)):
		fm.write(str(mat[i][j])+"  ")
		#print(str(mat[i][j]))
	fm.write("\n")


#GDF generation
fm.close()

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
			print(" ")

print("done")
fw.close()


