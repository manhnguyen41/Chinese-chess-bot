from State.GameStateModule import *
from Rule.move import *
from Heuristic.evaluate_board import *

def AB(state: GameState, depth, alpha, beta, isMax):
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
                eval = AB(state,depth - 1,alpha,beta, not isMax)
                state.board[curMove[0]][curMove[1]] = state.board[nextMove[0]][nextMove[1]]
                state.board[nextMove[0]][nextMove[1]] = temp
                bestMove = max(bestMove,eval)
                alpha = max(alpha,bestMove)
                if beta <= alpha :
                    return bestMove
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
                eval = AB(state,depth - 1,alpha,beta, not isMax)
                state.board[curMove[0]][curMove[1]] = state.board[nextMove[0]][nextMove[1]]
                state.board[nextMove[0]][nextMove[1]] = temp
                bestMove = min(bestMove,eval)
                beta = min(beta,bestMove)
                if beta <= alpha :
                    return bestMove
        return bestMove

def find_best_move(state : GameState,depth,isMax):
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
                move_point = AB(state, depth - 1, -99999, 99999, not isMax)
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
                move_point = AB(state, depth - 1, -99999, 99999, not isMax)
                state.board[curMove[0]][curMove[1]] = state.board[nextMove[0]][nextMove[1]]
                state.board[nextMove[0]][nextMove[1]] = temp
                if move_point <= bestValue:
                    bestValue = move_point
                    bestMove = [curMove, nextMove]
        return bestMove


"""
def recurseEvaluation(state : GameState,depth,alpha,beta):
    isMax = state.current_player == "black"
    if depth == 0:
        print(state.board)
        return heuristic(state.board)
    moves = all_posible_moves(2 if isMax == True else 1, state.board)
    nextEvals = []
    move_key = list(moves.keys())
    move_value = list(moves.values())
    for i in range(len(move_value)):
        for j in range(len(move_value[i][1])):
            movePieceName = move_key[i][0]
            curMove = list(move_key[i][1])
            nextMove = list(move_value[i][1][j])
            curBoard = state.board
            state.board[nextMove[0]][nextMove[1]] = state.board[curMove[0]][curMove[1]] 
            state.board[curMove[0]][curMove[1]] = ""
            evalResult = [recurseEvaluation(state,depth - 1,alpha,beta),[movePieceName,nextMove]]
            state.board = curBoard
            nextEvals.append(evalResult)
            if isMax : 
                alpha = max(alpha, evalResult[0])
                if beta <= alpha :
                    return evalResult
            else :
                beta = min(beta, evalResult[0])
                if beta <= alpha :
                    return evalResult
    scores = list(map(lambda x:x[0],nextEvals))
    index = scores.index(max(scores))
    if isMax:
        index = scores.index(max(scores))
    else:
        index = scores.index(min(scores))
    return (nextEvals[index])

def comptuteNextMove(curr_state):
    evalResult = recurseEvaluation(curr_state, 1, -99999999, 99999999)
    movePiece = evalResult[1][0]
    return [movePiece, evalResult[1][1]]
"""