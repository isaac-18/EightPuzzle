def welcome():
    print('Welcome to Isaac\'s 8-puzzle solver.')
    puzzleChoice = int(input('Type “1” to use a default puzzle, or “2” to enter your own puzzle. '))

    rows, cols = (3, 3)
    puzzle = [[0 for i in range(cols)] for j in range(rows)]
    if puzzleChoice == 1:
        # Default puzzle
        puzzle = [[1, 2, 3], 
                  [4, 8, 0], 
                  [7, 6, 5]]
    elif puzzleChoice == 2:
        print('Enter your puzzle. Use a zero to represent the blank and use space or tabs between numbers.')
        for i in range(rows):
            try:
                # Take multiple inputs using list comprehension. Uses maxsplit argument of split() to ensure valid input
                puzzle[i] = [int(item) for item in input('Row {}: '.format(i+1)).split(None, cols - 1)] 
            except:
                print('You can only input {} numbers per row. Try again.'.format(cols))
                return -1
    for row in puzzle:
        print(row)

    print('Enter your choice of algorithm: ')
    print(' 1. Uniform Cost Search\n 2. A* with the Misplaced Tile heuristic.\n 3. A* with the Manhattan distance heuristic.')
    algoChoice = int(input())

welcome()