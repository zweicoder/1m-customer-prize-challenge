# Product of all elements in a list
def multiply_list(lst):
    return reduce(lambda x, y: x * y, lst)


'''
Finds the item combination with the highest value and smallest weight, constrained
by total volume <= V, via dynamic programming.

Volume: 50 - Value: 41298 Items: [1370, 4887, 5084, 6532, 8699, 9972, 10496, 10981, 12856, 12979, 14301, 14448, 17788, 17896, 26950, 27376, 31288, 33638, 34414, 35280, 36175, 36769, 39987]

450166
'''


def solve(items, capacity):
    dp = {capacity: [0, [], 0]}
    # Base Case

    # Recursive Case
    for i in range(len(items)):
        item = items[i]
        for v_old in dp.keys():
            # Update new volume if we choose to take
            v_new = v_old - item[2]
            if v_new >= 0:
                prev_node = dp[v_old]
                node = [prev_node[0] + item[1], prev_node[1] + [item[0]], prev_node[-1] + item[-1]]
                if v_new not in dp:
                    # If there isn't already a node there, directly set a node
                    dp[v_new] = node
                else:
                    # Else we compare the current Node with the new Node and
                    # choose by highest value, lowest weight
                    current_node = dp[v_new]
                    if current_node[0] <= node[0]:
                        dp[v_new] = node
                    elif current_node[0] == node[0]:
                        if node[-1] < current_node[-1]:
                            dp[v_new] = node

    best_node = max(dp.values(), key=(lambda v: v[0]))

    print('Items: %s = %s' % (sorted(best_node[1]), sum(best_node[1])))
    return best_node[1]


tote_dims = [30, 35, 45]  # Dimensions of tote, manually sorted in ascending order
V = multiply_list(tote_dims)  # Total volume of tote
products = []  # [(ID, price/value, volume, weight)]

with open('small.csv', 'rb') as f:
    for line in f:
        data = [int(e) for e in line.strip().split(',')]
        # Compare dimension of items with dimension of box to see if they can fit. Eliminates 2067 items
        item_dims = [dim for dim, max_dim in zip(sorted(data[2:5]), tote_dims) if dim <= max_dim]
        if len(item_dims) == 3:
            products.append((data[0], data[1], multiply_list(data[2:5]), data[5]))

    solve(products, V)
