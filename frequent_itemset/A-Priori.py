import sys,csv 


def open_file():
    with open(sys.argv[1],'r') as fi:
        reader=csv.reader(fi)
        lines=list(reader)
    temp=[i[0].split(' ') for i in lines]
    rows=[i[:-1] for i in temp]
    del rows[0]
    return rows


def pass1(rows,s):
    items={}
    for i in rows:
        for j in i:
            if j not in items:
                items[j]=1
            else:
                items[j]+=1
    frequent_items=[i for i in items if items[i] >= support]
    return frequent_items


def pass2(rows,c1,s):
    item_pairs={}
    for i in range(len(c1)):
        for j in range(i+1,len(c1)):
            item_pairs[(c1[i],c1[j])]=0
    for r in rows:
        for p in item_pairs:
            if p[0] in r and p[1] in r:
                item_pairs[p]+=1
    doubleton=[p for p in item_pairs if item_pairs[p] >= support]
    return doubleton


def pass3(rows,c2,s):
    
    def all_in(three,c2):
        p1=(three[0],three[1])
        p2=(three[0],three[2])
        p3=(three[1],three[2])
        p1_in=False
        p2_in=False
        p3_in=False
        for c in c2:
            if set(p1)==set(c):
                p1_in=True
            if set(p2)==set(c):
                p2_in=True
            if set(p3)==set(c):
                p3_in=True
        return p1_in and p2_in and p3_in
    
    def not_duplicate(three,tripleton):
        not_in=True
        for t in tripleton:
            if set(t)==set(three):
                not_in=False
        return not_in
    
    tripleton={}
    
    for i in range(len(c2)-1):
        for j in range(i+1,len(c2)):
            
            three=tuple(set(c2[i]+c2[j]))
            
            if len(three)==3 :
                if all_in(three,c2):
                    if not_duplicate(three,tripleton):
                        tripleton[three]=0
                        
            elif len(three)==4:
                t1=(three[1],three[2],three[3])
                t2=(three[0],three[2],three[3])
                t3=(three[0],three[1],three[3])
                t4=(three[0],three[1],three[2])
                
                four=[t1,t2,t3,t4]
                for f in four:
                    if not_duplicate(f,tripleton):
                        if all_in(f,c2):
                            tripleton[f]=0   

    print(len(tripleton))

    temp=[]
    t=list(tripleton)
    for i in range(len(t)-1):
        for j in range(i+1,len(t)):
            if set(t[i]) == set(t[j]):
                temp.append(t[j])
    assert(len(temp)==0),'Exist Duplicate Tripleton Elements'
    for i in temp:
        del tripleton[i]
    
    for r in rows:
        for p in tripleton:
            if p[0] in r and p[1] in r and p[2] in r:
                tripleton[p]+=1
    L3=[p for p in tripleton if tripleton[p] >= s]
    return L3
    

import time,winsound
start = time.clock()

rows=open_file()

baskets=len(rows)
support=round(0.01*baskets)
confidence=0.5

singleton=pass1(rows,support)
doubleton=pass2(rows,singleton,support)
t1=pass3(rows,doubleton,support)

    

print(len(singleton))
print(len(doubleton))
print(len(t1))


end = time.clock()
print ('Run Time:',end-start)

winsound.Beep(400, 1000)

duration = 1000  # millisecond
freq = 440  # Hz
