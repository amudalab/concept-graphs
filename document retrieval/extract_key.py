fn=open("filewords(om)3")
for each_line in fn:
    l=each_line.split(">")
    filen=l[0]
    wl=(l[1].lower()).split(",")
    f=open("Keys/"+l[0],"w")
    for i in range(len(wl)):
        f.write(wl[i]+"\n")
    f.close()

fn.close()
    
