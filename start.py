import pygame
import subprocess
import sys

#Initialize the window start
pygame.init()

#Declare constants
WIDTH, HEIGHT = 600, 700

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Welcome to Chinese Chess game")

#Upload background image
backgroundImage = pygame.image.load("image/background.jpg").convert()
backgroundWidth = 600
backgroundHeight = 700
#Convert size of background image
backgroundImage = pygame.transform.scale(backgroundImage, (backgroundWidth, backgroundHeight))

#Create "Start" button
start_button_image = pygame.image.load("image/start_button.png").convert_alpha()
start_button_image = pygame.transform.scale(start_button_image, (WIDTH // 4, HEIGHT // 9.5))
start_button_rect = start_button_image.get_rect()
start_button_rect.center = (WIDTH // 2, HEIGHT // 3)

def start_screen():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Check if the mouse click is on the "Start" button
                if start_button_rect.collidepoint(event.pos):
                    running = False  
                    open_chinese_chess_window()

        # Draw background
        screen.blit(backgroundImage, (0, 0))

        # Check if the mouse is hovering over the button
        if start_button_rect.collidepoint(pygame.mouse.get_pos()):
            hover_button_image = pygame.transform.scale(start_button_image, (int(WIDTH // 4 * 1.1), int(HEIGHT // 8 * 1.1)))
            screen.blit(hover_button_image, start_button_rect)
        else:
            screen.blit(start_button_image, start_button_rect)

        pygame.display.flip()

    # Close the start screen window
    pygame.quit()

    


def open_chinese_chess_window():
    python_path = sys.executable
    #print(python_path)
    subprocess.Popen([python_path, "ChineseChess.py"])

if __name__ == "__main__":
    start_screen()
