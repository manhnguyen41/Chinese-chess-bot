from Rule.move import all_posible_moves
from State.GameStateModule import GameState
from Heuristic import *
from ABPruning import *

board = [
        ["x12", "m12", "tj12", "s12", "ts2", "s22", "tj22", "m22", "x22"],
        ["", "", "", "", "", "", "", "", ""],
        ["", "p12", "", "", "", "", "", "p22", ""],
        ["to12", "", "to22", "", "to32", "", "to42", "", "to52"],
        ["", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", ""],
        ["to11", "", "to21", "", "to31", "", "to41", "", "to51"],
        ["", "p11", "", "", "", "", "m21", "p21", ""],
        ["", "", "", "", "", "", "", "", ""],
        ["x11", "m11", "tj11", "s11", "ts1", "s21", "tj21", "", "x21"],
    ]

game_state = GameState(board)
#moves = all_posible_moves(1, game_state.board)
#move_key = list(moves.keys())
#move_value = list(moves.values())
#for i in range(len(move_value)):
#    for j in range(len(move_value[i][1])):
#        print("name = " , move_key[i][0], "curPos = " ,  list(move_key[i][1]))
#        print("name = " , move_value[i][0], "toPos = " ,  list(move_value[i][1][j]))

#a = list(move_key[0][1])
#for i in range(len(move_key)):
        #print("name = " , move_key[i][0], "toPos = " ,  list(move_key[i][1]))

#board1 = game_state.board 

#game_state.board[list(move_key[0][1])[0]][list(move_key[0][1])[1]] = game_state.board[list(move_value[0][1][0])[0]][list(move_value[0][1][0])[1]]
#print(game_state.board)
#game_state.board

#print(list(move_value))
#print(heuristic(board))

#comptuteNextMove(game_state)


bestmove = find_best_move(game_state,1,True)
print(bestmove)


