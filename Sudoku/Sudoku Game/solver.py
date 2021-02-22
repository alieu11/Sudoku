import random


def solve_board(board):
    find_next_open_slot = find_open_slot(board)
    if not find_next_open_slot:
        return True
    else:
        row, col = find_next_open_slot

    for i in range(1, 10):
        if check_if_valid_move(board, i, (row, col)):
            board[row][col] = i

            if solve_board(board):
                return True

            board[row][col] = 0

    return False


def check_if_valid_move(board, value, coordinates):
    # Check row
    for i in range(9):
        if board[coordinates[0]][i] == value and coordinates[1] != i:
            return False

    # Check column
    for i in range(9):
        if board[i][coordinates[1]] == value and coordinates[0] != i:
            return False

    # Check box
    box_x = coordinates[1] // 3
    box_y = coordinates[0] // 3

    for i in range(box_y*3, box_y*3 + 3):
        for j in range(box_x * 3, box_x*3 + 3):
            if board[i][j] == value and (i, j) != coordinates:
                return False

    return True


def print_board(sudoku_board):
    for row in sudoku_board:
        for column in row:
            print(column, end=" ")
        print()


def find_open_slot(sudoku_board):
    for row in range(9):
        for col in range(9):
            if sudoku_board[row][col] == 0:
                return row, col  # row, col

    return None


def randomize_board():
    board = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]
    board[0] = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    random.shuffle(board[0])
    # solving board ensures that the board is completely valid
    solve_board(board)

    # print_board(board)
    # print("~~~~~~~~~~~~~~~~~")
    # change this for more blank squares
    for i in range(75):
        row = random.randint(0, 8)
        # print("Row: " + str(row))
        col = random.randint(0, 8)
        # print("Col: " + str(col))
        board[row][col] = 0
    # print_board(board)
    return board
