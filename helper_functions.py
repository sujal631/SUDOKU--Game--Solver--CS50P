from import_module import itertools


def find_empty_slot(board):
    """
    Function to find an empty slot in the board.

    Args:
        - board (list): 2D list representing the Sudoku board.

    Returns:
        - tuple: coordinates of the first found empty slot. If no empty slot is found, returns None.
    """
    for row_index, col_index in itertools.product(range(len(board)), range(len(board[0]))):
        if board[row_index][col_index] == 0:
            return row_index, col_index
    return None


def is_move_valid(board, num, pos):
    """
    Function to check if a number is valid at the given position on the board.

    Args:
        - board (list): 2D list representing the Sudoku board.
        - num (int): The number to validate.
        - pos (tuple): The coordinates (row, column) of the position on the board.

    Returns:
        - bool: True if the number is valid at the position, False otherwise.
    """
    row_index, col_index = pos

    # Check if the number is not in the same row.
    for i in range(len(board[0])):
        if board[row_index][i] == num and col_index != i:
            return False

    # Check if the number is not in the same column.
    for i in range(len(board)):
        if board[i][col_index] == num and row_index != i:
            return False

    # Check if the number is not in the same 3x3 box.
    box_start_row, box_start_col = 3 * (row_index // 3), 3 * (col_index // 3)
    for i, j in itertools.product(range(box_start_row, box_start_row + 3), range(box_start_col, box_start_col + 3)):
        if board[i][j] == num and (i, j) != pos:
            return False

    return True
