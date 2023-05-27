import pytest
from sudoku import Sudoku_Grid, Sudoku_Cube


def test_sudoku_grid_init():
    """
    Tests the Sudoku_Grid class' initializer to ensure it properly sets all attributes.
    """
    grid = Sudoku_Grid(9, 9, 600, 600, None, 73, "EASY")

    assert grid.rows == 9
    assert grid.cols == 9
    assert grid.width == 600
    assert grid.height == 600
    assert grid.avg_rank == 73
    assert grid.difficulty == "EASY"
    assert grid.wrong_inputs == 0
    assert grid.final_score == 0
    assert grid.game_over == False
    assert grid.selected is None
    assert grid.solved_by_solver == False


def test_generate_board():
    """
    Tests Sudoku_Grid's generate_board method to ensure it correctly creates a 2D list of the right dimensions.
    """
    grid = Sudoku_Grid(9, 9, 600, 600, None, 73, "EASY")
    board = grid.generate_board()

    assert len(board) == 9
    for row in board:
        assert len(row) == 9


def test_generate_cubes():
    """
    Tests Sudoku_Grid's generate_cubes method to ensure it correctly creates a 2D list of Sudoku_Cube objects.
    """
    grid = Sudoku_Grid(9, 9, 600, 600, None, 73, "EASY")

    cubes = grid.generate_cubes()
    # Check if there are 9 rows and 9 columns in the cube
    assert len(cubes) == 9
    for row in cubes:
        assert len(row) == 9
    # Check if all items in the cube are instances of Sudoku_Cube
    for row in cubes:
        for cube in row:
            assert isinstance(cube, Sudoku_Cube)


def test_update_model():
    """
    Tests Sudoku_Grid's update_model method to ensure it correctly updates the model after generating the cubes.
    """
    grid = Sudoku_Grid(9, 9, 600, 600, None, 73, "EASY")
    grid.generate_cubes()

    assert grid.model is not None


def test_get_selected_cube():
    """
    Tests Sudoku_Grid's get_selected_cube method to ensure it correctly retrieves the currently selected cube.
    """
    grid = Sudoku_Grid(9, 9, 540, 540, None, 3, "easy")
    grid.cubes = [
        [Sudoku_Cube(1, 0, 0, 540, 540), Sudoku_Cube(2, 0, 1, 540, 540)],
        [Sudoku_Cube(3, 1, 0, 540, 540), Sudoku_Cube(4, 1, 1, 540, 540)]
    ]

    # Select a cube at position (0, 1)
    grid.selected = (0, 1)
    selected_cube = grid.get_selected_cube()

    # Check if the selected cube is correct
    assert selected_cube == grid.cubes[0][1]


def test_is_valid_move():
    """
    Tests Sudoku_Grid's is_valid_move method to ensure it correctly identifies valid and invalid moves on the grid.
    """
    grid = Sudoku_Grid(9, 9, 540, 540, None, 3, "easy")
    grid.selected = (0, 2)
    grid.model = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]

    # Check if an invalid move returns False
    assert grid.is_valid_move(5) == False
    assert grid.is_valid_move(8) == False

    # Check if a valid move returns True
    assert grid.is_valid_move(1) == True


def test_reset_cube_values():
    """
    Tests Sudoku_Grid's reset_cube_values method to ensure it correctly resets a cube's value to 0.
    """
    grid = Sudoku_Grid(9, 9, 600, 600, None, 73, "EASY")
    grid.select_cube(0, 0)
    grid.place_value_in_selected_cube(1)

    grid.reset_cube_values(grid.get_selected_cube())

    assert grid.cubes[0][0].value == 0


def test_is_within_grid():
    """
    Tests Sudoku_Grid's is_within_grid method to ensure it correctly identifies whether or not a given point is within the grid.
    """
    grid = Sudoku_Grid(9, 9, 600, 600, None, 73, "EASY")

    assert grid.is_within_grid((21, 251)) == True
    assert grid.is_within_grid((1000, 1000)) == False


def test_get_grid_coordinate():
    """
    Tests Sudoku_Grid's get_grid_coordinate method to ensure it correctly calculates the grid coordinate of a given point.
    """
    grid = Sudoku_Grid(9, 9, 600, 600, None, 73, "EASY")

    assert grid.get_grid_coordinate(100, 10, 10) == 9.0


def test_is_sudoku_solved():
    """
    Tests Sudoku_Grid's is_sudoku_solved method to ensure it correctly identifies whether or not the Sudoku puzzle is solved.
    """
    grid = Sudoku_Grid(9, 9, 600, 600, None, 73, "EASY")
    grid.generate_cubes()

    assert grid.is_sudoku_solved() == False


def test_calculate_score():
    """
    Tests Sudoku_Grid's calculate_score method to ensure it correctly calculates the score based on the grid's difficulty, average rank, and wrong inputs.
    """
    grid = Sudoku_Grid(9, 9, 600, 600, None, 73, "EASY")
    grid.wrong_inputs = 5
    grid.start_time -= 300
    score = grid.calculate_score()

    assert score == 65


def test_sudoku_cube_init():
    """
    Tests the Sudoku_Cube class' initializer to ensure it properly sets all attributes.
    """
    cube = Sudoku_Cube(1, 0, 0, 10, 10)

    assert cube.value == 1
    assert cube.temp == 0
    assert cube.row == 0
    assert cube.col == 0
    assert cube.width == 10
    assert cube.height == 10


def test_sudoku_cube_update_value():
    """
    Tests Sudoku_Cube's update_value method to ensure it correctly updates the cube's value.
    """
    cube = Sudoku_Cube(1, 0, 0, 10, 10)

    cube.update_value(2)

    assert cube.value == 2


def test_sudoku_cube_update_temp_value():
    """
    Tests Sudoku_Cube's update_temp_value method to ensure it correctly updates the cube's temporary value.
    """
    cube = Sudoku_Cube(1, 0, 0, 10, 10)

    cube.update_temp_value(73)

    assert cube.temp == 73
