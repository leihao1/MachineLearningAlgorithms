import random
import math
from math import sqrt
import sys
import csv


fipath=sys.argv[1]

with open(fipath,'r') as fi:
    reader=csv.reader(fi)
    lines=list(reader)

ROW=len(lines)
COLUMN=len(lines[0])

all_points=[]

'all_clusters={cluster_id:[x,y,sumx,sumy,N]}'
all_clusters={} 

stablize=True


back_up={}
'good_k={number:avg_cenroid_dis}'

'change clusters\' name.Defulat:0,1,2...k'
def rename_cluster(cluster_name=None):
    global all_clusters
    if all_clusters:
        if cluster_name!=None:
            print("CLUSTER[>",cluster_name,"<]:")  
            str = input()
            all_clusters[str]=all_clusters[cluster_name]
            del all_clusters[cluster_name]
        else:
            new_clusters={}
            for c in all_clusters:
                print("CLUSTER[>",c,"<] :")
                str = input()
                new_clusters[str]=all_clusters[c]
            all_clusters=new_clusters

'get all data coordinate from exist cluster file'
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


'select best K'
def select_k():
    return 4


'pick K initial points as K clusters by dispersed method'
def pick_initial_points(K):
    '  1.sampling'
    '->2.dispersed'

    copy=list(all_points)
    'print("all_points:",all_points)'
    first=random.choice(all_points)
    'print("first:",first)'
    init_clusters={}
    init_clusters[0]=[first[0],first[1],0,0,0]

    copy.remove(first)
    picked=[first]
    
    for n in range(1,K):
        max_distance,waitlist=0,0
        for p in copy:
            distance=0
            for i in picked:
                distance+=math.hypot(p[0]-i[0],p[1]-i[1])
            if distance>max_distance:
                max_distance,waitlist=distance,p
        copy.remove(waitlist)
        picked.append(waitlist)
 
        init_clusters[n]=[waitlist[0],waitlist[1],0,0,0]
    
    return init_clusters
        

'go through the whole dataset and assign each point to one cluster by centroid distance'
def assigning_cluster(points,clusters):
    all_clusters=clusters
    all_points=points

    for p in all_points:

        cluster_dis=[]
        for c in all_clusters:
            dis=math.hypot(p[0]-all_clusters[c][0],p[1]-all_clusters[c][1])
            cluster_dis.append(dis)

        min_dis,assign=cluster_dis[0],0
        for i in range(1,len(cluster_dis)):
            if cluster_dis[i] < min_dis:
                min_dis,assign=cluster_dis[i],i

        'change sumx and sumy and total points number N'
        all_clusters[assign][2]+=p[0]
        all_clusters[assign][3]+=p[1]
        all_clusters[assign][4]+=1
    "print('after assigning:')"
    'print(all_clusters)'

    final_cluesters=reset_cluster(all_clusters)
    return final_cluesters


def reset_cluster(cluster):
    global stablize
    stablize=True
    for c in cluster:    
        x=cluster[c][0]
        y=cluster[c][1]
        sumx=cluster[c][2]
        sumy=cluster[c][3]
        N=cluster[c][4]
        if x!=sumx/N or y!=sumy/N:
            stablize=False
            x=sumx/N
            y=sumy/N
            cluster[c][0]=x 
            cluster[c][1]=y
            cluster[c][2]=0
            cluster[c][3]=0
            cluster[c][4]=0

    return cluster

'clustering by K-means '
def a():
    global all_points
    global all_clusters
    
    all_points=find_from_cluster(lines)

    'step one'
    K=select_k()

    'step two'
    all_clusters=pick_initial_points(K)
    print('intit clusters:',all_clusters)

    'step three'
    all_clusters=assigning_cluster(all_points,all_clusters)

    'loop between step two and three'
    while stablize==False:
        all_clusters=assigning_cluster(all_points,all_clusters)
    print('final clusters:',all_clusters)    


def output():
    return 0

