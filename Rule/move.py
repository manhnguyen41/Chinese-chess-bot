from piece_move import (get_xiangqi_king_moves, get_xiangqi_guard_moves, get_xiangqi_elephant_moves,
                        get_xiangqi_cannon_moves, get_xiangqi_knight_moves, get_xiangqi_rook_moves,
                        get_xiangqi_pawn_moves)


def move_piece(position, piece, state):
    """_summary_

    Args:
        position (tuple): current position of piece
        piece (_type_): _description_
    """
    move = []

    # todo: Red team
    if piece == 'k_1':
        move = get_xiangqi_king_moves(position, state, piece)

    if piece == 'g_1':
        move = get_xiangqi_guard_moves(position, state, piece)

    if piece == 'h_1':
        move = get_xiangqi_knight_moves(position, state, piece)

    if piece == 'e_1':
        move = get_xiangqi_elephant_moves(position, state, piece)

    if piece == 'r_1':
        move = get_xiangqi_rook_moves(position, state, piece)

    if piece == 'c_1':
        move = get_xiangqi_cannon_moves(position, state, piece)

    if piece == 'p_1':
        move = get_xiangqi_pawn_moves(position, state, piece)

    # todo: Black team
    if piece == 'k_2':
        move = get_xiangqi_king_moves(position, state, piece)

    if piece == 'g_2':
        move = get_xiangqi_guard_moves(position, state, piece)

    if piece == 'h_2':
        move = get_xiangqi_knight_moves(position, state, piece)

    if piece == 'e_2':
        move = get_xiangqi_elephant_moves(position, state, piece)

    if piece == 'r_2':
        move = get_xiangqi_rook_moves(position, state, piece)

    if piece == 'c_2':
        move = get_xiangqi_cannon_moves(position, state, piece)

    if piece == 'p_2':
        move = get_xiangqi_pawn_moves(position, state, piece)

    return (piece, move)


red_pieces = ["k_1", "g_1", "h_1", "e_1", "r_1", "c_1", 'p_1']
black_pieces = ["k_2", "g_2", "h_2", "e_2", "r_2", "c_2", 'p_2']


def all_posible_moves(team, state):
    """
    Calculates all possible moves for a given team on a chessboard represented by the state.

    Args:
        team (int): 1 for red pieces, 2 for black pieces.
        state (list): A 2D list representing the chessboard, where each element is a string
                      indicating the piece at that position (empty spaces can be denoted by
                      a special string like '-').

    Returns:
        dict: A dictionary where keys are tuples of the form (piece, old_position),
              and values are the resulting state after the move.

    Raises:
        ValueError: If the team number is not 1 or 2.
    """

    result = dict()

    if team not in (1, 2):
        raise ValueError("Invalid team number. Must be 1 (red) or 2 (black).")

    if team == 1:
        team_pieces = red_pieces
    else:
        team_pieces = black_pieces

    for i in range(len(state)):
        for j in range(len(state[i])):
            if state[i][j] in team_pieces:
                key = (state[i][j], (i, j))
                result[key] = move_piece((i, j), state[i][j], state)

    return result
