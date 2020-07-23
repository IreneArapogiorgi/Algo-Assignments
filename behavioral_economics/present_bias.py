import argparse

# Retrieve arguments passed on command line
parser = argparse.ArgumentParser()

parser.add_argument("filename", help="name of input file")
parser.add_argument("bias_parameter", help="number of bias parameter", type=float)
parser.add_argument("start_node", help="start node of graph")
parser.add_argument("end_node", help="end node of graph")

args = parser.parse_args()
bias_parameter = args.bias_parameter
start_node = args.start_node
end_node = args.end_node

print()

# Read file & convert to graph
my_graph = {}
my_file = open(args.filename, 'r')

lines = [line.strip('\n') for line in my_file.readlines()] # list of file's lines
#print('File's lines are: , lines)
#print()
my_file.close()

elements = [element.split(" ") for element in lines] # list of line's elements
#print("File's elements of each line are: ", elements)
#print()

nodes = []
for element in elements:
    if len(element) == 3:
        nodes.append(element[0])
        nodes.append(element[1])

nodes = set(nodes)
#print('Nodes of given graph are: ', nodes)
#print()

# Create graph
for node in nodes:
    nodelist = []
    for element in elements:
        if len(element) == 3:
            if node == element[0]:
                nodelist.append(element[1])
                my_graph[node] = nodelist
#print('Given graph is: ', my_graph)
#print()

# Find all paths by using depth-first search algorithm - step 1
path = []
paths = []

def find_paths(graph, start_node, end_node):
    path.append(start_node)
    #print(path)
    #print()

    if start_node == end_node:
        paths.append(list(path))
        #print(paths)
        #print()
    else:
        for v in graph[start_node]:
            find_paths(graph, v, end_node)

    path.pop()

find_paths(my_graph, start_node, end_node)
#print('All paths are: ', paths)
#print()

# Calculate each path's real cost & lowest cost - step 2
def shortest_path(bias):
    real_cost = []

    for path in paths:
        cost_value = 0
        for index in range(len(path)-1):
            for element in elements:
                if len(element) == 3:
                    if path[index] == element[0] and path[index + 1] == element[1]:
                        cost_value = cost_value + bias * int(element[2]) if index != 0 else cost_value + int(element[2])
                        break
        real_cost = real_cost + [cost_value]
    #print('Cost of each path is: ', real_cost)
    #print()

    best_indexes = [index for index, c in enumerate(real_cost) if c == min(real_cost)]

    # Return best path and its cost
    for index in best_indexes:
        return paths[index], real_cost[index]

best_path, rc = shortest_path(1)
print(best_path, rc) #print('Lowest real cost is: ', rc, 'of path: ', best_path)
                     #print()

# Find user's path - step 3
user_path = []
count = 0

while True:
    
    node = best_path[0] if count == 0 else best_path[1]
    user_path.append(node)
    #print('User path creation: ', user_path)
    #print()

    paths = []
    path = []
    find_paths(my_graph, node, end_node)
    #print('All paths - step 3 - are: ', paths)
    #print()

    best_path, cost = shortest_path(bias_parameter)
    
    if best_path[0] == node and best_path[1] == end_node:
        user_path.append(best_path[1])
        break
    
    count = 1

user_cost = 0
for index in range(len(user_path)-1):
    for element in elements:
        if len(element) == 3:
            if user_path[index] == element[0] and user_path[index + 1] == element[1]:
                user_cost = user_cost + int(element[2])
                break

print(user_path, user_cost) #print('User uses path: ', user_path, 'of cost: ', user_cost)