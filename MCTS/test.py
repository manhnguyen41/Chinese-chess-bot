import math
import random
import copy

from MCTS.evaluate_board import get_piece_value
from MCTS.greedy import greedy_best_move
from State.GameStateModule import GameState
from Rule.move import *

class Node:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        self.children = []
        self.visits = 0
        self.score = 0

    def expand(self):
        next_states = generate_next_states(self.state)
        for state in next_states.values():
            self.children.append(Node(state, parent=self))

    def is_fully_expanded(self):
        return len(self.children) == len(generate_next_states(self.state))

    def select_child(self, exploration_constant=1.4):
        if not self.children:
            return None
        for child in self.children:
            if child.visits == 0:
                return child
        best_child = None
        best_score = float('-inf')
        for child in self.children:
            exploitation = child.score / child.visits
            exploration = math.sqrt(2 * math.log(self.visits) / child.visits)
            score = exploitation + exploration
            if score > best_score:
                best_child = child
                best_score = score
        return best_child

def generate_next_states(state):
    next_states = {}
    board = state.board
    possible_moves = all_posible_moves(2, board)
    for piece, moves in possible_moves.items():
        moves = moves[1]
        for move in moves:
            new_board = copy.deepcopy(board)
            old_position = piece[1]
            next_position = move
            new_board[next_position[0]][next_position[1]] = piece[0]
            new_board[old_position[0]][old_position[1]] = ''
            next_states[(piece, old_position)] = GameState(new_board)
    return next_states

def simulate(state):
    copy_state = copy.deepcopy(state)
    while not is_terminal(copy_state):
        player = 1 if copy_state.current_player == 'red' else 2
        copy_state = greedy_best_move(player, copy_state)
        copy_state.current_player = 'red' if player == 2 else 'black'
        if is_draw(copy_state):
            return 0
    if copy_state.num_moves > 5:
        bonus = evaluate_state(copy_state)
        return bonus * 0.0001
    return 0

def get_result(state):
    bonus = evaluate_state(state)
    if state.num_moves > 5:
        return bonus * 0.0001

def evaluate_state(state):
    total_evaluation = 0
    for i in range(10):
        for j in range(9):
            total_evaluation += get_piece_value(state.board[i][j], i, j)
    return total_evaluation

def is_king_captured(board, player):
    king_piece = f"ts{player}"
    for row in board:
        if king_piece in row:
            return False
    return True

def is_draw(state):
    return (not any(all_posible_moves(1, state.board).values()) and
            not any(all_posible_moves(2, state.board).values())) or state.num_moves >= 30

def is_terminal(state):
    board = state.board
    return is_king_captured(board, 1) or is_king_captured(board, 2)

def backpropagate(node, score):
    while node is not None:
        node.visits += 1
        node.score += score
        node = node.parent

def mcts(state, num_iterations):
    root = Node(state)
    root.expand()
    for _ in range(num_iterations):
        node = root
        while node.is_fully_expanded():
            node = node.select_child()
            if not node:
                break
        if node and not node.is_fully_expanded():
            node.expand()
        if node.children:
            selected_child = node.select_child()  # Chọn một trong các node con đã được mở rộng
            if selected_child:
                score = simulate(selected_child.state)
                backpropagate(selected_child, score)
    if root.children:
        best_child = max(root.children, key=lambda child: child.visits)
        return best_child.state
    else:
        return state

def main():
    initial_state = [
        ["x12", "m12", "tj12", "s12", "ts2", "s22", "tj22", "m22", "x22"],
        ["", "", "", "", "", "", "", "", ""],
        ["", "p12", "", "", "", "", "", "p22", ""],
        ["to12", "", "to22", "", "to32", "", "to42", "", "to52"],
        ["", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", ""],
        ["to11", "", "to21", "", "to31", "", "to41", "", "to51"],
        ["", "", "", "", "p11", "", "", "p21", ""],
        ["", "", "", "", "", "", "", "", ""],
        ["x11", "m11", "tj11", "s11", "ts1", "s21", "tj21", "m21", "x21"],
    ]

    state = GameState(initial_state)
    state.current_player = 'red'  # Khởi tạo người chơi hiện tại
    num_iterations = 100
    best_state = mcts(state, num_iterations)
    print(best_state.board)

if __name__ == "__main__":
    main()
