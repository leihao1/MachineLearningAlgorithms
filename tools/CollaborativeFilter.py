from math import sqrt
import sys
import csv

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
