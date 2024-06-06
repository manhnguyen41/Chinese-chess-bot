from Rule.MoveRule import (get_xiangqi_king_moves, get_xiangqi_guard_moves, get_xiangqi_elephant_moves,
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
    if piece == 'ts1':
        move = get_xiangqi_king_moves(position, state, piece)

    if piece == 's11' or piece == 's21':
        move = get_xiangqi_guard_moves(position, state, piece)

    if piece == 'm11' or piece == 'm21':
        move = get_xiangqi_knight_moves(position, state, piece)

    if piece == 'tj11' or piece == 'tj21':
        move = get_xiangqi_elephant_moves(position, state, piece)

    if piece == 'x11' or piece == 'x21':
        move = get_xiangqi_rook_moves(position, state, piece)

    if piece == 'p11' or piece == 'p21':
        move = get_xiangqi_cannon_moves(position, state, piece)

    if piece == 'to11' or piece == 'to21' or piece == 'to31' or piece == 'to41' or piece == 'to51':
        move = get_xiangqi_pawn_moves(position, state, piece)

    # todo: Black team
    if piece == 'ts2':
        move = get_xiangqi_king_moves(position, state, piece)

    if piece == 's12' or piece == 's22':
        move = get_xiangqi_guard_moves(position, state, piece)

    if piece == 'm12' or piece == 'm22':
        move = get_xiangqi_knight_moves(position, state, piece)

    if piece == 'tj12' or piece == 'tj22':
        move = get_xiangqi_elephant_moves(position, state, piece)

    if piece == 'x12' or piece == 'x22':
        move = get_xiangqi_rook_moves(position, state, piece)

    if piece == 'p12' or piece == 'p22':
        move = get_xiangqi_cannon_moves(position, state, piece)

    if piece == 'to12' or piece == 'to22' or piece == 'to32' or piece == 'to42' or piece == 'to52':
        move = get_xiangqi_pawn_moves(position, state, piece)

    return (piece, move)


red_pieces = ['to11', 'to21', 'to31', 'to41', 'to51', 'p11', 'p21', 'x11', 'm11', 'tj11', 's11', 'ts1', 's21', 'tj21', 'm21', 'x21']
black_pieces = ['x12', 'm12', 'tj12', 's12', 'ts2', 's22', 'tj22', 'm22', 'x22', 'p12', 'p22', 'to12', 'to22', 'to32', 'to42', 'to52']


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