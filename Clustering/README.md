# K-Means Algorithm

#### Clustering input data by k-means algorithm:

##### STEP 1: Select K
* Select the most suitable K value by system using 'elbow' method
* Select specific by user
##### STEP 2: Pick initial K points(cluster centroid)
* Sampling
* Dispersed(we use this one)
##### STEP 3: Assigning every data points to K clusters by centroid distance
##### STEP 4: Reset the centroid for each clusters and do STEP 3 again until clusters are stable(centroids do not move)
##### STEP 5: Show clusters by visulization tool matplotlib
#
#### Library Dependency:
* [matplotlib](https://matplotlib.org/)
`import matplotlib as plt`
* [numpy](http://www.numpy.org/)
 `import numpy as np`
 * [scipy](https://www.scipy.org/)
 `from scipy.io import arff`
#
#### TEST FILES:
* [simple_cluster](https://github.com/leihao1/Mining-Massive-Datasets/blob/master/Clustering/simple_cluster.csv)
#
#### FUNCTIONS:
* select_k()
* pick_initial_points()
* assigning_cluster()
* reset_cluster()
* [kmeans()](#kmeansdataKNone)
* [visualizer()](#visualizercluster)

##### `kmeans(data,K=None)`
> -clustering by K-means

    $ python  -i k-means.py simple_cluster.csv
    >>> kmeans()
    Initial Clusters: {0: [5, 6, 0, 0, 0], 1: [18, 9, 0, 0, 0], 2: [1, 2, 0, 0, 0], 3: [18, 4, 0, 0, 0]}`
    
    Final Clusters:
    {0: [3.8333333333333335, 7.666666666666667, 46, 92, 12], 1: [15.909090909090908, 8.090909090909092, 175, 89, 11], 
    2: [3.727272727272727,2.090909090909091, 41, 23, 11], 3: [15.4, 3.4, 154, 34, 10]}

    Final Members:
    {0: [(1, 7), (1, 10), (2, 7), (2, 8), (3, 6), (3, 8), (4, 7), (5, 7), (5, 9), (6, 8), (7, 7), (7, 8)], 
    1: [(14, 9), (15, 7), (15, 8), (15, 9), (16, 6), (16, 8), (16, 9), (16, 10), (17, 7), (17, 8), (18, 8)], 
    2: [(2, 1), (2, 2), (2, 3), (3, 1), (3, 3), (4, 2), (4, 3), (5,1), (5, 2), (5, 3), (6, 2)], 
    3: [(13, 1), (14, 3), (14, 4), (15, 3), (15, 5), (16, 2), (16, 4), (17, 3), (17, 4), (17, 5)]}
    `
#####  `visualizer(cluster)`
> -cluster visualization
> * `>>>final_controids,final_members,history=kmeans(`[`simple_cluster`](https://github.com/leihao1/Mining-Massive-Datasets/blob/master/Clustering/datasets/simple_cluster.csv)`,4)`
> * `>>>visualizer(history)`
>
> ![initial](https://github.com/leihao1/Mining-Massive-Datasets/blob/master/Clustering/figures/simple_cluster.csv1.png)
> ![pick_k_points](https://github.com/leihao1/Mining-Massive-Datasets/blob/master/Clustering/figures/simple_cluster.csv2.png)
> ![round_1](https://github.com/leihao1/Mining-Massive-Datasets/blob/master/Clustering/figures/simple_cluster.csv3.png)
> ![round_2](https://github.com/leihao1/Mining-Massive-Datasets/blob/master/Clustering/figures/simple_cluster.csv4.png)


