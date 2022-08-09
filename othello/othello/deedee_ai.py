#!/usr/bin/env python3
# -*- coding: utf-8 -*

"""


An AI player for Othello. This is the template file that you need to
complete and submit.

"""
corners = [(0,0),(0,7),(7,0),(7,7)]

import random
import sys
import time
from datetime import timedelta, datetime

# You can use the functions in othello_shared to write your AI
from othello_shared2 import find_lines, get_possible_moves, get_score_weighted, play_move








cached = {} #STATE : UTILITY

moveOrder = 0


def compute_utility(board, color):
    """
    Return the utility of the given board state
    (represented as a tuple of tuples) from the perspective
    of the player "color" (1 for dark, 2 for light)
    """

    scores = get_score_weighted(board)

    if color== 1:
        return scores[0]-scores[1]
    else:
        return scores[1]-scores[0]

############ MINIMAX ###############################
#MAX = 1
#MIN = 2
def minimax_min_node(board, color, limit, level): #returns lowest attainable utility
    if color == 1 : 
        opponent = 2
    else : 
        opponent = 1
    level += 1
    if board in cached:
        return cached[board]
    if not get_possible_moves(board,opponent) or level == limit:
        return compute_utility(board,color)
    v = float("Inf")
    for move in get_possible_moves(board,opponent):
        #new_move = play_move(board,color,move[0],move[1])
        v = min(v,minimax_max_node(play_move(board,opponent,move[0],move[1]),color,limit, level))
    return v


def minimax_max_node(board, color, limit, level): #returns highest possible utility
    if color == 1 : 
        opponent = 2
    else: 
        opponent = 1
    level += 1
    if board in cached:
        return cached[board]
    if not get_possible_moves(board,color) or level == limit:
        return compute_utility(board,color)
    v = float("-Inf")
    for move in get_possible_moves(board,color):
        #new_move = play_move(board,color,move[0],move[1])
        v = max(v,minimax_min_node(play_move(board,opponent,move[0],move[1]),color, limit, level))
    return v

def select_move_minimax(board, color):
    """
    Given a board and a player color, decide on a move.
    The return value is a tuple of integers (i,j), where
    i is the column and j is the row on the board.
    """
    moves = []
    for option in get_possible_moves(board,color): #get all minimizer moves
        new_move = play_move(board,color,option[0],option[1])
        utility = minimax_max_node(new_move,color,4,0)
        if new_move not in cached:
            cached[new_move] = utility
        moves.append([(option[0], option[1]), utility])
    sorted_options = sorted(moves, key = lambda x: x[1], reverse=True)
    return sorted_options[0][0]

############ ALPHA-BETA PRUNING #####################


def alphabeta_min_node(board, color, depth, alpha, beta, end_time):

    possible_moves = get_possible_moves(board, color)
    current_time = datetime.now()
    if possible_moves == [] or current_time >= end_time:
        
        score = get_score_weighted(board) #get_score(board)
        if color == 1: #then min is black, so ai player is white
            return score[1]-score[0] #score for ai white
        else:
            return score[0]-score[1] #score for ai black
    else:
        if color == 1: 
            next_color = 2
        else:
            next_color = 1
        best_min_score = 1000000
        for move in possible_moves:
            if move in corners:
                new_board = play_move(board, color, move[0], move[1])
                score = get_score_weighted(new_board)
                if color == 1: #then min is black, so ai player is white
                 return score[1]-score[0] #score for ai white
                else:
                 return score[0]-score[1] #score for ai black
            new_board = play_move(board, color, move[0], move[1])
            move_score = alphabeta_max_node(new_board, next_color, depth-1, alpha, beta, end_time)
            

            if move_score < best_min_score:
                best_min_score = move_score
                beta = min(beta, move_score)
            if beta <= alpha:
                break
        return best_min_score
    return None


#alphabeta_max_node(board, color, alpha, beta, level, limit)
def alphabeta_max_node(board, color, depth, alpha, beta, end_time):
    
    

    possible_moves = get_possible_moves(board, color)
    current_time = datetime.now() 
    if possible_moves == []  or current_time >= end_time:
        score = get_score_weighted(board) #get_score(board)
    
        if color == 1: #then ai player is black
            return score[0]-score[1] #score for ai black
        else:
            return score[1]-score[0] #score for ai white
    else:
        if color == 1: 
            next_color = 2
        else:
            next_color = 1
        
        best_max_score = -1000000
        for move in possible_moves:
            if move in corners:
                new_board = play_move(board, color, move[0], move[1])
                score = get_score_weighted(new_board)
                if color == 1: #then ai player is black
                    return score[0]-score[1] #score for ai black
                else:
                    return score[1]-score[0] #score for ai white

            new_board = play_move(board, color, move[0], move[1])
            move_score = alphabeta_min_node(new_board, next_color, depth-1, alpha, beta, end_time)

            if move_score > best_max_score:
                best_max_score = move_score
                alpha = max(alpha, move_score)
            if beta <= alpha:
                break
        
       
            
        return best_max_score
    return None


def select_move_alphabeta(board, color, depth, end_time): 

    """
    Given a board and a player color, decide on a move. 
    The return value is a tuple of integers (i,j), where
    i is the column and j is the row on the board.  
    """
    best_max_score = -10000000
    alpha = -1000000
    beta = 1000000

    
    possible_moves = get_possible_moves(board, color)

        
    if color == 1: 
        next_color = 2
    else:
        next_color = 1
    
    for move in possible_moves:
        #return move[0], move[1] #SPECIAL RETURN SEE IF ITS WORKING
        if move in corners:
            return move
        new_board = play_move(board, color, move[0], move[1])
        move_score = alphabeta_min_node(new_board, next_color, depth-1, alpha, beta, end_time)
        
        
        if move_score > best_max_score:
            best_max_score = move_score
            best_move = move

    
    return best_move

####################################################

def run_ai():
    """
    This function establishes communication with the game manager.
    It first introduces itself and receives its color.
    Then it repeatedly receives the current score and current board state
    until the game is over.
    """
    print("Minimax") # First line is the name of this AI
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
        current_time = datetime.now()
        end_time = current_time + timedelta(seconds=9.9)

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

            #movei, movej = select_move_minimax(board, color)
            movei, movej = select_move_alphabeta(board, color, 10000, end_time)
            print("{} {}".format(movei, movej))


if __name__ == "__main__":
    run_ai()