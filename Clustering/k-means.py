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
K=0
all_points=[]

def find_all_points():
    for r in range(ROW):
        for c in range(COLUMN):
            if lines[r][c] != '':
                global all_points
                global back_up
                position=(r+1,c+1)
                all_points.append(position)
                back_up[position]=int(lines[r][c])

def choose_K():
    return 0

def a():
    find_all_points()
    return pick_initial_points(4)

def pick_initial_points(K):
    '1.sampling'
    '2.dispersed'
    copy=list(all_points)
    picked=[random.choice(all_points)]
    print(picked)
    copy.remove(picked[0])
    
    for n in range(K-1):
        max_distance,waitlist=0,0
        for p in copy:
            distance=0
            for i in picked:
                distance+=math.hypot(p[0]-i[0],p[1]-i[1])
            if distance>max_distance:
                max_distance,waitlist=distance,p
        picked.append(waitlist)
        print(waitlist)
        copy.remove(waitlist)

    return picked 
        

    
                
        
    return 0

def classify():
    return 0

def reset_cluster():
    if table:
        'next phase'
        return 0
    else:
        classify()
    return 0

def output():
    return 0
