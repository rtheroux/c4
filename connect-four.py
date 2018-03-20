################################################################################
## File:    connect-four.py
## Author:
## Date:
## Collaborators:
################################################################################

import sys


class ConnectFour:
    '''
    Connect Four has a 6-high, 7-wide board. Players alternate placing colored
    pieces. Each piece can be dropped into a column and rests on top of the
    last placed piece in that column, or the bottom of the column if no piece
    has yet been placed in it. Four in a row---up, across, or diagonal---wins
    the game.
    '''
    def __init__(self):
        pass

    def getInitialState(self):
        '''
        States are formatted as: (current player mark, (board))
        where (board) is a 2D tuple with '' for empty spaces,
        'x' for player 1 spaces, and 'o' for player 2 spaces.

        'x' is considered the main player, so an evaluation of 1 means player 1
        wins, and -1 means player 'o' wins.
        '''
        ## TODO Update this for the Connect Four board. You'll probably want to
        ## generate it automatically rather than hard coding it.
        initialList = [['' for x in range(7)] for x in range(6)]

        # print "column", column
        print "list", initialList

        return ('', initialList)


    ## TODO This function doesn't make sense for Connect Four, but you can
    ## probably modify it's name and behavior to apply to Connect Four.
    def playerWith3InRow(self, board):
        '''
        Determines which player, if any, has three in a row.

        @param board The game board.
        @return 'x' or 'o' if either have three in a row, '' otherwise.
        '''
        ## check rows
        for i in range(3):
            if( board[i][0] != '' and
                board[i][0] == board[i][1] and board[i][1] == board[i][2]):
                return board[i][0]

        ## check columns
        for j in range(3):
            if( board[0][j] != '' and
                board[0][j] == board[1][j] and board[1][j] == board[2][j]):
                return board[0][j]

        ## check diagonals
        if( board[0][0] != '' and
            board[0][0] == board[1][1] and board[1][1] == board[2][2]):
            return board[0][0]
        if( board[2][0] != '' and
            board[2][0] == board[1][1] and board[1][1] == board[0][2]):
            return board[2][0]

        return ''

    def numEmptySpots(self, state):
        '''
        Counts the number of empty spaces on the board.

        @param state Should be in the format: [player, board, move]
        @return The number of empty spots.
        '''
        count = 0
        for row in state[1]:
            for cell in row:
                if cell == '':
                    count+=1
        return count

    def countPattern(self, board, pattern):
        '''
        Counts the number of times the given pattern occurs on the board.

        @param board The game board.
        @param pattern A list of three characters to search for.
        @return The number of times the given pattern occurs on the board.
        '''
        ## TODO This currently doesn't search over a board of the size used for
        ## Connect Four.
        count = 0
        for i in range(3):
            if(board[i][0] == pattern[0] and board[i][1] == pattern[1] and
                board[i][2] == pattern[2]):
                count += 1

        for j in range(3):
            if(board[0][j] == pattern[0] and board[1][j] == pattern[1] and
                board[2][j] == pattern[2]):
                count += 1

        if(board[0][0] == pattern[0] and board[1][1] == pattern[1] and
            board[2][2] == pattern[2]):
            count += 1
        if(board[2][0] == pattern[0] and board[1][1] == pattern[1] and
            board[0][2] == pattern[2]):
            count += 1

        return count

    def evaluateState(self, state):
        '''
        Evaluates the given state. If a terminal, then a 1 is returned if 'x'
        won, -1 if 'o' won, or 0 if it's a draw.

        If not a terminal state, then an estimate is made.

        @param state Should be in the format: [player, board, move]
        @return Either the exact utility if this is a terminal state or an
            estimate otherwise.
        '''

        ## TODO Update this to work for Connect Four. Because of the search
        ## space required for Connect Four, you will need a good evaluation
        ## function, so think about what makes sense. Try some different things
        ## out and see which causes agent's to make better decisions.


        threeInARow = self.playerWith3InRow(state[1])
        if threeInARow == 'x':
            # print "x's win:"
            # self.printBoard(state)
            return 1
        elif threeInARow == 'o':
            # print "o's win:"
            # self.printBoard(state)
            return -1
        elif self.numEmptySpots(state) == 0:
            return 0

        ## Evaluation function:
        ## If we reached here, we need estimate the cost.
        ## Let's do: (.75 * #xx_ + .25*#x__) - (.75 * #oo_ + .25*#o__)
        counts = {'x': 0, 'o': 0}
        for c in ['x', 'o']:
            counts[c] = (
                0.75 * (self.countPattern(state[1], [c,c,'']) +
                        self.countPattern(state[1], ['',c,c])) +
                0.25 * (self.countPattern(state[1], [c,'','']) +
                        self.countPattern(state[1], ['','',c]) +
                        self.countPattern(state[1], ['',c,'']))
            )

        return counts['x'] - counts['o']


    def isGoalState(self, state):
        '''
        Tests if the current state is a goal state (either someone has won
        or it was a draw).

        @param state Should be in the format: [player, board, move]
        '''

        ## TODO This needs a slight tweak to make sense.

        return self.numEmptySpots(state) == 0 or self.playerWith3InRow(state[1]) != ''


    def getSuccessors(self, state):
        '''
        Gets the successors of state.

        @param state Should be in the format: [player, board, move]
        @return A list of states, where each state is
            [next player, next board, next move] -- 'next board' shows the
            outcome of 'next player' making 'next move' on the previous board.
        '''

        ## TODO Update this. Remember that in Tic Tac Toe, you can move into any
        ## empty space -- that's not true in Connect Four. There are at most
        ## 6 valid successors.

        nextPlayer = 'x'
        if state[0] == 'x':
            nextPlayer = 'o'

        successors = []

        # for i in range(6):
        #     for j in range(7):
        #         if state[1][i][j] == '':
        #             newBoard = [row[:] for row in state[1]]
        #             newBoard[i][j] = nextPlayer
        #             successors.append((nextPlayer, newBoard, (i,j)))
        for j in range(7):
            if state[1][5][j] == '':
                newBoard = [row[:] for row in state[1]]
                newBoard[5][j] = nextPlayer
                state1 = (nextPlayer, newBoard, (5,j))
                successors.append(state1)
                # self.printBoard(state1)
                # print '\n', '\n'


        for i in range(5):
            for j in range(7):
                if state[1][i][j] == '' and state[1][i+1][j] != '':
                    # print i,j
                    newBoard = [row[:] for row in state[1]]
                    newBoard[i][j] = nextPlayer
                    successors.append((nextPlayer, newBoard, (i,j)))

        return successors

    def printBoard(self, state):
        '''
        Prints the board.

        @param state Should be in the format: [player, board, move]
        '''

        ## TODO Update this. Needs a minor tweak.

        for i in range(6):
            for j in range(7):
                c = state[1][i][j]
                if c == '': #and j != 1 or i != 1:
                    c = '_'
                # elif c == '' and j == 1 and i == 1:
                #     c = 'Q'
                sys.stdout.write('{:2} '.format(c))
            print ''


    def isMaxState(self, state):
        '''
        Decides if this is a state to be maximized or minimized. If player
        is 'o' or '', then 'x' has the next move and therefore is considered
        a maximizer.

        @param state Should be in the format: [player, board, move]
        @return True if this 'x' has the next move.
        '''
        return state[0] == 'o' or state[0] == ''



## TODO This should work with your reformulation of Tic Tac Toe to Connect Four,
## but needs Alpha Beta pruning. I strongly suggest that you first get your
## representation of Connect Four working with this (probably with a depth of
## 10 or so), and only move to Alpha Beta after you have Connect Four working
## with the non-pruning version.

## Minimax with optional depth.
def minimax(problem, state, depth=-1):
    if problem.isGoalState(state) or depth==0:
        return [state, problem.evaluateState(state)]
    elif problem.isMaxState(state):
        return maxValue(problem, state, depth)
    else:
        return minValue(problem, state, depth)

def minValue(problem, state, depth):
    minUtility = 999999
    minSuccessor = None
    for successor in problem.getSuccessors(state):
        tmp = minimax(problem, successor, depth-1)
        if tmp[1] < minUtility:
            minUtility = tmp[1]
            minSuccessor = successor
    return [minSuccessor, minUtility]

def maxValue(problem, state, depth):
    maxUtility = -999999
    maxSuccessor = None
    for successor in problem.getSuccessors(state):
        tmp = minimax(problem, successor, depth-1)
        if tmp[1] > maxUtility:
            maxUtility = tmp[1]
            maxSuccessor = successor
    return [maxSuccessor, maxUtility]



def aiVsAi(depth):
    connectFour = ConnectFour()
    startState = connectFour.getInitialState()
    print "Current board:"
    connectFour.printBoard(startState)


    currentState = startState
    while not connectFour.isGoalState(currentState):
        (currentState, utility) = minimax(connectFour, currentState, depth)
        print "Player {} next move: {} (utility: {})".format(currentState[0], currentState[2], utility)
        connectFour.printBoard(currentState)
        print "="*80

def humanVsAi(depth):
    ## TODO Implement this. Have the player go first and alternate turns between
    ## the human and the AI.
    pass


gameType = raw_input("Please select an option:\n[a] Human vs AI\n[b] AI vs AI")
depth = raw_input("What depth would you like to use for minimax? Use -1 to search the entire space: ")
if gameType == 'a':
    humanVsAi(int(depth))
else:
    aiVsAi(int(depth))
