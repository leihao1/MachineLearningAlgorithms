# Item-Item Collaborative Filtering tool
Simple tool to predict item rating will be given by specific users
with Collaborative Filtering algorithsm.

Function `sim()`
-
>calculate cosine similarity value between two vectors

* `>>> a=[1,2,3]`
* `>>> b=[3,2,1]`
* `>>> sim(a,b)`
* `0.7142857142857143`

Function `subtract()`
-
>subtract mean rating mi from each items(row)
>
* `>>> a=[1,None,3,None,None,5,None,None,5,None,4,None]`
* `>>> subtract(a)`
* `[-2.6, 0, -0.6000000000000001, 0, 0, 1.4, 0, 0, 1.4, 0, 0.3999999999999999, 0]`


