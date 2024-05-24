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
                    position = (row, col)
                    board_dict[piece] = position
        return board_dict

    # Connect with Rule
    def convert_rule_state(self, board):
        # Define the mapping
        mapping = {
            'x': 'r',
            'm': 'h',
            'tj': 'e',
            's': 'g',
            'ts': 'k',
            'p': 'c',
            'to': 'p'
        }

        # Function to apply mapping and create new element
        def transform_element(element):
            if element == "":
                return "-"
            # Extract the letter part and the number part
            for key in mapping:
                if element.startswith(key):
                    # Construct the new string based on the mapping
                    num = element[-1:]
                    letter = mapping[key]
                    new_num = num[0]
                    return f"{letter}_{new_num}"
            return element

        # Transform the board
        output_board = [[transform_element(element) for element in row] for row in board]

        # Replace "-" back to "" for clarity in the output
        output_board = [[element if element != "-" else "" for element in row] for row in output_board]

        return output_board