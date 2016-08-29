#extracts all the keywords and keyphrases obtained after the Porter-Stemmer, and writes into the format filename>keywords in filewords(om)3 and all the keywords in nwdb
import re
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords
import nltk
import operator
from nltk.collocations import*
from os import listdir


def get_phrasepos(doc, phrase,text):
    pos = list()
    #print phrase
    
    #tokens = nltk.word_tokenize(phrase)
    
    tokens = nltk.regexp_tokenize(phrase,"[\w']+")
    for i in range(len(doc)):
        phrase1=phrase
        if len(tokens)>0:
            if doc[i] == tokens[0]:
                j=0
                tokens2 = list()
                #print (i+len(tokens)), len(doc)
                if (i+len(tokens) < len(doc)):
                    for j in range(len(tokens)):
                        tokens2.append(doc[i+j])
                    if matchphrases(tokens,tokens2) ==1:
##                        if phrase[:-1] in text:
##                            phrase=phrase[:-1]
                        #print tokens, ": in doc:", tokens2
                        ph=phrase1.replace("-"," ")
                        if ph in text or ph[:-1] in text:
                            if ph[len(ph)-1]=="s" and ph[:-1] in text:
                                phrase1=ph[:-1]
                            else:
                                phrase1=ph
                        if phrase1[len(phrase1)-1]=="s" and phrase1[:-1] in text:
                            phrase1=phrase1[:-1]

                        
                        pos.append([phrase1,i])
    return pos

def matchphrases(phrase1, phrase2):
    maybematch = False
    for i in range(len(phrase1)-1):
        if phrase1[i]==phrase2[i]:
            maybematch = True
        else:
            maybematch = False
            break
    plen = len(phrase1)-1
    if maybematch:
        word1 = stemplural(phrase1[plen])
        item1 = stemplural(phrase2[plen])
        if (word1 == item1):
            maybematch = True
        else:
            maybematch = False
    if maybematch == True:
        #print phrase1, ": in doc:", phrase2
        return 1
    else:
        return -1

def stem(word):
    regexp = r'^(.*?)(ing|ly|ed|ious|ies|ive|es|s|ment|er|r)?$'
    stem, suffix = re.findall(regexp, word)[0]
    return stem

def stemplural(word):
    regexp = r'^(.*?)(s)?$'
    stem, suffix = re.findall(regexp, word)[0]
    return stem

lis = [f for f in listdir("C:/Users/Romauld/Desktop/final year project/tree/key_phrase_scores")]
print (lis)
stop=stopwords.words('english')
fl=open("filewords(om)3",'w')
fn=open("nwdb",'w')
keywords=[]
tfidf={}
for each_file in lis:
        fd=open("key_phrase_scores/"+each_file)
        #fil=open("out/ds8.txt",'w')
        each_file=each_file[0:-4]
        print(each_file)
        key=[]
        k=[]
        temp=[]
        temp1=[]
        
        #print(fd)
        for each_line in fd:
                x=each_line.strip().lower()
                k.append(x)
        #print(k)
        for line in k:
                #print(line)
        #        print('\n')
                y=line.split()
        #        print(y)
                temp.append(y)
        #print(temp)
        l=0
        e=len(temp[0])-1
        for i in range(len(temp[0])):
            if temp[0][i]=="tfidf":
                tf=i
                break
            
            
        for sent in temp:
                #print(len(sent))
                i=len(sent)-e		
        #        print(sent[0:i])
                str=''
                for x in range(0,i):
                        str=str+" "+sent[x]
                str=str[1:]
                #str=str
                if(l>=2):
                        if "=" not in str and ":" not in str and "%" not in str and ";" not in str and ">" not in str and "<" not in str and "." not in str and "," not in str:
                                key.append(str)
                                if str in tfidf.keys():
                                    #tfidf[str]+=float(sent[i+tf]
                                    if tfidf[str]<sent[i+tf]:
                                        tfidf[str]=float(sent[i+tf])
                                else:
                                    tfidf[str]=float(sent[i+tf])
                        #print(str)
                l=l+1
        temp={}
        



srt = sorted(tfidf.items(), key=operator.itemgetter(1), reverse=True)
for i in range(len(srt)):
    print srt[i]
maxi=srt[0][1]
##print "maxi",maxi
cut_off=float(maxi)*0.1
##cut_off=0.0
##print "cut_off",cut_off
for each_file in lis:
        fd=open("key_phrase_scores/"+each_file)
        #fil=open("out/ds8.txt",'w')
        each_file=each_file[0:-4]
        fil=open("Keys/intro/comp/"+each_file,'w')
#        print(each_file)
        key=[]
        k=[]
        temp=[]
        temp1=[]
        
        #print(fd)
        for each_line in fd:
                x=each_line.strip().lower()
                k.append(x)
        #print(k)
        for line in k:
                #print(line)
        #        print('\n')
                y=line.split()
        #        print(y)
                temp.append(y)
        #print(temp)
        l=0
        e=len(temp[0])-1
            
            
        for sent in temp:
                #print(len(sent))
                i=len(sent)-e		
        #        print(sent[0:i])
                str=''
                for x in range(0,i):
                        str=str+" "+sent[x]
                str=str[1:]
                #str=str
                if(l>=2):
                        if "=" not in str and ":" not in str and "%" not in str and ";" not in str and ">" not in str and "<" not in str and "." not in str and "," not in str:
                            if tfidf[str]>cut_off:
                                key.append(str)
##                            elif tfidf[str]==0.0:
##                                print "0 tf:",str
##                            else:
##                                print "other tf:",str
                        #print(str)
                l=l+1
        temp={}
        f = open("Corpus/intro/"+each_file+".txt")
        basetext = f.read().lower()
        btokens = nltk.regexp_tokenize(basetext,"[\w']+")
        rem=[]
        for j in key:
                pos = list(get_phrasepos(btokens,j,key))
                if len(pos)>0:
                        if pos[0][0] in temp.keys():
                                for i in range(len(pos)):
                                    if pos[i] not in temp[pos[0][0]]:
                                        temp[pos[0][0]].append(pos[i])
                        else:
                                temp[pos[0][0]]=pos
                else:
#                        print ("NULL: ",j)
                        rem.append(j)
        for j in temp.keys():
                if len(temp[j])<2:
#                        print("removed:",j)
                        key.remove(j)
        for j in rem:
                key.remove(j)
        for j in key:
                tmptokens = nltk.regexp_tokenize(j,"[\w']+")
                for k in tmptokens:
                        if k not in stop:
                                if len(k)>1 and not(k.isdigit()):
                                        temp1.append(k)

        tmp=list(set(key)|set(temp1))
        tmp.sort()
        #print(tmp)
        
        fl.write(each_file+'>')
        str2=""
        #print(keywords)
        keywords=list(set(keywords)|set(tmp))
        #print(keywords)
        for j in tmp:
                str=j+'\n'
                str2=str2+j+','
                fil.write(str)
        fl.write(str2[0:-1]+'\n')
        fil.close()
        fd.close()
        #f.close()
        
keywords.sort()
#print "keywords: ",keywords
for j in keywords:
        str=j+'\n'
        fn.write(str)
fn.close() 
fl.close()
