import pprint
import argparse

# Retrieve arguments passed on command line
#
# Optional argument -p means that we must print the graph at the end
# Argument size stores the required polyominoes' size 

parser = argparse.ArgumentParser()

parser.add_argument("-p", "--print", action='store_true', help="print graph")
parser.add_argument("size", type=int, help="polyominoes' size")

args = parser.parse_args()

# Parameter n stores the required polyominoes' size

n = args.size

# Find the graph's nodes based on the given polyominoes' size n
#
# The first block of loops corresponds to finding nodes with positive x and y
# The second block of loops corresponds to finding nodes with negative x and positive y
#
# Disclaimer: graph's nodes are depicted in the form of (x,y)

def find_nodes(nodes, n):
    for first_num in range(0,n):
        for second_num in range(0,n-first_num):
            nodes.append((first_num,second_num))

    for first_num in range(-1,1-n,-1):
        for second_num in range(1,n+first_num):
            nodes.append((first_num,second_num))

    return nodes

nodes = find_nodes([], n)

# Create graph based on the nodes' list we created previously

graph = {}

for node in nodes:
    
    # Possible neighbors are created in this specific order to be later depicted clockwised

    neighbor_1 = (node[0] + 1, node[1])
    neighbor_2 = (node[0], node[1] + 1)
    neighbor_3 = (node[0] - 1, node[1])
    neighbor_4 = (node[0], node[1] - 1)

    neighbors = [neighbor_1, neighbor_2, neighbor_3, neighbor_4]

    # Final neighbors of each node are those which can be found in list nodes

    graph[node] = [neighbor for neighbor in neighbors if neighbor in nodes]

    # Detailed implementation of adjacency lists creation
    #
    # The following block of code can both replace & explain line 57
    #
    # adjacencylist = []
    #
    # for neighbor in neighbors:
    #    if neighbor in nodes:
    #        adjacencylist.append(neighbor)
    #
    # graph[node] = adjacencylist

# Count fixed polyominoes based on the given graph

def count_fixed_polyominoes(graph, untried, n, p, c):
    while untried:

        u = untried.pop()
        p.append(u)

        # Find Neighbors(p\u)

        p_neighbors = set()

        for node in p:
            if node != u:
                p_neighbors.update(graph[node])

        # Continue with the rest of the algorithm

        if len(p) == n:
            c += 1
        else:
            new_neighbors = set()

            for neighbor in graph[u]:
                if neighbor not in untried and neighbor not in p and neighbor not in p_neighbors:
                    new_neighbors.add(neighbor)

            new_untried = set(list(untried) + list(new_neighbors))

            c = count_fixed_polyominoes(graph, new_untried, n, p, c)
        p.remove(u)
    return c

# Print final results

if args.print:
    pprint.pprint(graph)

print(count_fixed_polyominoes(graph, {(0,0)}, n, [], 0))