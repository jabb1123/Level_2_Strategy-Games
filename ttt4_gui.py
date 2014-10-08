#!/usr/bin/env python
# 
#
#
# Game Programming, Level 2 Project
#
# TIC-TAC-TOE 4
# Jack Fan
# Jacob Riedel
#
# A simple strategy game, an extension of the standard 3x3 tic-tac-toe
#
# We tested the minimax and found out that when there are six pieces on the board,
# the waiting time is around 1 min which is acceptable.
# We decided to write some predetermined sequences of moves as look up for the AI.
# Note that the first six moves are extremely fast, and then minimax takes over.
# We used a 1D array rather than a 2D array to represent the board.
# We also added a "neighbor" function that returns the list of neighbor positions.
# This is useful in the predetermined sequences of moves.

# The strategy the AI uses for the predetermined sequence depends on whether it 
# goes first or second. If it goes first, it utilizes the "offense" function and the
# "defense" function otherwise. The reason we chose this approach is because there is 
# no guaranteed win sequence of moves in the first 6 moves. Theoretically, we can
# randomly choose 6 positions and still guarantee a draw.

import sys
from graphics import *

GRIDSIZE = 150

def fail (msg):
    raise StandardError(msg)

WIN_SEQUENCES = [
    [0,1,2,3],
    [4,5,6,7],
    [8,9,10,11],
    [12,13,14,15],
    [0,4,8,12],
    [1,5,9,13],
    [2,6,10,14],
    [3,7,11,15],
    [0,5,10,15],
    [3,6,9,12]
]

MARK_VALUE = {
    'O': 1,
    ' ': 0,
    'X': 10
}

CORNER = {0,3,12,15}
SIDE = {1,2,4,7,8,11,13,14}
CENTER = {5,6,9,10}

def create_board (string='................'):
    board = []
    for i in string:
        if i == '.':
            board.append(' ')
        else:
            board.append(i) 
    return board
    

    # Take a description of the board as input and create the board
    #  in your representation
    #
    # The string description is a sequence of 16 characters,
    #   each either X or O, or . to represent a free space
    # It is allowed to pass in a string describing a board
    #   that would never arise in legal play starting from an empty
    #   board
    # return board


# Check if a board is a win for X or for O.
# Return 'X' if it is a win for X, 'O' if it is a win for O,
# and False otherwise
def has_win (board):
    for positions in WIN_SEQUENCES:
        s = sum(MARK_VALUE[board[pos]] for pos in positions)
        if s == 4:
            return 'O'
        if s == 40:
            return 'X'
    return False

# Check if the board is done, either because it is a win or a draw
def done (board):
    return (has_win(board) or not [ e for e in board if (e == ' ')])

def print_board (board):
    for i in range(4):
        if i*4 == 12:
            sys.stdout.write(str(i*4) + ' |')
        else:
            sys.stdout.write(str(i*4) + '  |')
        for k in range(4):
            sys.stdout.write('  ')
            if board[i*4+k] == ' ':
                sys.stdout.write('.')
            else:
                sys.stdout.write(board[i*4+k])
        print ''
    print


# Read player input when playing as 'player' (either 'X' or 'O')
# Return a move (an integer)
def read_player_input (board,player,window):
    valid = [ i for (i,e) in enumerate(board) if e == ' ']
    while True:
        move = raw_input('Position (0-15)? ')
        if move == 'q':
            exit(0)
        if len(move)>0 and int(move) in valid:
            return int(move)

# return a new board with a move made by a player
def make_move (board,move,mark):
    new_board = board[:]
    new_board[move] = mark
    return new_board

# return list of possible moves in a given board
def possible_moves (board):
    return [i for (i,e) in enumerate(board) if e == ' ']

# return list of X positions in a given board
def xPos (board):
    return [i for (i,e) in enumerate(board) if e == 'X']

# return list of O positions in a given board
def oPos (board):
    return [i for (i,e) in enumerate(board) if e == 'O']

# return a list of neighbor positions of the specified position
def neighbor (mark):
    neighbor=[]
    neighbor.extend([i for i in [mark+4,mark-4] if i >= 0 and i <= 15])
    neighbor.extend([i for i in [mark+1,mark-1] if i >= 0 and i <= 15 and i/4==mark/4])
    return neighbor

# runs in place of minimax in the first six moves of the game
# redirect to either offense() or defense()
def predefined_moves(board,player):
    Xnum = len([i for (i,e) in enumerate(board) if e == 'X'])
    Onum = len([i for (i,e) in enumerate(board) if e == 'O'])
    if Onum == Xnum:
        return offense(board,player)
    else:
        return defense(board,player)

# the strategy the computer uses for the first six moves of the game if it made the
# first move
def offense(board,player):
    opp = other(player)
    if opp == 'X':
        enemy = xPos(board)
        mark = oPos(board)
    else:
        enemy = oPos(board)
        mark = xPos(board)
    pieces = len(possible_moves(board))
    if pieces == 16:
        return (0,5)
    elif pieces == 14:
        mark = mark[0]
        no_opp = False
        for i in neighbor(mark):
            for j in neighbor(i):
                if board[j] == opp:
                    no_opp = False
                    break
                else:
                    no_opp =True
            if no_opp == True:
                return (0,i)
    elif pieces == 12:
        for positions in WIN_SEQUENCES:
            s = sum(MARK_VALUE[board[pos]] for pos in positions)
            if player == 'X' and s == 20 or player == 'O' and s == 2:
                for move in positions:
                    if move not in mark:
                        for i in neighbor(move):
                            if opp == board[i]:
                                return (0,move)
                return (0,[move for move in positions if move not in mark][0])
            else:
                for i in CENTER:
                    if board[i] == ' ':
                        return (0,i)


# the strategy the computer uses for the first six moves of the game if it made the
# second move
def defense(board,player):
    opp = other(player)
    if opp == 'X':
        enemy = xPos(board)
    else:
        enemy = oPos(board)
    pieces = len(possible_moves(board))
    if pieces == 15:
        if enemy[0] == 0:
            return (0,5)
        elif enemy[0] == 3:
            return (0,6)
        elif enemy[0] == 12:
            return (0,9)
        elif enemy[0] == 15:
            return (0,10)
        elif enemy[0] in [1,4,5]:
            return (0,0)
        elif enemy[0] in [2,6,7]:
            return (0,3)
        elif enemy[0] in [8,9,13]:
            return (0,12)
        elif enemy[0] in [10,11,14]:
            return (0,15)
    elif pieces == 13 or pieces == 11:
        for positions in WIN_SEQUENCES:
            s = sum(MARK_VALUE[board[pos]] for pos in positions)
            if opp == 'X' and s == 20 or opp == 'O' and s == 2:
                for move in positions:
                    if move not in enemy:
                        for i in neighbor(move):
                            if player == board[i]:
                                return (0,move)
                return (0,[move for move in positions if move not in enemy][0])
            else:
                for i in CENTER:
                    if board[i] == ' ':
                        return (0,i)

        




# Select a move for the computer, when playing as 'player' (either 
#   'X' or 'O')
def computer_move (board,player,window):
    if len(possible_moves(board)) >= 11:
        return predefined_moves(board,player)

    bestMove = []
    if player == 'O':
        for i in possible_moves(board):
            new_board = make_move(board,i,'O')
            if done(new_board) == 'O':
                return (1,i)
            elif done(new_board) == True:
                bestMove.insert(0,(0,i))                
            else:
                next = computer_move(new_board,'X',window)
                if next[0] == -1:
                    return (1,i)
                elif next[0] == 1:
                    bestMove.append((-1,i))
                else:
                    bestMove.insert(0,(0,i))
    else:
        for i in possible_moves(board):
            new_board = make_move(board,i,'X')
            if done(new_board) == 'X':
                return (1,i)
            elif done(new_board) == True:
                bestMove.insert(0,(0,i))
            else:
                next = computer_move(new_board,'O',window)
                if next[0] == -1:
                    return (1,i)
                elif next[0] == 1:
                    bestMove.append((-1,i))
                else:
                    bestMove.insert(0,(0,i))
    return bestMove[0]

def other (player):
    if player == 'X':
        return 'O'
    return 'X'

# GUI initialization
def gui_init (board):
    window = GraphWin('Tic-Tac-Toe 4x4', GRIDSIZE*4, GRIDSIZE*4)
    for i in range(1,4):
        Line(Point(0,GRIDSIZE*i),Point(GRIDSIZE*4,GRIDSIZE*i)).draw(window)
        Line(Point(GRIDSIZE*i,0),Point(GRIDSIZE*i,GRIDSIZE*4)).draw(window)
    window.setBackground('white')
    return window

# draws on the GUI
def draw_board (board, window):
    for i in range(4):
        for k in range(4):
            if board[i*4+k] == ' ':
                continue
            elif board[i*4+k] == 'X':
                X = Text(Point(GRIDSIZE/2+k*GRIDSIZE,GRIDSIZE/2+i*GRIDSIZE),board[i*4+k])
                X.setSize(36)
                X.setTextColor('blue')
                X.draw(window)
            else:
                O = Text(Point(GRIDSIZE/2+k*GRIDSIZE,GRIDSIZE/2+i*GRIDSIZE),board[i*4+k])
                O.setSize(36)
                O.setTextColor('red')
                O.draw(window)

# GUI mouse interactions
def wait_player_input (board,player,window):
    while True:
        valid = [ i for (i,e) in enumerate(board) if e == ' ']
        mouse = window.getMouse()
        move = mouse.getY()/GRIDSIZE*4 + mouse.getX()/GRIDSIZE
        if move in valid:
            return move

# draws the ending texts on the GUI
def ending(winner,window):
    if winner != False:
        text = Text(Point(GRIDSIZE*2,GRIDSIZE*2), winner + ' has won the game!\n Press anywhere to exit.')
    else:
        text = Text(Point(GRIDSIZE*2,GRIDSIZE*2), 'It\'s a draw game!\n Press anywhere to exit.')
    text.setSize(36)
    text.setStyle('bold')
    text.draw(window)
    mouse = window.getMouse()
    window.close()


def run (string,player,playX,playO): 

    board = create_board(string)
    window = gui_init(board)
    draw_board(board,window)
    print_board(board)
    while not done(board):
        if player == 'X': 
            move = playX(board,player,window)
        elif player == 'O':
            move = playO(board,player,window)
        else:
            fail('Unrecognized player '+player)
        if type(move) == tuple:
            move = move[1]
        board = make_move(board,move,player)
        draw_board(board, window)
        print_board(board)
        print player,'chose',move
        player = other(player)

    winner = has_win(board)
    if winner:
        ending(winner,window)
        print winner,'wins!'
    else:
        ending(winner,window)
        print 'Draw'
        
def main ():
    run('.' * 16, 'X', read_player_input, computer_move)


# read_player_input allows you to play the console I/O version of the game
# wait_player_input lets you play the GUI version of the game
# please comment out line to turn off GUI
PLAYER_MAP = {
    #'human': read_player_input,
    'human': wait_player_input,
    'computer': computer_move
}

if __name__ == '__main__':
    try:
        string = sys.argv[1] if len(sys.argv)>1 else '.' * 16
        player = sys.argv[2] if len(sys.argv)>3 else 'X'
        playX = PLAYER_MAP[sys.argv[3]] if len(sys.argv)>3 else wait_player_input
        playO = PLAYER_MAP[sys.argv[4]] if len(sys.argv)>4 else computer_move
    except:
        print 'Usage: %s [starting board] [X|O] [human|computer] [human|computer]' % (sys.argv[0])
        exit(1)
    run(string,player,playX,playO)


