# Product of all elements in a list
def mulList(lst):
	return reduce(lambda x, y: x*y, lst)

'''
Finds the item combination with the highest value and smallest weight, constrained
by total volume <= V, via dynamic programming.

Volume: 50 - Value: 41298 Items: [1370, 4887, 5084, 6532, 8699, 9972, 10496, 10981, 12856, 12979, 14301, 14448, 17788, 17896, 26950, 27376, 31288, 33638, 34414, 35280, 36175, 36769, 39987]

450166
'''

def printTop(n, dp):
	print('================Top %s==================='%n)
	for k,v in sorted(dp.items(), key= lambda x:x[1][0], reverse=True)[0:n]:
		print('Volume: %s - Value: %s Items: %s'%(k, v[0], v.[1]))

def solve(items, V):
	dp = {}
	# Base Case
	dp[V] = [0, [], 0]

	# Recursive Case
	for i in range(len(items)):
		item = items[i]
		for Vold in dp.keys():
			# Update new volume if we choose to take
			Vnew = Vold-item[2]
			if Vnew >= 0:
				old = dp[Vold]
				node = [old[0] + item[1], old[1] + [item[0]], old[-1] + item[-1]]
				if not Vnew in dp:
					# If there isn't already a node there, directly set a node
					dp[Vnew] = node
				else:
					# Else we compare the current Node with the new Node and 
					# choose by highest value, lowest weight
					currentBest = dp[Vnew]
					if(currentBest[0] <= node[0]):
						dp[Vnew] = node
					elif currentBest[0] == node[0]:
						if node[-1] < currentBest[-1]:
							dp[Vnew] = node

	bestV = max(dp.keys(), key=(lambda k:dp[k][0]))
	
	node = dp[bestV]
	# printTop(5,dp)
	print('Items: %s = %s'%(sorted(node[1]), sum(node[1])))
	return node[1]

toteDims = [30, 35, 45] # Dimensions of tote, sorted asc
V =  mulList(toteDims) # Total volume of tote
items=[] # [(ID, price/value, volume, weight)]

with open('products.csv','rb') as f:
	
	for line in f:
		data = [int(e) for e in line.strip().split(',')]		
		# Compare dimension of items with dimension of box to see if they can fit. Eliminates 2067 items
		itemDims = [dim for dim, maxDim in zip(sorted(data[2:5]), toteDims) if dim <= maxDim]
		if len(itemDims) == 3:
			items.append((data[0], data[1], mulList(data[2:5]), data[5]))

	solve(items, V)
