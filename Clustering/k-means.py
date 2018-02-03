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

back_up={}
cluster_id=0
all_points=[]

'all_clusters={cluster_id:[x,y,sumx,sumy,N]}'
all_clusters={}

'good_k={number:avg_cenroid_dis}'

def find_all_points():
    points=[]
    for r in range(ROW):
        for c in range(COLUMN):
            if lines[r][c] != '':
                position=(r+1,c+1)
                points.append(position)
                global back_up
                back_up[position]=int(lines[r][c])
    return points

def select_K():
    return 4

def a():
    global all_points
    all_points=find_all_points()
    global all_clusters
    all_clusters=pick_initial_points(select_K())
    print('all_clusters:',all_clusters)
    assigning_cluster()
    print('after all_clusters:',all_clusters)
    

'pick K initial points as K clusters by dispersed method'
def pick_initial_points(K):
    '  1.sampling'
    '->2.dispersed'

    copy=list(all_points)
    print("all_points:",all_points)
    first=random.choice(all_points)
    print("first:",first)
    init_clusters={}
    init_clusters[0]=[first[0],first[1],first[0],first[1],1]

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
 
        init_clusters[n]=[waitlist[0],waitlist[1],waitlist[0],waitlist[1],1]
        
    return init_clusters
        
'go through the whole dataset and assign each point to one cluster by distance'
def assigning_cluster():
    global all_clusters
    copy=list(all_points)
    for p in copy:

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


def reset_cluster():
    if tablelize:
        'next phase'
        return 0
    else:
        assigning_cluster()
    return 0

def output():
    return 0

