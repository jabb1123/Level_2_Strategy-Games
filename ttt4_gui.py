#!/usr/bin/env python
# 

#
# Game Programming, Level 2 Project
#
# TIC-TAC-TOE 4
#
# A simple strategy game, an extension of the standard 3x3 tic-tac-toe
#

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

def create_board (str='................'):
    board = []
    for i in str:
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
    return board

def has_mark (board,x,y):
    # FIX ME
    #
    # Take a board representation and checks if there's a mark at
    #    position x, y (each between 1 and 4)
    # Return 'X' or 'O' if there is a mark
    # Return False if there is not
    return None

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
        for k in range(4):
            sys.stdout.write('  ')
            if board[i*4+k] == ' ':
                sys.stdout.write('.')
            else:
                sys.stdout.write(board[i*4+k])
        print ''
    print


# Read player input when playing as 'player' (either 'X' or 'O')
# Return a move (a tuple (x,y) with each position between 1 and 4)

def read_player_input (board,player):
    valid = [ i for (i,e) in enumerate(board) if e == ' ']
    while True:
        move = raw_input('Position (0-15)? ')
        if move == 'q':
            exit(0)
        if len(move)>0 and int(move) in valid:
            return int(move)

def make_move (board,move,mark):
    new_board = board[:]
    new_board[move] = mark
    return new_board

# return list of possible moves in a given board
def possible_moves (board):
    return [i for (i,e) in enumerate(board) if e == ' ']
    
# Select a move for the computer, when playing as 'player' (either 
#   'X' or 'O')
# Return the selected move (a tuple (x,y) with each position between 
#   1 and 4)

def computer_move (board,player):
    bestMove = []
    if player == 'O':
        for i in possible_moves(board):
            new_board = make_move(board,i,'O')
            if done(new_board) == 'O':
                return (1,i)
            elif done(new_board) == True:
                bestMove.insert(0,(0,i))                
            else:
                next = computer_move(new_board,'X')
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
                next = computer_move(new_board,'O')
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

def gui_init (board):
    window = GraphWin('Tic-Tac-Toe 4x4', GRIDSIZE*4, GRIDSIZE*4)
    for i in range(1,4):
        Line(Point(0,GRIDSIZE*i),Point(GRIDSIZE*4,GRIDSIZE*i)).draw(window)
        Line(Point(GRIDSIZE*i,0),Point(GRIDSIZE*i,GRIDSIZE*4)).draw(window)
    window.setBackground('white')
    return window

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
def run (str,player,playX,playO): 

    board = create_board(str)
    window = gui_init(board)
    draw_board(board,window)
    print_board(board)
    while not done(board):
        if player == 'X': 
            move = playX(board,player)
        elif player == 'O':
            move = playO(board,player)
        else:
            fail('Unrecognized player '+player)
        if type(move) == tuple:
            move = move[1]
        board = make_move(board,move,player)
        draw_board(board, window)
        print_board(board)
        player = other(player)

    winner = has_win(board)
    if winner:
        print winner,'wins!'
    else:
        print 'Draw'
        
def main ():
    run('.' * 16, 'X', read_player_input, computer_move)


PLAYER_MAP = {
    'human': read_player_input,
    'computer': computer_move
}

if __name__ == '__main__':
    try:
        str = sys.argv[1] if len(sys.argv)>1 else '.' * 16
        player = sys.argv[2] if len(sys.argv)>3 else 'X'
        playX = PLAYER_MAP[sys.argv[3]] if len(sys.argv)>3 else read_player_input
        playO = PLAYER_MAP[sys.argv[4]] if len(sys.argv)>4 else computer_move
    except:
        print 'Usage: %s [starting board] [X|O] [human|computer] [human|computer]' % (sys.argv[0])
        exit(1)
    run(str,player,playX,playO)


