from os import listdir
lis1 = [f for f in listdir("C:/Users/Romauld/Desktop/final version 4/stack/Keys/")]

i=0

keys=[]
dockeys=[0 for x in range(len(lis1))]
for j in range(len(lis1)):
    f=open("Keys/"+lis1[j])
    raw=f.read()
    raw=raw.split("\n")
    #print raw
    keys=list(set(keys)|set(raw))
    dockeys[j]=list(set(raw))
    dockeys[j].remove('')
keys.remove('')
print keys.index('pop')

comat = [[0 for x in range(len(keys))] for x in range(len(keys))]

for i in range(len(lis1)):
    for j in range(len(dockeys[i])):
        print 'i'
