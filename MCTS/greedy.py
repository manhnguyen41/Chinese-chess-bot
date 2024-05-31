from MCTS.evaluate_board import evaluate_board
from Rule.move import all_posible_moves


def greedy_best_move(player, board_dict, piece_weight_table):
    best_move = None
    best_weight = float('-inf') if player == 1 else float('inf')

    for piece, position in board_dict.items():
        if piece[0] == str(player):  # Chỉ xem xét các quân cờ của người chơi hiện tại
            for move in all_posible_moves(piece, position, board_dict):
                move_weight = evaluate_move(move, board_dict, piece_weight_table)
                # Chọn nước đi có trọng số tốt nhất cho người chơi hiện tại
                if (player == 1 and move_weight > best_weight) or (player == 2 and move_weight < best_weight):
                    best_move = move
                    best_weight = move_weight

    return best_move

def evaluate_move(move, board_dict):
    # Tạm thời thực hiện nước đi để tính toán trọng số mới
    update_board_dict = board_dict.copy()
    update_board_dict[move[0]] = move[1]
    # Tính tổng trọng số mới sau khi thực hiện nước đi
    total_weight = sum(evaluate_board(update_board_dict, piece_weight_table).values())
    return total_weight
