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
import math
import logging
import statistics

# You can use the functions in othello_shared to write your AI 
from othello_shared import find_lines, get_possible_moves, get_score, play_move

def compute_utility(board, color):
    (dark, light) = get_score(board)
    if color == dark:
        return dark - light
    else:
        return light - dark


############ MINIMAX ###############################

def minimax_min_node(board, color, depth):
    opp_color = 1 if color == 2 else 2
    possible_moves = get_possible_moves(board, color)
    possible_moves = implement_bias(board, possible_moves)
    if len(possible_moves) == 0 or depth == 0:
        return compute_utility(board, color)
    else:
        min = math.inf
        for possible_move in possible_moves:
            new_board = play_move(board, color, possible_move[0], possible_move[1])
            util = minimax_max_node(new_board, opp_color, depth-1)
            if util < min:
                min = util
        return min


def minimax_max_node(board, color, depth):
    opp_color = 1 if color == 2 else 2
    possible_moves = get_possible_moves(board, color)
    possible_moves = implement_bias(board, possible_moves)
    if len(possible_moves) == 0 or depth == 0:
        return compute_utility(board, color)
    else:
        max = -math.inf
        for possible_move in possible_moves:
            new_board = play_move(board, color, possible_move[0], possible_move[1])
            util = minimax_min_node(new_board, opp_color, depth-1) #compute_utility(new_board)
            if util > max:
                max = util
        return max

    
def select_move_minimax(board, color, depth):
    """
    Given a board and a player color, decide on a move. 
    The return value is a tuple of integers (i,j), where
    i is the column and j is the row on the board.  
    """
    opp_color = 1 if color == 2 else 2
    possible_moves = get_possible_moves(board, color)
    possible_moves = implement_bias(board, possible_moves)
    max = -math.inf
    best_move = (0,0)
    logging.basicConfig(level = logging.INFO)
    logging.info(possible_moves)
    for possible_move in possible_moves:
        new_board = play_move(board, color, possible_move[0], possible_move[1])
        util = minimax_min_node(new_board, opp_color, depth-1)
        if util > max:
            max = util
            best_move = possible_move
    return best_move


implement_bias_bool = False

def implement_bias(board, possible_moves):
    global implement_bias_bool
    implement_bias_bool = True
    corners = [(0, 0), (0, len(board) - 1), (len(board) - 1, 0), (len(board) - 1, len(board) - 1)]
    adj_corners = [(0, 1), (1, 0), (1, 1), (1, len(board) - 1), (0, len(board) - 2), (1, len(board) - 2), (len(board) -1, 1), (len(board) -2, 0), (len(board) -2, 1), (len(board) - 1, len(board) - 2), (len(board) - 2, len(board) - 1), (len(board) - 2, len(board) - 2)]
    corners_found = []
    normal_found = []
    adj_corners_found = []
    for possible_move in possible_moves:
        if possible_move in corners:
            corners_found.append(possible_move)
        elif possible_move in adj_corners:
            adj_corners_found.append(possible_move)
        else:
            normal_found.append(possible_move)
    if len(corners_found) != 0:
        return corners_found
    elif len(normal_found) != 0:
        return normal_found
    else:
        return adj_corners_found

############ ALPHA-BETA PRUNING #####################

def alphabeta_min_node(board, color, alpha, beta):
    opp_color = 1 if color == 2 else 2
    possible_moves = get_possible_moves(board, color)
    possible_moves = implement_bias(board, possible_moves)
    if len(possible_moves) == 0:
        return compute_utility(board, color)
    else:
        min = math.inf
        for possible_move in possible_moves:
            new_board = play_move(board, color, possible_move[0], possible_move[1])
            util = alphabeta_max_node(new_board, opp_color, alpha, beta)
            if util < min:
                min = util
            if alpha < min:
                min = alpha
            if beta < min:
                min = beta
            if min <= alpha:
                return min
            if min < beta:
                beta = min
        return min


def alphabeta_max_node(board, color, alpha, beta):
    opp_color = 1 if color == 2 else 2
    possible_moves = get_possible_moves(board, color)
    possible_moves = implement_bias(board, possible_moves)
    if len(possible_moves) == 0:
        return compute_utility(board, color)
    else:
        max = -math.inf
        for possible_move in possible_moves:
            new_board = play_move(board, color, possible_move[0], possible_move[1])
            util = alphabeta_max_node(new_board, opp_color, alpha, beta)
            if util > max:
                max = util
            if alpha > max:
                max = alpha
            if beta > max:
                max = beta
            if max >= beta:
                return max
            if alpha > max:
                alpha = max
        return max


def select_move_alphabeta(board, color, alpha, beta): 
    opp_color = 1 if color == 2 else 2
    possible_moves = get_possible_moves(board, color)
    possible_moves = implement_bias(board, possible_moves)
    max = -math.inf
    best_move = (0, 0)
    logging.basicConfig(level = logging.INFO)
    logging.info(possible_moves)
    for possible_move in possible_moves:
        new_board = play_move(board, color, possible_move[0], possible_move[1])
        util = alphabeta_max_node(new_board, opp_color, alpha, beta)
        if util > max:
            max = util
        if alpha > max:
            max = alpha
        if beta > max:
            max = beta
        if max >= beta:
            best_move = possible_move
        if alpha > max:
            alpha = max
    return best_move


####################################################
def run_ai():
    """
    This function establishes communication with the game manager. 
    It first introduces itself and receives its color. 
    Then it repeatedly receives the current score and current board state
    until the game is over. 
    """
    def saveData():
        original_stdout = sys.stdout
        with open("ai_data.txt", "r") as f:
            sys.stdout = f
            lines = []
            for line in f:
                lines.append(line)
            test1 = lines[0]
            test2 = lines[1]
            dark, light = get_score(board)
            if implement_bias_bool == False:
                test1.append(light - dark)
            if implement_bias_bool == True:
                test2.append(light - dark)
            print(test1)
            print(test2)
            print("Average score advantage with no bias: " + statistics.mean(test1))
            print("Average score advantage with bias: " + statistics.mean(test2))
            sys.stdout = original_stdout
            print("File about to close")
            f.close()
    print("Corner Seeker") # First line is the name of this AI  
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
            saveData()
            print
        else: 
            board = eval(input()) # Read in the input and turn it into a Python
                                  # object. The format is a list of rows. The 
                                  # squares in each row are represented by 
                                  # 0 : empty square
                                  # 1 : dark disk (player 1)
                                  # 2 : light disk (player 2)
                    
            # Select the move and send it to the manager 
            depth = 3
            alpha = -math.inf
            beta = math.inf
            #movei, movej = select_move_minimax(board, color, depth)
            movei, movej = select_move_alphabeta(board, color, alpha, beta)
            print("{} {}".format(movei, movej)) 


if __name__ == "__main__":
    run_ai()
