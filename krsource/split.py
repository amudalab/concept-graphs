import nltk
fx=open("testpaper1.txt")
fy=open("keyword.txt")
fn=open("newtestpaper.txt","w")

key=[]
badwords=["the","and","of","to","on","in","an","a","for","is","it","its",""]
for eline in fy:
    x=eline.strip('\n')
    key.append(x+' ')
#print (key)
global i
i=0
for line in fx:
    s=line.strip('.')
    l=s.split(' ')
    #print (l)
    for w in l:
        w=w.lower()
        w1=w
        if w not in badwords:
            w=' '+w+' '
            #w.replace(",",'')
            #print("W: ",w)
            for k in key:
                #print("KEY: ",k,"value",k.find(w))
                if k.find(w)>=0:
                    #w=w[1:]
                    i=i+1
                    fn.write(str(w1))
                    fn.write("\n")
                    
                    #print(w)
                    break
        #z=input()
print(i)       
print("SUCCESS")

fn.close()

    
