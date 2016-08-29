from os import listdir
lis1 = [f for f in listdir("C:/Users/Romauld/Desktop/final year project/update 24.2/all")]
for i in lis1:
    f=open("all/"+i)
    x=i.replace(" ","")
    fw=open("output/"+x+".txt","w")
    raw=f.read()
    fw.write(raw)
    f.close()
    fw.close()
print (lis1)
