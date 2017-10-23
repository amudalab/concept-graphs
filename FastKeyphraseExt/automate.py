import os
import sys
from os import listdir


def update_key(x,f):
	fkey=open(f,"a+")
	fkey.write(str(x)+"\n")
	fkey.close()

def load_skip_list():
	try:
		l = open("txt2keyphrase.txt","r")
		sl = l.read()
		sl = sl.split("\n")
		return sl
	except:
		print "Attention!!!, Please create 2 empty files named,\"txt2keyphrase.txt , txt2keyphrase_0E.txt \" in folder adjacent to automate.py to proceed further"
		sys.exit()
	
def main(root_dir, skip_list, stem, val):
	lis = [f for f in listdir(root_dir)]
	for file in lis:
		if file not in skip_list:
			print "---------------------------------------------"
			print file +"\nPOS1 -> 1"
			os.system('python preprocess_audio/pos1.py '+file+' '+stem+' '+"enable")
			print "GRAMS --> 2"			
			os.system('python preprocess_audio/grams.py '+file+' '+val+' '+stem)
			print "CSCORE ---> 3"			
			os.system('python audio_features/cscore.py '+file+' '+stem)
			print "LOCAL_SPAN -----> 5"
			os.system('python audio_features/localspan.py '+file+' '+val+' '+stem)
			print "CUE ------> 6"
			os.system('python audio_features/cue.py '+file+' '+stem+' '+val)
			print "DISPERSION -------> 7"
			os.system('python audio_features/dispersiontest.py '+file+' '+val+' '+stem)
			print "WRITING TAB OUTPUT --------> 8"
			try:
				os.system("python audio_features/write.py "+file+" 'cscore,localspan,cuewords,dispersion,tfidf' '_cscore.txt,_localspan.txt,_cue.txt,_disp.txt,_tfidf.txt' none")
				print("Success!!"+file)
				update_key(file,"txt2keyphrase.txt")
			except:
				print("Error!!"+file)
				update_key(file,"txt2keyphrase_0E.txt")
		else:
            		print("FILE: "+file+" keyphrase already extracted")

if __name__=="__main__":
	root_dir = "/home/varun/concept-graphs/FastKeyphraseExt/transcript/" #set Input here
	stemmer = "Porter-Stemmer"
	val = "3"
	skip_list = load_skip_list()
	main(root_dir, skip_list, stemmer, val)

