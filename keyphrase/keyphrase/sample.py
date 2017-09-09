import os
from os import listdir
def main():
				lis = [f for f in listdir("/media/New Volume/ACIST quick reference/LatestKeyphrase/keyphrase/")]
				for each_file in lis:
					print(each_file) 
					os.system("python pos.py "+each_file+" none enable")
					os.system("python grams.py "+each_file+" 4 none")
					os.system("python audio_features/cscore.py "+each_file+" none")
					os.system('python audio_features/tfidf.py "none" 4 "'+each_file+'"')
					os.system('python audio_features/localspan.py '+each_file+' 4 "none"')
					os.system('python audio_features/cue.py '+each_file+' "none" 4')
					os.system('python audio_features/dispersion.py '+each_file+' 4 "none"')
					os.system("python ml_audio/write.py "+each_file+" 'cscore,localspan,cuewords,tfidf,dispersion' '_cscore.txt,_localspan.txt,_cue.txt,_tfidf.txt,_disp.txt' none")
					os.system("python ml_audio/Naive-Bayes/Naive-Bayes.py all_features.tab "+each_file)
if __name__=="__main__":
				main()
