import file_reader as fr
import visualizer as vi
from math import *
import math,sys,random

'=========================2-D Hierarchical Clustering Library========================'
def bottom_up(init_points,number=1,cohesion=1):
    final=None
    k=len(init_points)
    'cluster=[(centroidx,centroidy,sumx,sumy,N),[(x1,y1),(x2,y2)...]]'
    temp=[[(i[0],i[1],i[0],i[1],1),[(i[0],i[1])]] for i in init_points]

    while k >number:
        temp=merge_by_close_pair(temp)
        k=len(temp)
        print('cluster numbers:',k)
    
    final=temp
    
    return final


'meger two cluster if they have a close pair of points'
def merge_by_close_pair(clusters):
    if len(clusters)==1:
        print('There is only one cluster left ,can not merge anymore')
        return clusters

    c0=None
    c1=None
    min_dis=math.inf

    for i in range(len(clusters)-1):
        c3=clusters[i]
        p3=c3[0]
        m3=c3[1]
        #print('m3:',m3)
        for j in range(i+1,len(clusters)):
            c4=clusters[j]
            p4=c4[0]
            m4=c4[1]
         #   print('m4:',m4)
            min_pair=math.inf
            for ipoints in m3:
                for jpoints in m4:
                    temp=math.hypot(ipoints[0]-jpoints[0],ipoints[1]-jpoints[1])
                    if temp<min_pair:
                        min_pair=temp
                        #print('ipoints:',ipoints)
                        #print('jpoints:',jpoints)
            #print('min_pair:',min_pair)
            if min_pair<min_dis:
           #     print('min_pair:',min_pair)
                min_dis=min_pair
                c0=c3
                c1=c4
    
    #print("c0:",c0[0])
    #print('c1:',c1[0])
    #print('min_dis:',min_dis)
    p0=c0[0]
    p1=c1[0]
    sumx=p0[2]+p1[2]
    sumy=p0[3]+p1[3]
    N=p0[4]+p1[4]
    d0_member=c0[1]
    d1_member=c1[1]
    new_member=d0_member+d1_member
    new_cluster=[(sumx/N,sumy/N,sumx,sumy,N),new_member]

    clusters.remove(c0)
    clusters.remove(c1)
    clusters.append(new_cluster)
    return clusters
'''======================================================'''

def sample(initial_points,points=500):
    sample_points=[initial_points[i] for i in sorted(random.sample(range(len(initial_points)),min(points,len(initial_points))))]
    return sample_points

def select_repre_points(sample_cluster,R=0.1):
    #select 10 %
    new_cluster=[]
    for c in sample_cluster:
        members=c[1]
        picked=[]
        picked.append(random.choice(members))
        members.remove(picked[0])
        K=R*len(members)

        while len(picked)<K:
            max_dis=0
            waitlist=None
            for m in members:
                local_min=math.inf
                for p in picked:
                    local_min=min(local_min,math.hypot(p[0]-m[0],p[1]-m[1]))
                if local_min>max_dis:
                    max_dis=local_min
                    waitlist=m
            picked.append(waitlist)
            members.remove(waitlist)
        temp=[c[0],picked]
        new_cluster.append(temp)
    assert(len(new_cluster)==len(sample_cluster)),"diff length between new_cluster and sample_cluster"
    return new_cluster

def move_to_centroid(repre_cluster,r=0.1):
    new_cluster=[]
    for c in repre_cluster:
        x0=c[0][0]
        y0=c[0][1]
        merbers=c[1]
        new_members=[]
        for m in merbers:
            x1=m[0]
            y1=m[1]
            k=(y1-y0)/(x1-x0)
            b=y1-k*x1
            length=math.sqrt((y1-y0)**2+(x1-x0)**2)
            A=k**2+1
            B=2*k*b-2*y0*k-2*x0
            C=b**2+y0**2-2*y0*b+x0**2-((1-r)*length)**2
            D=B**2-4*A*C
            solx1=(-B-math.sqrt(D))/(2*A)
            solx2=(-B+math.sqrt(D))/(2*A)
            soly1=k*solx1+b
            soly2=k*solx2+b
            topx=max(x0,x1)
            topy=max(y0,y1)
            botx=min(x0,x1)
            boty=min(y0,y1)
            if (solx1<topx and solx1>botx and soly1<topy and soly1>boty):
                new_cor=(solx1,soly1)
                new_members.append(new_cor)
            elif(solx2<topx and solx2>botx and soly2<topy and soly2>boty):
                new_cor=(solx2,soly2)
                new_members.append(new_cor)
            else:
                print("NO solution!!")
                print('x0,x1,solx1,solx2',x0,x1,solx1,solx2)
                print('y0,y1,soly1,soly2',y0,y1,soly1,soly2)
        temp=[c[0],new_members]
        new_cluster.append(temp)
    return new_cluster

def assign_points(initial_points,new_cluster):
    final_cluster=[ [n[0],[]] for n in new_cluster]
    for p in initial_points:
        min_dis=math.inf
        assign_to=None
        for i in range(len(new_cluster)):
            c=new_cluster[i]
            repre_points=c[1]
            min_local=math.inf
            for r in repre_points:
                min_local=min(min_local,math.hypot(r[0]-p[0],r[1]-p[1]))
            if min_local<min_dis:
                min_dis=min_local
                assign_to=i
        final_cluster[assign_to][1].append(p)
        #print("remining points:",len(initial_points)-total)

    total_points=0
    for f in final_cluster:
        total_points+=len(f[1])
    assert(total_points==len(initial_points)),"diff length between final cluster and initial points!"
    
    return final_cluster

    
initial_points=fr.open_file()

initial_cluster={}
initial_cluster[0]=initial_points
vi.show_scatter(initial_cluster)


sample_points=sample(initial_points)

small_cluster={}
small_cluster[0]=sample_points
vi.show_scatter(small_cluster)


k=int(sys.argv[2])
sample_cluster=bottom_up(sample_points,k)

cluster_dicts={}
for i in range(len(sample_cluster)):
    cluster_dicts[i]=sample_cluster[i][1]
vi.show_scatter(cluster_dicts)


repre_cluster=select_repre_points(sample_cluster)

repre_dicts={}
for i in range(len(repre_cluster)):
    repre_dicts[i]=repre_cluster[i][1]
vi.show_scatter(repre_dicts)


new_cluster=move_to_centroid(repre_cluster)

new_dicts={}
for i in range(len(new_cluster)):
    new_dicts[i]=new_cluster[i][1]
vi.show_scatter(new_dicts)


whole_cluster=assign_points(initial_points,new_cluster)

whole_dicts={}
for i in range(len(whole_cluster)):
    whole_dicts[i]=whole_cluster[i][1]
vi.show_scatter(whole_dicts)

