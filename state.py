#Game state class
class GameState:
    def __init__(self, board):
        self.current_player = 'red'
        self.board_dict = self.convert_dict(board)

    def switch_player(self):
        self.current_player = 'black' if self.current_player == 'red' else 'red'

    def print_turn_player(self):
        print(self.current_player)

    # Change array board to dict
    def convert_dict(self, board):
        board_dict = {}
        for row in range(10):
            for col in range(9):
                piece = board[row][col]
                if piece:
                    postion = (row, col)
                    board_dict[piece] = postion
        return board_dict