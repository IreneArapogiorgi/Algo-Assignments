import argparse

# Retrieve arguments passed on command line
parser = argparse.ArgumentParser()

parser.add_argument("filename", help="name of input file")

args = parser.parse_args()

print()

# Read file & get each column
my_file = open(args.filename, 'r')

lines = [line.strip('\n') for line in my_file.readlines()] # list of file's lines
lines = list(filter(lambda x: x != '', lines)) # getting rid of empty lines
#print("File's lines are: ", lines)
#print()
my_file.close()

elements = [element.split(", ") for element in lines] # list of line's elements
#print("File's elements of each line are: ", elements)
#print()

columns = []
for i in range(0, len(elements)):
    draft = []
    for element in elements:
        draft.append(element[i])
    columns.append(draft)
#print('Each column is: ', columns)
#print()

# Find all transversals - step 1
transversals = []

def find_transversal(count):
    if count == len(columns):
        transversals.append(list(transversal))
        transversal.pop()
        indexes.pop()
        return
    else:
            column = columns[count]
            for i, num in enumerate(column):
                if i not in indexes and num not in transversal:
                    transversal.append(num)
                    indexes.append(i)
                    find_transversal(count + 1)

    if len(transversal) < count + 1 and len(transversal) > 0 and len(indexes) > 0:
        transversal.pop()
        indexes.pop()

for index, element in enumerate(columns[0]):
    transversal = []
    indexes = []

    transversal.append(element)
    indexes.append(index)
    find_transversal(1)

#print('All transversals are: ', transversals)
#print()

# Find n transversals - step 2

n = 1
count = 0
dif = True
new_transversals = []

for transversal in transversals:
    start_element = transversal[0]
    new_transversals.append(transversal)
    for transversal2 in transversals[count + 1:]:
        if transversal2[0] != start_element:
            for tr in new_transversals:
                for i in range(len(transversal2)):
                    if tr[i] != transversal2[i]:
                        dif = True
                    else:
                        dif = False
                        break
                if dif == False:
                    break
            if dif == True:
                n = n + 1
                start_element = transversal2[0]
                new_transversals.append(transversal2)
    if n != len(columns):
        new_transversals.pop()
    else:
        break

    count = count + 1

#print('All different n transversals are: ', new_transversals)
#print()

# Create new square - step 3
if new_transversals:
    new_columns = [row[:] for row in columns]
    visited = [row[:] for row in columns]

    for index, transversal in enumerate(new_transversals):
        for i, element in enumerate(transversal):
            for column in new_columns[i:]:
                for j, num in enumerate(column):
                    if num == element and visited[i][j] != 'VISITED': 
                        column[j] = transversal[0]
                        visited[i][j] = 'VISITED'
                        break
                break
    #print('Each new column is: ', new_columns)
    #print()

    # Final square - step 4
    final_square = []

    for i in range(len(columns)):
        draft = []
        for j in range(len(columns)):
            t = tuple(columns[j][i] + new_columns[j][i])
            draft.append(tuple((int(x) for x in t)))
        final_square.append(draft)

    print(*final_square, sep = ',\n', end = '')
    print()
else:
    print([])