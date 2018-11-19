import random,math,sys,csv
from math import *
import file_reader as fr ,visualizer as vi

'===============================k-means clustering library=========================='
'select best K by elbow method'
def select_k(initial_cluster):
    diff_k={}
    initial_points=[]
    for c in initial_cluster:
        initial_points += initial_cluster[c]
    #n=len(initial_points)

    #print(diff_k)

    def enter():
        str=input("Please Enter K Value:")
        try:
            k=int(str)
        except:
            #print('K must be an integer!')
            print('Apply elbow method !')
            n=20
            for k in range(1,n+1):
                final_centroid,final_clusters,history=kmeans(initial_cluster,k)
                if len(final_centroid)!=len(final_clusters):
                    print('final centroid and final clusters inconsistent')
                    exit()
                sse=0
                for i in range(0,len(final_clusters)):
                    xmean,ymean=final_centroid[i][0],final_centroid[i][1]
                    for p in final_clusters[i]:
                        x,y=p[0],p[1]
                        sse+=(x-xmean)**2+(y-ymean)**2
                diff_k[k]=sse
            coordinate=[]
            for k in diff_k:
                coordinate.append((k,diff_k[k]))
            vi.show_line(coordinate)
            k=enter()
        if k<=0:
            print('K must be bigger than zero!')
            k=enter()
        return k
    return enter()


'pick K initial points as K clusters by dispersed method'
def pick_init_centroid(K,initial_points):
    assert(type(initial_points)==dict),"Input data type must be dict"
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
            distance=math.inf
            for i in picked:
                distance=min(distance,math.hypot(p[0]-i[0],p[1]-i[1]))
            if distance>max_distance:
                max_distance,waitlist=distance,p
        picked.append(waitlist)
        initial_points.remove(waitlist)
        initial_centroids[n]=[waitlist[0],waitlist[1],0,0,0]
    return initial_centroids
        

'assign each points in dataset to one closest cluster'
def assigning_cluster(initial_points,all_centroid):
    assert(type(initial_points)==dict),"Input data type must be dict"
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

        all_centroid[assign][2]+=p[0]
        all_centroid[assign][3]+=p[1]
        all_centroid[assign][4]+=1
        cluster_members[assign].append(p)
        #print(cluster_members)
        #visualizer(cluster_members)
    '''
    print('After Assigning(centroid):')
    print(all_centroid)
    print('')
    print('After Assigning(members):')
    print(cluster_members)
    print('')
    '''
    final_centroid,stabilize=reset_cluster(all_centroid)
    '''
    print('After Reset(centroid):')
    print(final_centroid)
    print('')
    print('After Reset(members):')
    print(cluster_members)
    print('')
    '''
    return final_centroid,cluster_members,stabilize

'reset cluster centroid and repeat assigning step untill stabilize'
def reset_cluster(cluster):
    assert(type(cluster)==dict),"Input data type must be dict"
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
    assert(K==None or (K>0 and type(K)==int)),"K should be a positive integer"
    assert(type(initial_points)==dict),"Input data type must be dict"
    assert(K==None or K<=len(initial_points[0])),"K should be less than exist points"
    if K==None:
        K=select_k(initial_points)

    history=[]
    history.append(initial_points)
    'all_centroid={"cluster_name":[x,y,sumx,sumy,N]}'
    all_centroid=pick_init_centroid(K,initial_points)
    cluster_members={}
    for c in all_centroid:
        cluster_members[c]=[(all_centroid[c][0],all_centroid[c][1])]
    #visualizer(cluster_members)
    history.append(cluster_members)
    '''
    print('')
    print('Initial Clusters:',all_centroid)
    print('')
    '''
    stabilize=False
    Round=0
    #visualizer(cluster_members)
    while stabilize==False:
        all_centroid,cluster_members,stabilize=assigning_cluster(initial_points,all_centroid)
        if stabilize==False:
            history.append(cluster_members)          
        Round+=1
        print('Round:',Round)
        #visualizer(cluster_members)
    '''
    print('Final Clusters:')
    print(all_centroid)   
    print('')
    print('Final Members:')
    print(cluster_members)
    print('')
    '''
    return all_centroid,cluster_members,history

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

initial_points=fr.open_file()

initial_cluster={}
initial_cluster[0]=initial_points

vi.show_scatter(initial_cluster)

final_centroid,final_cluster,history=kmeans(initial_cluster)
'''
for h in history:
    vi.show_scatter(h)
'''
vi.show_scatter(history[1])
vi.show_scatter(final_cluster)


