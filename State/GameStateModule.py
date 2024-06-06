#Game state class
class GameState:
    def __init__(self, board):
        self.current_player = 'black'
        self.board_dict = self.convert_dict(board)
        self.board = board
        self.num_moves = 0  # Thêm thuộc tính để đếm số lượt di chuyển

    def switch_player(self):
        self.current_player = 'red' if self.current_player == 'black' else 'black'

    def print_turn_player(self):
        print(self.current_player)

    # Change array board to dict
    def convert_dict(self, board):
        board_dict = {}
        for row in range(10):
            for col in range(9):
                piece = board[row][col]
                if piece:
                    position = (row, col)
                    board_dict[piece] = position
        return board_dict

    """
        Args
        old_position: example (6, 0)
        next_position: example (5, 0)
    """
    def next_state(self, old_position, next_position):
        tmp = self.board[old_position[0]][old_position[1]]
        self.board[old_position[0]][old_position[1]] = ''
        self.board[next_position[0]][next_position[1]] = tmp
        self.num_moves += 1  # Cập nhật số lượt di chuyển sau mỗi nước đi