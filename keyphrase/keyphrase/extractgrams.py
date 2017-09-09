import os
import sys
from stopwords_video import vid_stopwords
from stop_words import stopword
import nltk
import re
from nltk import stem
stemmer = stem.PorterStemmer()
from operator import itemgetter
import math

try:
	folder_name=sys.argv[1]
	folder_name="output/"+folder_name.split(".txt")[0]
	max_gram=sys.argv[2]
	#min_freq=sys.argv[3]
	output_folder="output"
	ext="_vgrams.txt"
except:
	print "No Mandatory Parameters"
	sys.exit()

global start_end_stop
start_end_stop=['of','in','at','for',"a","an","the"]
global end_stop
end_stop=["a","an","the"]
global symbols
symbols=["+","-","*","/","-","@","?",".","(",")","[","]","{","}"]
global video
global numbers
numbers=['1','2','3','4','5','6','7','8','9','0']
video=[]
global max_height
max_height=0
global phrase
phrase=[]
#Initially Unique text sides for each video has to be identified and stored inside a folder "X" under input folder


#dir_name="input/ds4"
#res_file="ds4.key"
files=os.listdir(folder_name)
text_files=[]
for f in files:
        if f.endswith(".txt"):
                text_files.append(f)

class video_text:
        def __init__(self,doc_name,height,text):
                self.doc_name=doc_name
                self.height=height
                self.text=text
                self.cand_phrase={}
		self.ext=ext

        def extract_grams(self,token,token_size,height):
                grams=[]
                grams.extend(nltk.ngrams(token,token_size))
                for g in grams:
                        word=""
                        len_g=len(g)
                        if g[0] not in start_end_stop and g[len_g-1] not in end_stop and g[len_g-1] not in start_end_stop and g[0] not in stopword and  g[len_g-1] not in stopword:
                                for t in g: 
                                        word+=t+" "
                                word=word.rstrip(" ")
                                word=remove_special_case(word)
                                if word not in (self.cand_phrase).keys(): 
                                        self.cand_phrase[word]=1
					if word not in phrase:
						phrase.append(word)
                                else:
                                        self.cand_phrase[word]+=1

                        else:
                                if token_size-1>=1:
                                        self.extract_grams(token,token_size-1,height)

        def extract_candidate_phrases(self):
                for t in range(len(self.text)):
                        self.text[t]=remove_hyphen(self.text[t])
                        self.text[t]=remove_special_case(self.text[t])
                        if ((len(self.text[t].split())>=1 and len(self.text[t].split())<=max_gram)) and self.text[t] not in vid_stopwords and stop_word_check(self.text[t]):
                                if self.text[t] not in (self.cand_phrase).keys():
                                        self.cand_phrase[self.text[t]]=1
					if self.text[t] not in phrase:
						phrase.append(self.text[t])
                                else:
                                        self.cand_phrase[self.text[t]]+=1
                        else:
                                if len(self.text[t].split())>=max_gram:
                                        token=(self.text[t]).split()
                                        self.extract_grams(token,max_gram,self.height[t])
                #print self.doc_name
                #print self.cand_phrase

	
def remove_hyphen(g):
        if g.count("-")>0:
                temp=g.split("-")
                l=len(temp)
                word=""
                for i in range(l):
                        word+=temp[i]+" "
                g=word.rstrip(" ")
        return g

def remove_special_case(g):
        token=g.split()
        word=""
        for t in token:
                t=t.rstrip(" ")
                t=t.lstrip(" ")
                t=t.rstrip("()")
                t=t.lstrip("()")
                t=t.lstrip("(")
                t=t.rstrip("(")
                t=t.rstrip(")")
                t=t.lstrip(")")
                t=t.lstrip("[")
                t=t.rstrip("]")
                t=t.lstrip("{")
                t=t.rstrip("}")
                t=t.rstrip(":")
                t=t.lstrip(":")
                t=t.lstrip(",")
                t=t.rstrip(",")
                t=t.rstrip(".")
                word+=t+" "
        word=word.rstrip(" ")
        #print word
        return word

def stop_word_check(t):
        token=t.split()
        token_len=len(token)
        if token[0] not in start_end_stop  and token[token_len-1] not in start_end_stop and token[token_len-1] not in end_stop and token[0] not in stopword and token[token_len-1] not in stopword:
              return 1
        else:
               return 0

def remove_phrase_with_spl_char():
	#print symbols+numbers
	remove_phrase=[]
	for word in phrase:
		for chars in symbols+numbers:
			if chars in word:
				remove_phrase.append(word)
				#print word
				break
	for word in remove_phrase:
		phrase.remove(word)
def write_phrase():
	output_file_name=folder_name.split("/")
	size=len(output_file_name)
	#res_file=output_folder+"/"+output_file_name[size-1]+"_grams.txt"
	res_file=output_folder+"/"+output_file_name[size-1]+ext
	f=open(res_file,"w")
	for p in phrase:
		f.write(p+"\n")
	f.close()

for f in sorted(text_files):
        height=[]
        row_num=[]
        text=[]
        ftxt=open(folder_name+"/"+f,"r")
        content=ftxt.readlines()
        ftxt.close()
        line_number=1
        for line in content:
                data=line.split("::")
                if len(data)==3:
                        height.append(int(data[1].split(" ")[1]))
                        if int(data[1].split(" ")[1])>max_height:
                                max_height=int(data[1].split(" ")[1])
                        text.append(data[2].rstrip("\n").lower())
        video.append(video_text(folder_name+"/"+f,height,text))   

for v in video:
        v.extract_candidate_phrases()

remove_phrase_with_spl_char()
write_phrase()
	
