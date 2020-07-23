import sys

print()

# Read graph file & convert to graph
my_file = open(sys.argv[1], 'r')

lines = [line.strip('\n') for line in my_file.readlines()] # list of file's lines
lines = list(filter(lambda x: x!= '', lines))

#print("File's lines are: ", lines)
#print()

my_file.close()

elements = [line.split(" ") for line in lines] # list of line's elements

nodes = []

# Convert file's elements to integers & create list of all nodes
for element in elements:

    element[0] = int(element[0])
    element[1] = int(element[1])

    nodes.append(element[0])
    nodes.append(element[1])

#print("File's elements of each line are: ", elements)
#print()

nodes = set(nodes)

#print('Nodes of given graph are: ', nodes)
#print()

# Create graph
my_graph = {}

for element in elements:

    if element[0] not in my_graph:
        my_graph[element[0]] = []

    if element[1] not in my_graph:
        my_graph[element[1]] = []

    my_graph[element[0]].append(element[1])
    my_graph[element[1]].append(element[0])

#print('Given graph is: ', my_graph)
#print()

# Insert in min heap functions

def parent(p):
    return (p - 1) // 2

def insert_in_mh(mh, pn):
    mh.append(pn)
    i = len(mh) - 1
    while i != 0 and mh[i][0] < mh[parent(i)][0]:
        p = parent(i)
        mh[i], mh[p] = mh[p], mh[i]
        i = p

# Parameter initialization & min heap creation
degree = [] # degree of each node
min_heap = [] # min heap

for key, adjacencylist in sorted(my_graph.items()):

    degree.append(len(adjacencylist))
    potential_node = [len(adjacencylist), key]

    insert_in_mh(min_heap, potential_node)

potential = degree[:] # potential core number of each node
core = [0 for i in range(len(my_graph))] # core number of each node -- in the worst scenario any node could have core number equal to zero

#print('Degree of each node is: ', degree)
#print()

#print('Min heap is: ', min_heap)
#print()

# Extract from min heap functions
def set_root(mh, c):
    if len(mh) != 0:
        mh[0] = c

def children(mh, p):
    if 2 * p + 2 < len(mh):
        return [2 * p + 1, 2 * p + 2]
    else:
        return [2 * p + 1]

def extract_min_from_mh(mh):
    c = mh[0]
    set_root(mh, mh.pop())
    i = 0
    while 2 * i + 1 < len(mh):
        j = min(children(mh, i), key=lambda x: mh[x][0])
        if mh[i][0] < mh[j][0]:
            return c
        mh[i], mh[j] = mh[j], mh[i]
        i = j
    return c

# Update min heap functions
def delete_node_from_adjlist(graph, key, element): # delete connected node (element) from key's adjacency list
    graph[key].remove(element)

def reconstruct_mh(mh, index): # reconstructs min heap after updating it

    if 2 * index + 1 < len(mh):

        min_child_index = min(children(mh, index), key=lambda x: mh[x][0])

        if mh[index][0] <= mh[min_child_index][0]:
            return

        mh[index], mh[min_child_index] = mh[min_child_index], mh[index]
        reconstruct_mh(mh, min_child_index)

# def reconstruct_mh_2(mh, index): # reconstructs min heap after updating it

#     left_child = 2 * index + 1
#     right_child = 2 * index + 2
#     min_child_index = index

#     if left_child < len(mh) and mh[index] > mh[left_child]:
#         min_child_index = left_child

#     if right_child < len(mh) and mh[min_child_index] > mh[right_child]:
#         min_child_index = right_child

#     if min_child_index != index:
#         mh[index], mh[min_child_index] = mh[min_child_index], mh[index]
#         reconstruct_mh_2(mh, min_child_index)

# def reconstruct_mh_3(mh): # reconstructs min heap after updating it -- NOT A PRACTICAL SOLUTION
#     i = 0
#     while 2 * i + 1 < len(mh):
#         j = min(children(mh, i), key=lambda x: mh[x][0])
#         if mh[i][0] < mh[j][0]:
#             return
#         mh[i], mh[j] = mh[j], mh[i]
#         i = j
#     return

def update_mh(mh, opn, npn): # updates opn with npn
    mh[mh.index(opn)] = npn
    reconstruct_mh(mh, mh.index(npn))
    #reconstruct_mh_2(mh, mh.index(npn))
    #reconstruct_mh_3(mh)

while len(min_heap) > 0:

    t = extract_min_from_mh(min_heap)
    core[t[1]] = t[0]
    
    if min_heap:

        for node in my_graph[t[1]]:

            degree[node] = degree[node] - 1

            delete_node_from_adjlist(my_graph, node, t[1]) # deletes extracted node t[1] from connected node's adjacency list

            old_potential_node = [potential[node], node]

            potential[node] = max(t[0], degree[node])

            new_potential_node = [potential[node], node]

            update_mh(min_heap, old_potential_node, new_potential_node)

for nodes_list, core_list in zip(nodes, core):
    print(str(nodes_list) + '\t' + str(core_list))