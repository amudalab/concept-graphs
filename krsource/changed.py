import nltk
import re

def spacerem(flist):
    intg=0
    fl=[]
    for i in range(0,len(flist)):
        if flist[i]==' ' and intg==0:
                intg=1
                fl.append(flist[i])
        elif flist[i]==' ' and intg==1:
                flist[i]=" "
    elif flist[i]!=' ' and flist[i]!='':
                intg=0
                fl.append(flist[i])
    return fl

def stem(word):
    regexp = r'^(.*?)(ed|ious|ies|es|s|er)?$'
    stem, suffix = re.findall(regexp, word)[0]
    return stem

def indxes(a,item):
    l=[]
    wlist=item.split(" ")
   # print wlist
    if len(wlist)>1:
        c1=a.count(stem(wlist[0]))
        c2=a.count(stem(wlist[1]))
        #print c1,c2
        if c1>c2:
                c=c2
        else:
                c=c1
        ini=0
        fin=len(a)-1
        while (c1>0 and c2>0):
                
                ind1=a[ini:fin].index(stem(wlist[0]))+ini
                if flist[ind1+1]==stem(wlist[1]):
                    l.append(ind1)
                ini=ind1+1
                c1=c1-1
                
    else:
            ini=0
            fin=len(a)
            c=a.count(stem(wlist[0]))           
            while c>0:
                ind=a[ini:fin].index(stem(item))+ini
                ini=ind+1
                c=c-1
                l.append(ind)
   # print l
    return l


fw = open("wd_timline.gdf","w")
fn=open("filewords(om)3")
fps=open("timeline","w")

fd=open("nwdb")
key=[]
for each_line in fd:
        x=each_line.strip('\n').lower()
        key.append(x)

mat = [[0 for x in xrange(len(key))] for x in xrange(len(key))]

ind_mat = [[0 for x in xrange(len(key))] for x in xrange(len(key))]



for each_line in fn:
    l=each_line.split(">")
    filen=l[0]
    wl=(l[1].lower()).split(",")

    fil=open("all/"+filen)
    fread=fil.read().lower()
    fread=fread.replace("\n"," ")
    fread=fread.replace("\t"," ")
    fread=fread.replace("("," ")
    fread=fread.replace(")"," ")
    fread=fread.replace("\\"," ")
    fread=fread.replace("/"," ")
    fread=fread.replace("."," ")
    fread=fread.replace("["," ")
    fread=fread.replace("]"," ")
    fread=fread.replace(":"," ")
    fread=fread.replace(","," ")
    
    flist=fread.split(" ")
    flist=spacerem(flist)
    
    fil_ind=open("out/"+filen,"w")
    
    
    for i in range(0,len(flist)):
        if len(flist[i])>1:
            flist[i]=stem(flist[i])
    

    ind=[[]for x in xrange(len(wl))]
    
    i=0
    for w in wl:
            
            w=w.strip("\n")
            w=w.strip(",")
            ind[i]=indxes(flist,w.lower())
            if len(ind[i])==0:
                print "empty word is",w
	    
	    
            for j in range(0,10):
    	    	print flist[j]
		
            if (i==0 or i==1) and (filen=="algorithms"):
	       	print ind[i],flist[ind[i][0]]	      
            i=i+1
    str1=""
    #print ind
    
    for i in range(0,len(wl)-1):
#        print i,filen
        for j in range(i+1,len(wl)):
            m=0
            n=0
            minim=100000
            
            while m<len(ind[i]) and n<len(ind[j]):
                if abs(ind[i][m]-ind[j][n])<minim:
                    minim=abs(ind[i][m]-ind[j][n])
                if ind[i][m]<ind[j][n]:
                    m=m+1
                else:
                    n=n+1
		if i==0 and j==1 and filen=="algorithms":
			print minim,wl[i],wl[j]
            
			ind_mat[key.index(wl[i].strip("\n"))][key.index(wl[j].strip("\n"))]=minim
            mat[key.index(wl[i].strip("\n"))][key.index(wl[j].strip("\n"))]=(mat[key.index(wl[i].strip("\n"))][key.index(wl[j].strip("\n"))]+minim)
            
	fil_ind.write("nodedef> name,label\n")
	for i in range(0,len(key)):
			str1="v"+str(i)+","+key[i]+"\n"
			fil_ind.write(str1)

	fil_ind.write("\nedgedef>node1,node2,directed,weight,labelvisible\n")
        
	for i in range(0,len(key)):
			for j in range(i+1,len(key)):
					if mat[i][j]!=0:
						str1="v"+str(i)+","+"v"+str(j)+","+"false"+","+str(mat[i][j])+","+"true\n"
						fil_ind.write(str1)          
	
            
                
                                
fm=open("matrix","w")

for i in range(0,len(key)):
        for j in range(0,len(key)):
                fm.write(str(mat[i][j])+"  ")
        fm.write("\n")

maxls=[]
for i in range(0,len(key)):
	maxls.append(max(mat[i]))

maxmt=max(maxls)+1
#GDF generation
print maxmt

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
