import random,math,sys,csv,matplotlib.pyplot as plt, numpy as np, pandas as pd
from math import *
from scipy.io import arff


'================================deal with input file==============================='
fipath=sys.argv[1]
back_up={}

def open_file():
    try:
        return open_csv()
    except :
        return open_arff()

def open_csv():
    with open(fipath,'r') as fi:
        reader=csv.reader(fi)
        lines=list(reader)
    ROW=len(lines)
    COLUMN=len(lines[0])

    'get data coordinate directly from file'
    def get_coordinate(files):
        is_cluster_file=False
        initial_points=[]
        for row in files:
            x=row[0]
            y=row[1]
            if x=='' or y=='':
                is_cluster_file=True
                break
            initial_points.append((float(x),float(y)))
        if is_cluster_file:
            initial_points=find_from_cluster(files)
        return initial_points

    'Find all data coordinate from exist cluster in the file'
    def find_from_cluster(files):
        initial_points=[]
        for r in range(ROW):
            for c in range(COLUMN):
                if files[r][c] != '':
                    position=(r+1,c+1)
                    initial_points.append(position)
                    global back_up
                    back_up[position]=int(files[r][c])
        return initial_points

    return get_coordinate(lines)
    
def open_arff():
    data = arff.loadarff(fipath)
    initial_points=[i for i in data[0]]
    return initial_points
'==================================================================================='



'=================================visualization====================================='
pid=0
xmax=0
xmin=0
ymax=0
ymin=0
count=30
def visualizer(cluster):
    
    # Create data
    k = len(cluster)
    data=[]
    global xmax,xmin,ymax,ymin,count,pid    

    for g in cluster:
        xy=cluster[g]
        x=[i[0] for i in xy]
        y=[i[1] for i in xy]
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
        if pid ==0:
            count+=len(x)

   
    groups = ['cluster'+str(i)+":["+str(len(cluster[i]))+"]" for i in cluster]
    colors = np.random.rand(k)
    
    # Create plot
    fig = plt.figure(figsize=(log(count,2),log(count,2)))
    #ax = fig.add_subplot(1, 1, 1, axisbg="1.0")

    for data,color,group in zip(data,colors,groups):
        x, y = data
        plt.scatter(x,y,alpha=1,edgecolors='none',s=10*(5-log(count,8)),label=group)
    
    plt.title('K-Means Clustering')

    #plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),fancybox=True, shadow=True, ncol=5)
    plt.legend(bbox_to_anchor=(1, 1))
    #plt.legend(loc='upper center', bbox_to_anchor=(1.05, 1.05),ncol=3, fancybox=True, shadow=True)
    #plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    
    plt.xlim(1.1*xmin,1.1*xmax)
    plt.ylim(1.1*ymin,1.1*ymax)
    #fig.tight_layout(pad=10)

    pid+=1
    datapath="./datasets/"
    filename=fipath.replace(datapath,'')
    plt.savefig('./figures/'+filename+str(pid)+'.png' ,bbox_inches='tight')
    #plt.show()
'==================================================================================='



'===============================k-means clustering library=========================='
'select best K'
'good_k={number:avg_cenroid_dis}'
def select_k():
    return 4


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
            distance=0
            for i in picked:
                distance+=math.hypot(p[0]-i[0],p[1]-i[1])
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
    print('After Assigning (centroid):')
    print(all_centroid)
    print('')
    print('After Assigning (members):')
    print(cluster_members)
    print('')
    '''
    final_centroid,stabilize=reset_cluster(all_centroid)
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
        K=select_k()

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
        print(Round)
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

initial_points= open_file()

initial_cluster={}
initial_cluster[0]=initial_points

#visualizer(initial_cluster)

final_centroid,final_cluster,history=kmeans(initial_cluster,4)

for h in history:
    visualizer(h)


