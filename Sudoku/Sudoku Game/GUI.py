import pygame
from solver import solve_board, check_if_valid_move, randomize_board, print_board
import random
from random import randrange

pygame.font.init()


class NineByNineGrid:
    board = randomize_board()

    def __init__(self, rows, columns, width, height):
        self.rows = rows
        self.cols = columns
        self.cubes = [[SingleSquare(self.board[i][j], i, j, width, height)
                       for j in range(columns)] for i in range(rows)]
        self.width = width
        self.height = height
        self.model = None
        self.selected = None

    # updates the model
    def update_model(self):
        self.model = [[self.cubes[i][j].value for j in range(self.cols)] for i in range(self.rows)]

    # placing a number into one of the empty boxes
    def insert_number(self, value):
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set_value(value)
            self.update_model()

            # if the placement is a valid move then return true
            if check_if_valid_move(self.model, value, (row, col)) and solve_board(self.model):
                return True
            # else its the wrong move, change things back to 0
            else:
                self.cubes[row][col].set_value(0)
                self.cubes[row][col].set_guess(0)
                self.update_model()
                return False

    # with the selected box change the greyed out number
    def guessing(self, val):
        row, col = self.selected
        self.cubes[row][col].set_guess(val)

    # drawing the lines of the grid of varying thickness
    def draw_lines(self, win):
        # Draw Grid Lines
        gap = self.width / 9
        for i in range(self.rows + 1):
            if i % 3 == 0 and i != 0:
                thick = 5
            else:
                thick = 2
            pygame.draw.line(win, (0, 0, 0), (0, i * gap), (self.width, i * gap), thick)
            pygame.draw.line(win, (0, 0, 0), (i * gap, 0), (i * gap, self.height), thick)

        # draw the cubes
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].draw(win)

    def select(self, row, col):
        # Reset all other
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].selected = False

        self.cubes[row][col].selected = True
        self.selected = (row, col)

    # clears the temporary "guess" to blank
    def reset_guess(self):
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set_guess(0)

    # clicking the box to select it
    def select_box(self, coordinates):
        if coordinates[0] < self.width and coordinates[1] < self.height:
            gap = self.width / 9
            x = coordinates[0] // gap
            y = coordinates[1] // gap
            return int(y), int(x)
        else:
            return None

    # check if the board is completed
    def is_completed(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.cubes[i][j].value == 0:
                    return False
        return True


# this is the single square
class SingleSquare:

    def __init__(self, value, row, col, width, height):
        self.value = value
        self.guess = 0
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False

    def draw(self, win):
        fnt = pygame.font.SysFont("arial", 40)

        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        if self.guess != 0 and self.value == 0:
            # greyed out color
            text = fnt.render(str(self.guess), 1, (128, 128, 128))
            win.blit(text, (x + 5, y + 5))
        elif not (self.value == 0):
            text = fnt.render(str(self.value), 1, (0, 0, 0))
            win.blit(text, (x + (gap / 2 - text.get_width() / 2), y + (gap / 2 - text.get_height() / 2)))

        if self.selected:
            # red color
            pygame.draw.rect(win, (255, 0, 0), (x, y, gap, gap), 3)

    def set_value(self, value):
        self.value = value

    def set_guess(self, value):
        self.guess = value


# use to refresh the window
def redraw_window(win, board):
    # color white
    win.fill((255, 255, 255))
    # Draw grid and board
    board.draw_lines(win)


def main():
    # size of the window
    win = pygame.display.set_mode((600, 600))
    pygame.display.set_caption("Sudoku")
    # size of the board
    board = NineByNineGrid(9, 9, 600, 600)
    user_input = None
    game_is_running = True
    while game_is_running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_is_running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    user_input = 1
                if event.key == pygame.K_2:
                    user_input = 2
                if event.key == pygame.K_3:
                    user_input = 3
                if event.key == pygame.K_4:
                    user_input = 4
                if event.key == pygame.K_5:
                    user_input = 5
                if event.key == pygame.K_6:
                    user_input = 6
                if event.key == pygame.K_7:
                    user_input = 7
                if event.key == pygame.K_8:
                    user_input = 8
                if event.key == pygame.K_9:
                    user_input = 9
                if event.key == pygame.K_DELETE:
                    board.reset_guess()
                    user_input = None
                if event.key == pygame.K_RETURN:
                    i, j = board.selected
                    if board.cubes[i][j].guess != 0:
                        if board.insert_number(board.cubes[i][j].guess):
                            print("Correct")
                        else:
                            print("Incorrect")

                        user_input = None

                        if board.is_completed():
                            print("Thanks For Playing!")
                            game_is_running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clicked = board.select_box(pos)
                if clicked:
                    board.select(clicked[0], clicked[1])
                    user_input = None

        if board.selected and user_input is not None:
            board.guessing(user_input)

        redraw_window(win, board)
        pygame.display.update()


main()
pygame.quit()
