import nltk, re, pprint, textgraph
import sys
#import pygraph
import adjmatrix
class Text(object):
    """
    A wrapper around a sequence of simple (string) tokens, which is
    intended to support initial exploration of texts (via the
    interactive console).  Its methods perform a variety of analyses
    on the text's contexts (e.g., counting, concordancing, collocation
    discovery), and display the results.  If you wish to write a
    program which makes use of these analyses, then you should bypass
    the C{Text} class, and use the appropriate analysis function or
    class directly instead.

    C{Text}s are typically initialized from a given document or
    corpus.  E.g.:
    
    >>> moby = Text(nltk.corpus.gutenberg.words('melville-moby_dick.txt'))
    """
    # This defeats lazy loading, but makes things faster.  This
    # *shouldnt* be necessary because the corpus view *should* be
    # doing intelligent caching, but without this it's running slow.
    # Look into whether the caching is working correctly.
    
    _COPY_TOKENS = True

    def __init__(self, tokens, name=None):
        """
        Create a Text object.
        
        @param tokens: The source text.
        @type tokens: C{sequence} of C{str}
        """
        if self._COPY_TOKENS:
            tokens = list(tokens)
        self.tokens = tokens
        if name:
            self.name = name
        elif ']' in tokens[:20]:
            end = tokens[:20].index(']')
            self.name = " ".join(map(str, tokens[1:end]))
        else:
            self.name = " ".join(map(str, tokens[:8])) + "..."

    def create_graph(self, filename):
        """
        Create the graph from the list of words in the document
        """
        from textgraph import create_graph
##        tokens1 = self.remove_stopword()
##	self.tokens = tokens1
	#print len(self.tokens)
        grmatrix = create_graph(self,filename)
        return grmatrix
   		

    def remove_stopword(self):
        """
            Remove stopwords from the text file
        """
        from nltk.corpus import stopwords
        stopset = set(stopwords.words('english'))
        #print stopset
        from nltk.collocations import BigramCollocationFinder
        from nltk.metrics import BigramAssocMeasures
        words = [w.lower() for w in self.tokens]
        content = [w for w in self.tokens if w.lower() not in stopset and len(w)>3]
        return content
    

    def update_graph(self, filename):
        """
        Create the graph from the list of words in the document
        """
        #print("update_graph")
        #print self.tokens
        from textgraph import update_graph
        poslist = update_graph(self,filename)
        return poslist
    
    def show_graph(self, tokens, adjgraph):
        from textgraph import draw_graph
        draw_graph(tokens,adjgraph)

##    def show_graph(self, tgraph):
##        from textgraph import draw_graph
##        draw_graph(tgraph)
        
    def index(self, word):
        """
            Find the index of the first occurrence of the word in the text.
        """
        return self.tokens.index(word)

    def findallpos(self, word):
        """
            This methods finds all the positions of occurrence of the phrase in
            the given text
        """
        wordspos = list()
        wordsinphrase = nltk.word_tokenize(word)
        return wordpos       

    def findfirstpos(self, word, startpos, endpos):
        """
            Find the position of the word in the document between the start and
            end indices
        """
        for i in range(startpos, endpos):
            if tokens[i] == word:
                return i
        return -1
    
    def findfirstpos(self, phrase, startpos, endpos):
        """
            Find the position of the word in the document between the start and
            end indices
        """
        wordsinphrase = nltk.word_tokenize(phrase)
        for i in range(startpos, endpos):
            for j in range(len(phrase)):
                if tokens[i+j] == phrase[j]:
                    maybephrase = True;
                if maybephrase == True:
                    return i
                else:
                    return -1
    def updatetokens(self, newtokens):
        """
            Method to update a new set of tokens to this list.
            
        """
        #print("updatetokens")
        curtokens = list(set(newtokens))
        curtokens.sort()
        for i in range(len(curtokens)):
            if curtokens[i] not in self.tokens:
                self.tokens.append(curtokens[i])
                
