from Strategy.ABPruning.ABPruning import find_best_move
from State.GameStateModule import GameState
from Strategy.Greedy.greedy import greedy_best_move
import time

from Strategy.MCTSAlgorithm.mcts import mcts
from Strategy.Minimax.Minimax import find_best_move_minimax


def is_king_captured(board, player):
    king_piece = f"ts{player}"
    for row in board:
        if king_piece in row:
            return False
    return True

def is_terminal(board):
    return is_king_captured(board, 1) or is_king_captured(board, 2)

def main():
    num_matches = 27
    blackWin = 0
    redWin = 0
    draw = 0
    total_time = 0
    for _ in range(num_matches):
        winner = ''
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
        running = True
        current_player = '1'
        turn = 0
        time_count = 0
        while running:
            if turn == 54:
                winner = 'draw'
                running = False
                continue
            # Check for game over
            if is_terminal(board):
                winner = "Red" if is_king_captured(board, 2) else "Black"
                running = False
                continue

            # Update the remaining time in clocks
            if current_player == '1':
                game_state = GameState(board)
                bestmove = find_best_move(game_state, 2, False)
                game_state.next_state(bestmove[0], bestmove[1])
                current_player = '2'

                # game_state = GameState(board)
                # new_state = greedy_best_move(1, game_state)
                # board = new_state.board
                # current_player = '2'

            else:  # lượt chơi người thứ 2
                start_time = time.time()

                # game_state = GameState(board)
                # new_state = greedy_best_move(2, game_state)
                # board = new_state.board
                # current_player = '1'

                num_iterations = 10
                game_state = GameState(board)
                new_state = mcts(game_state, num_iterations)
                new_board = new_state.board
                board = new_board
                current_player = '1'
                print(new_board)

                # game_state = GameState(board)
                # bestmove = find_best_move(game_state, 2, True)  # Chinh depth cho player 2
                # game_state.next_state(bestmove[0], bestmove[1])
                # current_player = '1'

                # game_state = GameState(board)
                # bestmove = find_best_move_minimax(game_state, 4, True)  # Chinh depth cho player 2
                # game_state.next_state(bestmove[0], bestmove[1])
                # current_player = '1'

                end_time = time.time()
                time_count += end_time - start_time

            turn+=1

        if winner == 'Red':
            redWin+=1
        elif winner == 'Black':
            blackWin+=1
        elif winner == 'draw':
            draw+=1

        total_time += time_count / turn * 2

        print(winner, _)
        print((time_count / turn * 2) * 1000)

    print(redWin)
    print(blackWin)
    print(draw)
    print((total_time / num_matches) * 1000)

if __name__ == "__main__":
    main()