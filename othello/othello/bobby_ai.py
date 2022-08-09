#!/usr/bin/env python3
# -*- coding: utf-8 -*
"""
An AI player for Othello. This is the template file that you need to  
complete.

@authors: Michael Del Toro ; mfd2141
          Shayan Idrees ; si2428
          Maria Carseli ; mc5333
          Maxim Ilin ; mai2130
"""

import random
import sys
import time
import math

# You can use the functions in othello_shared to write your AI
from othello_shared import find_lines, get_possible_moves, get_score, play_move


def compute_utility(board, color):
    discs = get_score(board)
    if color == 1:
        return discs[0] - discs[1]
    return discs[1] - discs[0]


def advanced_utility(board, color):
    discs = get_score(board)
    utility = abs(discs[0] - discs[1])

    height = len(board)
    width = len(board[0])

    if color == 1:
        oppColor = 0
    else:
        oppColor = 1

    if board[0][0] == color or board[height - 1][width - 1] == color or board[
            0][width - 1] == color or board[height - 1][0] == color:
        utility += 3

    if board[0][0] == oppColor or board[height - 1][
            width - 1] == oppColor or board[0][width - 1] == oppColor or board[
                height - 1][0] == oppColor:
        utility -= 3

    return utility


############ MINIMAX ###############################


def minimax_min_node(board, color, ply):
    opp_color = 1 if color == 2 else 2
    moves = get_possible_moves(board, opp_color)
    if not moves or ply == 4:
        return advanced_utility(board, color)
    utility = {}

    for move in moves:
        utility[move] = minimax_max_node(
            play_move(board, opp_color, move[0], move[1]), color, ply + 1)

    minMove = moves[0]

    for key in utility:
        if utility[key] < utility[minMove]:
            minMove = key

    return utility[minMove]


def minimax_max_node(board, color, ply):
    moves = get_possible_moves(board, color)
    if not moves or ply == 4:
        return advanced_utility(board, color)

    utility = {}

    for move in moves:
        utility[move] = minimax_min_node(
            play_move(board, color, move[0], move[1]), color, ply + 1)

    maxMove = moves[0]

    for key in utility:
        if utility[key] > utility[maxMove]:
            maxMove = key

    return utility[maxMove]


def select_move_minimax(board, color):
    """
    Given a board and a player color, decide on a move. 
    The return value is a tuple of integers (i,j), where
    i is the column and j is the row on the board.  
    """

    moves = get_possible_moves(board, color)
    if not moves:
        raise RuntimeError("Called select_move_minimax on terminal state")

    utility = {}

    for move in moves:
        utility[move] = minimax_min_node(
            play_move(board, color, move[0], move[1]), color, 1)

    maxMove = moves[0]

    for key in utility:
        if utility[key] > utility[maxMove]:
            maxMove = key

    return maxMove


############ ALPHA-BETA PRUNING #####################


#alphabeta_min_node(board, color, alpha, beta, level, limit)
def alphabeta_min_node(board, color, alpha, beta, depth, start):
    opp_color = 1 if color == 2 else 2
    moves = get_possible_moves(board, opp_color)
    if not moves:
        #print("Terminating in min at depth", depth, file=sys.stderr)
        return compute_utility(board, color)
    elif depth == 4:
        return advanced_utility(board, color)

    v = math.inf

    actions = []
    for action in moves:
        if action == (0, 0) or action == (7, 7) or action == (
                0, 7) or action == (7, 0):
                return alphabeta_max_node(play_move(board, opp_color, action[0], action[1]), color, alpha, beta, depth + 1, start)              
        else:
            actions.append(action)

    for action in actions:
        v = min(v, (alphabeta_max_node(
            play_move(board, opp_color, action[0], action[1]), color, alpha,
            beta, depth + 1, start)))
        if time.time() - start >= 8:
          return v
        if v <= alpha:
            #print("CUT in min at utility", v, file=sys.stderr)
            return v
        beta = min(beta, v)

    return v


#alphabeta_max_node(board, color, alpha, beta, level, limit)
def alphabeta_max_node(board, color, alpha, beta, depth, start):

    moves = get_possible_moves(board, color)
    if not moves:
        #print("Terminating in max at depth", depth, file=sys.stderr)
        return compute_utility(board, color)
    elif depth == 4:
        return advanced_utility(board, color)

    v = -1 * math.inf

    actions = []
    for action in moves:
        if action == (0, 0) or action == (7, 7) or action == (
                0, 7) or action == (7, 0):
            return alphabeta_min_node(play_move(board, color, action[0], action[1]), color, alpha, beta, depth + 1, start)                  
        else:
            actions.append(action)

    for action in actions:
        v = max(
            v,
            (alphabeta_min_node(play_move(board, color, action[0], action[1]),
                                color, alpha, beta, depth + 1, start)))
        if time.time() - start >= 8:
          return v
        if v >= beta:
            #print("CUT in max at utility", v, file=sys.stderr)
            return v
        alpha = max(alpha, v)

    return v


def select_move_alphabeta(board, color):
    start = time.time()
  
    sys.setrecursionlimit(2000)
    moves = get_possible_moves(board, color)
    if not moves:
        raise RuntimeError("Called select_move_minimax on terminal state")

    utility = {}

    for move in moves:
        utility[move] = alphabeta_min_node(
            play_move(board, color, move[0], move[1]), color, -math.inf,
            math.inf, 0, start)

    maxMove = moves[0]

    for key in utility:
        if utility[key] > utility[maxMove]:
            maxMove = key

    return maxMove


####################################################
def run_ai():
    """
    This function establishes communication with the game manager. 
    It first introduces itself and receives its color. 
    Then it repeatedly receives the current score and current board state
    until the game is over. 
    """
    print("Minimax AI")  # First line is the name of this AI
    color = int(input())  # Then we read the color: 1 for dark (goes first),
    # 2 for light.

    while True:  # This is the main loop
        # Read in the current game status, for example:
        # "SCORE 2 2" or "FINAL 33 31" if the game is over.
        # The first number is the score for player 1 (dark), the second for player 2 (light)
        next_input = input()
        status, dark_score_s, light_score_s = next_input.strip().split()
        dark_score = int(dark_score_s)
        light_score = int(light_score_s)

        if status == "FINAL":  # Game is over.
            print
        else:
            board = eval(
                input())  # Read in the input and turn it into a Python
            # object. The format is a list of rows. The
            # squares in each row are represented by
            # 0 : empty square
            # 1 : dark disk (player 1)
            # 2 : light disk (player 2)

            # Select the move and send it to the manager
            # movei, movej = select_move_minimax(board, color)
            movei, movej = select_move_alphabeta(board, color)
            print("{} {}".format(movei, movej))


if __name__ == "__main__":
    run_ai()
