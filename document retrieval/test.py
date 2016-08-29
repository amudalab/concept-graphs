# Import graphviz
import sys
#import pygraph

import nltk, re, pprint, textmodel,textgraph, adjmatrix
from textmodel import Text
from adjmatrix import AdjMatrix
from os import listdir
import copy
import xlwt


def initgraph(keyfile,textfile):
    f = open(keyfile)
    raw = f.read().lower()
    global text
    text = Text(raw)
    #tokens = nltk.word_tokenize(raw)
    tokens = nltk.line_tokenize(raw)
    text.tokens = list(set(tokens))
    text1 = removelinebreak(text.tokens)
    #print text1
    text1.sort()
    #text1.append(textfile)
    text.tokens = text1
    #print text.tokens
    #print len(text.tokens)
    global amatrix
    #print ("before: ",text.tokens)
    amatrix = text.create_graph(textfile)
    #print("init:",len(text.tokens))
    #amatrix.draw_ind_png(text.tokens,text.tokens,textfile)
    #print len(amatrix.gmatrix)
    return text.tokens

def populate(keyfile,textfile):
    #imatrix=copy.deepcopy(amatrix)
    #itext=text.tokens[:]
    print("populate : ",keyfile)
    f = open('Keys/'+keyfile)
    raw = f.read().lower()
    #tokens1 = nltk.word_tokenize(raw)
    tokens1 = nltk.line_tokenize(raw)
    text11 = removelinebreak(tokens1)
    tokens1 = text11
    text1 = Text(raw)
    text1.tokens = tokens1
    #print(tokens1)
    #text.updatetokens(tokens1)
    #text.tokens.append(textfile)
    #print(text.tokens)
    if len(text1.tokens)>0:
        poslist = text1.update_graph('Corpus/'+textfile)
        text.updatetokens(text1.tokens)
        #print ("after: ",text.tokens)
        amatrix.updateMatrix(text.tokens, poslist, False)
        text.tokens.sort()
    print(amatrix)
    rem=[]
    for i in text.tokens:
        if i[len(i)-1]=="s" and i[:-1] in text.tokens:
            t=i[:-1]
            for j in text.tokens:
                if amatrix.gmatrix[j][i].weight != float('inf'):
                    if amatrix.gmatrix[j][t].weight != float('inf'):
                        amatrix.gmatrix[j][t].weight+=amatrix.gmatrix[j][i].weight
                        amatrix.gmatrix[j][t].numupdate+=amatrix.gmatrix[j][i].numupdate
                        amatrix.gmatrix[t][j].weight=amatrix.gmatrix[j][t].weight
                        amatrix.gmatrix[t][j].numupdate=amatrix.gmatrix[j][t].numupdate
                    else:
                        amatrix.gmatrix[j][t].weight=amatrix.gmatrix[j][i].weight
                        amatrix.gmatrix[j][t].numupdate=amatrix.gmatrix[j][i].numupdate
                        amatrix.gmatrix[t][j].weight=amatrix.gmatrix[j][t].weight
                        amatrix.gmatrix[t][j].numupdate=amatrix.gmatrix[j][t].numupdate
            print ("pop remove: ",i)
            rem.append(i)
    for i in rem:
        for j in text.tokens:
            del amatrix.gmatrix[j][i]
    for i in rem:
        print(i,"hi")
        del amatrix.gmatrix[i]
        text.tokens.remove(i)
##                
    
    #print ("after:",text.tokens)
    #mat=imatrix.updateIndMatrix(amatrix, tokens1, itext,text.tokens)
    #print("pop:",len(itext))
    #print ("text:",len(text.tokens))
    #mat.draw_ind_png(text.tokens,tokens1,textfile)

def removelinebreak(text):
    #print text
    text1= list()
    for i in range(len(text)):
        #print text[i]
        temp1 = text[i].rstrip('\r');
        #temp = text[i].rstrip(' \t\t\t\t\t\t');
        temp = temp1.rstrip(' \t\t\t\t\t\t');
       # print temp
        text1.append(temp)
    return text1


def remove_stopword(tokens):
    """
        Remove stopwords from the text file
    """
    from nltk.corpus import stopwords
    stopset = set(stopwords.words('english'))
    #print stopset
    from nltk.collocations import BigramCollocationFinder
    from nltk.metrics import BigramAssocMeasures
    words = [w.lower() for w in tokens]
    content = [w for w in tokens if w.lower() not in stopset and len(w)>3]
         
    return content

def demo():
    lis1 = [f for f in listdir("G:\Research\document retrieval\document retrieval\Corpus/")]
    keywrd=[]
    for j in range (len(lis1)):
        print(lis1[j])
        initgraph('Keys/'+lis1[j][:-4]+".key",'Corpus/'+lis1[j])
        keywrd=list(set(keywrd+text.tokens))
        amatrix.draw_png(text.tokens,lis1[j][:-4])
    print(keywrd)
    fkey=open("keywords","w")
    for txt in keywrd:
        fkey.write(txt+"\n")
    
##    initgraph('ds11.mkey','ds11.txt')
######    initgraph('biochem2','biochem2.txt')
####    initgraph('binarytree','binarytree.txt')
##    populate('Adjacencylist','Adjacencylist.txt')
##    populate('ds6','ds6.txt')
##    populate('ds7','ds7.txt')
##    populate('ds8','ds8.txt')
##    populate('cg1','cg1.txt')
##    populate('cg2','cg2.txt')
##    populate('cg3','cg3.txt')
##    populate('biochem2','biochem2.txt')
#==============================================================================
    #populate('Keys/intro/nummeth1.key','Corpus/intro/nummeth1.txt')
#     populate('Keys/intro/proglang1.key','Corpus/intro/proglang1.txt')
#     populate('Keys/intro/comparch1.key','Corpus/intro/comparch1.txt')
#     populate('Keys/intro/cg1.key','Corpus/intro/cg1.txt')
#     populate('Keys/intro/dbms1.key','Corpus/intro/dbms1.txt')
#     populate('Keys/intro/embsys1.key','Corpus/intro/embsys1.txt')
#     populate('Keys/intro/it1.key','Corpus/intro/it1.txt')
#     populate('Keys/intro/ml1.key','Corpus/intro/ml1.txt')
#==============================================================================

##    initgraph('Keys/ds/ds1.key','Corpus/ds/ds1.txt')
#==============================================================================
#     populate('Keys/ds/ds2.key','Corpus/ds/ds2.txt')
#     populate('Keys/ds/ds3.key','Corpus/ds/ds3.txt')
#     populate('Keys/ds/ds4.key','Corpus/ds/ds4.txt')
#     populate('Keys/ds/ds5.key','Corpus/ds/ds5.txt')
#     populate('Keys/ds/ds6.key','Corpus/ds/ds6.txt')
#     populate('Keys/ds/ds7.key','Corpus/ds/ds7.txt')
#     populate('Keys/ds/ds8.key','Corpus/ds/ds8.txt')
#     populate('Keys/ds/ds10.key','Corpus/ds/ds10.txt')
#     populate('Keys/ds/ds11.key','Corpus/ds/ds11.txt')
#     populate('Keys/ds/ds12.key','Corpus/ds/ds12.txt')
#     populate('Keys/ds/ds13.key','Corpus/ds/ds13.txt')
#==============================================================================
    #text.tokens.append('Corpus/intro/ds1.txt')
#    for i in range(len(text.tokens)):
#        print (amatrix.gmatrix[len(text.tokens)][i])
    
#    amatrix.display(text.tokens)
##    tmplist = list(text.tokens)
##    tmplist = list(set(tmplist)) 
##    tmplist.sort()
##    text.show_graph(tmplist,amatrix)

#    pmatrix = amatrix.Floyd_Warshall()
#    pmatrix.draw_paths(text.tokens)
    
##    tmplist = list(text.tokens)
##    tmplist = list(set(tmplist)) 
##    tmplist.sort()
##    text.show_graph(tmplist,pmatrix)
    
if __name__ == '__main__':
    demo()

__all__ = ["ContextIndex",
           "ConcordanceIndex",
           "TokenSearcher",
           "Text",
           "TextCollection"]
