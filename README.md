# Redmart 1,000,000th Customer Prize Challenge

This is my solution for the [challenge](http://geeks.redmart.com/2015/10/26/1000000th-customer-prize-another-programming-challenge/). The challenge is largely the same as a classic 0-1 knapsack problem, but with some minor rule changes and a large dataset to play with, it nonetheless made for an interesting and fun problem!

## Problem
- 1 of each item
- Combined volume < tote capacity (45 * 30 * 25 = 47250)
- Item must fit individually (Dimensions are such that it can fit into the tote, e.g. 45 * 45 * 1 wouldn't fit)
- **Maximize** value of combined products
- **Minimize** weight on draws

## Solution
Using Dynamic Programming, I was able to come to a solution with `O(nV)`  time complexity and pseudo `O(n)` space complexity:

`dp[v] = [val, items, w]`
`dp[v]` is the outstanding value in the tote having chosen 0 / 1 for the item (taking or not taking), with v remaining capacity and w combined weight. It also stores a list of the IDs of the products it contains.

`items = [(ID, value, volume, weight)]`
`items` stores the list of items parsed from the `.csv` file, after eliminating those that do not fit into the tote (compared dimension by dimension)

#### Base Case:
`dp[V] = [0, [], 0] `

#### Recursive Case:
`dp[v] = max(dp[v], dp[v'] + item[1])` where `v = v' - item[2]`

## Conclusion
Dealing with a humongous data set with 47250 * ~18000 = ~85 **million** loops was an interesting challenge. I had to cut as much overhead as possible to keep space complexity to a bare minimum in order to speed up the algorithm. Originally I experimented with using a wrapper object for each `dp` node in this [branch](https://github.com/zweicoder/1m-customer-prize-challenge/tree/node-wrapper) for verbosity but it increased the time taken by ~1.5x, so I switched back to using lists. 

Sadly the best timing I got after all the optimization was **8m1.649s** :cry: