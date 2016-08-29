import urllib2
import nltk
from bs4 import BeautifulSoup

#function return a dict of word urls 
def get_word_det(word_ls):
        word_url=dict.fromkeys(word_ls)
        for n in word_ls:
                wordpt=n.split(' ')
                wo=wordpt[0]
                for i in range(1,len(wordpt)):
                        wo=wo+"+"+wordpt[i]
                

                search_url="http://en.wikipedia.org/w/index.php?search="+wo+"&title=Special%3ASearch"
		
		req = urllib2.Request(search_url, headers={'User-Agent' : "Magic Browser"})
		con = urllib2.urlopen( req )
		soup=BeautifulSoup(con.read())
		
		str1=(soup.get_text()).encode('ascii','ignore')
		wantls=str1.split("firstHeading ",1)
		if len(wantls)==1:
			str1=wantls[0]
		else:
			str1= wantls[1]	
		#wantls=[]
		wantls=str1.split("/content",1)
		#wantls=wantls[0].split("Database models\nDatabase normalization",1)	
		str1=wantls[0]
		filen="moon/"+n
		fwo=open(filen,"w+")		
		fwo.write(str1)
		fwo.close()


		
	



#creatin list from text file of words
fl=open("moonfilelist.txt")

wordls=[]

for each_line in fl:
	x=each_line.strip('\n')
	wordls.append(x)

for word in wordls:
	print word	
get_word_det(wordls)

