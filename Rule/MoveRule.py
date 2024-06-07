def get_xiangqi_king_moves(current_pos, state, name):
    """
    Returns a list of valid positions to which the king can move in Xiangqi.

    Args:
        current_pos (tuple): Current position of the knight (row, column).
        state (list): The current state of the Xiangqi board.
        name (string): name of the piece
    Returns:
        list: List of valid positions (tuples) where the king can move.
    """
    row, col = current_pos
    king_moves = []

    # Possible king moves (up, down, left, right)
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    if name == 'ts2':
        for i in range(row+1, 10, 1):
            if state[i][col] == '':
                continue
            else:
                if state[i][col] == 'ts1':
                    king_moves.append((i, col))
                    break
                else:
                    break

    if name == 'ts1':
        for i in range(row-1, -1, -1):
            if state[i][col] == '':
                continue
            else:
                if state[i][col] == 'ts2':
                    king_moves.append((i, col))
                    break
                else:
                    break

    for dr, dc in directions:
        new_row, new_col = row + dr, col + dc
        # Check if the new position is within the 3x3 palace boundaries
        if name == 'ts1' and check_palace(new_row, new_col):
            if "1" not in color_position(state[new_row][new_col]):
                king_moves.append((new_row, new_col))

        if name == 'ts2' and check_palace(new_row, new_col):
            if "2" not in color_position(state[new_row][new_col]):
                king_moves.append((new_row, new_col))

    return king_moves


def get_xiangqi_guard_moves(current_pos, state, name):
    """
    Returns a list of valid positions to which the guard can move in Xiangqi.

    Args:
        current_pos (tuple): Current position of the knight (row, column).
        state (list): The current state of the Xiangqi board.
        name (string): name of the piece
    Returns:
        list: List of valid positions (tuples) where the guard can move.
    """
    row, col = current_pos
    guard_moves = []

    # Possible guard moves (diagonals)
    directions = [(1, 1), (-1, -1), (1, -1), (-1, 1)]

    for dr, dc in directions:
        new_row, new_col = row + dr, col + dc

        # Check if the new position is within the 3x3 palace boundaries
        if (name == 's11' or name == 's21') and check_palace(new_row, new_col):
            if "1" not in color_position(state[new_row][new_col]):
                guard_moves.append((new_row, new_col))

        if (name == 's12' or name == 's22') and check_palace(new_row, new_col):
            if "2" not in color_position(state[new_row][new_col]):
                guard_moves.append((new_row, new_col))

    return guard_moves


def get_xiangqi_elephant_moves(current_pos, state, name):
    """
    Returns a list of valid positions to which the elephant (bishop) can move in Xiangqi.

    Args:
        current_pos (tuple): Current position of the knight (row, column).
        state (list): The current state of the Xiangqi board.
        name (string): name of the piece
    Returns:
        list: List of valid positions (tuples) where the elephant can move.
    """
    row, col = current_pos
    elephant_moves = []

    # Possible diagonal moves (up-left, up-right, down-left, down-right)
    directions = [(1, 1), (-1, 1), (1, -1), (-1, -1)]

    for dr, dc in directions:
        new_row, new_col = row + 2 * dr, col + 2 * dc
        row_near, col_near = row + dr, col + dc

        # Check if the new position is within the board boundaries and not crossing the river
        if (name == "tj11" or name == "tj21") and check_board(new_row, new_col) and new_row >= 5:
            if state[row_near][col_near] == '':
                if "1" not in color_position(state[new_row][new_col]):
                    elephant_moves.append((new_row, new_col))

        # Check if the new position is within the board boundaries and not crossing the river
        if (name == "tj12" or name == "tj22") and check_board(new_row, new_col) and new_row <= 4:
            if state[row_near][col_near] == '':
                if "2" not in color_position(state[new_row][new_col]):
                    elephant_moves.append((new_row, new_col))

    return elephant_moves


def get_xiangqi_knight_moves(current_pos, state, name):
    """
    Returns a list of valid positions to which the knight (horse) can move in Xiangqi.

    Args:
        current_pos (tuple): Current position of the knight (row, column).
        state (list): The current state of the Xiangqi board.
        name (string): name of the piece
    Returns:
        list: List of valid positions (tuples) where the knight can move.
    """
    row, col = current_pos
    knight_moves = []

    # Possible knight moves (L-shaped)
    moves = [(1, 2), (2, 1), (-1, 2), (-2, 1),
             (1, -2), (2, -1), (-1, -2), (-2, -1)]

    for dr, dc in moves:
        new_row, new_col = row + dr, col + dc

        # Check if there is a piece adjacent to the knight in the horizontal or vertical direction
        row_near = row + dr // 2 if dr > 0 else row - (dr // -2)
        col_near = col + dc // 2 if dc > 0 else col - (dc // -2)
        # Check if the new position is within the board boundaries
        if (name == 'm11' or name == 'm21') and check_board(new_row, new_col):
            if state[row_near][col_near] == '':
                if "1" not in color_position(state[new_row][new_col]):
                    knight_moves.append((new_row, new_col))

        if (name == 'm12' or name == 'm22') and check_board(new_row, new_col):
            if state[row_near][col_near] == '':
                if "2" not in color_position(state[new_row][new_col]):
                    knight_moves.append((new_row, new_col))

    return knight_moves


def get_xiangqi_pawn_moves(current_pos, state, name):
    """
    Returns a list of valid positions to which the pawn (soldier) can move in Xiangqi.

    Args:
        current_pos (tuple): Current position of the pawn (row, column).
        state (list): The current state of the Xiangqi board.
        name (string): name of the piece

    Returns:
        list: List of valid positions (tuples) where the pawn can move.
    """
    row, col = current_pos
    pawn_moves = []

    # Determine the direction of movement based on pawn color
    direction = -1 if name == 'to11' or name == 'to21' or name == 'to31' or name == 'to41' or name == 'to51' else 1

    # Possible pawn moves (forward and diagonal captures)
    forward_row = row + direction
    left_col, right_col = col - 1, col + 1

    if name == 'to11' or name == 'to21' or name == 'to31' or name == 'to41' or name == 'to51':
        if row <= 4:
            if check_board(row, left_col) and "1" not in color_position(state[row][left_col]) :
                pawn_moves.append((row, left_col))
            if check_board(row, right_col) and "1" not in color_position(state[row][right_col]) :
                pawn_moves.append((row, right_col))
            if check_board(forward_row, col) and "1" not in color_position(state[forward_row][col]):
                pawn_moves.append((forward_row, col))
        if row > 4:
            if  check_board(forward_row, col) and "1" not in color_position(state[forward_row][col]) :
                pawn_moves.append((forward_row, col))

    if name == 'to12' or name == 'to22' or name == 'to32' or name == 'to42' or name == 'to52':
        if row >= 5:
            if check_board(row, left_col) and "2" not in color_position(state[row][left_col]) :
                pawn_moves.append((row, left_col))
            if check_board(row, right_col) and "2" not in color_position(state[row][right_col]) :
                pawn_moves.append((row, right_col))
            if check_board(forward_row, col) and "2" not in color_position(state[forward_row][col]) :
                pawn_moves.append((forward_row, col))
        if row < 5:
            if check_board(forward_row, col) and "2" not in color_position(state[forward_row][col]):
                pawn_moves.append((forward_row, col))

    return pawn_moves


def get_xiangqi_rook_moves(current_pos, state, name):
    """
    Returns a list of valid positions to which the rook (chariot) can move in Xiangqi.

    Args:
        current_pos (tuple): Current position of the rook (row, column).
        state (list): The current state of the Xiangqi board.
        name (string): name of the piece

    Returns:
        list: List of valid positions (tuples) where the rook can move.
    """
    row, col = current_pos
    rook_moves = []

    # todo: check row move
    for i in range(1, 10):
        new_row = row + i
        if not check_board(new_row, col):
            break
        if state[new_row][col] == '':
            rook_moves.append((new_row, col))
            continue
        else:
            if '2' in color_position(state[new_row][col]) and (name == 'x11' or name == 'x21'):
                rook_moves.append((new_row, col))
                break
            if '1' in color_position(state[new_row][col]) and (name == 'x12' or name == 'x22'):
                rook_moves.append((new_row, col))
                break
            break

    for i in range(1, 10):
        new_row = row - i
        if not check_board(new_row, col):
            break
        if state[new_row][col] == '':
            rook_moves.append((new_row, col))
            continue
        else:
            if '2' in color_position(state[new_row][col]) and (name == 'x11' or name == 'x21'):
                rook_moves.append((new_row, col))
                break
            if '1' in color_position(state[new_row][col]) and (name == 'x12' or name == 'x22'):
                rook_moves.append((new_row, col))
                break
            break

    # todo: check col move
    for i in range(1, 10):
        new_col = col + i
        if not check_board(row, new_col):
            break
        if state[row][new_col] == '':
            rook_moves.append((row, new_col))
            continue
        else:
            if '2' in color_position(state[row][new_col]) and (name == 'x11' or name == 'x21'):
                rook_moves.append((row, new_col))
                break
            if '1' in color_position(state[row][new_col]) and (name == 'x12' or name == 'x22'):
                rook_moves.append((row, new_col))
                break
            break

    for i in range(1, 10):
        new_col = col - i
        if not check_board(row, new_col):
            break
        if state[row][new_col] == '':
            rook_moves.append((row, new_col))
            continue
        else:
            if '2' in color_position(state[row][new_col]) and (name == 'x11' or name == 'x21'):
                rook_moves.append((row, new_col))
                break
            if '1' in color_position(state[row][new_col]) and (name == 'x12' or name == 'x22'):
                rook_moves.append((row, new_col))
                break
            break

    return rook_moves


def get_xiangqi_cannon_moves(current_pos, state, name):
    """
    Returns a list of valid positions to which the rook (chariot) can move in Xiangqi.

    Args:
        current_pos (tuple): Current position of the knight (row, column).
        state (list): The current state of the Xiangqi board.
        name (string): name of the piece
    Returns:
        list: List of valid positions (tuples) where the rook can move.
    """
    row, col = current_pos
    cannon_moves = []
    cross_over = []

    # todo: check row move
    for i in range(1, 10 + 1):  # ? i : 1 -> 9
        new_row = row + i
        if len(cross_over) == 0:
            if not check_board(new_row, col):
                break
            if state[new_row][col] == '':
                cannon_moves.append((new_row, col))
            else:
                cross_over.append(state[new_row][col])
        else:
            if not check_board(new_row, col):
                cross_over.pop()
                break
            if state[new_row][col] == '':
                continue
            if '1' in color_position(state[new_row][col]) and (name == "p12" or name == "p22"):
                cross_over.pop()
                cannon_moves.append((new_row, col))
                break
            if '2' in color_position(state[new_row][col]) and (name == "p11" or name == "p21"):
                cross_over.pop()
                cannon_moves.append((new_row, col))
                break
            if '2' in color_position(state[new_row][col]) and (name == "p12" or name == "p22"):
                cross_over.pop()
                break
            if '1' in color_position(state[new_row][col]) and (name == "p11" or name == "p21"):
                cross_over.pop()
                break

    # todo: check row move
    for i in range(1, 10 + 1):  # ? i : 1 -> 10
        new_row = row - i
        if len(cross_over) == 0:
            if not check_board(new_row, col):
                break
            if state[new_row][col] == '':
                cannon_moves.append((new_row, col))
            else:
                cross_over.append(state[new_row][col])
        else:
            if not check_board(new_row, col):
                cross_over.pop()
                break
            if state[new_row][col] == '':
                continue
            if '1' in color_position(state[new_row][col]) and (name == "p12" or name == "p22"):
                cross_over.pop()
                cannon_moves.append((new_row, col))
                break
            if '2' in color_position(state[new_row][col]) and (name == "p11" or name == "p21"):
                cross_over.pop()
                cannon_moves.append((new_row, col))
                break
            if '2' in color_position(state[new_row][col]) and (name == "p12" or name == "p22"):
                cross_over.pop()
                break
            if '1' in color_position(state[new_row][col]) and (name == "p11" or name == "p21"):
                cross_over.pop()
                break

    # todo: check col move
    for i in range(1, 9 + 1):  # ? i : 1 -> 9
        new_col = col + i
        if len(cross_over) == 0:
            if not check_board(row, new_col):
                break
            if state[row][new_col] == '':
                cannon_moves.append((row, new_col))
            else:
                cross_over.append(state[row][new_col])
        else:
            if not check_board(row, new_col):
                cross_over.pop()
                break
            if state[row][new_col] == '':
                continue
            if '1' in color_position(state[row][new_col]) and (name == "p12" or name == "p22"):
                cross_over.pop()
                cannon_moves.append((row, new_col))
                break
            if '2' in color_position(state[row][new_col]) and (name == "p11" or name == "p21"):
                cross_over.pop()
                cannon_moves.append((row, new_col))
                break
            if '2' in color_position(state[row][new_col]) and (name == "p12" or name == "p22"):
                cross_over.pop()
                break
            if '1' in color_position(state[row][new_col]) and (name == "p11" or name == "p21"):
                cross_over.pop()
                break

    # todo: check col move
    for i in range(1, 9 + 1):  # ? i : 1 -> 9
        new_col = col - i
        if len(cross_over) == 0:
            if not check_board(row, new_col):
                break
            if state[row][new_col] == '':
                cannon_moves.append((row, new_col))
            else:
                cross_over.append(state[row][new_col])
        else:
            if not check_board(row, new_col):
                cross_over.pop()
                break
            if state[row][new_col] == '':
                continue
            if '1' in color_position(state[row][new_col]) and (name == "p12" or name == "p22"):
                cross_over.pop()
                cannon_moves.append((row, new_col))
                break
            if '2' in color_position(state[row][new_col]) and (name == "p11" or name == "p21"):
                cross_over.pop()
                cannon_moves.append((row, new_col))
                break
            if '2' in color_position(state[row][new_col]) and (name == "p12" or name == "p22"):
                cross_over.pop()
                break
            if '1' in color_position(state[row][new_col]) and (name == "p11" or name == "p21"):
                cross_over.pop()
                break

    return cannon_moves

def check_palace(row, col):
    if 3 <= col <= 5 and 0 <= row <= 2:
        return True
    if 3 <= col <= 5 and 7 <= row <= 9:
        return True
    return False


def check_board(row, col):
    if 0 <= col <= 8 and 0 <= row <= 9:
        return True
    return False


def color_position(state):
    if state == '':
        return ''
    if state[-1] == '1':
        return '1'
    if state[-1] == '2':
        return '2'