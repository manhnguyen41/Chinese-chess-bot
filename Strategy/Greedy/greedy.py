from Heuristic.evaluate_board import heuristic
from Rule.move import all_posible_moves
from State.GameStateModule import GameState


def greedy_best_move(player, state):
    best_move = None
    best_weight = float('-inf') if player == 2 else float('inf')

    possible_moves = all_posible_moves(player, state.board)  # Xem xét lượt của người chơi hiện tại

    for (piece, old_position), moves in possible_moves.items():
        for new_position in moves[1]:
            # Tạo ra trạng thái bàn cờ mới
            new_state = GameState([row[:] for row in state.board])
            new_state.next_state(old_position, new_position)

            # Tính trọng số của trạng thái mới
            weight = heuristic(new_state.board)

            # Cập nhật nước đi tốt nhất
            if (player == 2 and weight > best_weight):
                best_weight = weight
                best_move = (piece, old_position, new_position)

            if (player == 1 and weight < best_weight):
                best_weight = weight
                best_move = (piece, old_position, new_position)



    state.next_state(best_move[1], best_move[2])
    return state

def main():
    # Định nghĩa trạng thái ban đầu ở đây
    initial_state = [
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






if __name__ == "__main__":
    main()

