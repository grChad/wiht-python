import pygame
import sys
import random

# Import the constants
from constants import SCREEN_DIMENSIONS, CELL_SIZE, WHITE, BLACK, RED, COLORS

# Initialize Pygame
pygame.init()

screen = pygame.display.set_mode(SCREEN_DIMENSIONS)

# titulo del juego
pygame.display.set_caption("game 2048")

# Matriz que representa el tablero
board = [[0] * 4 for _ in range(4)]

# Estados del juego
game_over = False
game_won = False


# Funciones necesarias para el juego
def draw_screen():
    font = pygame.font.Font(None, 40)
    message_font = pygame.font.Font(None, 30)

    screen.fill(WHITE)

    for i in range(4):
        for j in range(4):
            value = board[i][j]
            color = COLORS.get(value, COLORS[0])
            pygame.draw.rect(
                screen, color, (j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE), 0
            )

            if value != 0:
                text = font.render(str(value), True, BLACK)
                text_rect = text.get_rect(
                    center=(
                        j * CELL_SIZE + CELL_SIZE // 2,
                        i * CELL_SIZE + CELL_SIZE // 2,
                    )
                )
                screen.blit(text, text_rect)

    if game_won:
        text = message_font.render("gamaste!!! Presiona 'R' para reiniciar", True, RED)
        screen.blit(text, (50, SCREEN_DIMENSIONS[0] // 2 - 20))
    if game_over:
        text = message_font.render("Game Over! Presiona 'R' para reiniciar", True, RED)
        screen.blit(text, (50, SCREEN_DIMENSIONS[0] // 2 - 20))


def generate_new_number():
    empty = [(i, j) for i in range(4) for j in range(4) if board[i][j] == 0]

    if empty:
        i, j = random.choice(empty)
        board[i][j] = random.choice([2, 4])


def compress(nums):
    new_nums = [num for num in nums if num != 0]
    nums[:] = new_nums + [0] * (4 - len(new_nums))


def merge(nums):
    for i in range(3):
        if nums[i] == nums[i + 1] and nums[1] != 0:
            nums[i] *= 2
            nums[i + 1] = 0


def move_left():
    moved = False
    for i in range(4):
        original = board[i][:]

        compress(board[i])
        merge(board[i])
        compress(board[i])

        if original != board[i]:
            moved = True

    return moved


def move_right():
    moved = False
    for i in range(4):
        original = board[i][:]

        board[i].reverse()
        compress(board[i])
        merge(board[i])
        compress(board[i])
        board[i].reverse()

        if original != board[i]:
            moved = True

    return moved


def move_up():
    moved = False
    for j in range(4):
        column = [board[i][j] for i in range(4)]
        original = column[:]

        compress(column)
        merge(column)
        compress(column)

        for i in range(4):
            board[i][j] = column[i]

        if original != column:
            moved = True

    return moved


def move_down():
    moved = False
    for j in range(4):
        column = [board[i][j] for i in range(4)]
        original = column[:]

        column.reverse()
        compress(column)
        merge(column)
        compress(column)
        column.reverse()

        for i in range(4):
            board[i][j] = column[i]
        if original != column:
            moved = True

    return moved


def check_win():
    return any(2048 in row for row in board)


def check_loss():
    if any(0 in row for row in board):
        return False

    for i in range(4):
        for j in range(4):
            if board[i][j] == board[i][j + 1] or board[j][i] == board[j + 1][i]:
                return False

    return True


def reset_game():
    global board, game_over, game_won
    board = [[0] * 4 for _ in range(4)]
    game_over = False
    game_won = False
    generate_new_number()
    generate_new_number()


reset_game()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            moved = False

            if event.key == pygame.K_r:
                reset_game()
            if not game_over and not game_won:
                if event.key == pygame.K_h:
                    moved = move_left()
                elif event.key == pygame.K_l:
                    moved = move_right()
                elif event.key == pygame.K_k:
                    moved = move_up()
                elif event.key == pygame.K_j:
                    moved = move_down()

            if moved:
                generate_new_number()
                if check_win():
                    game_won = True
                elif check_loss():
                    game_over = True

    draw_screen()
    # pygame.display.update()
    pygame.display.flip()
