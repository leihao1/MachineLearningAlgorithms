import file_reader as fr
import visualizer as vi
from math import *
import math,sys

'=========================2-D Hierarchical Clustering Library========================'
def bottom_up(init_points,number=1,cohesion=1):
    final=None
    return_dict=1
    if return_dict:
        k=len(init_points)
        temp=[[(i[0],i[1],i[0],i[1],1),[(i[0],i[1])]] for i in init_points]

        while k >number:
            temp=fast_merge(temp)
            k=len(temp)
            print(k)

        cluster_dicts={}
        for i in range(len(temp)):
            cluster_dicts[i]=temp[i][1]
        final=cluster_dicts
    else:
        'tree=[(centroidx,centroidy,sumx,sumy,leaves),[left tree],[right tree]]'
        cluster_trees=[[(i[0],i[1],i[0],i[1],1),[None],[None]] for i in init_points]
        k=len(cluster_trees)
        while k>number:
            cluster_trees=merge(cluster_trees)
            k=len(cluster_trees)
            print(k)
        final=cluster_trees
    
    return final


def fast_merge(temp):
    if len(temp)==1:
        print('There is only one cluster left ,can not merge anymore')
        return temp
    d0=temp[0]
    d1=temp[1]
    p0=d0[0]
    p1=d1[0]
    min_dis=math.hypot(p1[0]-p0[0],p1[1]-p0[1])

    for i in range(len(temp)-1):
        d3=temp[i]
        p3=d3[0]
        for j in range(i+1,len(temp)):
            d4=temp[j]
            p4=d4[0]
            temp_dis=math.hypot(p3[0]-p4[0],p3[1]-p4[1])
            if temp_dis<min_dis:
                min_dis=temp_dis
                d0=d3
                d1=d4
    p0=d0[0]
    p1=d1[0]
    sumx=p0[2]+p1[2]
    sumy=p0[3]+p1[3]
    N=p0[4]+p1[4]
    d0_member=d0[1]
    d1_member=d1[1]
    new_member=d0_member+d1_member
    new_point=[(sumx/N,sumy/N,sumx,sumy,N),new_member]

    temp.remove(d0)
    temp.remove(d1)
    temp.append(new_point)
    return temp


def merge(cluster_trees):
    if len(cluster_trees)==1:
        print('There is only one cluster left ,can not merge anymore')
        return cluster_trees
    tree0=cluster_trees[0]
    tree1=cluster_trees[1]
    min_dis=math.hypot(tree1[0][0]-tree0[0][0],tree1[0][1]-tree0[0][1])
    
    for i in range(len(cluster_trees)-1):
            tree=cluster_trees[i]
            node=tree[0]
            left=tree[1]
            right=tree[2]
            for j in range(i+1,len(cluster_trees)):
                next_tree=cluster_trees[j]
                next_node=next_tree[0]
                next_left=next_tree[1]
                next_right=next_tree[2]
                temp_dis=math.hypot(next_node[0]-node[0],next_node[1]-node[1])
                if temp_dis<min_dis:
                    min_dis=temp_dis
                    tree0=tree
                    tree1=next_tree         
    n0=tree0[0]
    n1=tree1[0]
    sumx=n0[2]+n1[2]
    sumy=n0[3]+n1[3]
    sumn=n0[4]+n1[4]

    new_node=(sumx/sumn,sumy/sumn,sumx,sumy,sumn)
    new_tree=[new_node,tree0,tree1]

    cluster_trees.remove(tree0)
    cluster_trees.remove(tree1)
    cluster_trees.append(new_tree)
    return cluster_trees


def top_down():
    pass
'===================================================================================='
test=[(0,0),(1,2),(2,1),(4,1),(5,0),(5,3)]
read=fr.open_file()

final=bottom_up(read,4)

vi.show_scatter(final)

