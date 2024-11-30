import pygame
import sys
import random

pygame.init()

# Screen dimensions and grid settings
WIDTH, HEIGHT = 500, 650
GRID_SIZE = 5
SQUARE_SIZE = (WIDTH // GRID_SIZE) - 5  # Reduced box size with more spacing
BORDER_THICKNESS = 3  # Thicker borders between boxes

# Updated color palette
COLORS = [(94, 78, 156),  
          (0, 128, 196),  
          (0, 169, 137),  
          (223, 221, 25)] 

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("лаб1 - 212059")

# Game board to store colors
board = [[-1 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

# Selected color (index)
selected_color = -1

# Start time for the timer
start_time = pygame.time.get_ticks()

def initialize_random_colors():
    for _ in range(random.randint(5, 7)):
        row, col = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
        color = random.randint(0, len(COLORS) - 1)
        if board[row][col] == -1:
            board[row][col] = color

def draw_grid():
    # Fill the grid background with light grey
    grid_background = (211, 211, 211)  # Light grey
    pygame.draw.rect(screen, grid_background, (0, 0, GRID_SIZE * (SQUARE_SIZE + BORDER_THICKNESS), GRID_SIZE * (SQUARE_SIZE + BORDER_THICKNESS)))

    # Draw the grid squares
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            x = col * (SQUARE_SIZE + BORDER_THICKNESS)
            y = row * (SQUARE_SIZE + BORDER_THICKNESS)
            color = COLORS[board[row][col]] if board[row][col] != -1 else (200, 200, 200)
            pygame.draw.rect(screen, color, (x, y, SQUARE_SIZE, SQUARE_SIZE))
            pygame.draw.rect(screen, (0, 0, 0), (x, y, SQUARE_SIZE, SQUARE_SIZE), BORDER_THICKNESS)

def draw_palette():
    for i, color in enumerate(COLORS):
        x = i * (WIDTH // len(COLORS))
        pygame.draw.rect(screen, color, (x, HEIGHT - 100, WIDTH // len(COLORS), 100))
        pygame.draw.rect(screen, (0, 0, 0), (x, HEIGHT - 100, WIDTH // len(COLORS), 100), 2)

def is_valid_color(row, col, color_index):
    neighbors = [
        (row - 1, col), (row + 1, col),
        (row, col - 1), (row, col + 1)
    ]
    for r, c in neighbors:
        if 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE:
            if board[r][c] == color_index:
                return False
    return True

def handle_click(pos):
    global selected_color
    if pos[1] >= HEIGHT - 100:
        selected_color = pos[0] // (WIDTH // len(COLORS))
        return

    if selected_color == -1:
        return

    col = pos[0] // (SQUARE_SIZE + BORDER_THICKNESS)
    row = pos[1] // (SQUARE_SIZE + BORDER_THICKNESS)

    if row < GRID_SIZE and col < GRID_SIZE:
        if board[row][col] != -1:
            return
        if is_valid_color(row, col, selected_color):
            board[row][col] = selected_color

def is_board_filled():
    for row in board:
        if -1 in row:
            return False
    return True

def draw_timer():
    elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
    remaining_time = 100 - elapsed_time
    font = pygame.font.Font(None, 36)
    timer_text = font.render(f"Time Left: {remaining_time}s", True, (255, 0, 0))
    screen.blit(timer_text, (WIDTH // 2 - 100, HEIGHT - 150))

def show_rules():
    font_title = pygame.font.Font(None, 40)
    font_text = pygame.font.Font(None, 25)

    screen.fill((255, 255, 0))  # Yellow background
    title = font_title.render("Правила на играта", True, (0, 0, 0))
    rules = [
        "1. Изберете боја од палетата подолу.",
        "2. Кликнете на квадратите за да ги обоите.",
        "3. Не смее да има иста боја во соседни квадрати.",
        "4. Имате 100 секунди за да ја пополните таблата.",
        "5. Победувате ако пополните целата табла навреме."
    ]

    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 100))
    for i, rule in enumerate(rules):
        rule_text = font_text.render(rule, True, (0, 0, 0))
        screen.blit(rule_text, (50, 200 + i * 30))

    start_text = font_text.render("Притиснете било кое копче за да започнете.", True, (0, 128, 0))
    screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT - 100))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                waiting = False

def main():
    global selected_color, start_time
    clock = pygame.time.Clock()
    running = True

    show_rules()
    initialize_random_colors()

    while running:
        screen.fill((255, 255, 255))
        draw_grid()
        draw_palette()
        draw_timer()

        if is_board_filled():
            font = pygame.font.Font(None, 74)
            text = font.render("Крај", True, (0, 128, 0))
            screen.blit(text, (WIDTH // 4, HEIGHT // 2))

        if (pygame.time.get_ticks() - start_time) > 120000:
            font = pygame.font.Font(None, 74)
            text = font.render("времето истече", True, (255, 0, 0))
            screen.blit(text, (WIDTH // 4, HEIGHT // 2))
            pygame.display.flip()
            pygame.time.wait(2000)
            running = False

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and not is_board_filled():
                handle_click(pygame.mouse.get_pos())

        clock.tick(30)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
