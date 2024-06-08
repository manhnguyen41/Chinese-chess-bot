import pygame
import subprocess
import sys

# Initialize the window start
pygame.init()

# Declare constants
WIDTH, HEIGHT = 600, 700
BUTTON_WIDTH, BUTTON_HEIGHT = WIDTH // 1.5, HEIGHT // 9.5

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Choosing algorithm of AI-AI")

# Upload background image
backgroundImage = pygame.image.load("View/image/background.jpg").convert()
backgroundWidth = 600
backgroundHeight = 700
# Convert size of background image
backgroundImage = pygame.transform.scale(backgroundImage, (backgroundWidth, backgroundHeight))

# Button rects
algo1_button_rect = pygame.Rect((WIDTH // 2 - BUTTON_WIDTH // 2, HEIGHT // 3 - BUTTON_HEIGHT), (BUTTON_WIDTH, BUTTON_HEIGHT))
algo2_button_rect = pygame.Rect((WIDTH // 2 - BUTTON_WIDTH // 2, HEIGHT // 2 - BUTTON_HEIGHT), (BUTTON_WIDTH, BUTTON_HEIGHT))
algo3_button_rect = pygame.Rect((WIDTH // 2 - BUTTON_WIDTH // 2, HEIGHT // 1.5 - BUTTON_HEIGHT), (BUTTON_WIDTH, BUTTON_HEIGHT))
algo4_button_rect = pygame.Rect((WIDTH // 2 - BUTTON_WIDTH // 2, HEIGHT // 1.2 - BUTTON_HEIGHT), (BUTTON_WIDTH, BUTTON_HEIGHT))

# Initialize font
font = pygame.font.Font(None, 34)

def render_button(button_rect, text, hover=False):
    color = (0, 128, 0) if not hover else (0, 255, 0)
    pygame.draw.rect(screen, color, button_rect)
    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=button_rect.center)
    screen.blit(text_surface, text_rect)

def start_screen():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if algo1_button_rect.collidepoint(event.pos):
                    running = False  
                    open_choosing_algo_AI_window("Greedy vs Alpha-Beta Search")
                if algo2_button_rect.collidepoint(event.pos):
                    running = False  
                    open_choosing_algo_AI_window("MCTS vs Greedy")
                if algo3_button_rect.collidepoint(event.pos):
                    running = False  
                    open_choosing_algo_AI_window("MCTS vs Alpha-Beta Search")
                if algo4_button_rect.collidepoint(event.pos):
                    running = False
                    open_choosing_algo_AI_window("Alpha-Beta vs Alpha-Beta")

        # Draw background
        screen.blit(backgroundImage, (0, 0))

        # Draw and render buttons
        render_button(algo1_button_rect, "Greedy vs Alpha-Beta Search", hover=algo1_button_rect.collidepoint(pygame.mouse.get_pos()))
        render_button(algo2_button_rect, "MCTS vs Greedy", hover=algo2_button_rect.collidepoint(pygame.mouse.get_pos()))
        render_button(algo3_button_rect, "MCTS vs Alpha-Beta Search", hover=algo3_button_rect.collidepoint(pygame.mouse.get_pos()))
        render_button(algo4_button_rect, "Alpha-Beta vs Alpha-Beta", hover=algo4_button_rect.collidepoint(pygame.mouse.get_pos()))

        pygame.display.flip()

    # Close the start screen window
    pygame.quit()

#def open_file(file_path):
#    python_path = sys.executable
#    subprocess.Popen([python_path, file_path])

#Def to navigate to file of corresponding algorithms
def open_choosing_algo_AI_window(mode):
    python_path = sys.executable
    subprocess.run([python_path, "View/ChineseChessAI.py", mode])
    file_path = "View/ChineseChessAi.py"
    open_file(file_path)

def open_file(file_path):
    python_path = sys.executable
    subprocess.Popen([python_path, file_path])

if __name__ == "__main__":
    start_screen()
