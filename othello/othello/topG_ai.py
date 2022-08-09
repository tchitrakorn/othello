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

# You can use the functions in othello_shared to write your AI
from othello_shared import find_lines, get_possible_moves, get_score, play_move

def compute_utility(board, color):
    dark_disks, light_disks = get_score(board)
    if color == 1:
        return dark_disks - light_disks
    else:
        return light_disks - dark_disks


############ MINIMAX ###############################
'''
min value: finds the best opponent move based on our move
max value: finds our best move based on opponent move
color: 
  - 1: dark
  - 2: light
'''
'''
def isOver(board, color):
  if len(get_possible_moves(board, color)) > 0:
    return False
  return True
'''

def select_move_minimax(board, color, moveCounter):
    """
    Given a board and a player color, decide on a move. 
    The return value is a tuple of integers (i,j), where
    i is the column and j is the row on the board.  
    """

    max = (float('-inf'), 0)

    for x in get_possible_moves(board, color):
        counter = 0
        temp = (minimax_min_node(play_move(board, color, x[0], x[1]), color,
                                 counter, moveCounter)[0], x)
        if temp[0] > max[0]:
            max = temp

    return max[1]


def minimax_min_node(board, color, counter, moveCounter, count=2):
    opp_color = 1 if color == 2 else 2
    counter += 1
    moves = get_possible_moves(board, color)
    if counter >= count or len(moves) == 0:
        return (getHeuristic(board, color, moveCounter), counter)
    min = (float('inf'), None)

    #both min and temp are ints
    for i, j in moves:
        temp = minimax_max_node(play_move(board, color, i, j), opp_color,
                                counter, moveCounter)
        if temp[0] < min[0]:
            min = temp
    return min


def minimax_max_node(board, color, counter, moveCounter, count=2):
    counter += 1
    opp_color = 1 if color == 2 else 2
    moves = get_possible_moves(board, color)
    if counter >= count or len(moves) == 0:
        return (getHeuristic(board, color, moveCounter), counter)
    max = (float('-inf'), None)
    for i, j in moves:
        temp = minimax_min_node(play_move(board, color, i, j), opp_color,
                                counter, moveCounter)
        if temp[0] > max[0]:
            max = temp
    return max


# base case: no more moves


def getHeuristic(board, color, moveCounter, size=8):
    #10 12 8
    game = 's'
    if moveCounter < 10:
        cornerCost = 10
        xSquareCost = -1
        moveCost = 1
        edgeCost = 0.5
        mobilityPerMoveCost = .05
        captureCost = 0
    elif moveCounter < 22:
        cornerCost = 10
        xSquareCost = -0.5
        moveCost = 1
        edgeCost = 0.5
        mobilityPerMoveCost = .05
        game = 'm'
        captureCost = 0
    else:
        cornerCost = 10
        xSquareCost = -0.5
        moveCost = 1
        edgeCost = 0.5
        mobilityPerMoveCost = .05
        captureCost = 5
        game = 'e'
    heuristicValue = 0
    opponentMove = {}
    moves = get_possible_moves(board, color)
    for move in moves:
        opponentMove[move] = get_possible_moves(
            play_move(board, color, move[0], move[1]), oppCol(color))
    if len(opponentMove) > 0:
        heuristicValue += moveCost / len(opponentMove)

    isCorner = [False, False, False,
                False]  #topleft, topright, bottomleft, bottomright
    # corners
    corners = [(0, 0), (0, size - 1), (size - 1, 0), (size - 1, size - 1)]
    for x in range(0, len(corners)-1):
      if board[corners[x][0]][corners[x][1]] == color:
          heuristicValue += cornerCost
          if corners[x] == color:
              isCorner[x] = True

    cornerHeuristicMultiplier = [1, 1, 1, 1]
    # x zone
    
    xSquares = [((0, 1), (1, 0), (1, 1)),
                ((0, size - 2), (1, size - 2), (1, size - 1)),
                ((size - 2, 0), (size - 2, 1), (size - 1, 1)),
                (())]
    for x in range(0, len(xSquares)-1):
        if isCorner[x]:
            cornerHeuristicMultiplier[x] = -1
        for i, j in xSquares[x]:
            if board[i][j] == color:
                heuristicValue += xSquareCost * cornerHeuristicMultiplier[x]
    #edges
    for x in range(2, size - 3):
        if board[0][x] == color:
            heuristicValue += edgeCost
        if board[size - 1][x] == color:
            heuristicValue += edgeCost
        if board[x][0] == color:
            heuristicValue += edgeCost
        if board[x][size - 1] == color:
            heuristicValue += edgeCost
    
    #mobilityPerMove
    for i in moves:
        heuristicValue += mobilityPerMoveCost

    dark, light = get_score(board)
    diff = dark - light
    if color == 2:
      diff *= -1
    heuristicValue += diff * captureCost
  
    return heuristicValue


def oppCol(color):
    if color == 1:
        return 2
    else:
        return 1


############ ALPHA-BETA PRUNING #####################

def alphabeta_min_node(board, color, alpha, beta, level, moveCounter, limit=1):
    opp_color = 1 if color == 2 else 2
    level += 1
    moves = get_possible_moves(board, opp_color)
    # base case
    
    if moves == []:
        return getHeuristic(board, color, moveCounter)
    beta = float('inf')
    if level <= limit or len(moves) == 0:
      for i, j in moves:
        v = alphabeta_max_node(play_move(board, color, i, j), opp_color, alpha, beta,level,moveCounter)
        if v <= alpha:
          return v
        beta = min(beta, v)
    return beta


#alphabeta_max_node(board, color, alpha, beta, level, limit)
def alphabeta_max_node(board, color, alpha, beta, level, moveCounter, limit=1):
    opp_color = 1 if color == 2 else 2
    moves = get_possible_moves(board, color)
    level += 1
    # base case
    if moves == []:
        return getHeuristic(board, color, moveCounter)
    alpha = -float('inf')
    if level <= limit or len(moves) == 0:
      
      for i, j in moves:
          v = alphabeta_min_node(play_move(board, color, i, j), opp_color, alpha, beta,level,moveCounter)
          if v >= beta:
            return v
          alpha = max(alpha, v)
    return alpha


def select_move_alphabeta(board, color, moveCounter):
    level = 0
    max = -math.inf
    best_move = None
    for x in get_possible_moves(board, color):
        temp = alphabeta_min_node(play_move(board, color, x[0], x[1]), color, max, -math.inf,level,moveCounter)
      
        if temp > max:
            max = temp
            best_move = x


    return best_move


####################################################
def run_ai():
    """
    This function establishes communication with the game manager. 
    It first introduces itself and receives its color. 
    Then it repeatedly receives the current score and current board state
    until the game is over. 
    """
    print("TopGai")  # First line is the name of this AI
    color = int(input())  # Then we read the color: 1 for dark (goes first),
    # 2 for light.
    moveCounter = 0
    while True:  # This is the main loop
        # Read in the current game status, for example:
        # "SCORE 2 2" or "FINAL 33 31" if the game is over.
        # The first number is the score for player 1 (dark), the second for player 2 (light)
        moveCounter += 1
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
            movei, movej = select_move_minimax(board, color, moveCounter)
            #movei, movej = select_move_alphabeta(board, color, moveCounter)
            print("{} {}".format(movei, movej))


if __name__ == "__main__":
    run_ai()
