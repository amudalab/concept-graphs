import os
import codecs
import unicodedata

path="C:\\Users\\Varun Shankar S\\Desktop\\Google PDF\\transcript"
txt=[]
asciitext=""
valid=['!','@','#','$','%','^','&','*','(',')','_','-','+','=','{','}','[',']',':',';','"','\'','<','>',',','.','?','/','|','\\','\n','\t',' ','~','`']
def updatekey(x):
    fkey=open("txt2ascii.txt","w")
    for t in x:
        fkey.write(str(t)+"\n")
    fkey.close()

def readtxtfile():
    tkey=open("txt2ascii.txt")
    key=tkey.read()
    txt=key.split("\n")
    return txt
    
def convert2ascii(f,asciitext):
    #print(f)
    file1=codecs.open(f,encoding='utf-8')
    text=file1.read()
    #print(type(text))
    '''
    asci=text.encode('ascii',"ignore")
    print(type(asci))
    print(asci)
    '''
    data=unicodedata.normalize("NFKD",text).encode("ascii","ignore")
    #print data
    #print(type(data))
    for i in data:
        if((i>='A' and i<='Z')or(i>='a' and i<='z')or(i>='0'and i<='9')or(i in valid)):
            asciitext=asciitext+str(i)
    #print(asciitext)
    file1.close()
    file2=open(f,'w')
    file2.write(asciitext)
    file2.close()
    print("FILE CONVERTED To ASCII...")
    
 
def readfiles(asciitext):
    for f in os.listdir(path):
        print(f)
        if f not in txt:
            k=path+"\\"+f
            convert2ascii(k,asciitext)
            txt.append(f)
            updatekey(txt)
            

txt=readtxtfile()
print(txt)
readfiles(asciitext)
