from math import sqrt
import sys
import csv
import operator

fipath=sys.argv[1]
'fopath=sys.argv[2]'

with open(fipath,'r') as fi:
    reader=csv.reader(fi)
    lines=list(reader)

ROW=len(lines)
COLUMN=len(lines[0])
HEADER=False

'''
Initialize input file : 
Fill empty data with None to make column correct.
Convert strings to integers in each row to calculate similarity later.
Return a item*user matrix.
'''
def initialize(matrix):

    if HEADER:
        begin=1
    else:
        begin=0
    for i in range(begin,ROW):
        for j in range(0,COLUMN):
            if matrix[i][j]:
                matrix[i][j]=int(matrix[i][j])
            else:
                matrix[i][j]=None
        while len(matrix[i])<COLUMN:
            matrix[i].append(None)
    return matrix

'subtract mean rating mi from each items(row)'
def subtract(vector):
    total,count=0,0
    for i in vector:
        if i==0 or i:
            total+=i
            count+=1
    mi=total/count
    new_vector=[]
    for i in range(0,len(vector)):
        if vector[i]==0 or vector[i]:
            new_vector.append(vector[i]-mi)
        else:
            new_vector.append(0)
    return new_vector

'calculate cosine similarity value between two vectors'
def sim(v1,v2):
    if v1==v2:
        return 1.00
    if len(v1)!=len(v2):
        print('Error')
    else:
        up,a,b=0,0,0
        for i in range(0,len(v1)):
            up+=v1[i]*v2[i]
            a+=v1[i]*v1[i]
            b+=v2[i]*v2[i]
        down=sqrt(a)*sqrt(b)
        return up/down

'calculate all similarity between items(rows) by comparing with the given item(row)'
def sim_between_rows(matrix,row):
    'Pearson Correlation'
    sub_matrix=[subtract(i) for i in matrix]

    all_sim={}
    for rows in range(1,ROW+1):
        if rows!=row:
            all_sim[rows]=sim(sub_matrix[row-1],sub_matrix[rows-1])
    return all_sim

'choose N most similar neighbors by the given number N'
def get_neighbor(all_sim,N):
    neighbors=[]
    for _ in range(0,N):
        max_sim_neighbor=max(all_sim.items(), key=operator.itemgetter(1))[0]
        neighbors.append([max_sim_neighbor,all_sim[max_sim_neighbor]])
        del all_sim[max_sim_neighbor]
    return neighbors

'''
Predict rating value at position (row,col) with N neighbors.
Default file has no header.
'''
def predict(row,col,N,with_header=False):
    HEADER=with_header

    'get integer matrix rows*columns'
    matrix=initialize(lines)

    'rating value in the given position already exist'
    if matrix[row-1][col-1]:
        return matrix[row-1][col-1]

    'all similarity values comparing with the given row'
    all_sim=sim_between_rows(matrix,row)

    'get N neighbors from all items(rows)'
    neighbors=get_neighbor(all_sim,N)

    'ensure the value is not empty in the given column among those neighbors(rows)'
    empty=False
    for i in neighbors:
        if matrix[i[0]-1][col-1]==None:
            empty=True
            print('Error: Empty value in neighbor\'s filed. row:',i[0],'coloumn:',col)

    'given position is not empty, return predict rating value'
    if empty==False:
        total,count=0,0
        for i in neighbors:
            total+=i[1]*matrix[i[0]-1][col-1]
            count+=i[1]
        predict=total/count
        return predict


