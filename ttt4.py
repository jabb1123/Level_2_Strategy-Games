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


def create_board (str):
    return [' '] * 16
    

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
                print 'type',type(board)
                sys.stdout.write(board[i*4+k])
        print ''
    print


def read_player_input (board, player):
    # FIX ME
    #
    # Read player input when playing as 'player' (either 'X' or 'O')
    # Return a move (a tuple (x,y) with each position between 1 and 4)
    return None

def make_move (board,move,mark):
    new_board = board[:]
    new_board[move] = mark
    return new_board

def computer_move (board,player):
    # FIX ME
    #
    # Select a move for the computer, when playing as 'player' (either 
    #   'X' or 'O')
    # Return the selected move (a tuple (x,y) with each position between 
    #   1 and 4)
    return None


def other (player):
    if player == 'X':
        return 'O'
    return 'X'


def run (str,player,playX,playO): 

    board = create_board(str)
    print('board0',board[0],type(board[0]))
    print_board(board)

    while not done(board):
        if player == 'X':
            move = playX(board,player)
        elif player == 'O':
            move = playO(board,player)
        else:
            fail('Unrecognized player '+player)
        board = make_move(board,move,player)
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


