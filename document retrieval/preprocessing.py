"""
   Preprocessing, including stemming, stopword etc.

"""

import nltk

"""
 Stop word removal
"""

def remove_stopword(text):
    """
       Remove stopwords from the text file
    """
    from nltk.corpus import stopwords
    stopset = set(stopwords.words('english'))
    #print stopset
    from nltk.collocations import BigramCollocationFinder
    from nltk.metrics import BigramAssocMeasures
    words = [w.lower() for w in text.tokens]
    content = [w for w in text.tokens if w.lower() not in stopset and len(w)>3]
    
    #print words
   # print content
    bcf = BigramCollocationFinder.from_words(words)
    filter_stops = lambda w: len(w) < 3 or w in stopset
    newwords = bcf.apply_word_filter(filter_stops)
    #bcf.nbest(BigramAssocMeasures.likelihood_ratio, 4)
    return content

def stemmer(text, words):
    """
        Stem the text using porter stemmer or lancaster stemmer
    """
    #from nltk.stem import LancasterStemmer
    #from nltk.stem import PorterStemmer
    from nltk.stem import WordNetLemmatizer
    #stemmer = LancasterStemmer()
    #stemmer = PorterStemmer()
    lemmatizer = WordNetLemmatizer()
    #content = [stemmer.stem(w) for w in words]
    content = [lemmatizer.lemmatize(w) for w in words]
    return content

if __name__ == '__main__':
    from nltk.corpus import gutenberg
    remove_stopword(gutenberg.words('austen-sense.txt'))
    #print textnew
