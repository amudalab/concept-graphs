#Sample command: python audio_features/dispersion.py <transcript_name> <max_gram> <stemmer_name>
#e.g : python audio_features/dispersion.py CG1.txt 4 "Porter-Stemmer"

import sys
import re
import numpy
import math
from operator import itemgetter
from numpy import *
from time import gmtime, strftime
from nltk import stem
from stem import * #imports functions from stem.py

#numpy.seterr(divide='ignore', invalid='ignore')

class dispersion:
    #Initializing parameters (input_folder,output_folder,grams,result_ext,untagged_file_ext,ext)
    def __init__(self,name,input_folder,output_folder,grams,result_ext,untagged_file_ext,ext):
        self.doc_name=input_folder+"/"+name+untagged_file_ext;
        f=open(self.doc_name,"r")
        self.tkn=f.read().lower(); 
        f.close()
        self.dtokens=self.tkn.split(); print "-------hi--", len(self.dtokens)
        self.size=len(self.dtokens); 
        self.grams=grams
        self.freq={}
        self.pos={}
        self.pg={}
        self.var={}
        self.max_gap=float(self.size)/float(4); 
        self.disp={}
        self.result=output_folder+"/"+name+ext;
        self.segment_count=3
        self.segment=self.size/self.segment_count; 
        self.max_gram_length=0
        for g in self.grams:
            l=len(g.split())
            if l>self.max_gram_length:
                self.max_gram_length=l;
                
    #The function calculates dispersion score
    #Input : grams
    #Output :  dispersion score
    def find_dispersion(self):

        #Finding out positions of each gram in the file
        for text in self.grams:
            if text in self.pos.keys():
                continue
            m=len(text.split())
            poss=[]
            pos_gap=[]
            for i in range((self.size)-m-1):
                word=""
                for j in range(m):
                    word+=self.dtokens[i+j]+" "
                word=word.rstrip(" ")
                if text==word:
                    poss.append(i)
            self.pos[text]=poss; 

        for low_term in self.grams:
            for h_term in self.grams:
                if len(low_term.split())<len(h_term.split()):
                    if low_term in h_term:
                        arr1=h_term.split()
                        arr2=low_term.split()
                        for a in range(len(arr1)):
                            if arr2[0]==arr1[a]:
                                break
                        for p in self.pos[h_term]:
                            if p+a in self.pos[low_term]:
                                self.pos[low_term].remove(p+a)

        #calculates dispersion score                      
        for term in self.grams:
            if len(term.split())>1:
                gap=[]
                a=0
                for p in self.pos[term]:
                    if a==0:
                        prev=p
                    elif a==len(self.pos[term]):
                        prev=p
                    else:
                        if(p-prev)>350:
                            gap.append(p-prev)
                            prev=p
                    a+=1	
                self.pg[term]=gap
                phrase_len=len(term.split())
                variance=var(numpy.array(gap))
		if numpy.isnan(variance):
			variance = 0
                if float(variance)!=float(0):
                    self.disp[term]=(float(len(gap))/float(variance))*math.log(phrase_len+1,2)

    #The function writes output file
    #<transcript_name>_disp.txt file in the output folder. This will contain dispersion scores for phrases.
    def display(self):		
        f_w=open(self.result,"w")
        items=self.disp.items()
        #print "Items=",items
        size=len(items)
        items.sort(key=itemgetter(1),reverse=True)
        maxx=items[0][1]
        for i,t in items:
            f_w.write(str(i)+"::"+str(t)+"\n")
        f_w.close()


global file_name
global input_folder
global output_folder
global max_gram
global result_ext
global gram_ext
global untagged_file_ext

try:
	file_name=sys.argv[1] #<transcript_name>.txt
	input_folder="output"
	output_folder="output"
	max_gram=sys.argv[2] # max gram
	result_ext="_dispersion"
	gram_ext="_grams.txt"
	untagged_file_ext="_untagged.txt"
	ext="_disp.txt"
	stemmer_name=sys.argv[3] # stemmer name
	key_file=""

except:
	print "Mandatory Parameters unavailable"
	sys.exit()

#read grams in grams file
name=(file_name).split(".")[0]
f_name=input_folder+"/"+name+gram_ext
print f_name
f=open(f_name,"r")
data=f.readlines()
f.close()
grams=[]
for r in data:
	grams.append(r.rstrip("\n"))

#print name,input_folder,output_folder,grams,result_ext,untagged_file_ext,ext
doc_disp=dispersion(name,input_folder,output_folder,grams,result_ext,untagged_file_ext,ext)
doc_disp.find_dispersion()
doc_disp.display()
#print "DONE................"
