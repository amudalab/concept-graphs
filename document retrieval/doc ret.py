import xlwt
import xlrd
import copy
from os import listdir
if __name__ == '__main__':
    workbook = xlrd.open_workbook("doc_det/ds2.xlsx")
    order=[]
    clust=[[] for i in range(4)]
    #Get a sheet by index
    sheet = workbook.sheet_by_index(0)
     
    #Access the cell value at (2,2)
    print sheet.cell_value(0,1)

    sheet_name = workbook.sheet_names() 
    sheet = workbook.sheet_by_name(sheet_name[0])
    j=len(sheet.row_values(0))-1
    for i in range(len(sheet.col_values(0))):
        s=[]
        s.append(str(sheet.row_values(i)[1]))
        s.append(str(sheet.row_values(i)[2]).replace("'",""))
        s.append(str(sheet.row_values(i)[3]))
        clust[int(str(sheet.row_values(i)[j]).replace("cluster",""))].append(s)
    print clust[2]
    avg_deg=[0.0 for i in range(len(clust))]
    for i in range(len(clust)):
        count=0
        avg=0
        for j in range(len(clust[i])):
            count +=1
            avg += int(float(clust[i][j][2]))
        avg_deg[i]=1.0*avg/count
    #print avg_deg
    sort_avg=copy.copy(avg_deg)
    sort_avg.sort()
    print sort_avg
    print avg_deg
    for i in range(4):
        order.append(avg_deg.index(sort_avg[i]))
    order = order[::-1]
    print order
    
