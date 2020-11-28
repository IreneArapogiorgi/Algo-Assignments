from collections import deque
import argparse
import random
import math
import sys

# Generate circles' radius
#
# If argument radius is given by user, all circles have the same radius
# Otherwise, each circle has a random radius
#
# Arguments min_radius and max_radius set boundaries for random radius

def generate_radius(radius, min_radius, max_radius):
    if radius:
        return radius
    else:
        return random.randint(min_radius, max_radius)

# Find circle's distance from starting point

def dist_from_start(circle, start):
    if circle == None:
        return None

    if start == (0, 0):
        d = math.sqrt(circle[0] ** 2 + circle[1] ** 2)
    else:
        d = math.sqrt((circle[0] - start[0]) ** 2 + (circle[1] - start[1]) ** 2)
    
    return round(d, 2)

# Find the closest to the starting point alive circle

def find_closest(forehead, dist, alive):
    # Find the minimum distance of an alive circle
    min_dist = min(d for i, d in enumerate(dist) if alive[i] != 0)

    for i in range(len(dist)):
        if dist[i] == min_dist and alive[i] == 1:
            return forehead[i]

# Find path between two circles in graph

def find_path(graph, start, end, path=[]):
    path = path + [start]

    if start == end:
        return path

    if graph[start] not in path:
        new_path = find_path(graph, graph[start], end, path)
        if new_path:
            return new_path
    return None

# Find intersected circles

def find_intersected(cm, cn, tangent, r, radius, forehead):
    # Find indexes of cm and cn in forehead
    cm_index = forehead.index(cm)
    cn_index = forehead.index(cn)

    # Create a list to store intersected circles
    intersected = []

    # Move from circle cn to cm in forehead
    for i in range(cn_index, cm_index - 1, -1):
        if forehead[i] != None:

            # Calculate distance between tangent circle and i-th circle between cn and cm
            dx = forehead[i][0] - tangent[0]
            dy = forehead[i][1] - tangent[1]
            d = dx ** 2 + dy ** 2

            # If True, tangent circle intersects forehead[i] circle
            if d < (radius[forehead[i]] + r) ** 2:
                intersected.append(forehead[i])

    return intersected

# Check intersection between tangent circle and any forehead's circles

def check_intersection(cm, cn, tangent, r, radius, graph, forehead):
    # Find intersected circles
    intersected = find_intersected(cm, cn, tangent, r, radius, forehead)

    # Remove cm and cn if they were found as intersected
    if cm in intersected: intersected.remove(cm)
    if cn in intersected: intersected.remove(cn)

    # Create a list to store removed circles
    removed = []

    if intersected:
        # Store first and last intersected circles
        first = intersected[0]
        last = intersected[-1]

        # Find circles between cn and first intersected circle
        first_to_cn = find_path(graph, first, cn)

        # Find circles between cm and last intersected circle
        cm_to_last = find_path(graph, cm, last)

        if len(cm_to_last) < len(first_to_cn):
            # Store circle previous to the last intersected circle
            c = list(graph.keys())[list(graph.values()).index(last)]

            # Find path between the circle after cn and the
            # circle previous to the last intersected circle
            removed = find_path(graph, graph[cn], c)

            cm = last

        if len(cm_to_last) > len(first_to_cn):
            # Store circle previous to cm
            c = list(graph.keys())[list(graph.values()).index(cm)]

            # Find path between the circle after the first
            # intersected circle and the circle previous to cm
            removed = find_path(graph, graph[first], c)

            cn = first
    
    return removed, cm, cn

# Find tangent circle
#
# c1, c2: two circles for which we find
# the tangent circle, given in the form of
# lists [x,y] with x, y being their coordinates
#
# r1, r2: radius of circles c1, c2
#
# r: radius of tangent circle

def tangent_circle(c1, c2, r1, r2, r):

    # Calculate distance between c1 and c2's centers
    dx = c2[0] - c1[0]
    dy = c2[1] - c1[1]
    d = math.sqrt(dx ** 2 + dy ** 2)

    # Calculate tangent circle's coordinates
    radius1 = r1 + r
    radius2 = r2 + r

    l = (radius1 ** 2 - radius2 ** 2 + d ** 2) / (2 * (d ** 2))
    e = math.sqrt((radius1 ** 2) / (d ** 2) - l ** 2)

    kx = c1[0] + l * dx - e * dy
    ky = c1[1] + l * dy + e * dx

    return (round(kx, 2), round(ky, 2))

# Find distance of a circle to a line segment
#
# u, v: points of the line segment, given in the form
# of lists [x,y] with x, y being their coordinates
#
# c: given circle

def line_segment_distance(u, v, c):
    l = (u[0] - v[0]) ** 2 + (u[1] - v[1]) ** 2

    if l == 0:
        d = math.sqrt((u[0] - c[0]) ** 2 + (u[1] - c[1]) ** 2)
        return round(d, 2)
    else:
        t = ((c[0] - u[0]) * (v[0] - u[0]) + (c[1] - u[1]) * (v[1] + u[1])) / l
        t = max(0, min(1, t))

        px = u[0] + t * (v[0] - u[0])
        py = u[1] + t * (v[1] - u[1])

        d = math.sqrt((px - c[0]) ** 2 + (py - c[1]) ** 2)
        return round(d, 2)

# Extract boundaries from text file

def read_boundaries(file):
    # Open and read given file
    with open(file, 'r') as file:

        # Extract file's lines and each line's elements in list
        lines = [line.strip('\n') for line in file.readlines()]
        segments = [line.split(' ') for line in lines]

        # Convert coordinates from strings to float numbers
        for s in segments:
            for i, coordinate in enumerate(s):
                s[i] = float(coordinate)
        
        return segments

# Check if tangent circle intersects given boundaries
#
# If True in intersects, circle intersects boundaries

def check_boundaries(tangent, r, segments):
    intersects = []

    for s in segments:
        d = line_segment_distance([s[0], s[1]], [s[2], s[3]], tangent)
        if d < r:
            intersects.append(True)
        else:
            intersects.append(False)

    return (True in intersects)

# Extract circles in text file

def extract_circles(output_file, boundary_file, radius):
    # Open and write output file
    with open(output_file, 'w') as of:
        for circle, r in radius.items():
            line = str(circle[0]) + ' ' + str(circle[1]) + ' ' + str(r) + '\n'
            of.write(line)

        # Append boundaries if given
        if boundary_file:
            with open(boundary_file, 'r') as bf:
                of.write(bf.read())

# Main function

def main():
    # Retrieve arguments passed on command line
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--items", type=int, help="number of circles")
    parser.add_argument("-r", "--radius", type=int, help="radius of all circles")
    parser.add_argument("--min_radius", type=int, help="min radius of circles")
    parser.add_argument("--max_radius", type=int, help="max radius of circles")
    parser.add_argument("-b", "--boundary_file", help="boundary file")
    parser.add_argument("-s", "--seed", type=int, help="seed of random number generator")
    parser.add_argument("output_file", help="output file")

    args = parser.parse_args()

    if args.items:
        circles = args.items # total number of circles to be inserted
    else:
        circles = sys.maxsize # no specific number of circles was given

    if args.boundary_file:
        boundaries = read_boundaries(args.boundary_file)

    if args.seed:
        random.seed(args.seed) # seed for random number generator

    # Create a queue to store forehead
    forehead = deque()

    # Create a dict to store circles' radius
    radius = {}

    # Add the first circle in forehead and store its radius
    radius[(0, 0)] = generate_radius(args.radius, args.min_radius, args.max_radius)
    forehead.append((0, 0))

    # Add the second circle in forehead and store its radius
    r = generate_radius(args.radius, args.min_radius, args.max_radius)
    radius[(radius[(0, 0)] + r, 0)] = r
    forehead.append((radius[(0, 0)] + r, 0))

    # Create a graph to store connected circles
    graph = {(0, 0): (radius[(0, 0)] + r, 0), (radius[(0, 0)] + r, 0): (0, 0)}

    # Create a list to store whether a circle is alive
    alive = [1 for i in range(2)]

    # Calculate each circle's distance from starting point
    dist = [dist_from_start(circle, (0, 0)) for circle in forehead]

    # Count circles added
    count = 2

    # Loop breaks when not having alive circles or not having circles to add
    while 1 in alive and count < circles:
        # Find the closest to the start alive circle
        cm = find_closest(forehead, dist, alive)
        orig_cm = cm

        # Find the circle following the cm one
        # That circle is the one which was last inserted to forehead
        cn = forehead[-1]

        intersects = True

        # Generate radius for upcoming tangent circle
        r = generate_radius(args.radius, args.min_radius, args.max_radius)

        # Loop breaks if tangent circle doesn't intersect any circles
        while intersects:

            # Find a circle tangent to cm and cn
            tangent = tangent_circle(cm, cn, radius[cm], radius[cn], r)

            # Check if tangent circle intersects any forehead circles
            # and store list with removed forehead circles if any
            removed, cm, cn = check_intersection(cm, cn, tangent, r, radius, graph, forehead)

            if removed:
                # Keep copies of all data
                graph_copy = graph.copy()
                forehead_copy = forehead.copy()
                alive_copy = alive.copy()

                for c in removed:
                    # Remove circle from graph
                    del graph[c]

                    # Remove circle from forehead and set as non-alive
                    i = forehead.index(c)
                    forehead[i] = None
                    alive[i] = 0

                # Last inserted circle should point to new first circle in forehead
                for c in forehead:
                    if c != None:
                        graph[forehead[-1]] = c
                        break
            else:
                intersects = False

        if args.boundary_file:
            if check_boundaries(tangent, r, boundaries):
                graph = graph_copy
                forehead = forehead_copy
                alive = alive_copy

                # Set orig_cm as non-alive
                alive[forehead.index(orig_cm)] = 0
            else:
                # Last inserted circle should point to tangent
                graph[forehead[-1]] = tangent

                # Tangent should point to cm
                graph[tangent] = cm

                # Add tangent circle to forehead, store its radius and mark it alive
                forehead.append(tangent)
                radius[tangent] = r
                alive.append(1)

                # Calculate each circle's distance from new starting point
                dist = [dist_from_start(circle, cm) for circle in forehead]

                # Mark as alive all non-alive forehead circles
                for i in range(len(alive)):
                    if forehead[i] != None and alive[i] == 0:
                        alive[i] = 1

                count += 1
        else:
            # Last inserted circle should point to tangent
            graph[forehead[-1]] = tangent

            # Tangent should point to cm
            graph[tangent] = cm

            # Add tangent circle to forehead, store its radius and mark it alive
            forehead.append(tangent)
            radius[tangent] = r
            alive.append(1)

            # Calculate each circle's distance from new starting point
            dist = [dist_from_start(circle, cm) for circle in forehead]

            count += 1

    # Store all inserted circles in text file
    extract_circles(args.output_file, args.boundary_file, radius)

    # Print total number of inserted circles
    print(count)

if __name__ == "__main__":
    main()