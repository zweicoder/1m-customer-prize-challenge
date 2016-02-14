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
    # Base Case
    dp = {capacity: (0, (), 0)}

    get_keys = dp.keys
    # Recursive Case
    for i in range(len(items)):
        item_id, item_val, item_volume, item_weight = items[i]
        for v_old in get_keys():
            # Update new volume if we choose to take
            v_new = v_old - item_volume
            if v_new >= 0:
                val, baggage, weight = dp[v_old]
                node = (val + item_val, baggage + (item_id,), weight + item_weight)
                if v_new not in dp:
                    # If there isn't already a node there, directly set a node
                    dp[v_new] = node
                else:
                    # Else we compare the current Node with the new Node and
                    # choose by highest value, lowest weight
                    current_val, b, current_weight = dp[v_new]
                    if current_val < node[0] or (current_val == node[0] and node[-1] < current_weight):
                        dp[v_new] = node
    return max(dp.values())


tote_dims = [30, 35, 45]  # Dimensions of tote, manually sorted in ascending order
V = multiply_list(tote_dims)  # Total volume of tote
products = []  # [(ID, price/value, volume, weight)]

with open('products.csv', 'rb') as f:
    for line in f:
        data = [int(e) for e in line.strip().split(',')]
        # Compare dimension of items with dimension of box to see if they can fit. Eliminates 2067 items
        item_dims = [dim for dim, max_dim in zip(sorted(data[2:5]), tote_dims) if dim <= max_dim]
        if len(item_dims) == 3:
            products.append((data[0], data[1], multiply_list(data[2:5]), data[5]))

print(solve(products, V))