import matplotlib.pyplot as plt,numpy as np
from math import *
import sys
'=================================visualization====================================='
pid=0
xmax=0
xmin=0
ymax=0
ymin=0
count=30
def show_scatter(cluster):
    assert(type(cluster)==dict),'show_scatter() input must be a dictionary'
    # Create data
    k = len(cluster)
    data=[]
    global xmax,xmin,ymax,ymin,count,pid    

    for g in cluster:
        xy=cluster[g]
        x=[i[0] for i in xy]
        y=[i[1] for i in xy]
        
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
    
    title=sys.argv[0].replace(".py",'')
    plt.title(title+' Clustering (k='+str(k)+')')

    #plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),fancybox=True, shadow=True, ncol=5)
    plt.legend(bbox_to_anchor=(1, 1))
    #plt.legend(loc='upper center', bbox_to_anchor=(1.05, 1.05),ncol=3, fancybox=True, shadow=True)
    #plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    
    plt.xlim(xmin-1,1+xmax)
    plt.ylim(ymin-1,1+ymax)
    #fig.tight_layout(pad=10)

    pid+=1
    datapath="./datasets/"
    filename=sys.argv[1]
    try:
        filename=filename.replace(datapath,'')
    except:
        pass
    try:
        filename=filename.replace(".csv",'')
    except:
        pass
    try:
        filename=filename.replace(".arff",'')
    except:
        pass
    codename=sys.argv[0].replace(".py",'')
    folderpath='./figures/'
    plt.savefig(folderpath+codename+'-'+filename+'-'+str(pid)+'.png' ,bbox_inches='tight')
    #plt.show()


'take a list of coordinates,e.g [(1,1)(3,3)(2,2)(4,4)]'
def show_line(coordinate):
    assert(type(coordinate)==list),'show_line() input must be a list'
    x_list = []
    y_list = []
    for xy in coordinate:
        x_list.append(xy[0])
        y_list.append(xy[1])

    plt.figure('Elbow Method')
    ax = plt.gca()

    ax.set_xlabel('Number of clusters(K)')
    ax.set_ylabel('Sum of squared errors')
    
    ax.plot(x_list, y_list, color='r', linewidth=1.5, alpha=0.6)
    
    plt.show()
'==================================================================================='

