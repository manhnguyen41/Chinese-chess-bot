import os
import pygame
import sys
from State.GameStateModule import *
from PIL import Image
from Rule.MoveRule import *
from Rule.move import *
from MCTS.mcts import *
from ABPruning import *

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 900, 650
CELL_SIZE = WIDTH // 15

BOARD_OFFSET_X = CELL_SIZE
BOARD_OFFSET_Y = CELL_SIZE
PIECE_FONT_SIZE = 40

PLAYER_AVATAR_SIZE = 100
AI_PLAYER_AVATAR_POS = (CELL_SIZE * 11, CELL_SIZE)
HUMAN_PLAYER_AVATAR_POS = (CELL_SIZE * 11, CELL_SIZE * 8)
AI_AVATAR_CENTER = (
AI_PLAYER_AVATAR_POS[0] + PLAYER_AVATAR_SIZE // 2, AI_PLAYER_AVATAR_POS[1] + PLAYER_AVATAR_SIZE // 1.5)

CIRCLE_RADIUS = PLAYER_AVATAR_SIZE // 1.5
CIRCLE_THICKNESS = 6
CIRCLE_COLOR = (26, 255, 26)
DOT_COLOR = (102, 217, 255)

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chinese Chess")


# Function to load images from folders
def load_images(folder):
    images = {}
    for filename in os.listdir(folder):
        name, ext = os.path.splitext(filename)
        if ext.lower() in ['.png', '.jpg', '.jpeg']:
            # Open image with PIL
            with Image.open(os.path.join(folder, filename)) as img:
                # Convert to RGBA color
                img = img.convert("RGBA")
                # Convert PIL image
                images[name] = pygame.image.fromstring(img.tobytes("raw", "RGBA"), img.size, "RGBA")
    return images


# Load images for pieces
home_pieces = load_images("image/1")
away_pieces = load_images("image/-1")


# Function to draw the board
def draw_board(valid_destinations=None):
    # Draw background color
    screen.fill((255, 228, 181))

    # Draw border
    pygame.draw.rect(screen, (0, 0, 0), (BOARD_OFFSET_X, BOARD_OFFSET_Y, CELL_SIZE * 8, CELL_SIZE * 9), 2)

    # Draw horizontal lines
    for row in range(9):
        pygame.draw.line(screen, (0, 0, 0), (BOARD_OFFSET_X, BOARD_OFFSET_Y + row * CELL_SIZE),
                         (BOARD_OFFSET_X + CELL_SIZE * 8, BOARD_OFFSET_Y + row * CELL_SIZE), 2)

    # Draw vertical lines
    for col in range(8):
        pygame.draw.line(screen, (0, 0, 0), (BOARD_OFFSET_X + col * CELL_SIZE, BOARD_OFFSET_Y),
                         (BOARD_OFFSET_X + col * CELL_SIZE, BOARD_OFFSET_Y + CELL_SIZE * 9), 2)

    # Draw river
    for col in range(1, 8):
        pygame.draw.line(screen, (255, 228, 181), (BOARD_OFFSET_X + col * CELL_SIZE, BOARD_OFFSET_Y + 4 * CELL_SIZE),
                         (BOARD_OFFSET_X + col * CELL_SIZE, BOARD_OFFSET_Y + 5 * CELL_SIZE), 2)

    # Draw palace
    pygame.draw.line(screen, (0, 0, 0), (BOARD_OFFSET_X + 3 * CELL_SIZE, BOARD_OFFSET_Y),
                     (BOARD_OFFSET_X + 5 * CELL_SIZE, BOARD_OFFSET_Y + 2 * CELL_SIZE), 2)
    pygame.draw.line(screen, (0, 0, 0), (BOARD_OFFSET_X + 5 * CELL_SIZE, BOARD_OFFSET_Y),
                     (BOARD_OFFSET_X + 3 * CELL_SIZE, BOARD_OFFSET_Y + 2 * CELL_SIZE), 2)
    pygame.draw.line(screen, (0, 0, 0), (BOARD_OFFSET_X + 3 * CELL_SIZE, BOARD_OFFSET_Y + 7 * CELL_SIZE),
                     (BOARD_OFFSET_X + 5 * CELL_SIZE, BOARD_OFFSET_Y + 9 * CELL_SIZE), 2)
    pygame.draw.line(screen, (0, 0, 0), (BOARD_OFFSET_X + 5 * CELL_SIZE, BOARD_OFFSET_Y + 7 * CELL_SIZE),
                     (BOARD_OFFSET_X + 3 * CELL_SIZE, BOARD_OFFSET_Y + 9 * CELL_SIZE), 2)

    if valid_destinations:
        for dest_row, dest_col in valid_destinations:
            pygame.draw.circle(screen, DOT_COLOR,
                               (BOARD_OFFSET_X + dest_col * CELL_SIZE, BOARD_OFFSET_Y + dest_row * CELL_SIZE), 4)


# Function to draw pieces on the board
def draw_pieces(board):
    for row in range(10):
        for col in range(9):
            piece = board[row][col]
            if piece.endswith('2'):
                image = away_pieces[piece]
            elif piece.endswith('1'):
                image = home_pieces[piece]
            else:
                continue
                # image = pygame.transform.scale(image, (CELL_SIZE, CELL_SIZE))

            piece_x = BOARD_OFFSET_X + col * CELL_SIZE - image.get_width() // 2
            piece_y = BOARD_OFFSET_Y + row * CELL_SIZE - image.get_height() // 2

            screen.blit(image, (piece_x, piece_y))


# Load images for avatar
AI_player_avatar = pygame.image.load("avatar/robot_avatar.png").convert_alpha()
AI_player_avatar = pygame.transform.scale(AI_player_avatar, (PLAYER_AVATAR_SIZE, PLAYER_AVATAR_SIZE))
human_player_avatar = pygame.image.load("avatar/player.jpg").convert_alpha()
human_player_avatar = pygame.transform.scale(human_player_avatar, (PLAYER_AVATAR_SIZE, PLAYER_AVATAR_SIZE))

# Load line text "player" below avatar
font = pygame.font.Font(None, 30)


# Function to draw avatar of human player and AI player
def draw_player_avatar(time_left_player1, time_left_player2):
    screen.blit(human_player_avatar, HUMAN_PLAYER_AVATAR_POS)
    human_text = font.render("Player 1", True, (0, 0, 0))
    human_text_rect = human_text.get_rect(center=(
    HUMAN_PLAYER_AVATAR_POS[0] + PLAYER_AVATAR_SIZE // 2, HUMAN_PLAYER_AVATAR_POS[1] + PLAYER_AVATAR_SIZE * 1.2))
    screen.blit(human_text, human_text_rect)
    draw_clock(time_left_player1, HUMAN_PLAYER_AVATAR_POS)

    screen.blit(AI_player_avatar, AI_PLAYER_AVATAR_POS)
    AI_text = font.render("Player 2", True, (0, 0, 0))
    AI_text_rect = AI_text.get_rect(
        center=(AI_PLAYER_AVATAR_POS[0] + PLAYER_AVATAR_SIZE // 2, AI_PLAYER_AVATAR_POS[1] + PLAYER_AVATAR_SIZE * 1.2))
    screen.blit(AI_text, AI_text_rect)
    draw_clock(time_left_player2, AI_PLAYER_AVATAR_POS)


# Function to draw clock
def draw_clock(time_left, pos):
    minutes = time_left // 60
    seconds = time_left % 60
    timer_text = font.render(f"Time left: {minutes:02}:{seconds:02}", True, (0, 0, 0))
    screen.blit(timer_text, (pos[0], pos[1] + 140))


# Function to draw dot
def draw_dot(current_player):
    if current_player == '1':
        pygame.draw.circle(screen, (0, 0, 0), (HUMAN_PLAYER_AVATAR_POS[0] + PLAYER_AVATAR_SIZE // 2 - 50,
                                               HUMAN_PLAYER_AVATAR_POS[1] + PLAYER_AVATAR_SIZE * 1.2), 5)
    else:
        pygame.draw.circle(screen, (0, 0, 0), (
        AI_PLAYER_AVATAR_POS[0] + PLAYER_AVATAR_SIZE // 2 - 50, AI_PLAYER_AVATAR_POS[1] + PLAYER_AVATAR_SIZE * 1.2), 5)


# Check with rule if move is valid (rules of moving pieces)
def is_valid_move(selected_piece, destination_square, board, valid_destinations):
    if destination_square in valid_destinations:
        return True
    return False


def move_piece(selected_piece, destination_square, board, game_state, current_player, state_move_piece):
    selected_row, selected_col = selected_piece
    piece = board[selected_row][selected_col]

    if piece[-1] == current_player:
        selected_row, selected_col = selected_piece
        dest_row, dest_col = destination_square
        piece_to_move = board[selected_row][selected_col]
        # update position in board
        board[selected_row][selected_col] = ''
        board[dest_row][dest_col] = piece_to_move

        # update position in board_dict
        game_state.board_dict[piece_to_move] = (dest_row, dest_col)
        # update state move piece
        state_move_piece[0] = True
        # Re-update pos of pieces
        draw_board()
        draw_pieces(board)
        pygame.display.flip()
    else:
        state_move_piece[0] = False


# Function to check for game over
def check_game_over(board):
    kings = sum(row.count('ts1') + row.count('ts2') for row in board)
    return kings < 2


# Function to display game over message
def display_game_over(winner):
    font = pygame.font.Font(None, 74)
    game_over_text = f"Game Over! {winner} Wins!"
    text = font.render(game_over_text, True, (255, 0, 0))
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.wait(5000)  # Display the message for 5 seconds


# Main
def main():
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
    game_state = GameState(board)

    start_ticks_player1 = pygame.time.get_ticks()
    start_ticks_player2 = pygame.time.get_ticks()

    time_limit = 1800  # 30 minutes converts to seconds
    time_left_player1 = time_limit
    time_left_player2 = time_limit
    elapsed_time_player1 = 0
    elapsed_time_player2 = 0

    current_player = '1'  # '1' for home and '2' for away
    state_move_piece = [False]

    selected_piece = None
    destination_square = None
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.constants.MOUSEBUTTONDOWN:
                # Handle mouse click
                mouse_x, mouse_y = event.pos

                # 30 is near haft value of image's size
                row = abs((mouse_y + 30 - BOARD_OFFSET_Y)) // CELL_SIZE
                col = abs((mouse_x + 30 - BOARD_OFFSET_X)) // CELL_SIZE
                if 0 <= row < 10 and 0 <= col < 9:
                    piece = board[row][col]

                    if piece:
                        if selected_piece is None:
                            selected_piece = (row, col)
                        else:
                            destination_square = (row, col)
                            # Check if the move is valid and update the board
                            if is_valid_move(selected_piece, destination_square, board, valid_destinations):
                                move_piece(selected_piece, destination_square, board, game_state, current_player,
                                           state_move_piece)
                                # state_move_piece = True
                            selected_piece = None
                            destination_square = None

                    else:
                        if selected_piece is not None:
                            destination_square = (row, col)
                            # Check if the move is valid and update the board
                            if is_valid_move(selected_piece, destination_square, board, valid_destinations):
                                move_piece(selected_piece, destination_square, board, game_state, current_player,
                                           state_move_piece)
                                # state_move_piece = True
                            selected_piece = None
                            destination_square = None
                # Switch turn in state
                if selected_piece is None and destination_square is None:
                    game_state.print_turn_player()
                    game_state.switch_player()
        # Check valid destination for each moves
        if selected_piece:
            name = board[row][col]
            if name == 'ts1' or name == 'ts2':
                valid_destinations = get_xiangqi_king_moves(selected_piece, board, name)
            if name == 's11' or name == 's21' or name == 's12' or name == 's22':
                valid_destinations = get_xiangqi_guard_moves(selected_piece, board, name)
            if name == "tj11" or name == "tj21" or name == "tj12" or name == "tj22":
                valid_destinations = get_xiangqi_elephant_moves(selected_piece, board, name)
            if name == 'm11' or name == 'm21' or name == 'm12' or name == 'm22':
                valid_destinations = get_xiangqi_knight_moves(selected_piece, board, name)
            if name == 'to11' or name == 'to21' or name == 'to31' or name == 'to41' or name == 'to51' or name == 'to12' or name == 'to22' or name == 'to32' or name == 'to42' or name == 'to52':
                valid_destinations = get_xiangqi_pawn_moves(selected_piece, board, name)
            if name == 'x11' or name == 'x21' or name == 'x12' or name == 'x22':
                valid_destinations = get_xiangqi_rook_moves(selected_piece, board, name)
            if name == 'p11' or name == 'p21' or name == 'p12' or name == 'p22':
                valid_destinations = get_xiangqi_cannon_moves(selected_piece, board, name)
        else:
            valid_destinations = None

        # Check for game over
        if check_game_over(board):
            winner = "Player 1" if current_player == '2' else "Player 2"
            display_game_over(winner)
            running = False
            continue

        # Update the remaining time in clocks
        if current_player == '1':
            elapsed_time_player1 = (pygame.time.get_ticks() - start_ticks_player1) // 1000
            elapsed_time_player1 -= elapsed_time_player2
            time_left_player1 = max(time_limit - elapsed_time_player1, 0)
        else: # lượt chơi người thứ 2
            elapsed_time_player2 = (pygame.time.get_ticks() - start_ticks_player2) // 1000
            elapsed_time_player2 -= elapsed_time_player1
            time_left_player2 = max(time_limit - elapsed_time_player2, 0)

            num_iterations = 1000
            # Chạy AB để tìm trạng thái tiếp theo tốt nhất
            game_state = GameState(board)
            print(game_state.board)
            old_board = game_state.board
            bestmove = find_best_move(game_state,1,True)
            game_state.next_state(bestmove[0],bestmove[1])
            print(game_state.board)
            current_player = '1'


        screen.fill((255, 255, 255))
        draw_board(valid_destinations)
        draw_pieces(board)

        draw_player_avatar(time_left_player1, time_left_player2)

        draw_dot(current_player)
        if state_move_piece[0] == True:
            # Switch turn of player
            if current_player == '1':
                current_player = '2'
            else:
                current_player = '1'
            state_move_piece[0] = False

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
