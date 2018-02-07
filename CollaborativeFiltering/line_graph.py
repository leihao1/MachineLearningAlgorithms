import matplotlib.pyplot as plt
'''
take coordinate list including tuples
eg:a=[(1,1),(4,5)(2,3)(5,8)]
'''
def show_line_graph(coordinate):
    x_list = []
    y_list = []
    for xy in coordinate:
        x_list.append(xy[0])
        y_list.append(xy[1])

    plt.figure('Line Graph')
    ax = plt.gca()

    ax.set_xlabel('Number Of Neighbors (N)')
    ax.set_ylabel('Root Mean Square Error (RMSE)')
    
    ax.plot(x_list, y_list, color='r', linewidth=1.5, alpha=0.6)
    
    plt.savefig('N-RMSE.png' ,bbox_inches='tight')
    plt.show()

