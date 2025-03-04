import pygame
import sys

# Constants
BOARD_ROWS = 3
BOARD_COLUMNS = 3
SQUARE_SIZE = 100
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GRAY = (128, 128, 128)

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((BOARD_COLUMNS * SQUARE_SIZE, BOARD_ROWS * SQUARE_SIZE))
pygame.display.set_caption("Tic-Tac-Toe AI")
font = pygame.font.SysFont(None, 40)

# Initialize game board
board = [[0 for _ in range(BOARD_COLUMNS)] for _ in range(BOARD_ROWS)]

# Function to draw the grid lines
def draws_lines(color=(0, 0, 0)):
    for row in range(1, BOARD_ROWS):
        pygame.draw.line(screen, color, (0, row * SQUARE_SIZE), (BOARD_COLUMNS * SQUARE_SIZE, row * SQUARE_SIZE), 3)
    for col in range(1, BOARD_COLUMNS):
        pygame.draw.line(screen, color, (col * SQUARE_SIZE, 0), (col * SQUARE_SIZE, BOARD_ROWS * SQUARE_SIZE), 3)

# Function to check for a win
def check_win(player, board_state=None):
    if board_state is None:
        board_state = board
    # Check rows, columns, and diagonals
    for row in range(BOARD_ROWS):
        if all(board_state[row][col] == player for col in range(BOARD_COLUMNS)):
            return True
    for col in range(BOARD_COLUMNS):
        if all(board_state[row][col] == player for row in range(BOARD_ROWS)):
            return True
    if all(board_state[i][i] == player for i in range(BOARD_ROWS)):
        return True
    if all(board_state[i][BOARD_ROWS - 1 - i] == player for i in range(BOARD_ROWS)):
        return True
    return False

# Function to check if the board is full
def is_board_full(board_state=None):
    if board_state is None:
        board_state = board
    return all(board_state[row][col] != 0 for row in range(BOARD_ROWS) for col in range(BOARD_COLUMNS))

# Minimax function
def minimax(minimax_board, depth, is_maximizing):
    if check_win(2, minimax_board):  # AI wins
        return float('inf')
    elif check_win(1, minimax_board):  # Player wins
        return float('-inf')
    elif is_board_full(minimax_board):  # Draw
        return 0

    if is_maximizing:
        best_score = float('-inf')
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLUMNS):
                if minimax_board[row][col] == 0:
                    minimax_board[row][col] = 2  # AI move
                    score = minimax(minimax_board, depth + 1, False)
                    minimax_board[row][col] = 0  # Undo move
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLUMNS):
                if minimax_board[row][col] == 0:
                    minimax_board[row][col] = 1  # Human move
                    score = minimax(minimax_board, depth + 1, True)
                    minimax_board[row][col] = 0  # Undo move
                    best_score = min(score, best_score)
        return best_score

# Function for AI to find the best move
def best_move():
    best_score = float('-inf')
    move = (-1, -1)
    
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLUMNS):
            if board[row][col] == 0:
                board[row][col] = 2  # Simulate AI move
                score = minimax(board, depth=0, is_maximizing=False)
                board[row][col] = 0  # Undo move
                
                if score > best_score:
                    best_score = score
                    move = (row, col)

    if move != (-1, -1):
        board[move[0]][move[1]] = 2  # AI makes actual move
        return True
    return False

# Function to restart game
def restart_game():
    global board, game_over, player
    screen.fill(WHITE)
    draws_lines()
    board = [[0 for _ in range(BOARD_COLUMNS)] for _ in range(BOARD_ROWS)]
    game_over = False
    player = 1

# Function to draw marks
def draw_figures():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLUMNS):
            if board[row][col] == 1:  # Player 1 (Human)
                pygame.draw.circle(screen, GREEN, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 3, 3)
            elif board[row][col] == 2:  # Player 2 (AI)
                pygame.draw.line(screen, RED, (col * SQUARE_SIZE + 20, row * SQUARE_SIZE + 20), (col * SQUARE_SIZE + SQUARE_SIZE - 20, row * SQUARE_SIZE + SQUARE_SIZE - 20), 3)
                pygame.draw.line(screen, RED, (col * SQUARE_SIZE + SQUARE_SIZE - 20, row * SQUARE_SIZE + 20), (col * SQUARE_SIZE + 20, row * SQUARE_SIZE + SQUARE_SIZE - 20), 3)

# Function to display message
def display_message(message):
    text = font.render(message, True, (0, 0, 0))
    screen.blit(text, (BOARD_COLUMNS * SQUARE_SIZE // 2 - text.get_width() // 2, BOARD_ROWS * SQUARE_SIZE // 2 - text.get_height() // 2))
    pygame.display.update()

# Draw initial grid
draws_lines()

# Game variables
player = 1
game_over = False

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mouseX = event.pos[0] // SQUARE_SIZE
            mouseY = event.pos[1] // SQUARE_SIZE

            if board[mouseY][mouseX] == 0:
                board[mouseY][mouseX] = player
                if check_win(player):
                    game_over = True
                    display_message("Victory! Press Enter to Restart")

                player = 3 - player  # Switch turn

                if not game_over:
                    if best_move():  # AI move
                        if check_win(2):
                            game_over = True
                            display_message("Game Over! Press Enter to Restart")
                        player = 3 - player

                if not game_over and is_board_full():
                    game_over = True
                    display_message("It's a Draw! Press Enter to Restart")
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                restart_game()
            if event.key == pygame.K_q:  # Press 'q' to quit the game
                pygame.quit()
                sys.exit()
            if event.key == pygame.K_RETURN and game_over:
                restart_game()

    screen.fill(WHITE)
    draws_lines()
    draw_figures()

    pygame.display.update()
