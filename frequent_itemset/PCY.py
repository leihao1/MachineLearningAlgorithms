import sys,csv,time
from math import *

'============================================'
def open_file():
    with open('retail.dat','r') as fi:
        reader=csv.reader(fi)
        lines=list(reader)
    temp=[i[0].split(' ') for i in lines]
    rows=[i[:-1] for i in temp]
    return rows
'============================================'


'============================================'
def pass1(baskets,s,N):
    items={}
    hasht={}
    '''
    for b in baskets:
      for i in range(len(b)):
        if b[i] not in items:
          items[b[i]]=1
        else:
          items[b[i]]+=1
          
        for j in range(i+1,len(b)):
          pair=(b[i],b[j])
          bucket=hash(pair)%N
          #bucket=int(b[i]+b[j])%N
          if bucket not in hasht:
            hasht[bucket]=1
          elif hasht[bucket]<s:
            hasht[bucket]+=1
    '''
    for b in baskets:
      for i in b:
        if i not in items:
          items[i]=1
        else:
          items[i]+=1
          
    for b in baskets:
      for i in range(len(b)-1):
        for j in range(i+1,len(b)):
          pair=(b[i],b[j])
          bucket=hash(pair)%N
          #bucket=int(b[i]+b[j])%N
          if bucket in hasht:
            hasht[bucket]+=1
          else:
            hasht[bucket]=1
    
    print('C1:',len(items))
    frequent_items=[(i,) for i in items if items[i] >= s]
    print('L1:',len(frequent_items))
    return frequent_items,hasht

  
#ffc=former frequent candidates
#s=support
#K=the size of frequent items that will return 
def passk(K,ffc,baskets,s,vector,N):
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
    
    if K==2:
      for i in range(len(ffc)-1):
        for j in range(i+1,len(ffc)):
          pair=ffc[i]+ffc[j]
          h=hash(pair)%N
          if h in vector:
            candidates[pair]=0
    else:
      for i in range(len(ffc)-1):
        for j in range(i+1,len(ffc)):
            merged=tuple(set(ffc[i]+ffc[j]))
            if len(merged)==K:
                if all_in_former(merged,ffc):
                  if not_duplicate(merged,candidates):
                    candidates[merged]=0
                               
    check=[]
    t=list(candidates)
    for i in range(len(t)-1):
        for j in range(i+1,len(t)):
            if set(t[i]) == set(t[j]):
                check.append(t[j])
    #print('Duplicate:',len(check))
    assert(len(check)==0),'Exist Duplicate Candidate Elements'
    
    print('C'+str(K)+':',len(candidates))
    
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
    print('L'+str(K)+':',len(freq_candidates))
    return freq_candidates
'============================================'


'==============outer interface====================='
def pcy(K,sup_rate=0.01,confidence=0.5,N=2**32):
  start = time.clock()
  
  baskets=open_file()
  del baskets[0]
  print('Data:',len(baskets))
  
  support=sup_rate*len(baskets)
  print('Support:',support)
  singleton,hasht=pass1(baskets,support,N)
  
  for i in hasht:
    if hasht[i]>=support:
      hasht[i]=1
    else:
      hasht[i]=0
  vector=[i for i in hasht if hasht[i]==1]
  
  freq_items=singleton
  for i in range(2,K+1):
    freq_items=passk(i,freq_items,baskets,support,vector,N)
  
  print ('Run Time:',time.clock()-start)
  return freq_items
'============================================'
