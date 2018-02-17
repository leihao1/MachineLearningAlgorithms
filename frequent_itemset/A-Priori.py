import sys,csv,time

'=====================================open file======================================'
'open data file from command line'
def open_file():
    with open(sys.argv[1],'r') as fi:
        reader=csv.reader(fi)
        lines=list(reader)
    temp=[i[0].split(' ') for i in lines]
    rows=[i[:-1] for i in temp]
    return rows
'===================================================================================='


'================================A-priori Three Passes==============================='
def pass1(baskets,s):
    items={}
    for i in baskets:
        for j in i:
            if j not in items:
                items[j]=1
            else:
                items[j]+=1
    frequent_items=[(i,) for i in items if items[i] >= s]
    return frequent_items


def pass2(baskets,c1,s):
    item_pairs={}
    for i in range(len(c1)):
        for j in range(i+1,len(c1)):
            item_pairs[c1[i]+c1[j]]=0
    for r in baskets:
        for p in item_pairs:
            if p[0] in r and p[1] in r:
                item_pairs[p]+=1
    doubleton=[p for p in item_pairs if item_pairs[p] >= s]
    return doubleton


def pass3(baskets,c2,s):
    
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
    
    for r in baskets:
        for p in tripleton:
            if p[0] in r and p[1] in r and p[2] in r:
                tripleton[p]+=1
    L3=[p for p in tripleton if tripleton[p] >= s]
    return L3
'===================================================================================='


'=========================A-priori General Solution (K passes)======================='
#ffc=former frequent candidates
#s=support
#K=the size of frequent items that will return 
def passk(K,ffc,baskets,s):
    assert(K>1),'Can Not Use Passk() At First Pass'
    def all_in_former(merged,ffc):
        sub={}
        merged=list(merged)
        for i in merged:
          temp=[i for i in merged]
          temp.remove(i)
          sub[tuple(temp)]=False
          
        for c in ffc:
          for s in sub:
            if set(c)==set(s):
              sub[s]=True
              
        all_in=True
        for s in sub:
          if sub[s]==False:
            all_in=False
            
        return all_in
    
    def not_duplicate(merged,candidates):
        not_in=True
        for t in candidates:
            if set(t)==set(merged):
                not_in=False
        return not_in
    
    candidates={}
    
    for i in range(len(ffc)-1):
        for j in range(i+1,len(ffc)):
            
            merged=tuple(set(ffc[i]+ffc[j]))
            
            if K==2:
              candidates[merged]=0
            else:
              if len(merged)==K:
                if all_in_former(merged,ffc):
                  if not_duplicate(merged,candidates):
                    candidates[merged]=0
                               
    temp=[]
    t=list(candidates)
    for i in range(len(t)-1):
        for j in range(i+1,len(t)):
            if set(t[i]) == set(t[j]):
                temp.append(t[j])
    #print('Duplicate:',len(temp))
    assert(len(temp)==0),'Exist Duplicate Candidate Elements'
    
    if K==2:
      for b in baskets:
        for c in candidates:
          if c[1] in b and c[0] in b:
            candidates[c]+=1
    else:
      for b in baskets:
        for c in candidates:
          all_in_basket=True
          for i in c:
            if i not in b:
              all_in_basket=False
              break
          if all_in_basket:
            candidates[c]+=1
        
    freq_candidates=[i for i in candidates if candidates[i]>=s]
    return freq_candidates
'===================================================================================='


'================================A-priori Algorithm=================================='
'K: The biggest size of frequent items that we want to find'
def apriori(K,support_rate=0.01,confidence=0.5,header=True):
    
    start = time.clock()

    baskets=open_file()
    if header:
        del baskets[0]
    support=support_rate*len(baskets)
    
    singleton=pass1(baskets,support)
    
    freq_items=singleton
    for i in range(2,K+1):
        freq_items=passk(i,freq_items,baskets,support)


    #doubleton=pass2(baskets,singleton,support)
    #tripleton=pass3(baskets,doubleton,support)

    print(len(freq_items))
    #print(len(doubleton))
    #print(len(tripleton))

    end = time.clock()
    print ('Run Time:',end-start)
    
    return freq_items
'===================================================================================='
