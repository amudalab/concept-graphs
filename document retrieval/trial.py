import xlwt 
##fc=open('closeness1.txt')
##raw=fc.read()
##close={}
##flag=0
##pl=raw.split("\n")
##for each_line in pl:
##    l=each_line.split(',')
##    print each_line
##    if len(l)==3:
##        if flag!=0:
##            close[l[1].replace("\n","")]=float(l[2])
##        flag=1
##fb=open('betweeness1.txt')
##raw=fb.read()
##between={}
##flag=0
##pl=raw.split("\n")
##for each_line in pl:
##    l=each_line.split(',')
##    print each_line
##    if len(l)==3:
##        if flag!=0:
##            between[l[1].replace("\n","")]=float(l[2])
##        flag=1
##fd=open('degree1.txt')
##raw=fd.read()
##degree={}
##flag=0
##pl=raw.split("\n")
##for each_line in pl:
##    l=each_line.split(',')
##    print each_line
##    if len(l)==3:
##        if flag!=0:
##            degree[l[1].replace("\n","")]=float(l[2])
##        flag=1
fs=open('strength.txt')
raw=fs.read()
strength={}
flag=0
pl=raw.split("\n")
for each_line in pl:
    l=each_line.split(',')
    print each_line
    if len(l)==3:
        if flag!=0:
            strength[l[1].replace("\n","")]=float(l[2])
        flag=1
book = xlwt.Workbook(encoding="utf-8")
sheet1 = book.add_sheet("Python Sheet 1")
i=1
#print close
##sheet1.write(0, 1, 'closeness')
##sheet1.write(0, 2, 'betweeness')
##sheet1.write(0, 3, 'degree')
sheet1.write(0, 1, 'strength')
for key in strength.keys():
    sheet1.write(i, 0, key)
##    sheet1.write(i, 1, close[key])
##    sheet1.write(i, 2, between[key])
##    sheet1.write(i, 3, degree[key])
    sheet1.write(i, 1, strength[key])
    i+=1
book.save("python_spreadsheet.xls")
##fc.close()
##fb.close()
##fd.close()
fs.close()
