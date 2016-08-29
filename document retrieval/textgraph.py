"""
    This program contains functions for creating graph, updating the graph edges,
    deleting and inserting new nodes etc
"""

import sys, re
sys.path.append('/usr/lib/pymodules/python2.6')
#import gv,pygraph
import textmodel, edge, adjmatrix, nltk
#import xmlrpclib

# Import pygraph
#from pygraph.classes.graph import graph
#from pygraph.classes.digraph import digraph
#from pygraph.algorithms.searching import breadth_first_search
#from pygraph.readwrite.dot import write
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords
import nltk
from nltk.collocations import*
stop=stopwords.words('english')
"""
    Graph creation from text
    each word is node
    currently every edge is connected since they are in same document
"""

def create_graph(text,filename):
    f = open(filename)
    basetext = f.read().lower()
    from textmodel import Text    
    btext = Text(basetext)
    #btokens = nltk.word_tokenize(basetext)
    btokens = nltk.regexp_tokenize(basetext,"[\w']+")
    btext.tokens = btokens
    if text is None:
        print("Grrrrrrrrrr");
    
    #text.tokens = text1
    #print ("..........",len(text.tokens))
    txt = list(text.tokens)
    poslist = list()
    #print ("..............", len(txt))
    #print text
    temp={}
    
    t=[]
    #creating poslist for the terms
    for x in txt:
        #tmptokens = nltk.word_tokenize(txt[x])
        tmptokens = nltk.regexp_tokenize(x,"[\w']+")
        #print(x,tmptokens)
        #print(tmptokens)
        #tmptokens = nltk.regexp_tokenize(text[x],"[\w']+")
        if len(tmptokens)==1:
            pos = list(get_positions(btext.tokens, tmptokens[0],txt))
        elif len(tmptokens)>1:
            pos = list(get_phrasepos(btext.tokens,x,txt))
        else:
            pos=[]
            t.append(x)
        if len(pos)>0:
            if pos[0][0] in temp.keys():
                for i in range(len(pos)):
                    if pos[i] not in temp[pos[0][0]]:
                        temp[pos[0][0]].append(pos[i])
            else:
                temp[pos[0][0]]=pos
            if pos[0][0]!=x:
                #print ("removed",x," | ",pos[0][0])
                t.append(x)
    #removing unneccessary sub-lists ie "linked" from "linked list"
    k=[]
    for x in temp.keys():
        for y in temp.keys():
            if x !=y:
                if x in y:
                    tmpx=nltk.word_tokenize(x)
                    tmpy=nltk.word_tokenize(y)
                    fx=0
                    fy=0
                    for i in range(len(tmpy)):
                        if tmpy[fy]==tmpx[fx]:
                            fy+=1
                            fx+=1
                        else:
                            fy+=1
                        if fx==len(tmpx):
                            if len(temp[x])==len(temp[y]):
                                #print("delete: ",x," | ",y)
                                if x not in k:
                                    #print(x)
                                    k.append(x)
                            break
    #print("k : ",k)
    for i in k:
        del temp[i]
        txt.remove(i)
    si={}
    for i in temp.keys():
        si[i]=len(temp[i])
    r=[]
    for i in temp.keys():
        tmpx=nltk.word_tokenize(i)
        if len(tmpx)>1:
            for j in temp:
                if i!=j:
                    if i in j:
                        si[i]-=si[j]
                        r.append(j)
##    for i in j:
##        si[i]=0
    
    for i in temp.keys():
        tmpx=nltk.word_tokenize(i)
        if len(tmpx)==1:
            for j in temp:
                if i!=j:
                    if i in j:
                        si[i]-=si[j]
    r=[]
    for i in temp.keys():
        if si[i]==0:
            #print ("to be removed: ",i)
            r.append(i)
    for i in r:
        txt.remove(i)
        del temp[i]
    for i in t:
        txt.remove(i)
    for i in temp.keys():
        poslist.append(temp[i])
##    #removing unneccessary sub-lists ie "linked" from "linked list"
##    d=[]        
##    for x in range(len(txt)):
##        tmptokens = nltk.word_tokenize(txt[x])
##        if len(tmptokens)>1:
##            for y in range(len(tmptokens)):
##                if tmptokens[y] not in stop:
##                    if tmptokens[y] in txt:
##                        u=0
##                        flag1=0
##                        flag2=0
##                        flag=0
##                        w=0
##                        z=0
##                        for u in range(len(poslist)):
##                            if len(poslist[u])>1:
##                                if poslist[u][0][0]==tmptokens[y] and flag1==0:
##                                    flag1=1
##                                    flag+=1
##                                    w=u
##                                if poslist[u][0][0]==txt[x] and flag2==0:
##                                    flag2=1
##                                    flag+=1
##                                    z=u
##                            if flag==2:
##                                break
##                        if flag1==1 and flag2==1:
##                            #print(poslist[u][0][0]," : ",len(poslist[u]),poslist[v][0][0]," : ",len(poslist[v]))
##                            if len(poslist[w])==len(poslist[z]):
##                                print("del: ",poslist[w][0][0],len(poslist[w])," ",txt[x],len(poslist[z]))
##                                d.append(poslist[w][0][0])
##                                del poslist[w]
##    for i in d:
##        txt.remove(i)
   
    
    
    #mlist is a merged list for merging the created positions in sorted order
    mlist = list()
    if len(poslist)>1:
        mlist= merge(poslist[0],poslist[1])
    x = 2
    while x < len(poslist):
        if len(poslist[x])!=0:
            #print len(poslist[x]), poslist[x]
            mlist = merge(mlist, poslist[x])
        x+=1

    t=[]
    for z in txt:
        count =0
        for i in range(len(mlist)):
            if z==mlist[i][0]:
                count +=1
##        if count==1:
##            print ("1: ",z)
        if count==0:
            #print ("0: ",z)
            t.append(z)
    for i in t:
        txt.remove(i)

    # Now create the adjacency matrix for the graph
    adjmatrix = list()
    txt.sort()
    text.tokens=txt
    #print ("txt::",txt)
    from adjmatrix import AdjMatrix
    amatrix = AdjMatrix()
    amatrix.createMatrix(txt, mlist, False)
    #text.append(filename)
    #print text
    #amatrix.addFilename(filename,text)
    #print(txt)
    return amatrix
    

def update_graph(text, filename):
    f = open(filename)
    basetext = f.read().lower()
    #basetext=basetext.replace("-"," ")
    from textmodel import Text    
    btext = Text(basetext)
    #btokens = nltk.word_tokenize(basetext)
    btokens = nltk.regexp_tokenize(basetext,"[\w']+")
    btext.tokens = btokens
    if text is None:
        print("Grrrrrrrrrr");
    
    #text.tokens = text1
    print ("..........",len(text.tokens))
    txt = list(text.tokens)
    poslist = list()
    print ("..............", len(txt))
    #print text
    temp={}
    t=[]
    #creating poslist for the terms
    for x in txt:
        #tmptokens = nltk.word_tokenize(txt[x])
        tmptokens = nltk.regexp_tokenize(x,"[\w']+")
        if len(tmptokens)==1:
            pos = list(get_positions(btext.tokens, tmptokens[0],txt))
        elif len(tmptokens)>1:
            pos = list(get_phrasepos(btext.tokens,x,txt))
        else:
            pos=[]
            t.append(x)
        if len(pos)>0:
            if pos[0][0] in temp.keys():
                for i in range(len(pos)):
                    if pos[i] not in temp[pos[0][0]]:
                        temp[pos[0][0]].append(pos[i])
            else:
                temp[pos[0][0]]=pos
            if pos[0][0]!=x:
                print ("removed",x," | ",pos[0][0])
                t.append(x)
    #removing unneccessary sub-lists ie "linked" from "linked list"
    k=[]
    for x in temp.keys():
        for y in temp.keys():
            if x !=y:
                if x in y:
                    tmpx=nltk.word_tokenize(x)
                    tmpy=nltk.word_tokenize(y)
                    fx=0
                    fy=0
                    for i in range(len(tmpy)):
                        if tmpy[fy]==tmpx[fx]:
                            fy+=1
                            fx+=1
                        else:
                            fy+=1
                        if fx==len(tmpx):
                            if len(temp[x])==len(temp[y]):
                                print("delete: ",x," | ",y)
                                if x not in k:
                                    k.append(x)
                            break
    for i in k:
        del temp[i]
        txt.remove(i)
    si={}
    for i in temp.keys():
        si[i]=len(temp[i])
    r=[]
    for i in temp.keys():
        tmpx=nltk.word_tokenize(i)
        if len(tmpx)>1:
            for j in temp:
                if i!=j:
                    if i in j:
                        si[i]-=si[j]
                        r.append(j)
##    for i in j:
##        si[i]=0
    
    for i in temp.keys():
        tmpx=nltk.word_tokenize(i)
        if len(tmpx)==1:
            for j in temp:
                if i!=j:
                    if i in j:
                        si[i]-=si[j]
    r=[]
    for i in temp.keys():
        if si[i]==0:
            print ("to be removed: ",i)
            r.append(i)
    for i in r:
        txt.remove(i)
        del temp[i]
    for i in t:
        txt.remove(i)
    for i in temp.keys():
        poslist.append(temp[i])
##    d=[]
##    #removing unneccessary sub-lists ie "linked" from "linked list"
##    for x in range(len(txt)):
##        tmptokens = nltk.word_tokenize(txt[x])
##        if len(tmptokens)>1:
##            for y in range(len(tmptokens)):
##                if tmptokens[y] not in stop:
##                    if tmptokens[y] in txt:
##                        u=0
##                        flag1=0
##                        flag2=0
##                        flag=0
##                        w=0
##                        z=0
##                        for u in range(len(poslist)):
##                            if len(poslist[u])>1:
##                                if poslist[u][0][0]==tmptokens[y] and flag1==0:
##                                    flag1=1
##                                    flag+=1
##                                    w=u
##                                if poslist[u][0][0]==txt[x] and flag2==0:
##                                    flag2=1
##                                    flag+=1
##                                    z=u
##                            if flag==2:
##                                break
##                        if flag1==1 and flag2==1:
##                            #print(poslist[u][0][0]," : ",len(poslist[u]),poslist[v][0][0]," : ",len(poslist[v]))
##                            if len(poslist[w])==len(poslist[z]):
##                                print("del: ",poslist[w][0][0],len(poslist[w])," ",txt[x],len(poslist[z]))
##                                d.append(poslist[w][0][0])
##                                del poslist[w]
##
##    for i in d:
##        txt.remove(i)
    
    #mlist is a merged list for merging the created positions in sorted order
    mlist = list()
    if len(poslist)>1:
        mlist= merge(poslist[0],poslist[1])
    x = 2
    while x < len(poslist):
        if len(poslist[x])!=0:
            mlist = merge(mlist, poslist[x])
        x+=1

    #print mlist
    #print(txt)
    t=[]
    for z in txt:
        count =0
        for i in range(len(mlist)):
            if z==mlist[i][0]:
                count +=1
        if count==1:
            print ("1: ",z)
        if count==0:
            print ("0: ",z)
            t.append(z)
    for i in t:
        txt.remove(i)
    txt.sort()
    text.tokens=txt
    return mlist

def stem(word):
    regexp = r'^(.*?)(ing|ly|ed|ious|ies|ive|es|s|ment|er|r)?$'
    stem, suffix = re.findall(regexp, word)[0]
    return stem

def stemplural(word):
    regexp = r'^(.*?)(s)?$'
    stem, suffix = re.findall(regexp, word)[0]
    return stem

def removelinebreak(text):
    #print text
    text1= list()
    for i in range(len(text)):
        #print text[i]
        temp = text[i].rstrip('\r')
       # print temp
        text1.append(temp)
    return text1
"""
http://docs.python.org/library/itertools.html
"""
"""
    This method returns the set of positions of a keyword in the given document
"""
def get_positions(doc, item, text):
    # return [(i, xs.index(item)) for i, item in enumerate(xs)]
    pos = list()
    i=0
    for word in doc:
        #if word == item:
        word1 = (word)
        item1 = (item)
##        if item == "executable":
##        print word1, word , item1, item
        
        if (word1 == item1):
            #print (item, i)
##            if item[:-1] in text:
##                item=item[:-1]
            item1=item
            ph=item1.replace("-"," ")
            if ph in text:
                if ph[len(ph)-1]=="s" and ph[:-1] in text:
                    item1=ph[:-1]
                else:
                    item1=ph
            pos.append([item1,i])
        i+=1
    return pos

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
    
"""
    Merges two sorted list in sorted order
"""
def merge(list1, list2):
    i=0
    j=0
    mlist = list()
    while i < len(list1) and j < len(list2):
        #print("Name",list1[i][0], list1[i][1],"Name",list2[i][0], list2[i][1])
        if list1[i][1] < list2[j][1]:
            mlist.append(list1[i])
            i += 1
        elif list1[i][1] > list2[j][1]:
            mlist.append(list2[j])
            j += 1
        else:
            mlist.append(list1[i])
            if list1[i][0]!=list2[j][0]:
                mlist.append(list2[j])
            i += 1
            j += 1
    if (i < len(list1)):
        while i < len(list1):
            mlist.append(list1[i])
            i += 1
    
    if (j < len(list2)):
        while j < len(list2):
            mlist.append(list2[j])
            j += 1

    #print (len(list1), len(list2), len(mlist))
    #for x in range(len(text)):print ("***********************")
    return mlist

def draw_png(gr):
    dot = write(gr)
    gvv = gv.readstring(dot)
    gv.layout(gvv,'dot')
    gv.render(gvv,'png','textgraph.png')

def draw_graph(text,amatrix):
   
##    U = ubigraph.Ubigraph()
##    U.clear()
    server_url = 'http://127.0.0.1:20738/RPC2'
    server = xmlrpclib.Server(server_url)
    U = server.ubigraph;
    U.clear()
    #smallRed = U.newVertexStyle(shape="octahedron", color="#ff0000", size="0.3")
    #smallRed = U.new_vertex_style(0)
    greenedge = U.new_edge_style(0)
##    U.set_vertex_style_attribute(smallRed, "color", "#ff0000")
##    U.set_vertex_style_attribute(smallRed, "size", "#0.1")
##    U.set_vertex_style_attribute(smallRed, "shape", "cube")
    
    U.set_edge_style_attribute(greenedge,"arrow","true")
    U.set_edge_style_attribute(greenedge,"width","2.0")
    U.set_edge_style_attribute(greenedge,"spline","true")
    U.set_edge_style_attribute(greenedge,"fontfamily","TimesRoman")
    U.set_edge_style_attribute(greenedge,"fontcolor","#888888")
    U.set_edge_style_attribute(greenedge,"stroke","dashed")
    
    
    
    
    x = list()

    for a in range(len(text)):
        #x.append(U.newVertex(style=smallRed, label=text[a]))
        temp = U.new_vertex_w_id(a)
        #U.change_vertex_style(a,smallRed)
        U.set_vertex_attribute(a,"label", text[a])
        #temp = U.get_vertex_w_id(a)
        #x.append(temp)
        
    for i in range(len(text)):
        #if gr.has_node((text[i])) == True:
        for j in range(len(text)):
            #if amatrix.gmatrix[i][j].weight != float('inf'):
            #if amatrix.gmatrix[i][j] != float('inf'):
            #if amatrix.gmatrix[i][j] < 100:
            if amatrix.gmatrix[i][j].weight <5:
                wt1= amatrix.gmatrix[i][j]
                #gr.add_edge((text[i],text[j]),wt = wt1, label = wt1)    
                if (i<j):
                    #U.newEdge(x[i],x[j],arrow=True, color = "#ccffcc", width = '2.0',
                    #      fontfamily = "Times Roman", fontsize = "18", spline = True,label=str(wt1), stroke = "dashed")
                    U.new_edge_w_id(i*len(text)+j,i,j)
                    U.change_edge_style(i*len(text)+j,greenedge)
                    U.set_edge_attribute(i*len(text)+j, "label",str(wt1))
                    U.set_edge_attribute(i*len(text)+j,"color","#ccffcc")
    
                    #U.set_edge_attribute(i*len(text)+j, "width","3.0/wt1")
                else:
                    #U.newEdge(x[i],x[j],arrow=True, color = "#33ffff", width = '3.0',
                    #      fontfamily = "Times Roman", fontsize = "18", fontcolor = "#ff33ff", spline = True,label=str(wt1), stroke = "dashed")
                    U.new_edge(i,j)
                    U.change_edge_style(i*len(text)+j,greenedge)
                    U.set_edge_attribute(i*len(text)+j, "label",str(wt1))
                    #U.set_edge_attribute(i*len(text)+j, "width","3.0/wt1")
                    U.set_edge_attribute(i*len(text)+j, "color","ff0000")

      
if __name__ == '__main__':
    from nltk.corpus import gutenberg
    words = ['biochem2.txt']
    create_graph(gutenberg.words('austen-sense.txt'), words)
