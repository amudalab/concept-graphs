import sys

fname=sys.argv[1]
outname="data/output/OP"+fname
fname="data/output/"+fname
f=open(fname)
out=open(outname,"w")
for line in f:
	#print len(line)
	z=line.split("\t")
	if(z[0]!=" "):
		out.write(z[0]+"\n")

out.close()
f.close()
