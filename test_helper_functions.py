import pytest
from helper_functions import find_empty_slot, is_move_valid


def test_find_empty_slot():
    filled_board = [[1 for _ in range(9)] for _ in range(9)]
    assert find_empty_slot(
        filled_board) is None, "Expected None for a filled board"

    empty_board = [[0 for _ in range(9)] for _ in range(9)]
    assert find_empty_slot(empty_board) == (
        0, 0), "Expected (0, 0) for an empty board"


def test_is_move_valid():
    valid_board = [
        [5, 3, 4, 6, 7, 8, 9, 1, 2],
        [6, 7, 2, 1, 9, 5, 3, 4, 8],
        [1, 9, 8, 3, 4, 2, 5, 6, 7],
        [8, 5, 9, 7, 6, 1, 4, 2, 3],
        [4, 2, 6, 8, 5, 3, 7, 9, 1],
        [7, 1, 3, 9, 2, 4, 8, 5, 6],
        [9, 6, 1, 5, 3, 7, 2, 8, 4],
        [2, 8, 7, 4, 1, 9, 6, 3, 5],
        [3, 4, 5, 2, 8, 6, 1, 7, 9]
    ]
    assert is_move_valid(valid_board, 2, (0, 0)
                         ) == False

    board_with_empty_slot = valid_board.copy()
    board_with_empty_slot[0][0] = 0
    assert is_move_valid(board_with_empty_slot, 5, (0, 0)
                         ) == True
