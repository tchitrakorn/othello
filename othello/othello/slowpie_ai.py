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

    parity = compute_utility(board, color) / (len(board) * len(board)) * 10
    corner_captured = compute_corner_captured(board, color) / 4 * 70
    side_captured = compute_side_captured(board, color) / ((len(board) * 4) - 4) * 20
    # mobility = compute_mobility(board, color) / (len(board) * len(board)) * 5

    score = parity + corner_captured + side_captured

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

def compute_side_captured(board, color):
    
    result = 0
    side_value = 50

    for row in range(0, len(board)):
        result += side_value if board[row][0] == color else 0
        result += side_value if board[row][len(board) - 1] == color else 0

    for col in range(1, len(board) - 1):
        result += side_value if board[0][col] == color else 0
        result += side_value if board[len(board) - 1][col] == color else 0

    return result

def compute_mobility(board, color):
    return len(get_possible_moves(board, color))

def compute_is_half_done(board):
    total = len(board) * len(board)
    occupied = 0
    for row in board:
        for cell in row:
            if cell == 0 or cell == 1:
                occupied += 1
    return occupied > (total // 2)

def get_best_moves(board, color, all_moves):
    corners = [ (0, 0), (len(board) - 1, len(board) - 1), (0, len(board) - 1), (len(board) - 1, 0) ]
    adj_corners  =[ (0, 1), (1, 0), (1, 1), (0, len(board) - 2), (1, len(board) - 1), (1, len(board) - 2), 
    (len(board) - 1, 1), (len(board) - 2, 0), (len(board) - 2, 1), (len(board) - 1, len(board) - 2), 
    (len(board) - 2, len(board) - 1), (len(board) - 2, len(board) - 2) ]

    is_half_done = compute_is_half_done(board)
    
    output = []
    corner_moves = []
    sides = []
    adj_corner_moves = []
    adj_sides = []
    other_moves = []

    for move in all_moves:
        if move in corners:
            if len(corner_moves) == 0 or not is_half_done:
                corner_moves.append(move)
            else:
                current_gain = compute_gain(board, color, move)
                old_gain = compute_gain(board, color, corner_moves[0])
                if current_gain > old_gain:
                    corner_moves.insert(0, move)
                else:
                    corner_moves.append(move)
        elif move in adj_corners:
            if len(adj_corner_moves) == 0 or not is_half_done:
                adj_corner_moves.append(move)
            else:
                current_gain = compute_gain(board, color, move)
                old_gain = compute_gain(board, color, adj_corner_moves[0])
                if current_gain > old_gain:
                    adj_corner_moves.insert(0, move)
                else:
                    adj_corner_moves.append(move)
        elif move[0] == 0 or move[0] == (len(board) - 1) or move[1] == 0 or move[1] == (len(board) - 1):
            if len(sides) == 0 or not is_half_done:
                sides.append(move)
            else:
                current_gain = compute_gain(board, color, move)
                old_gain = compute_gain(board, color, sides[0])
                if current_gain > old_gain:
                    sides.insert(0, move)
                else:
                    sides.append(move)
        elif move[0] == 1 or move[0] == (len(board) - 2) or move[1] == 1 or move[1] == (len(board) - 2):
            if len(adj_sides) == 0 or not is_half_done:
                adj_sides.append(move)
            else:
                current_gain = compute_gain(board, color, move)
                old_gain = compute_gain(board, color, adj_sides[0])
                if current_gain > old_gain:
                    adj_sides.insert(0, move)
                else:
                    adj_sides.append(move)
        else:
            if len(other_moves) == 0 or not is_half_done:
                other_moves.append(move)
            else:
                current_gain = compute_gain(board, color, move)
                old_gain = compute_gain(board, color, other_moves[0])
                if current_gain > old_gain:
                    other_moves.insert(0, move)
                else:
                    other_moves.append(move)
    
    if len(corner_moves) != 0:
        output += corner_moves
    elif len(sides) != 0:
        output += sides
    elif len(other_moves) != 0:
        output += other_moves
    elif len(adj_corner_moves) != 0:
        output += adj_corner_moves
    output += adj_sides
    return output

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

    opp_moves = get_best_moves(board, color, opp_moves)
    
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

    opp_moves = get_best_moves(board, color, opp_moves)
    
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

def compute_gain(board, color, move):
    total_gain = 0
    lines = find_lines(board, move[0], move[1], color)
    for line in lines:
        total_gain += len(line)
    return total_gain

    
############ ALPHA-BETA PRUNING #####################

#alphabeta_min_node(board, color, alpha, beta, level, limit)
def alphabeta_min_node(board, color, depth, alpha, beta, start_time): 

    opp_color = 1 if color == 2 else 2
    opp_moves = get_possible_moves(board, color)

    if len(opp_moves) == 0:
        return (compute_utility(board, color), None)

    if time.time() - start_time > 9.5:
        return (compute_heuristic(board, color), None)

    # if depth == 0:
    #     return (compute_heuristic(board, color), None)
    
    global_move = None
    global_min = sys.maxsize

    opp_moves = get_best_moves(board, color, opp_moves)

    for move in opp_moves:
        new_board = play_move(board, color, move[0], move[1]) 
        current_min, current_move = alphabeta_max_node(new_board, opp_color, depth - 1, alpha, beta, start_time)
        if current_min < beta:
            beta = current_min
            global_move = move
            if beta <= alpha:
                break
     
    return (beta, global_move)


#alphabeta_max_node(board, color, alpha, beta, level, limit)
def alphabeta_max_node(board, color, depth, alpha, beta, start_time):
    opp_color = 1 if color == 2 else 2
    opp_moves = get_possible_moves(board, color)

    if len(opp_moves) == 0 :
        return (compute_utility(board, color), None)

    if time.time() - start_time > 9.5:
        return (compute_heuristic(board, color), None)

    # if depth == 0:
    #     return (compute_heuristic(board, color), None)
    
    global_move = None
    global_max = -sys.maxsize - 1

    opp_moves = get_best_moves(board, color, opp_moves)
    
    for move in opp_moves:
        new_board = play_move(board, color, move[0], move[1]) 
        current_max, current_move = alphabeta_min_node(new_board, opp_color, depth - 1, alpha, beta, start_time)
        if current_max > alpha:
            alpha = current_max
            global_move = move
            if alpha >= beta:
                break
     
    return (alpha, global_move)


def select_move_alphabeta(board, color): 
    start_time = time.time()
    return alphabeta_max_node(board, color, 8, -sys.maxsize - 1, sys.maxsize, start_time)[1]


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
