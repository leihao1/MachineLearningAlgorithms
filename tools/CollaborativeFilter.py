from math import sqrt

'calculate cosine similarity value between two vectors'
def sim(v1,v2):
    if v1==v2:
        return 1.00
    if len(v1)!=len(v2):
        print('Error')
    else:
        up,a,b=0,0,0
        for i in range(0,len(v1)):
            up+=v1[i]*v2[i]
            a+=v1[i]*v1[i]
            b+=v2[i]*v2[i]
        down=sqrt(a)*sqrt(b)
        return up/down
