import pygame, sys
import numpy as np

pygame.init()

WIDTH = 600  # in python usually use capitals for constants
HEIGHT = WIDTH
screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("TIC TAC TOE")
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

CYAN = (17, 186, 172)
screen.fill(CYAN)

# console board
BOARD_ROWS = 3  # numbering in python starts form 0 so 0 1 2
BOARD_COLS = 3
board = np.zeros((BOARD_ROWS, BOARD_COLS))
# print(board)

SQUARE_SIZE = WIDTH // BOARD_COLS  # double division // because we want an integer...can also be BOARD_ROWS...size of one square

GREEN = (23, 145, 135)
LINE_WIDTH = 15

CIRCLE_RADIUS = SQUARE_SIZE // 3  # approx 60
CIRCLE_WIDTH = 15
CIRCLE_COLOR = (223, 224, 204)

CROSS_WIDTH = 25
CROSS_COLOR = (66, 66, 66)
SPACE = SQUARE_SIZE // 4  # space between line and corners....approx 55

player = 1

game_over = False


def draw_line():
    # 1 horizontal
    pygame.draw.line(screen, GREEN, (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), LINE_WIDTH)
    # 2 horizontal
    pygame.draw.line(screen, GREEN, (0, 2 * SQUARE_SIZE), (WIDTH, 2 * SQUARE_SIZE), LINE_WIDTH)
    # 1 vertical
    pygame.draw.line(screen, GREEN, (SQUARE_SIZE, 0), (SQUARE_SIZE, HEIGHT), LINE_WIDTH)
    # 2 vertical
    pygame.draw.line(screen, GREEN, (2 * SQUARE_SIZE, 0), (2 * SQUARE_SIZE, HEIGHT), LINE_WIDTH)


draw_line()


# draw circles and crosses
def draw_figures():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 1:  # player one has marked the square
                pygame.draw.circle(screen, CIRCLE_COLOR, (
                    int(col * SQUARE_SIZE + SQUARE_SIZE // 2), int(row * SQUARE_SIZE + SQUARE_SIZE // 2)),
                                   CIRCLE_RADIUS, CIRCLE_WIDTH)  # value of col and row are b/w 0 to 2
            elif board[row][col] == 2:
                pygame.draw.line(screen, CROSS_COLOR,
                                 (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE),
                                 (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE),
                                 CROSS_WIDTH)
                pygame.draw.line(screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE),
                                 (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE),
                                 CROSS_WIDTH)


# marked square
def mark_square(row, col, player):  # player as in player who is marking the square
    board[row][col] = player


# unmarked square
def avaialble_square(row, col):  # zero means unmarked
    return board[row][col] == 0  # this can also be written as
    # if board[row][col] == 0:
    # return True
    # else:
    # return False


# board full
def is_board_full():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 0:
                return False
    return True


def check_win(player):
    # vertical win check
    for col in range(BOARD_COLS):
        if board[0][col] == player and board[1][col] == player and board[2][col] == player:
            draw_vertical_winning_line(col, player)
            return True  # returning true breaks the function...wont check for any more possible wins
    # horizontal win check
    for row in range(BOARD_ROWS):
        if board[row][0] == player and board[row][1] == player and board[row][2] == player:
            draw_horizontal_winning_line(row, player)
            return True
    # asc diagonal win check
    if board[2][0] == player and board[1][1] == player and board[0][2] == player:
        draw_ascending_diagonal(player)
        return True
    # des diagonal win check
    if board[0][0] == player and board[1][1] == player and board[2][2] == player:
        draw_descending_diagonal(player)
        return True

    return False  # if we reach here theres no win


def draw_vertical_winning_line(col, player):
    PosX = col * SQUARE_SIZE + SQUARE_SIZE // 2
    if player == 1:
        color = CIRCLE_COLOR
    elif player == 2:
        color = CROSS_COLOR
    pygame.draw.line(screen, color, (PosX, 15), (PosX, HEIGHT - 15), 15)


def draw_horizontal_winning_line(row, player):
    PosY = row * SQUARE_SIZE + SQUARE_SIZE // 2
    if player == 1:
        color = CIRCLE_COLOR
    elif player == 2:
        color = CROSS_COLOR
    pygame.draw.line(screen, color, (15, PosY), (WIDTH - 15, PosY), 15)


def draw_ascending_diagonal(player):
    if player == 1:
        color = CIRCLE_COLOR
    elif player == 2:
        color = CROSS_COLOR
    pygame.draw.line(screen, color, (15, HEIGHT - 15), (WIDTH - 15, 15), 25)


def draw_descending_diagonal(player):
    if player == 1:
        color = CIRCLE_COLOR
    elif player == 2:
        color = CROSS_COLOR
    pygame.draw.line(screen, color, (15, 15), (WIDTH - 15, HEIGHT - 15), 25)


def restart():
    screen.fill(CYAN)
    draw_line()
    player = 1
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            board[row][col] = 0


# print(is_board_full())
# print(avaialble_square(1, 1))
# mark_square(1, 1, 5)
# print(avaialble_square(1, 1))
# print(board)

# game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            MouseX = event.pos[0]  # 0 refers to x coordinate of mouse
            MouseY = event.pos[1]  # 1 refers to y coordinate of mouse
            clicked_row = int(MouseY // SQUARE_SIZE)  # we want the value in integer not float
            clicked_col = int(MouseX // SQUARE_SIZE)  # // rounds the number till 200
            # print(clicked_row)
            # print(clicked_col)
            if avaialble_square(clicked_row, clicked_col):
                if player == 1:
                    mark_square(clicked_row, clicked_col, 1)
                    if check_win(player):  # should be before player value changes
                        game_over = True
                    player = 2
                elif player == 2:
                    mark_square(clicked_row, clicked_col, 2)
                    if check_win(player):
                        game_over = True
                    player = 1

                # refactoring above block of code
                #ark_square(clicked_row, clicked_col, player)
                #if check_win(player):
                    #game_over = True
                    #player = player % 2 + 1 ....but this code is not working for some reason

                draw_figures()
                # print(board)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                restart()
                game_over = False

    pygame.display.update()
