from math import sqrt
import sys
import csv
import operator

fipath=sys.argv[1]
ftest_path=sys.argv[2]

with open(fipath,'r') as fi:
    reader=csv.reader(fi)
    lines=list(reader)
with open(ftest_path,'r') as ftest:
    reader2=csv.reader(ftest)
    test_set=list(reader2)

ROW=len(lines)
COLUMN=len(lines[0])
HEADER=False
overall_avg_rating=0

'''
Initialize input file : 
Fill empty data with None to make column correct.
Convert strings to integers in each row to calculate similarity later.
Return a item*user matrix.
'''
def initialize(matrix):
    rating=0
    total=0
    if HEADER:
        begin=1
    else:
        begin=0
    for i in range(begin,ROW):
        for j in range(0,COLUMN):
            if matrix[i][j]:
                matrix[i][j]=int(matrix[i][j])
                rating+=matrix[i][j]
                total+=1
            else:
                matrix[i][j]=None
        while len(matrix[i])<COLUMN:
            matrix[i].append(None)
    global overall_avg_rating
    overall_avg_rating=rating/total
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
        print('Can not calculate vectors with different length')
        exit()
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


'estimate final predict value by basic CF or combine with global baseline'
def estimate(matrix,neighbors,col,baseline=0):
    total,count=0,0
    for i in neighbors:
        if matrix[i[0]-1][col-1]!=None:
            total+=i[1]*(matrix[i[0]-1][col-1]-baseline)
            count+=i[1]
    if count==0:
        total,count=0,1
    predict=baseline+total/count
    return predict    


'''
Predict rating value at position (row,col) with N neighbors.
Default file has no header.
'''
def basic_predict(row,col,N,with_header=False):
    HEADER=with_header
    assert(0<N<ROW),'Neighbor N must between 0 and the maximum row number'
    assert(row>0 and col>0),"Row or Column must be positive integers"
    assert(row<=ROW and col<=COLUMN),"Row or Column out of dataset boundary"

    'get integer matrix rows*columns'
    matrix=initialize(lines)

    """
    rating value in the given position already exist
    if matrix[row-1][col-1]:
        exist=True
        origin=matrix[row-1][col-1]
    """

    'all similarity values comparing with the given row'
    all_sim=sim_between_rows(matrix,row)

    'get N neighbors from all items(rows)'
    neighbors=get_neighbor(all_sim,N)

    'ensure the value is not empty in the given column among those neighbors(rows)'
    empty=False
    for i in neighbors:
        if matrix[i[0]-1][col-1]==None:
            empty=True
            print('Empty value in neighbor\'s filed. row:',i[0],'coloumn:',col)

    'given position is not empty, return predict rating value'
    if empty==False:
        predict = estimate(matrix,neighbors,col)
        return predict
    else:
        exit()


'predict user rating using CF combine with baseline algorithsm'
def baseline_predict(row,col,N):

    assert(0<N<ROW),'Neighbor N must between 0 and the maximum row number'
    assert(row>0 and col>0),"Row or Column must be positive integers"
    assert(row<=ROW and col<=COLUMN),"Row or Column out of dataset boundary"
    matrix=initialize(lines)

    all_sim=sim_between_rows(matrix,row)
    neighbors=get_neighbor(all_sim,N)

    userx_rating=0
    userx_count=0
    for point in matrix:
        if point[col-1] or point[col-1]==0:
            userx_rating += point[col-1]
            userx_count += 1
    userx_avg=userx_rating/userx_count

    item_rating=0
    item_count=0
    for p in matrix[row-1]:
        if p or p==0:
            item_rating += p
            item_count += 1
    item_avg=item_rating/item_count
    
    bx=userx_avg - overall_avg_rating
    bi=item_avg - overall_avg_rating
    baseline=overall_avg_rating+bx+bi
    predict=estimate(matrix,neighbors,col,baseline)
    return predict


'return the points that need to be test (set T)'
def get_test_points():
    matrix=initialize(lines)
    test_matrix=initialize(test_set)
    test_points=[]
    for row in range(len(matrix)):
        for col in range(len(matrix[row])):
            if matrix[row][col]!=test_matrix[row][col]:
                temp=[]
                temp.append(row)
                temp.append(col)
                temp.append(matrix[row][col])
                test_points.append(temp)
    return test_points


'''
Evaluate different algorithms(basic/baseline+cf) with given neighbors.
RMSE:Root-mean-square error.
'''
def evaluate(function,neighbors):
    test_set=get_test_points()
    square_error=0
    N=len(test_set)

    assert(N>1),"Test set must including more than one data"

    for p in test_set:
        predict=function(p[0]+1,p[1]+1,neighbors)
        square_error += pow(predict-p[2],2)

    RMSE=sqrt(square_error/N)
    return RMSE

'evaluate basic CF algorithms'
def basic_evaluate(neighbors):
    return evaluate(basic_predict,neighbors)

'evaluate CF+baseline algorithms'
def baseline_evaluate(neighbors):
    return evaluate(baseline_predict,neighbors)

