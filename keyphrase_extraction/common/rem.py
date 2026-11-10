from os import listdir
import os
lis1 = [f for f in listdir("set4 files")]
lis2 = [f for f in listdir("data/transcripts")]
print (lis1)
for i in lis1:
	if i in lis2:
		os.remove('data/transcripts/'+i)
