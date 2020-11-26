from collections import deque
import argparse

# Extract file's nodes in list

def extract_nodes(file):

    # Open and read given file

    with open(file, 'r') as file:

        # Extract file's lines & each line's nodes in list

        lines = [line.strip('\n') for line in file.readlines()]
        nodes = [node.split(" ") for node in lines]
        return nodes

# Create graph

def create_graph(nodes):
    graph = {}

    for node in nodes:

        if int(node[0]) not in graph:
            graph[int(node[0])] = []

        if int(node[1]) not in graph:
            graph[int(node[1])] = []

        graph[int(node[0])].append(int(node[1]))
        graph[int(node[1])].append(int(node[0]))

    return graph

# Calculate each node's degree

def find_degree(graph):
    degree = []

    for key, adjacencylist in sorted(graph.items()):
        degree.append(len(adjacencylist))

    return degree

# Immunize network based on the degree of each node

def immunize_by_degree(graph, degree, num_nodes):

    # Initialize removed_nodes list which stores nodes removed & their degree

    removed_nodes = []

    for i in range(num_nodes):
        max_degree = max(degree)

        # Find & remove node with maximum degree
        #
        # In case of multiple nodes having the maximum degree, remove the smallest one
        # To achieve that, we iterate the sorted graph

        for key, adjacencylist in sorted(graph.items()):
            if degree[key-1] == max_degree:
                
                # Store removed node in variable removed
                removed = key

                # Set removed node to have no neighbors
                graph[key] = []

                # Set removed node's degree to -1 which could not be found in list degree
                degree[key-1] = -1
                break

        # Delete removed node from adjacencylists when found & decrease degree when needed

        for key, adjacencylist in sorted(graph.items()):
            if removed in adjacencylist:
                degree[key-1] -= 1
                adjacencylist.remove(removed)

        # List removed_nodes stores all nodes removed from graph and their degree

        removed_nodes.append([removed, max_degree])
    return removed_nodes

# Before we go into immunizing the network based on the collective influence (ci) of each node,
# we need to implement the following functions: find_path_length(), ball_sum(), affected_nodes() & calculate_ci()

# Find the minimum path length starting from each node until we reach node i of the graph
#
# Function is based on BFS algorithm

def find_path_length(graph, size, i):

    # Initialize path_length list which stores the minimum distance between each node of the graph and given node i

    path_length = [0] * size

    # Find path length for each node of the graph
    #
    # n corresponds to each node of the graph
    # range(size) is equal to the total number of nodes in graph

    for n in range(size):

        # Initialize visited & inqueue lists

        visited = [False] * size
        inqueue = [False] * size

        # Initialize dist list which stores the distance between the starting node n and each neighbor

        dist = [0] * size

        # Create a new queue with deque() function

        q = deque()

        # Queue named q stores nodes we visit
        #
        # We append n+1 because graph's nodes start with 1, 2, ... while variable n with 0, 1, ... but corresponds to 1, 2, ...

        q.append(n+1)
        inqueue[n] = True

        while q:
            c = q.pop()
            inqueue[c-1] = False
            visited[c-1] = True

            # While loop stops when we reach node i passed as a parameter
            #
            # path_length[n] is the minimum distance between node n and i

            if c == i:
                path_length[n] = dist[i-1]
                break

            for neighbor in graph[c]:
                if not visited[neighbor-1] and not inqueue[neighbor-1]:
                    q.appendleft(neighbor)
                    inqueue[neighbor-1] = True

                    # Each time we visit a node's neighbor, we set or update the neighbor's path length by adding 1 to its predecessor's

                    if dist[neighbor-1] == 0 or dist[neighbor-1] > dist[c-1] + 1:
                        dist[neighbor-1] = dist[c-1] + 1

    return path_length

# Find the sum of (kj-1) for each j with path length equal to r
#
# Disclaimer: kj is equal to degree[j]

def ball_sum(graph, degree, i, r):
    ball_sum = 0

    # Find path length starting from each node until we reach node i+1
    #
    # We pass i+1 because graph's nodes start with 1, 2, ... while variable i with 0, 1, ... but corresponds to 1, 2, ...

    path_length = find_path_length(graph, len(degree), i+1)

    for j, length in enumerate(path_length):
        if length == r:
            ball_sum += degree[j] - 1

    return ball_sum

# Find nodes affected from removing key i
#
# Affected nodes have path length equal to or less than r+1 passed in function as parameter r

def affected_nodes(graph, size, i, r):
    affected = []

    # Find path length starting from each node until we reach node i, which is the removed one

    path_length = find_path_length(graph, size, i)

    for j, length in enumerate(path_length):
        if length <= r + 1:
            affected.append(j)

    return affected

# Calculate collective influence of given node

def calculate_ci(graph, degree, node, r):

    # For removed nodes, whose degree[i] == -1, set ci to -1

    if degree[node] == -1:
        return -1
    else:
        return (degree[node] - 1) * ball_sum(graph, degree, node, r)

# Immunize network based on the collective influence (ci) of each node

def immunize_by_ci(graph, degree, r, num_nodes):

    # Initialize removed_nodes list which stores nodes removed & their ci

    removed_nodes = []

    # Initialize ci list which stores each node's collective influence

    ci = [0] * len(graph)

    # Calculate collective influence of graph's nodes

    for node in range(len(ci)):
        ci[node] = calculate_ci(graph, degree, node, r)

    for i in range(num_nodes):
        max_ci = max(ci)

        # Find & remove node with maximum ci
        #
        # In case of multiple nodes having the maximum ci, we remove the smallest one
        # To achieve that, we iterate the sorted graph

        for key, adjacencylist in sorted(graph.items()):
            if ci[key-1] == max_ci:
                
                # Store removed node in variable removed
                removed = key

                # Set removed node to have no neighbors
                graph[key] = []

                # Set removed node's degree to -1 which could not be found in list degree
                degree[key-1] = -1
                break

        # Delete removed node from adjacencylists when found & decrease degree when needed

        for key, adjacencylist in sorted(graph.items()):
            if removed in adjacencylist:
                degree[key-1] -= 1
                adjacencylist.remove(removed)

        # Update collective influence of affected nodes

        for node in affected_nodes(graph, len(degree), removed, r):
            ci[node] = calculate_ci(graph, degree, node, r)

        # List removed_nodes stores all nodes removed from graph and their ci

        removed_nodes.append([removed, max_ci])
    return removed_nodes

# Main function

def main():
    # Retrieve arguments passed on command line
    #
    # Optional argument -c means that we immunize the network by degree
    # Optional argument -r means that we immunize the network by collective influence
    #
    # Argument num_nodes stores the number of nodes to be removed
    # Argument input_file stores nodes' links

    parser = argparse.ArgumentParser()

    parser.add_argument("-c", "--degree", action='store_true', help="immunize by degree")
    parser.add_argument("-r", "--radius", type=int, help="radius")
    parser.add_argument("num_nodes", type=int, help="nodes to be removed")
    parser.add_argument("input_file", help="nodes' links")

    args = parser.parse_args()

    nodes = extract_nodes(args.input_file)
    graph = create_graph(nodes)
    degree = find_degree(graph)

    # Immunize the network based on the given arguments

    if args.degree:
        removed_nodes = immunize_by_degree(graph, degree, args.num_nodes)
    else:
        removed_nodes = immunize_by_ci(graph, degree, args.radius, args.num_nodes)

    # Print both nodes removed & their degree/ci

    for node in removed_nodes:
        print(*node)

if __name__ == "__main__":
    main()