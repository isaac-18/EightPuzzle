import queue
import heapq
from copy import deepcopy

# Board Size
ROWS, COLS = (3, 3)

nodesExpanded = 0
maxQueueSize = 1

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
        # global nodesExpanded
        if child not in self.children:
            self.children.append(child)
            # nodesExpanded += 1

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
    def blankCoord(self):
        for x, col in enumerate(self.data):
            try:
                return x, col.index(0)
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


def UCS(start):
    h = 0
    return start.g + h

def MTH(start, goal):
    # Calculate number of misplaced tiles for h
    return

def MDH(start, goal):
    # Distance of blank square to goal position for h
    return

def expand(node, queue):
        puzzle = node.data
        coords = node.blankCoord()
        g = node.g + 1
        global nodesExpanded

        try:
            # Move left
            # print('Moving left')
            newPuzzle = deepcopy(puzzle)
            print(coords)
            if coords[1] != 0:
                newPuzzle[coords[0]][coords[1]], newPuzzle[coords[0]][coords[1]-1] = newPuzzle[coords[0]][coords[1]-1], newPuzzle[coords[0]][coords[1]]
                newNode = Node(newPuzzle, g)
                if (newPuzzle != puzzle) and (newNode not in queue):
                    node.add_child(newNode)
                    nodesExpanded += 1
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
            if (newPuzzle != puzzle) and (newNode not in queue):
                node.add_child(newNode)
                nodesExpanded += 1
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
                if (newPuzzle != puzzle) and (newNode not in queue):
                    node.add_child(newNode)
                    nodesExpanded += 1
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
            if (newPuzzle != puzzle) and (newNode not in queue):
                node.add_child(newNode)
                nodesExpanded += 1
        except:
            # print('Can\'t move down!')
            # print('-------------')
            pass

def generalSearch(puzzleStart, puzzleEnd, queueFunc):
    # Root node/start state
    rootNode = Node(puzzleStart, 0)
    nodes = []
    heapq.heappush(nodes, (0, 0, rootNode))

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
        print('Popped')
        print(node.state())

        if node.state() == puzzleEnd:
            print('Success!')
            print('Expanded {} nodes'.format(nodesExpanded))
            print('The maximum number of nodes in the queue at any one time was {}'.format(maxQueueSize))
            print('The depth of the goal node was {}'.format(node.g))
            # return node ?
            return
        
        if queueFunc == 1:
            # Expands the parent node and places all the children in queue.
            # Priority queue deals with ordering. Then we pop off highest priority 
            # child and repeat this process.
            
            # node.expand()
            expand(node, nodes)
            print('Expanding {} children'.format(len(node.get_children())))
            for child in node.get_children():
                queuePosition += 1
                if child not in nodes:
                    heapq.heappush(nodes, (UCS(child), queuePosition, child))
                    child.display()
                    print('-------------')
                    # nodesExpanded += 1
            print('Next level')
            print('===============')

        # elif queueFunc == 2:
        #     node.expand()
        #     nodesExpanded += 1
        #     for child in node.children:
        #         nodes.put(MTH(child, puzzleEnd), child)
        # elif queueFunc == 3:
        #     node.expand()
        #     nodesExpanded += 1
        #     for child in node.children:
        #         nodes.put(MDH(child, puzzleEnd), child)
    

def main():
    # welcome()
    puzzle = [[0 for i in range(COLS)] for j in range(ROWS)]
    puzzle = [[1, 2, 3], 
              [4, 5, 6], 
              [0, 7, 8]]
    # puzzle = [[1, 2, 3], 
    #           [5, 0, 6], 
    #           [4, 7, 8]] # AB 23 iterations 4 depth
    
    puzzleEnd = [[1, 2, 3], 
                 [4, 5, 6], 
                 [7, 8, 0]]

    generalSearch(puzzle, puzzleEnd, 1)
    
    
main()