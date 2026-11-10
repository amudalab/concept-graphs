import sys
import xlwt
fp = open('taxK.gdf')
#fil_fin=open("shortest_path_tree1/comp_shortest_path_tree.gdf","w")
text=fp.read()
pl=text.split('\n')
#print(p1)
flag=0
V=[]
VN={}
flag=0
for each_line in pl:
    l=each_line.split(',')
    if len(l)==2:
        if flag!=0:
            V.append(l[0])
            VN[l[0]]=l[1]
        flag=1
book = xlwt.Workbook(encoding="utf-8")
sheet1 = book.add_sheet("taxonomy for K")
b=1
sheet1.write(0, 0, 'vertex 1')
sheet1.write(0, 1, 'vertex 2')
flag=0
for each_line in pl:
    l=each_line.split(',')
    if len(l)==5:
        if flag!=0:
            sheet1.write(b, 0, VN[l[1]])
            sheet1.write(b, 1, VN[l[0]])
            b+=1
        flag=1

fp = open('taxEM4.gdf')
#fil_fin=open("shortest_path_tree1/comp_shortest_path_tree.gdf","w")
text=fp.read()
pl=text.split('\n')
#print(p1)
flag=0
V=[]
VN={}
flag=0
for each_line in pl:
    l=each_line.split(',')
    if len(l)==2:
        if flag!=0:
            V.append(l[0])
            VN[l[0]]=l[1]
        flag=1
sheet2 = book.add_sheet("taxonomy for EM")
b=1
sheet2.write(0, 0, 'vertex 1')
sheet2.write(0, 1, 'vertex 2')
flag=0
for each_line in pl:
    l=each_line.split(',')
    if len(l)==5:
        if flag!=0:
            sheet2.write(b, 0, VN[l[1]])
            sheet2.write(b, 1, VN[l[0]])
            b+=1
        flag=1
book.save("tax_edges.xls")
