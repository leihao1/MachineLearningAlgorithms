import random
import math
from math import sqrt
import sys
import csv
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cbook as cbook

'================================deal with input file=============================='
fipath=sys.argv[1]
with open(fipath,'r') as fi:
    reader=csv.reader(fi)
    lines=list(reader)
ROW=len(lines)
COLUMN=len(lines[0])
back_up={}
'find all data coordinate from exist cluster in the file'
'given cluster are used to evaluate select_k function'
def find_from_cluster(lines):
    init_points=[]
    for r in range(ROW):
        for c in range(COLUMN):
            if lines[r][c] != '':
                position=(r+1,c+1)
                init_points.append(position)
                global back_up
                back_up[position]=int(lines[r][c])
    return init_points

'get data coordinate directly from file'
def get_coordinate():
    pass
'==================================================================================='

coordinates = find_from_cluster(lines)

'===============================k-means clustering library=========================='
'select best K'
'good_k={number:avg_cenroid_dis}'
def select_k():
    return 4


'pick K initial points as K clusters by dispersed method'
def pick_initial_points(K,all_points):
    '  1.sampling'
    '->2.dispersed'

    first=random.choice(all_points)
    init_clusters={}
    init_clusters[0]=[first[0],first[1],0,0,0]

    picked=[first]
    
    for n in range(1,K):
        max_distance,waitlist=0,0
        for p in all_points:
            distance=0
            for i in picked:
                distance+=math.hypot(p[0]-i[0],p[1]-i[1])
            if distance>max_distance:
                max_distance,waitlist=distance,p
        
        picked.append(waitlist)
        init_clusters[n]=[waitlist[0],waitlist[1],0,0,0]
       
    return init_clusters
        

'go through the whole dataset and assign each point to one cluster by centroid distance'
def assigning_cluster(all_points,all_centroid):
    cluster_members={}
    for c in all_centroid:
        cluster_members[c]=[]
    for p in all_points:
        cluster_dis=[]
        for c in all_centroid:
            dis=math.hypot(p[0]-all_centroid[c][0],p[1]-all_centroid[c][1])
            cluster_dis.append(dis)

        min_dis,assign=cluster_dis[0],0
        
        for i in range(1,len(cluster_dis)):
            if cluster_dis[i] < min_dis:
                min_dis,assign=cluster_dis[i],i

        'change sumx and sumy and total number of points'
        all_centroid[assign][2]+=p[0]
        all_centroid[assign][3]+=p[1]
        all_centroid[assign][4]+=1
        cluster_members[assign].append(p)
    '''
    print('After Assigning (centroid):')
    print(all_centroid)
    print('')
    print('After Assigning (members):')
    print(cluster_members)
    print('')
    '''
    final_centroid,stablize=reset_cluster(all_centroid)
    return final_centroid,cluster_members,stablize

'reset cluster centroid and repeat assigning untill stabilize'
def reset_cluster(cluster):
    stable=True
    for c in cluster:    
        x=cluster[c][0]
        y=cluster[c][1]
        sumx=cluster[c][2]
        sumy=cluster[c][3]
        N=cluster[c][4]
        if x!=sumx/N or y!=sumy/N:
            stable=False
            x=sumx/N
            y=sumy/N
            cluster[c][0]=x 
            cluster[c][1]=y
            cluster[c][2]=0
            cluster[c][3]=0
            cluster[c][4]=0
    return cluster,stable

'clustering by K-means '
def kmeans(all_points=coordinates,K=None):
    assert(K==None or (K>0 and type(K)==int)),"K must be a positive integer"
    assert(type(all_points)==list),"Input data type must be list"

    if K==None:
        K=select_k()

    'all_centroid={"cluster_name":[x,y,sumx,sumy,N]}'
    all_centroid=pick_initial_points(K,all_points)
    print('Initial Clusters:',all_centroid)
    print('')
    
    all_centroid,cluster_members,stable=assigning_cluster(all_points,all_centroid)

    while stable==False:
        all_centroid,cluster_members,stable=assigning_cluster(all_points,all_centroid)
    '''
    print('Final Clusters:')
    print(all_centroid)   
    print('')
    print('Final Members:')
    print(cluster_members)
    print('')
    '''
    return all_centroid,cluster_members


"change clusters' name(defulat name:0,1,2...k)"
def rename_cluster(cluster,cluster_name=None):
    assert(type(cluster)==dict and len(cluster)>0),"Target cluster must be a valid dictionary"
    
    if cluster_name!=None:
        print("CLUSTER[>",cluster_name,"<]:")  
        str = input()
        cluster[str]=cluster[cluster_name]
        del cluster[cluster_name]
    else:
        new_clusters={}
        for c in cluster:
            print("CLUSTER[>",c,"<] :")
            str = input()
            new_clusters[str]=cluster[c]
        cluster=new_clusters
    return cluster
'==============================================================================='

centroid,members=kmeans()

'=================================visualization================================='

'show scatterplot by matplotlib and numpy'
def visualize(cluster=members):
    
    # Create data
    k = len(cluster)
    data=[]
    count=0
    for g in cluster:
        xy=cluster[g]
        x=[i[0] for i in xy]
        y=[i[1] for i in xy]
        g=(np.array(x), np.array(y))
        data.append(g)
        count+=len(x)
    print(data)
    print(count)
    for i in range(k):
        pass
    colors = ("red", "green", "blue")
    groups = ("coffee", "tea", "water") 
    
    # Create plot
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1, axisbg="2.0")
     
    for data, color, group in zip(data, colors, groups):
        x, y = data
        ax.scatter(x, y)
     
    plt.title('Matplot scatter plot')
    plt.legend(loc=2)
    plt.show()
'==============================================================================='
visualize()
