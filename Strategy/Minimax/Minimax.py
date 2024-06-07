from State.GameStateModule import *
from Rule.move import *
from Heuristic.evaluate_board import *

def Minimax(state: GameState, depth, isMax):
    if(depth == 0):
        return heuristic(state.board)
    moves = all_posible_moves(2 if isMax == True else 1, state.board)
    if(isMax):
        bestMove = -9999
        move_key = list(moves.keys())
        move_value = list(moves.values())
        for i in range(len(move_value)):
            for j in range(len(move_value[i][1])):
                movePieceName = move_key[i][0]
                curMove = list(move_key[i][1])
                nextMove = list(move_value[i][1][j])
                temp = state.board[nextMove[0]][nextMove[1]]
                state.board[nextMove[0]][nextMove[1]] = state.board[curMove[0]][curMove[1]]
                state.board[curMove[0]][curMove[1]] = ""
                eval = Minimax(state,depth - 1, not isMax)
                state.board[curMove[0]][curMove[1]] = state.board[nextMove[0]][nextMove[1]]
                state.board[nextMove[0]][nextMove[1]] = temp
                bestMove = max(bestMove,eval)
        return bestMove
    else:
        bestMove = 9999
        move_key = list(moves.keys())
        move_value = list(moves.values())
        for i in range(len(move_value)):
            for j in range(len(move_value[i][1])):
                movePieceName = move_key[i][0]
                curMove = list(move_key[i][1])
                nextMove = list(move_value[i][1][j])
                temp = state.board[nextMove[0]][nextMove[1]]
                state.board[nextMove[0]][nextMove[1]] = state.board[curMove[0]][curMove[1]]
                state.board[curMove[0]][curMove[1]] = ""
                eval = Minimax(state,depth - 1, not isMax)
                state.board[curMove[0]][curMove[1]] = state.board[nextMove[0]][nextMove[1]]
                state.board[nextMove[0]][nextMove[1]] = temp
                bestMove = min(bestMove,eval)
        return bestMove

def find_best_move_minimax(state : GameState,depth,isMax):
    if isMax:
        bestMove = None
        bestValue = -9999
        moves = all_posible_moves(2 if isMax == True else 1, state.board)
        move_key = list(moves.keys())
        move_value = list(moves.values())
        for i in range(len(move_value)):
            for j in range(len(move_value[i][1])):
                movePieceName = move_key[i][0]
                curMove = list(move_key[i][1])
                nextMove = list(move_value[i][1][j])
                temp = state.board[nextMove[0]][nextMove[1]]
                state.board[nextMove[0]][nextMove[1]] = state.board[curMove[0]][curMove[1]]
                state.board[curMove[0]][curMove[1]] = ""
                move_point = Minimax(state, depth - 1, not isMax)
                state.board[curMove[0]][curMove[1]] = state.board[nextMove[0]][nextMove[1]]
                state.board[nextMove[0]][nextMove[1]] = temp
                if move_point >= bestValue:
                    bestValue = move_point
                    bestMove = [curMove, nextMove]
        return bestMove
    else:
        bestMove = None
        bestValue = 9999
        moves = all_posible_moves(2 if isMax == True else 1, state.board)
        move_key = list(moves.keys())
        move_value = list(moves.values())
        for i in range(len(move_value)):
            for j in range(len(move_value[i][1])):
                movePieceName = move_key[i][0]
                curMove = list(move_key[i][1])
                nextMove = list(move_value[i][1][j])
                temp = state.board[nextMove[0]][nextMove[1]]
                state.board[nextMove[0]][nextMove[1]] = state.board[curMove[0]][curMove[1]]
                state.board[curMove[0]][curMove[1]] = ""
                move_point = Minimax(state, depth - 1, not isMax)
                state.board[curMove[0]][curMove[1]] = state.board[nextMove[0]][nextMove[1]]
                state.board[nextMove[0]][nextMove[1]] = temp
                if move_point <= bestValue:
                    bestValue = move_point
                    bestMove = [curMove, nextMove]
        return bestMove