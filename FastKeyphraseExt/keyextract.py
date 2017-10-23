import sys
import os


def write_data(root_dir,f,keywords):
	outfile=os.path.join(root_dir,f.strip(".tab")+".key")
	print outfile
	print len(keywords)
	out=open(outfile,"w")
	for i in keywords:
		out.write(i+"\n")
	out.close()


def normalise_data(f):
	n=0
	max_set=[]
	omit=["keyphrase","keyword"]
	File=open(f)
	data=File.read()
	line=data.split("\n")[0].split("\t")
	for i in line:
		if i not in omit:
			max_set.append(0.0)
	
	for line in data.split("\n"):
		n=n+1
		if(n>3):
			meas=line.split("\t")
			for i in range(len(meas)-1):
				if i!=0:
					if meas[i]!="nan" and meas[i]>max_set[i-1]:
						max_set[i-1]=meas[i]
	
	for i in range(len(max_set)):
		max_set[i]=float(max_set[i])

	#print max_set
	n=0
	score=[]
	key=[]
	keyword=[]
	for line in data.split("\n"):
		n=n+1
		if(n>3):
			meas=line.split("\t")
			total=0.0
			for i in range(len(meas)-1):
				if i!=0 and max_set[i-1]>float(0):
					total+=float(float(meas[i])/float(max_set[i-1]))
			score.append(total)
			key.append(meas[0])
	
	#print score
	avg=0.0
	for i in score:
		avg+=i
	avg=avg/len(score)
	#print "AVG:"+str(avg)

	count=0
	double_avg=0.0
	for i in score:
		if i>avg:
			double_avg+=i
			count+=1
	double_avg=double_avg/count

	for i in range(len(score)):
		if score[i]>=double_avg:
			keyword.append(key[i].rstrip(" "))
	return keyword


def main(root_dir):
	lis = [f for f in os.listdir(root_dir)]
	print "KEYPHRASE EXT ----> 99"
	for file in lis:
		if file.endswith(".tab"):
			keywords = normalise_data(os.path.join(root_dir,file))
			write_data(root_dir,file,keywords)

if __name__=="__main__":
	root_dir = "/home/varun/concept-graphs/FastKeyphraseExt/output/" #set Input here
	main(root_dir)

