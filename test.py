from Rule.move import all_posible_moves
from State.GameStateModule import GameState

board = [
        ["x12", "m12", "tj12", "s12", "ts2", "s22", "tj22", "m22", "x22"],
        ["", "", "", "", "", "", "", "", ""],
        ["", "p12", "", "", "", "", "", "p22", ""],
        ["to12", "", "to22", "", "to32", "", "to42", "", "to52"],
        ["", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", ""],
        ["to11", "", "to21", "", "to31", "", "to41", "", "to51"],
        ["", "p11", "", "", "", "", "", "p21", ""],
        ["", "", "", "", "", "", "", "", ""],
        ["x11", "m11", "tj11", "s11", "ts1", "s21", "tj21", "m21", "x21"],
    ]

game_state = GameState(board)
for i in range(10):
        print(board[i])
moves = all_posible_moves(1, board)
print(moves)