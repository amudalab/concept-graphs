import sys

fname=sys.argv[1]
outname="output/IP"+fname
fname="output/"+fname
f=open(fname)
f1=open(fname)
out=open(outname,"w")
x=0
z4=0
z5=0
n=0
z3=0
for line1 in f:
	
	n=n+1
	z=line1.split("\t")
	if(n>3):

		z4=z4+float(z[4])
		z5=z5+float(z[5])
		z3=z3+float(z[3])
az4=z4/(n-3)
#print az4
az3=z3/(n-3)
az5=z5/(n-3)
for line in f1:
	#print "pp"
	x=x+1
	if(x!=1 and x!=2 and x!=3):
		z=line.split("\t")
		h=0
		for i in range(6):
			if(z[i]!="0.0"):
				h=h+1
		if(h>2 and z[0]!=" " and (float(z[3])>=az3 or (float(z[4])>az4 and float(z[5])>az5))):
			out.write(z[0]+"\n")
	else:
		z=line.split("\t")
		if(x==1):
			out.write(z[0]+"\n")
		else:
			out.write("\n")
				
		#if(z[0]!=" " and h>2):
   #out.write(z[0]+"\n")
out.close()
f.close()
