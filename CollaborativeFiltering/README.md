## Item-Item Collaborative Filtering tool ([basic version](https://github.com/leihao1/soen691/releases/tag/basic))
Simple tool to predict item rating will be given by specific users with Collaborative Filtering algorithsm.

#### Test Files:
* [fi.csv](https://github.com/leihao1/soen691/blob/master/CollaborativeFiltering/fi.csv)
* [target.png](https://github.com/leihao1/soen691/blob/master/CollaborativeFiltering/target.png)
* [similarity.png](https://github.com/leihao1/soen691/blob/master/CollaborativeFiltering/similarity.png)
* [result.png](https://github.com/leihao1/soen691/blob/master/CollaborativeFiltering/result.png)

#### Function `sim()`
>calculate cosine similarity value between two vectors
>
>* `>>> a=[1,2,3]`
>* `>>> b=[3,2,1]`
>* `>>> sim(a,b)`
>* `0.7142857142857143`

#### Function `subtract()`

>subtract mean rating mi from each items(row)
>
>* `>>> a=[1,None,3,None,None,5,None,None,5,None,4,None]`
>* `>>> subtract(a)`
>* `[-2.6, 0, -0.6000000000000001, 0, 0, 1.4, 0, 0, 1.4, 0, 0.3999999999999999, 0]`

#### Function `initialize()`

>Initialize input file : 
>* Fill empty data with None to make column correct.
>* Convert strings to integers in each row to calculate similarity later.
>* Return a item*user integer matrix.

#### Function `sim_between_rows()`

>calculate all similarity between items(rows) by comparing with the given item(row)
>
>* `>>> sim_between_rows(initialize(lines),1)`
>* `{2: -0.17854212213729673, 3: 0.41403933560541256, 4: -0.10245014273309601, 5: -0.3
>0895719032666236, 6: 0.5870395085642741}`

#### Function `get_neighbor()`

>choose N most similar neighbors by the given number N
>
>* `>>> get_neighbor(sim_between_rows(initialize(lines),1),2)`
>* `[[6, 0.5870395085642741], [3, 0.41403933560541256]]`

#### Function `predict()`

>Predict rating value at position (row,col) with N neighbors.
>
>Default file has no header.
>
>* `>>> predict(1,5,2)`
>* `2.586406866934817`

## Global baseline + Collaborative Filtering algorithms ([baseline version](https://github.com/leihao1/soen691/releases/tag/baseline))
CF combine with global baseline algorithms to solve cold start problem of CF.
System can predict one item's rating now by using similar items even some of them did not rated by that user.

#### Test Files:
* [sample_movie_ratings.csv](https://github.com/leihao1/soen691/blob/master/CollaborativeFiltering/sample_movie_ratings.csv)

#### Function `basic_predict()`
>same as `predict()` function in basic version 

#### Function `baseline_predict()`
>predict item's rating by global baseline even some neighbors did not rated by that user
>* `>>> basic_predict(20,29,5)`
>* `Error: Empty value in neighbor's filed. row: 13 coloumn: 29`
>* `Error: Empty value in neighbor's filed. row: 16 coloumn: 29`
>* `>>> baseline_predict(20,29,5)`
>* `2.603113815971248`

## Evaluating Predictions




