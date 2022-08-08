#!/usr/bin/env python3
# -*- coding: utf-8 -*

"""
An AI player for Othello. This is the template file that you need to  
complete.

@author: YOUR NAME AND UNI 
"""

import random
import sys
import time
import logging

# You can use the functions in othello_shared to write your AI 
from othello_shared import find_lines, get_possible_moves, get_score, play_move

def compute_utility(board, color):
    score = get_score(board)
    if color == 1:
        return score[0] - score[1]
    return score[1] - score[0]

def compute_heuristic(board, color):
    score = 0
    parity = compute_utility(board, color) / (len(board) * len(board)) * 25
    corner_captured = compute_corner_captured(board, color) / 4 * 75
    score = parity + corner_captured
    return score

def compute_corner_captured(board, color):

    result = 0

    corner_value = 100
    result += corner_value if board[0][0] == color else 0
    result += corner_value if board[0][len(board) - 1] == color else 0
    result += corner_value if board[len(board) - 1][0] == color else 0
    result += corner_value if board[len(board) - 1][len(board) - 1] else 0

    side_corner_value = 10
    result -= side_corner_value if board[0][1] == color else 0
    result -= side_corner_value if board[1][0] == color else 0
    result -= side_corner_value if board[1][1] == color else 0
    result -= side_corner_value if board[0][len(board) - 2] == color else 0
    result -= side_corner_value if board[1][len(board) - 1] == color else 0
    result -= side_corner_value if board[1][len(board) - 2] == color else 0
    result -= side_corner_value if board[len(board) - 1][1] == color else 0
    result -= side_corner_value if board[len(board) - 2][0] == color else 0
    result -= side_corner_value if board[len(board) - 2][1] == color else 0
    result -= side_corner_value if board[len(board) - 1][len(board) - 2] else 0
    result -= side_corner_value if board[len(board) - 2][len(board) - 1] else 0
    result -= side_corner_value if board[len(board) - 2][len(board) - 2] else 0
    #logging.basicConfig(level=logging.INFO)
    #logging.info(result)
    return result

############ MINIMAX ###############################

def minimax_min_node(board, color, depth):
    
    opp_color = 1 if color == 2 else 2
    opp_moves = get_possible_moves(board, color)

    if len(opp_moves) == 0:
        return (compute_utility(board, color), None)

    if depth == 0:
        return (compute_heuristic(board, color), None)
    
    global_move = None
    global_min = sys.maxsize
    
    for move in opp_moves:
        new_board = play_move(board, color, move[0], move[1]) 
        current_min, current_move = minimax_max_node(new_board, opp_color, depth - 1)
        #logging.basicConfig(level=logging.INFO)
        #logging.info("{curMax}, {curMoveX}, {curMoveY}".format(curMax = current_min,curMoveX = move[0],curMoveY=move[1]))
        if current_min < global_min:
            global_min = current_min
            global_move = move
     
    return (global_min, global_move)


def minimax_max_node(board, color, depth):
    opp_color = 1 if color == 2 else 2
    opp_moves = get_possible_moves(board, color)

    if len(opp_moves) == 0:
        return (compute_utility(board, color), None)

    if depth == 0:
        return (compute_heuristic(board, color), None)
    
    global_move = None
    global_max = -sys.maxsize - 1
    
    for move in opp_moves:
        new_board = play_move(board, color, move[0], move[1]) 
        current_max, current_move = minimax_min_node(new_board, opp_color, depth - 1)
        #logging.basicConfig(level=logging.INFO)
        #logging.info("{curMax}, {curMoveX}, {curMoveY}".format(curMax = current_max,curMoveX = move[0],curMoveY=move[1]))
        if current_max > global_max:
            global_max = current_max
            global_move = move
     
    return (global_max, global_move)

    
def select_move_minimax(board, color):
    """
    Given a board and a player color, decide on a move. 
    The return value is a tuple of integers (i,j), where
    i is the column and j is the row on the board.  
    """
    #logging.basicConfig(level=logging.INFO)
    #logging.info("{board}".format(board=board))
    return minimax_max_node(board, color, 4)[1]
    
############ ALPHA-BETA PRUNING #####################

#alphabeta_min_node(board, color, alpha, beta, level, limit)
def alphabeta_min_node(board, color, depth, alpha, beta): 

    opp_color = 1 if color == 2 else 2
    opp_moves = get_possible_moves(board, color)

    if len(opp_moves) == 0:
        return (compute_utility(board, color), None)

    if depth == 0:
        return (compute_heuristic(board, color), None)
    
    global_move = None
    global_min = sys.maxsize
    
    for move in opp_moves:
        new_board = play_move(board, color, move[0], move[1]) 
        current_min, current_move = alphabeta_max_node(new_board, opp_color, depth - 1, alpha, beta)
        if current_min < beta:
            beta = current_min
            global_move = move
            if beta <= alpha:
                break
     
    return (beta, global_move)


#alphabeta_max_node(board, color, alpha, beta, level, limit)
def alphabeta_max_node(board, color, depth, alpha, beta):
    opp_color = 1 if color == 2 else 2
    opp_moves = get_possible_moves(board, color)

    if len(opp_moves) == 0:
        return (compute_utility(board, color), None)

    if depth == 0:
        return (compute_heuristic(board, color), None)
    
    global_move = None
    global_max = -sys.maxsize - 1
    
    for move in opp_moves:
        new_board = play_move(board, color, move[0], move[1]) 
        current_max, current_move = alphabeta_min_node(new_board, opp_color, depth - 1, alpha, beta)
        if current_max > alpha:
            alpha = current_max
            global_move = move
            if alpha >= beta:
                break
     
    return (alpha, global_move)


def select_move_alphabeta(board, color): 
    return alphabeta_max_node(board, color, 6, -sys.maxsize - 1, sys.maxsize)[1]


####################################################
def run_ai():
    """
    This function establishes communication with the game manager. 
    It first introduces itself and receives its color. 
    Then it repeatedly receives the current score and current board state
    until the game is over. 
    """
    print("Minimax AI") # First line is the name of this AI  
    color = int(input()) # Then we read the color: 1 for dark (goes first), 
                         # 2 for light. 

    while True: # This is the main loop 
        # Read in the current game status, for example:
        # "SCORE 2 2" or "FINAL 33 31" if the game is over.
        # The first number is the score for player 1 (dark), the second for player 2 (light)
        next_input = input() 
        status, dark_score_s, light_score_s = next_input.strip().split()
        dark_score = int(dark_score_s)
        light_score = int(light_score_s)

        if status == "FINAL": # Game is over. 
            print 
        else: 
            board = eval(input()) # Read in the input and turn it into a Python
                                  # object. The format is a list of rows. The 
                                  # squares in each row are represented by 
                                  # 0 : empty square
                                  # 1 : dark disk (player 1)
                                  # 2 : light disk (player 2)
                    
            # Select the move and send it to the manager
            
            
            #movei,movej = select_move_minimax(board, color)
            movei, movej = select_move_alphabeta(board, color)
            print("{} {}".format(movei, movej)) 


if __name__ == "__main__":
    run_ai()
