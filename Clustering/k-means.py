import random
import math
from math import sqrt
import sys
import csv
import matplotlib.pyplot as plt
import numpy as np


'================================deal with input file==============================='
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
    initial_points=[]
    for r in range(ROW):
        for c in range(COLUMN):
            if lines[r][c] != '':
                position=(r+1,c+1)
                initial_points.append(position)
                global back_up
                back_up[position]=int(lines[r][c])
    temp={}
    temp[0]=initial_points
    initial_points=temp
    return initial_points

'get data coordinate directly from file'
def get_coordinate():
    pass
'==================================================================================='



'=================================visualization====================================='
pid=0
xmax=0
xmin=1
ymax=0
ymin=1
'show scatterplot by matplotlib and numpy'
def visualizer(cluster):
    
    # Create data
    k = len(cluster)
    data=[]
    count=0
    global xmax,xmin,ymax,ymin    
    print('cluster:',cluster)
    for g in cluster:
        xy=cluster[g]
        #print('xy:',xy)
        x=[i[0] for i in xy]
        y=[i[1] for i in xy]
        print("x",x)
        print('y',y)
        #x,y=y,[max(x)-i+1 for i in x] #convert to csv format standar
        if len(x) >0 and len(y)>0:
            if max(x)>xmax:
                xmax=max(x)
            if min(x)<xmin:
                xmin=min(x)
            if max(y)>ymax:
                ymax=max(y)
            if min(y)<ymin:
                ymin=min(y)
        g=(np.array(x), np.array(y))
        data.append(g)
        count+=len(x)

    groups = ['cluster '+str(i) for i in cluster]
    colors = np.random.rand(k)
    #print('color: ',colors)
    # Create plot
    fig = plt.figure()
    #ax = fig.add_subplot(1, 1, 1, axisbg="1.0")

    for data,color,group in zip(data,colors,groups):
        x, y = data
        plt.scatter(x,y,alpha=1,label=group)
    
    plt.title('K-Means Clustering')
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
          fancybox=True, shadow=True, ncol=5)
    print("four: ",xmax,xmin,ymax,ymin)
    plt.xlim(xmin-1,xmax+1)
    plt.ylim(ymin-1,ymax+1)
    
    #ax.legend(bbox_to_anchor=(1.1, 1.05))
    #ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.05),
    #      ncol=3, fancybox=True, shadow=True)
    #plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    global pid
    pid+=1
    plt.savefig(str(pid)+'.png')
    #plt.show()
'==================================================================================='

#visualizer(initial_cluster)

'===============================k-means clustering library=========================='
'select best K'
'good_k={number:avg_cenroid_dis}'
def select_k():
    return 4


'pick K initial points as K clusters by dispersed method'
def pick_init_centroid(K,initial_points):
    '  1.sampling'
    '->2.dispersed'
    temp=[]
    for c in initial_points:
        temp += initial_points[c]
    initial_points =temp
    first=random.choice(initial_points)

    initial_centroids={}
    initial_centroids[0]=[first[0],first[1],0,0,0]

    picked=[first]
    initial_points.remove(first)

    for n in range(1,K):
        max_distance,waitlist=0,0
        for p in initial_points:
            distance=0
            for i in picked:
                distance+=math.hypot(p[0]-i[0],p[1]-i[1])
            if distance>max_distance:
                max_distance,waitlist=distance,p
        picked.append(waitlist)
        initial_points.remove(waitlist)
        initial_centroids[n]=[waitlist[0],waitlist[1],0,0,0]
       
    return initial_centroids
        

'go through the whole dataset and assign each point to one cluster by centroid distance'
def assigning_cluster(initial_points,all_centroid):
    cluster_members={}
    temp=[]
    for p in initial_points:
        temp+=initial_points[p]
    initial_points=temp

    for c in all_centroid:
        cluster_members[c]=[]

    for p in initial_points:
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
        #print(cluster_members)
        visualizer(cluster_members)
    '''
    print('After Assigning (centroid):')
    print(all_centroid)
    print('')
    print('After Assigning (members):')
    print(cluster_members)
    print('')
    '''
    final_centroid,stabilize=reset_cluster(all_centroid)
    return final_centroid,cluster_members,stabilize


'reset cluster centroid and repeat assigning untill stabilize'
def reset_cluster(cluster):
    stabilize=True
    for c in cluster:    
        x=cluster[c][0]
        y=cluster[c][1]
        sumx=cluster[c][2]
        sumy=cluster[c][3]
        N=cluster[c][4]
        if N!=0:
            if x!=sumx/N or y!=sumy/N:
                stabilize=False
                x=sumx/N
                y=sumy/N
                cluster[c][0]=x 
                cluster[c][1]=y
                cluster[c][2]=0
                cluster[c][3]=0
                cluster[c][4]=0
    return cluster,stabilize

'clustering by K-means '
def kmeans(initial_points,K=None):
    assert(K==None or (K>0 and type(K)==int)),"K must be a positive integer"
    assert(type(initial_points)==dict),"Input data type must be list"
    if K==None:
        K=select_k()

    cluster_history=[]
    
    visualizer(initial_points)

    'all_centroid={"cluster_name":[x,y,sumx,sumy,N]}'
    all_centroid=pick_init_centroid(K,initial_points)
    cluster_members={}
    for c in all_centroid:
        cluster_members[c]=[(all_centroid[c][0],all_centroid[c][1])]
    visualizer(cluster_members)

    '''
    print('')
    print('Initial Clusters:',all_centroid)
    print('')
    '''

    all_centroid,cluster_members,stabilize=assigning_cluster(initial_points,all_centroid)
    cluster_history.append(cluster_members)
    
    visualizer(cluster_members)
    while stabilize==False:
        all_centroid,cluster_members,stabilize=assigning_cluster(initial_points,all_centroid)
        cluster_history.append(cluster_members)  
        visualizer(cluster_members)
    
    print('Total Rounds: ',len(cluster_history))
    print('')
    '''
    print('Final Clusters:')
    print(all_centroid)   
    print('')
    print('Final Members:')
    print(cluster_members)
    print('')
    '''
    return all_centroid,cluster_members,cluster_history


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
'==================================================================================='

initial_cluster= find_from_cluster(lines)
centroid,demo,cluster_history=kmeans(initial_cluster)



'''
for h in cluster_history:
    visualizer(h)
''' 
#visualizer(demo)
