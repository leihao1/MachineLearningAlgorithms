''''
convert 'a::b::c::' data format to csv UI format (utility matrix)

'''
import sys
import csv

fipath=sys.argv[1]
fopath=sys.argv[2]

with open(fipath,'r')as fi:
    reader=csv.reader(fi)
    lines=list(reader)
lines=[i[0] for i in lines]
lines=[i.split('::') for i in lines]
user_profile={}

def build_profile(user,movie,rating):
    profile={}
    #print(lines)
    for i in lines:
        if i[user] not in profile:
            profile[i[user]]={}
            profile[i[user]][i[movie]]=i[rating]
        else:
            profile[i[user]][i[movie]]=i[rating]
    return profile 

user_profile=build_profile(0,1,2)
item_profile=build_profile(1,0,2)
rating_profile=build_profile(2,1,0)

title=[i for i in user_profile]

with open(fopath,'w',newline='')as fo:
    writer=csv.writer(fo)
    
    #row=[r'item\rating/user']
    #row+=title
    #writer.writerow(row)
    
    for i in item_profile:
        #row=[i]
        row=[]
        for t in title:
            if t in item_profile[i]:
                row.append(item_profile[i][t])
            else:
                row.append('')
        #print(row)
        writer.writerow(row)
    print('Finished.Please Check Your Output File')


'''
def lab2():
    lines=open_csv()
    lines=[i[0] for i in lines]
    lines=[i.split('::') for i in lines]
    #print(lines)
    userid=[int(i[0]) for i in lines]
    movieid=[int(i[1]) for i in lines]
    rating=[int(i[2]) for i in lines]
    rows=list(set(movieid))
    cols=list(set(userid))
    matrix=[]
    for r in range(len(rows)):
        matrix.append([])
        for c in range(len(cols)):
            matrix[r].append([])
            matrix[r][c]=None
    #print(matrix)
    print(len(matrix))
    print(len(matrix[0]))
    
    for r in movieid:
        for c in userid:
            for r in rating:
                matrix[r][c]=r
    
    for i in lines:
        matrix[int(i[1])][int(i[0])]=int(i[2])
    print(matrix)
    return matrix
'''
