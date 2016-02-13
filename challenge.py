# Product of all elements in a list
def mulList(lst):
	return reduce(lambda x, y: x*y, lst)

'''
Finds the item combination with the highest value and smallest weight, constrained
by total volume <= V, via dynamic programming.

dp[i][v] = (val, prev, w)
dp[i][v] is the outstanding value in the tote having chosen 0 / 1 for the item 
(taking or not taking), with v remaining capacity and w weight. Stores pointer to previous node.

Base Case:
dp[0][V] = [0, None, 0] # <Node> uses a mutable type (list) so that when passing in a reference to
						#  the previous node this will hopefully prevent the overhead of nesting nodes 
						# as in the immutable casee.g. (99, (12, (3,None,0), 1), 4)
Recursive Case:
dp[i][v][0] = max(dp[i-1][v], dp[i-1][v'] + item[2])  # <Item> (ID, price/value, volume, weight)

if dp[i-1][v][0] > dp[i-1][v'][0]:
	dp[i][v][1] = dp[i-1][v]
elif dp[i-1][v][0] == dp[i-1][v'][0]:
	# compare weight if equal value
	dp[i][v][1] = dp[i-1][v] if dp[i-1][v][2] < dp[i-1][v'][2] else dp[i-1][v']
else:
	dp[i-1][v][1] = dp[i-1][v']

where v' = v + item[3]
'''

# Really just a wrapper around a list of items so we dont have to constantly
# recompute value, weight etc
class Node:
	def __init__(self, value, items, weight):
		self.value = value
		self.weight = weight
		self.items = items
	def __str__(self):
		return 'Stats: %s with Items: %s'%([self.value, self.weight], self.items)

def solve(items, V):
	dp = {}

	# Base Case
	dp[V] = Node(0, [], 0)
	dp[V-items[0][2]] = Node(items[0][1], [items[0][0]], items[0][-1])

	# Recursive Case
	for i in range(1, len(items), 1):
		if not i % 5:
			print('Iteration: %s'%i)
		item = items[i]
		for Vold in dp.keys():
			# Choose not to take
			old = dp[Vold]

			# Update new volume if we choose to take
			Vnew = Vold-item[2]
			if Vnew >= 0:
				node = Node(old.value + item[1], old.items + [item[0]], old.weight + item[-1])
				if not Vnew in dp:
					# If there isn't already a node there, directly set a node
					dp[Vnew] = node
				else:
					# Else we compare the current Node with the new Node and 
					# choose by highest value, lowest weight
					currentBest = dp[Vnew]
					if(currentBest.value < node.value):
						currentBest = node
					elif currentBest.value == node.value:
						if node.weight < currentBest.weight:
							currentBest = node 

	
	# Backtrack
	bestV = max(dp.keys(), key=(lambda k:dp[k].value))
	# bestV = max(dp.values(), key=(lambda k:k.value))
	
	node = dp[bestV]
	print('Best Value: %s @ capacity of: %s' % (node.value, V-bestV))
	
	print('Items: %s'%node.items)
	return node.items

toteDims = [30, 35, 45] # Dimensions of tote, sorted asc
V =  mulList(toteDims) # Total volume of tote
items=[] # [(ID, price/value, volume, weight)]

with open('small.csv','rb') as f:
	for line in f:
		data = [int(e) for e in line.strip().split(',')]		
		# Compare dimension of items with dimension of box to see if they can fit. Eliminates 2067 items
		itemDims = [dim for dim, maxDim in zip(sorted(data[2:5]), toteDims) if dim <= maxDim]
		if len(itemDims) == 3:
			items.append((data[0], data[1], mulList(data[2:5]), data[5]))
	print('Max Capacity: %s'%V)
	products = solve(items, V)
	# print(products)
