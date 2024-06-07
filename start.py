import pygame
import subprocess
import sys

# Initialize the window start
pygame.init()

# Declare constants
WIDTH, HEIGHT = 600, 700
BUTTON_WIDTH, BUTTON_HEIGHT = WIDTH // 3, HEIGHT // 9.5

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Welcome to Chinese Chess game")

# Upload background image
backgroundImage = pygame.image.load("View/image/background.jpg").convert()
backgroundWidth = 600
backgroundHeight = 700
# Convert size of background image
backgroundImage = pygame.transform.scale(backgroundImage, (backgroundWidth, backgroundHeight))

# Button rects
option1_button_rect = pygame.Rect((WIDTH // 2 - BUTTON_WIDTH // 2, HEIGHT // 3 - BUTTON_HEIGHT // 2), (BUTTON_WIDTH, BUTTON_HEIGHT))
option2_button_rect = pygame.Rect((WIDTH // 2 - BUTTON_WIDTH // 2, HEIGHT // 2 - BUTTON_HEIGHT // 2), (BUTTON_WIDTH, BUTTON_HEIGHT))

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
                if option1_button_rect.collidepoint(event.pos):
                    running = False
                    open_choosing_algo_window("AI - Human")
                elif option2_button_rect.collidepoint(event.pos):
                    running = False
                    open_choosing_algo_window("AI - AI")

        # Draw background
        screen.blit(backgroundImage, (0, 0))

        # Draw and render buttons
        render_button(option1_button_rect, "AI - Human", hover=option1_button_rect.collidepoint(pygame.mouse.get_pos()))
        render_button(option2_button_rect, "AI - AI", hover=option2_button_rect.collidepoint(pygame.mouse.get_pos()))

        pygame.display.flip()

    # Close the start screen window
    pygame.quit()

def open_choosing_algo_window(mode):
    python_path = sys.executable
    if mode == "AI - Human":
        subprocess.Popen([python_path, "View/ChooseAlgo.py", mode])
    elif mode == "AI - AI":
        subprocess.Popen([python_path, "View/ChooseAlgoAI.py", mode])

if __name__ == "__main__":
    start_screen()