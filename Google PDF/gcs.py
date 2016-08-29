from apiclient.discovery import build
import urllib
import os
  # Build a service object for interacting with the API. Visit
  # the Google APIs Console <http://code.google.com/apis/console>
  # to get an API key for your own application.

rel=open("docrel.txt","w")
compkey=[]
query='google custom search api'
nosearch= False
fpath="Gsearch/"+query
val=0
rval=0
def updatekeycount(x):
    fkey=open("keycount.txt","w")
    fkey.write(str(x))
    fkey.close()
    
def keycount():
    fkey=open("keycount.txt")
    keyval=fkey.read()
    keyval=int(keyval)
    fkey.close()
    return keyval

def readcompkey():
    f=open("compkey.txt")
    txt=f.read().lower()
    key=txt.split("\n")
    c=0
    for i in key:
        ni=i.split("\t")
        compkey.append(ni[0])
        c+=1    
    #print(compkey,c)

def downloadpdf(res,rval):
    if nosearch == False:
        for items in res[u'items']:
            url = items[u'link']
            title = items[u'title']
            snippet = items[u'snippet']
            print url
            print title
            print snippet
            print "\n\n"
            px=url.rsplit('/',1)[1]
            px=fpath+"/"+px
            
            flag=1
            try:
                pdffile = urllib.URLopener()
                pdffile.retrieve(url,px)
            except Exception as ex:
                template = "An exception of type {0} occured. Arguments:\n{1!r}"
                message = template.format(type(ex).__name__, ex.args)
                print message
                flag=0
            if flag==1:
                rval+=1
                x=px+" "+str(rval)+" "
                print x
                rel.write(x)


val=keycount()
readcompkey()
i=0
j=0
print "vikiy"
while ((len(compkey)>val+i+j) and i<30):
    rval=0
    query=compkey[val+i+j]
    fpath="Gsearch/"+query
    print query
    rel.write(str(query+"\t"))
    print fpath
    if os.path.exists(fpath):
        nosearch=True
        j+=1
        print("Search query already indexed\n")
    
    if not os.path.exists(fpath):
        os.makedirs(fpath)
        nosearch=False
        i+=1
        print("Search in progress...\n")
        
    if nosearch == False:
        service = build("customsearch", "v1",
                        developerKey="AIzaSyCHbN-nmTnEppdrv5rW2IxZVWFw_rfNb1k")
        res = service.cse().list(
            q=query,
            cx='003335988826150944671:b2x-yb6_ihm',fileType='pdf',
            lr='lang_en',
            num='10',
            ).execute()
        print res
        downloadpdf(res,rval)

        res1 = service.cse().list(
            q=query,
            cx='003335988826150944671:b2x-yb6_ihm',
            fileType='pdf',
            lr='lang_en',
            num='10',
            lowRange='11',
            highRange='20',
            ).execute()
        downloadpdf(res1,rval)
        updatekeycount(val+i+j)
        rel.write("\n")
    
        '''
        res2 = service.cse().list(
            q=query,
            cx='003335988826150944671:b2x-yb6_ihm',
            fileType='pdf',
            lr='lang_en',
            num='10',
            lowRange='21',
            highRange='30',
            ).execute()
        downloadpdf(res2)
'''        

updatekeycount(val+i+j)
rel.close()
