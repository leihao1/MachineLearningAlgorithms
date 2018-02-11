import sys,csv 
from scipy.io import arff
'================================open files (csv,arff)==============================='
try:
    fipath=sys.argv[1]
except:
    print('No Input File Was Given, Please Try Again.')
    exit()
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
                    back_up[position]=files[r][c]
        x=[p[0] for p in initial_points]
        y=[p[1] for p in initial_points]
        x,y=y,[max(x)-i+1 for i in x] #convert to UI coordinates 
        for i in range(len(x)):
            initial_points[i]=(x[i],y[i])
        return initial_points

    return get_coordinate(lines)
    
def open_arff():
    data = arff.loadarff(fipath)
    initial_points=[i for i in data[0]]
    return initial_points
'==================================================================================='

