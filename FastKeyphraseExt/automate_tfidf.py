import os
import sys
from os import listdir

	
def main(root_dir, stem, val):
	lis = [f for f in listdir(root_dir)]
	for file in lis:
		print "TFIDF ----> 4"
		os.system('python audio_features/tfidf.py '+stem+' '+val+' "'+file+'"')
		break


if __name__=="__main__":
	root_dir = "/home/varun/concept-graphs/FastKeyphraseExt/transcript/" #set Input here
	stemmer = "Porter-Stemmer"
	val = "3"
	main(root_dir, stemmer, val)
