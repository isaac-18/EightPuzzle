import queue
import heapq
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


def welcome():
    print('Welcome to Isaac\'s 8-puzzle solver.')
    
    puzzleChoice = int(input('Type “1” to use a default puzzle, or “2” to enter your own puzzle. '))
    puzzle = [[0 for i in range(COLS)] for j in range(ROWS)]
    
    if puzzleChoice == 1:
        # Default puzzle
        puzzle = [[1, 2, 3], 
                  [4, 8, 0], 
                  [7, 6, 5]]
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
                # if (newPuzzle != puzzle) and (newPuzzle not in visitedStates):
                if newPuzzle not in visitedStates:
                    node.add_child(newNode)
                else:
                    print('node is already in queue')
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
            # if (newPuzzle != puzzle) and (newPuzzle not in visitedStates):
            if newPuzzle not in visitedStates:
                node.add_child(newNode)
            else:
                print('node is already in queue')
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
                # if (newPuzzle != puzzle) and (newPuzzle not in visitedStates):
                if newPuzzle not in visitedStates:
                    node.add_child(newNode)
                else:
                    print('node is already in queue')
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
            # if (newPuzzle != puzzle) and (newPuzzle not in visitedStates):
            if newPuzzle not in visitedStates:
                node.add_child(newNode)
            else:
                print('node is already in queue')
        except:
            # print('Can\'t move down!')
            # print('-------------')
            pass

def generalSearch(puzzleStart, puzzleEnd, queueFunc):
    # Root node/start state
    rootNode = Node(puzzleStart, 0)
    nodes = []
    heapq.heappush(nodes, (0, 0, rootNode))

    # global visitedStates
    # visitedStates = []

    global nodesExpanded
    maxQueueSize = 1
    queuePosition = 0   # Tie breaker 

    while True:
        if len(nodes) > maxQueueSize:
            maxQueueSize = len(nodes)

        if len(nodes) == 0: # Queue empty
            print('Failure. No solution.')
            return
        
        node = heapq.heappop(nodes)[2]
        
        visitedStates.append(node.data)

        print('Popped')
        print(node.state())
        nodesExpanded += 1
        

        if node.state() == puzzleEnd:
            print('Success!')
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
            
            # node.expand()
            expand(node, nodes)
            print('Expanding {} children'.format(len(node.get_children())))
            for child in node.get_children():
                queuePosition += 1
                if child.data not in visitedStates:
                    heapq.heappush(nodes, (UCS(child), queuePosition, child))
            #         child.display()
            #         print('-------------')
            # #         # nodesExpanded += 1
            # print('Next level')
            # print('===============')

        # Misplaced tile heuristic
        elif queueFunc == 2:
            expand(node, nodes)
            print('Expanding {} children'.format(len(node.get_children())))
            for child in node.get_children():
                queuePosition += 1
                if child.data not in visitedStates:
                    heapq.heappush(nodes, (MTH(child, puzzleEnd), queuePosition, child))
        elif queueFunc == 3:
            expand(node, nodes)
            print('Expanding {} children'.format(len(node.get_children())))
            for child in node.get_children():
                queuePosition += 1
                if child.data not in visitedStates:
                    heapq.heappush(nodes, (MDH(child, puzzleEnd), queuePosition, child))
    

def main():
    # welcome()
    puzzle = [[0 for i in range(COLS)] for j in range(ROWS)]
    
    puzzle = [[1, 2, 3], 
              [4, 5, 6], 
              [0, 7, 8]]

    puzzle1 = [[1, 2, 3], 
              [5, 0, 6], 
              [4, 7, 8]] # AB 23 iterations 4 depth
    
    A = [[1, 2, 3], # 0
        [4, 5, 6],
        [7, 8, 0]]

    B = [[1, 2, 3], 
        [4, 5, 6],  # 2
        [0, 7, 8]]

    C = [[1, 2, 3], 
        [5, 0, 6],  # 4
        [4, 7, 8]]

    D = [[1, 3, 6], 
        [5, 0, 2],  # 8
        [4, 7, 8]]

    E = [[1, 3, 6], 
        [5, 0, 7],  # 12
        [4, 8, 2]]

    F = [[1, 6, 7], # 16
        [5, 0, 3],
        [4, 8, 2]]

    G = [[7, 1, 2], 
        [4, 8, 5],  # 20
        [6, 3, 0]]

    H = [[0, 7, 2], # 24
        [4, 6, 1],
        [3, 5, 8]]

    I = [[8, 6, 7], # 31
        [2, 5, 4],
        [3, 0, 1]]


    puzzleEnd = [[1, 2, 3], 
                 [4, 5, 6], 
                 [7, 8, 0]]

    generalSearch(G, puzzleEnd, 3)
    
    
main()