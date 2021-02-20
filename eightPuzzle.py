import heapq
import time
from random import randint
from copy import deepcopy

# Board Size
ROWS, COLS = (3, 3)

nodesExpanded = 0
maxQueueSize = 1
visitedStates = []

class Node:
    def __init__(self, data, g):
        self.data = data
        self.children = []
        # self.depth = depth
        self.g = g
        # self.h = h
        # self.f = g + h
        return

    def add_child(self, child):
        if child not in self.children:
        # if child not in nodes:
            self.children.append(child)
        else:
            print('Duplicate')

    def state(self):
        return self.data

    def get_children(self):
        return self.children

    # Prints puzzle
    def display(self):
        for row in self.data:
            print(row)
        return

    # Returns coordinates the of blank square
    def findCoords(self, searchValue):
        for x, col in enumerate(self.data):
            try:
                return x, col.index(searchValue)
            except ValueError:
                pass
        return

    def printChildren(self):
        for child in self.children:
            print(child.data)
            print('-------------')


def UCS(node):
    h = 0
    return node.g + h

def MTH(node, goal):
    puzzle = node.data
    h = 0

    # Calculate number of misplaced tiles for h
    for y in range(COLS):
        for x in range(ROWS):
            if puzzle[y][x] != goal[y][x]:
                h +=1
    return node.g + h

def MDH(node, goal):
    puzzle = node.data
    h = 0

    for y in range(COLS):
        for x in range(ROWS):
            # If there is a misplaced tile it finds the coordinates of it and then 
            # calculates the distance to where it should be.
            if puzzle[y][x] != goal[y][x]:
                tileCoords = node.findCoords(goal[y][x])    # Location of misplaced tile
                horizontalMoves = abs(x - tileCoords[1])
                verticalMoves = abs(y - tileCoords[0])
                h += (horizontalMoves + verticalMoves)
                    
    return node.g + h

def expand(node, queue):
        puzzle = node.data
        coords = node.findCoords(0) # Coordinates of the empty square
        g = node.g + 1
        global nodesExpanded

        try:
            # Move left
            # print('Moving left')
            newPuzzle = deepcopy(puzzle)
            if coords[1] != 0:
                newPuzzle[coords[0]][coords[1]], newPuzzle[coords[0]][coords[1]-1] = newPuzzle[coords[0]][coords[1]-1], newPuzzle[coords[0]][coords[1]]
                newNode = Node(newPuzzle, g)
                if newPuzzle not in visitedStates:
                    node.add_child(newNode)
        except:
            # print('Can\'t move left!')
            # print('-------------')
            pass

        try:
            # Move right
            # print('Moving right')
            newPuzzle = deepcopy(puzzle)
            newPuzzle[coords[0]][coords[1]], newPuzzle[coords[0]][coords[1]+1] = newPuzzle[coords[0]][coords[1]+1], newPuzzle[coords[0]][coords[1]]
            newNode = Node(newPuzzle, g)
            if newPuzzle not in visitedStates:
                node.add_child(newNode)
        except:
            # print('Can\'t move right!')
            # print('-------------')
            pass

        try:
            # Move up
            # print('Moving up')
            newPuzzle = deepcopy(puzzle)
            if coords[0] != 0:
                newPuzzle[coords[0]][coords[1]], newPuzzle[coords[0]-1][coords[1]] = newPuzzle[coords[0]-1][coords[1]], newPuzzle[coords[0]][coords[1]]
                newNode = Node(newPuzzle, g)
                if newPuzzle not in visitedStates:
                    node.add_child(newNode)
        except:
            # print('Can\'t move up!')
            # print('-------------')
            pass

        try:
            # Move down
            # print('Moving down')
            newPuzzle = deepcopy(puzzle)
            newPuzzle[coords[0]][coords[1]], newPuzzle[coords[0]+1][coords[1]] = newPuzzle[coords[0]+1][coords[1]], newPuzzle[coords[0]][coords[1]]
            newNode = Node(newPuzzle, g)
            if newPuzzle not in visitedStates:
                node.add_child(newNode)
        except:
            # print('Can\'t move down!')
            # print('-------------')
            pass

def generalSearch(puzzleStart, puzzleEnd, queueFunc):
    # Root node/start state
    rootNode = Node(puzzleStart, 0)
    nodes = []
    heapq.heappush(nodes, (0, 0, rootNode))

    print('\nPuzzle start state:')
    rootNode.display()
    print('===========')

    global nodesExpanded
    maxQueueSize = 1
    queuePosition = 0               # Tie breaker - enqueue order
    numInitialExpansions = 3        # Counter to keep track of how many initial expansions to display

    while True:
        if len(nodes) > maxQueueSize:
            maxQueueSize = len(nodes)

        if len(nodes) == 0: # Queue empty
            print('Failure. No solution.')
            return
        
        node = heapq.heappop(nodes)[2]
        expand(node, nodes)
        nodesExpanded += 1
        visitedStates.append(node.data)        

        if numInitialExpansions > 0:
            print('Expanding node:')
            node.display()
            numInitialExpansions -= 1

        if node.state() == puzzleEnd:
            print('\n~~~~~ Steps omitted ~~~~~\n')
            print('Expanding node:')
            for row in visitedStates[-1]:
                print(row)
            print('\nSuccess!\n')
            print('Expanded {} nodes'.format(nodesExpanded))
            print('The maximum number of nodes in the queue at any one time was {}'.format(maxQueueSize))
            print('The depth of the goal node was {}'.format(node.g))
            # return node ?
            return
        
        # Uniform cost search
        if queueFunc == 1:
            # Expands the parent node and places all the children in queue.
            # Priority queue deals with ordering. Then we pop off highest priority 
            # child and repeat this process.
            
            # expand(node, nodes)
            for child in node.get_children():
                queuePosition += 1
                if child.data not in visitedStates:
                    heapq.heappush(nodes, (UCS(child), queuePosition, child))
        # Misplaced tile heuristic
        elif queueFunc == 2:
            # expand(node, nodes)
            for child in node.get_children():
                queuePosition += 1
                if child.data not in visitedStates:
                    heapq.heappush(nodes, (MTH(child, puzzleEnd), queuePosition, child))
        # Manhattan distance heuristic
        elif queueFunc == 3:
            # expand(node, nodes)
            for child in node.get_children():
                queuePosition += 1
                if child.data not in visitedStates:
                    heapq.heappush(nodes, (MDH(child, puzzleEnd), queuePosition, child))
    

def main():
    print('Welcome to Isaac\'s 8-puzzle solver.')
    
    puzzleChoice = int(input('Type “1” to use a default puzzle, or “2” to enter your own puzzle. '))
    puzzle = [[0 for i in range(COLS)] for j in range(ROWS)]
    
    if puzzleChoice == 1:        
        # Default puzzles
        defaultPuzzles = {
            "1" : [[1, 2, 3],     # Depth 0
                   [4, 5, 6],
                   [7, 8, 0]],
            "2" : [[1, 2, 3],     # Depth 2
                   [4, 5, 6], 
                   [0, 7, 8]],
            "3" : [[1, 2, 3],     # Depth 4
                   [5, 0, 6],  
                   [4, 7, 8]],
            "4" : [[1, 3, 6],     # Depth 8 
                   [5, 0, 2],
                   [4, 7, 8]],
            "5" : [[1, 3, 6],     # Depth 12 
                   [5, 0, 7],
                   [4, 8, 2]],
            "6" : [[1, 6, 7],     # Depth 16
                   [5, 0, 3],
                   [4, 8, 2]],
            "7" : [[7, 1, 2],     # Depth 20
                   [4, 8, 5],  
                   [6, 3, 0]],
            "8" : [[0, 7, 2],     # Depth 24
                   [4, 6, 1],
                   [3, 5, 8]],
            "9" : [[8, 6, 7],     # Depth 31
                   [2, 5, 4],
                   [3, 0, 1]]
        }
        # puzzle = defaultPuzzles[str(randint(1, 9))]
        puzzle = defaultPuzzles[input('Default puzzle (1-9): ')]

    elif puzzleChoice == 2:
        print('Enter your puzzle. Use a zero to represent the blank and use space or tabs between numbers.')
        for i in range(ROWS):
            try:
                # Take multiple inputs using list comprehension. Uses maxsplit argument of split() to ensure valid input
                puzzle[i] = [int(item) for item in input('Row {}: '.format(i+1)).split(None, COLS - 1)] 
            except:
                print('You can only input {} numbers per row. Try again.'.format(COLS))
                return -1

    print('Enter your choice of algorithm: ')
    print(' 1. Uniform Cost Search\n 2. A* with the Misplaced Tile heuristic.\n 3. A* with the Manhattan distance heuristic.')
    algoChoice = int(input())      

    puzzleEnd = [[1, 2, 3], 
                 [4, 5, 6], 
                 [7, 8, 0]]

    start = time.time()
    generalSearch(puzzle, puzzleEnd, algoChoice)
    end = time.time()
    print('Time elapsed: {} seconds'.format(end - start))
    
    
main()