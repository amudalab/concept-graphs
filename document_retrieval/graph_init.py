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
    f = open('data/keys/'+keyfile)
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
        poslist = text1.update_graph('data/corpus/'+textfile)
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
    lis1 = [f for f in listdir("data/corpus/")]
    keywrd=[]
    for j in range (len(lis1)):
        print(lis1[j])
        initgraph('data/keys/'+lis1[j][:-4]+".key",'data/corpus/'+lis1[j])
        keywrd=list(set(keywrd+text.tokens))
        amatrix.draw_png(text.tokens,lis1[j][:-4])
    print(keywrd)
    fkey=open("data/keywords","w")
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
    #populate('data/keys/nummeth1.key','data/corpus/nummeth1.txt')
#     populate('data/keys/proglang1.key','data/corpus/proglang1.txt')
#     populate('data/keys/comparch1.key','data/corpus/comparch1.txt')
#     populate('data/keys/cg1.key','data/corpus/cg1.txt')
#     populate('data/keys/dbms1.key','data/corpus/dbms1.txt')
#     populate('data/keys/embsys1.key','data/corpus/embsys1.txt')
#     populate('data/keys/it1.key','data/corpus/it1.txt')
#     populate('data/keys/ml1.key','data/corpus/ml1.txt')
#==============================================================================

##    initgraph('data/keys/ds1.key','data/corpus/ds1.txt')
#==============================================================================
#     populate('data/keys/ds2.key','data/corpus/ds2.txt')
#     populate('data/keys/ds3.key','data/corpus/ds3.txt')
#     populate('data/keys/ds4.key','data/corpus/ds4.txt')
#     populate('data/keys/ds5.key','data/corpus/ds5.txt')
#     populate('data/keys/ds6.key','data/corpus/ds6.txt')
#     populate('data/keys/ds7.key','data/corpus/ds7.txt')
#     populate('data/keys/ds8.key','data/corpus/ds8.txt')
#     populate('data/keys/ds10.key','data/corpus/ds10.txt')
#     populate('data/keys/ds11.key','data/corpus/ds11.txt')
#     populate('data/keys/ds12.key','data/corpus/ds12.txt')
#     populate('data/keys/ds13.key','data/corpus/ds13.txt')
#==============================================================================
    #text.tokens.append('data/corpus/ds1.txt')
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
