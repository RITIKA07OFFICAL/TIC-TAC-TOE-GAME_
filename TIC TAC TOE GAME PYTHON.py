import pygame
import sys
import time

# Initialize pygame
pygame.init()

# Colors
WHITE = (255, 255, 255)
LINE_COLOR = (0, 0, 0)
BG_COLOR = (30, 30, 30)
X_COLOR = (200, 30, 30)
O_COLOR = (30, 144, 255)

# Screen
WIDTH = 600
HEIGHT = 600
LINE_WIDTH = 15
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = SQUARE_SIZE // 4

# Fonts
pygame.font.init()
font = pygame.font.SysFont("comicsans", 60)
game_over_font = pygame.font.SysFont("comicsans", 80)

# Create screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cinematic Tic-Tac-Toe")
screen.fill(BG_COLOR)

# Board
board = [[None]*3 for _ in range(3)]

# Functions
def draw_lines():
    # Horizontal
    for i in range(1, 3):
        pygame.draw.line(screen, LINE_COLOR, (0, i * SQUARE_SIZE), (WIDTH, i * SQUARE_SIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (i * SQUARE_SIZE, 0), (i * SQUARE_SIZE, HEIGHT), LINE_WIDTH)

def draw_figures():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 'O':
                pygame.draw.circle(screen, O_COLOR, (int(col * SQUARE_SIZE + SQUARE_SIZE/2), int(row * SQUARE_SIZE + SQUARE_SIZE/2)), CIRCLE_RADIUS, CIRCLE_WIDTH)
            elif board[row][col] == 'X':
                start_x = col * SQUARE_SIZE + SPACE
                start_y = row * SQUARE_SIZE + SPACE
                end_x = (col + 1) * SQUARE_SIZE - SPACE
                end_y = (row + 1) * SQUARE_SIZE - SPACE
                pygame.draw.line(screen, X_COLOR, (start_x, start_y), (end_x, end_y), CROSS_WIDTH)
                pygame.draw.line(screen, X_COLOR, (start_x, end_y), (end_x, start_y), CROSS_WIDTH)

def mark_square(row, col, player):
    board[row][col] = player

def is_available(row, col):
    return board[row][col] is None

def is_board_full():
    for row in board:
        for cell in row:
            if cell is None:
                return False
    return True

def check_win(player):
    # Check rows
    for row in range(BOARD_ROWS):
        if all([cell == player for cell in board[row]]):
            return True
    # Check columns
    for col in range(BOARD_COLS):
        if all([board[row][col] == player for row in range(BOARD_ROWS)]):
            return True
    # Check diagonals
    if all([board[i][i] == player for i in range(BOARD_ROWS)]):
        return True
    if all([board[i][BOARD_ROWS - i - 1] == player for i in range(BOARD_ROWS)]):
        return True
    return False

def show_game_over(winner):
    text = game_over_font.render(f'{winner} Wins!' if winner else 'Draw!', True, WHITE)
    screen.fill(BG_COLOR)
    screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2))
    pygame.display.update()
    pygame.time.wait(2500)

def restart_game():
    global board
    board = [[None]*3 for _ in range(3)]
    screen.fill(BG_COLOR)
    draw_lines()

# Main loop
draw_lines()
player = 'X'
game_over = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mouseX = event.pos[0]
            mouseY = event.pos[1]

            clicked_row = mouseY // SQUARE_SIZE
            clicked_col = mouseX // SQUARE_SIZE

            if is_available(clicked_row, clicked_col):
                mark_square(clicked_row, clicked_col, player)

                draw_figures()
                pygame.display.update()
                time.sleep(0.2)  # Animation feel

                if check_win(player):
                    game_over = True
                    show_game_over(player)
                    restart_game()
                    game_over = False
                elif is_board_full():
                    game_over = True
                    show_game_over(None)
                    restart_game()
                    game_over = False
                else:
                    player = 'O' if player == 'X' else 'X'

    pygame.display.update()
