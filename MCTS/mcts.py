import math  # Import thư viện toán học
import random  # Import thư viện random để sinh số ngẫu nhiên
import copy  # Import thư viện copy để tạo bản sao sâu của đối tượng

from MCTS.evaluate_board import get_piece_value
from MCTS.greedy import greedy_best_move
from State.GameStateModule import GameState  # Import class GameState từ module State.GameStateModule
from Rule.move import *  # Import tất cả các hàm từ module Rule.move

class Node:
    def __init__(self, state, parent=None):
        self.state = state  # Trạng thái hiện tại của node
        self.parent = parent  # Node cha của node hiện tại
        self.children = []  # Danh sách các node con của node hiện tại
        self.visits = 0  # Số lượt truy cập node hiện tại
        self.score = 0  # Điểm tích lũy từ việc backpropagation

    def expand(self):
        # Mở rộng node bằng cách tạo ra tất cả các trạng thái tiếp theo có thể
        next_states = generate_next_states(self.state)  # Tạo các trạng thái kế tiếp có thể từ trạng thái hiện tại
        for state in next_states.values():
            self.children.append(Node(state, parent=self))  # Thêm các node con mới vào danh sách

    def is_fully_expanded(self):
        # Kiểm tra xem tất cả các trạng thái tiếp theo có thể đã được khám phá
        return len(self.children) == len(generate_next_states(self.state))

    def select_child(self, exploration_constant=1.4):
        best_child = None  # Node con tốt nhất
        best_score = float('-inf')  # Điểm tốt nhất
        for child in self.children:
            if child.visits == 0:  # Kiểm tra xem số lượt truy cập của node con có phải là 0 không
                score = float('inf')  # Đặt điểm là vô cực để tránh lỗi chia cho 0
            else:
                exploitation = child.score / child.visits  # Tính exploitation score
                exploration = math.sqrt(2 * math.log(self.visits) / child.visits)  # Tính exploration score
                score = exploitation + exploration_constant * exploration  # Tổng hợp score
            if score > best_score:
                best_child = child
                best_score = score
        return best_child

def generate_next_states(state):
    next_states = {}  # Danh sách các trạng thái tiếp theo
    if isinstance(state, tuple):
        # Nếu trạng thái là tuple, giả sử nó đại diện cho bảng trực tiếp
        board = state
    else:
        # Nếu trạng thái là một đối tượng GameState, lấy thuộc tính board
        board = state.board

    possible_moves = all_posible_moves(2, board)  # Chỉ xem xét lượt của đội đen (team = 2)

    for piece, moves in possible_moves.items():
        moves = moves[1]
        for move in moves:
            new_board = copy.deepcopy(board)  # Tạo một bản sao sâu của bảng
            old_position = piece[1]
            next_position = move
            # Thực hiện nước đi trên bảng mới
            new_board[next_position[0]][next_position[1]] = piece[0]
            new_board[old_position[0]][old_position[1]] = ''
            next_states[(piece, old_position)] = GameState(new_board)  # Chuyển đổi thành đối tượng GameState

    return next_states

def simulate(state):
    copy_state = copy.deepcopy(state)

    while not is_terminal(copy_state):

        copy_state = greedy_best_move(2, copy_state)
        
        if is_draw(copy_state):
            return 0  # Trò chơi hòa

    if is_king_captured(copy_state.board, 1):
        return 1  # Người chơi 2 thắng
    elif is_king_captured(copy_state.board, 2):
        return -1  # Người chơi 1 thắng

def get_result(state):
    if is_king_captured(state.board, 1):
        return 1  # Người chơi 2 thắng
    elif is_king_captured(state.board, 2):
        return -1  # Người chơi 1 thắng
    elif is_draw(state):
        return 0  # Trò chơi hòa

def evaluate_state(state):
    # Đánh giá giá trị của trạng thái dựa trên trọng số của các quân cờ
    total_evaluation = 0
    for i in range(10):
        for j in range(9):
            total_evaluation += get_piece_value(state.board[i][j], i, j)
    return total_evaluation

def is_king_captured(board, player):
    """
    Kiểm tra xem quân tướng của người chơi có còn trên bàn cờ hay không.

    Args:
    - board: danh sách 2D đại diện cho bàn cờ
    - player: người chơi (1 hoặc 2)

    Returns:
    - True nếu quân tướng đã bị bắt, False nếu còn trên bàn cờ
    """
    king_piece = f"ts{player}"
    for row in board:
        if king_piece in row:
            return False
    return True

def is_draw(state):
    # Trò chơi kết thúc hòa nếu không còn nước đi hợp lệ hoặc đã đi quá 100 nước
    return (not any(all_posible_moves(1, state.board).values()) and
            not any(all_posible_moves(2, state.board).values())) or state.num_moves >= 100
def is_terminal(state):
    """
    Kiểm tra nếu trò chơi đã kết thúc.

    Args:
    - state: trạng thái của trò chơi, bao gồm bàn cờ và thông tin khác

    Returns:
    - True nếu trò chơi đã kết thúc, False nếu không
    """
    board = state.board
    return is_king_captured(board, 1) or is_king_captured(board, 2)

def backpropagate(node, score):
    # Truyền lại kết quả mô phỏng lên cây
    while node is not None:
        node.visits += 1
        node.score += score
        node = node.parent

def mcts(state, num_iterations):
    root = Node(state)
    root.expand()  # Mở rộng node gốc trước khi bắt đầu các vòng lặp
    for _ in range(num_iterations):
        node = root
        while not node.is_fully_expanded() and node.children:
            node = node.select_child()
        if not node.children and not node.is_fully_expanded():
            node.expand()
            if node.children:  # Kiểm tra xem có sinh ra các node con không
                selected_child = greedy_best_move(2, node.children)
                score = simulate(selected_child.state)
                backpropagate(selected_child, score)
        elif node.children:  # Kiểm tra xem có các node con không để tránh lỗi NoneType
            selected_child = node.select_child()
            score = simulate(selected_child.state)
            backpropagate(selected_child, score)
    if root.children:  # Kiểm tra xem node gốc có các node con không
        best_child = max(root.children, key=lambda child: child.visits)
        return best_child.state
    else:
        return state  # Trả về trạng thái ban đầu nếu không có node con nào được sinh ra
