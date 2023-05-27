# Import necessary modules
from import_module import *
from helper_functions import *

# Game parameters
DIFFICULTY_SCORES = {"EASY": 150, "MEDIUM": 250, "HARD": 350, "EXTREME": 500}
GRID_OFFSET_X = 20
GRID_OFFSET_Y = 250


class Sudoku_Grid:
    """
    A class representing the Sudoku grid. 
    """

    def __init__(self, rows: int, cols: int, width: int, height: int, screen, avg_rank: int, difficulty: str):
        """
        Constructs a Sudoku_Grid object.

        Args:
            - rows (int): The number of rows in the grid.
            - cols (int): The number of columns in the grid.
            - width (int): The width of the grid.
            - height (int): The height of the grid.
            - screen: The screen where the grid is displayed.
            - avg_rank (int): The average rank of the Sudoku game.
            - difficulty (str): The difficulty level of the Sudoku game.
        """
        self.rows = rows
        self.cols = cols
        self.width = width
        self.height = height
        self.screen = screen
        self.avg_rank = avg_rank
        self.difficulty = difficulty
        self.start_time = time.time()
        self.wrong_inputs = 0
        self.final_score = 0
        self.game_over = False
        self.board = self.generate_board()
        self.cubes = self.generate_cubes()
        self.model = None
        self.update_model()
        self.selected = None
        self.solved_by_solver = False

    def generate_board(self):
        """
        Generates a new Sudoku board.

        Returns:
            - board: A list of lists representing the Sudoku board.
        """
        random_sudoku = generators.random_sudoku(avg_rank=self.avg_rank)
        str_sudoku = list(str(random_sudoku))
        board = []

        for i in range(0, len(str_sudoku), self.rows):
            row = [int(num) for num in str_sudoku[i:i+self.rows]]
            board.append(row)

        return board

    def generate_cubes(self):
        """
        Generates Sudoku_Cube objects for the Sudoku board.

        Returns:
            - cubes: A list of lists representing the Sudoku cubes.
        """
        cubes = []

        for i in range(self.rows):
            row_cubes = []
            for j in range(self.cols):
                cube = Sudoku_Cube(
                    self.board[i][j], i, j, self.width, self.height)
                row_cubes.append(cube)
            cubes.append(row_cubes)

        return cubes

    def update_model(self):
        """
        Updates the Sudoku model with the current state of the cubes.

        This method is called every time a cube's value changes.
        """
        self.model = [[self.cubes[i][j].value for j in range(
            self.cols)] for i in range(self.rows)]

    def select_cube(self, row, col):
        """
        Set the cube at (row, col) as the selected cube.

        Args:
            - row (int): The row index of the cube.
            - col (int): The column index of the cube.
        """
        self.reset_all_cubes_selection()
        self.cubes[row][col].selected = True
        self.selected = (row, col)

    def get_selected_cube(self):
        """
        Returns the currently selected cube.

        Returns:
            - Sudoku_Cube: The currently selected cube.
        """
        row, col = self.selected
        return self.cubes[row][col]

    def place_value_in_selected_cube(self, val):
        """
        Attempts to place a value in the currently selected cube.

        If the placement of the value is a valid move and the Sudoku puzzle can still be solved,
        the method will return True. Otherwise, the method will return False, indicating that the move was invalid.

        Args:
            - val (int): The value to be placed.

        Returns:
            - bool: Whether the move was valid.
        """
        selected_cube = self.get_selected_cube()

        if selected_cube.value == 0:
            self.set_value_and_update_model(selected_cube, val)

            if self.is_valid_move(val) and self.solve_sudoku():
                return True
            else:
                self.wrong_inputs += 1

            self.reset_cube_values(selected_cube)
            return False

    def set_value_and_update_model(self, cube, val):
        """
        Sets a value to a cube and updates the Sudoku model.

        Args:
            - cube (Sudoku_Cube): The cube where the value should be set.
            - val (int): The value to be set.
        """
        cube.update_value(val)
        self.update_model()

    def is_valid_move(self, val):
        """
        Checks whether a move is valid.

        Args:
            - val (int): The value that should be checked.

        Returns:
            - bool: Whether the move is valid.
        """
        row, col = self.selected
        return is_move_valid(self.model, val, (row, col))

    def reset_cube_values(self, cube):
        """
        Resets the values of a cube and updates the Sudoku model.

        Args:
            - cube (Sudoku_Cube): The cube where the values should be reset.
        """
        cube.update_value(0)
        cube.update_temp_value(0)
        self.update_model()

    def sketch_temp_value(self, val):
        """
        Sets a temporary value in the currently selected cube.

        Args:
            - val (int): The value to be set temporarily.
        """
        selected_cube = self.get_selected_cube()
        selected_cube.update_temp_value(val)

    def draw_grid_and_cubes(self):
        """
        Draws the grid lines and all cubes.
        """
        self.draw_grid_lines()
        self.draw_all_cubes()

    def draw_grid_lines(self):
        """
        Draws the grid lines of the Sudoku grid.
        """
        gap = self.width / self.rows
        for i in range(self.rows + 1):
            line_thickness = self.get_line_thickness(i)
            pygame.draw.line(self.screen, (0, 0, 0), (0 + GRID_OFFSET_X, i*gap + GRID_OFFSET_Y),
                             (self.width + GRID_OFFSET_X, i*gap + GRID_OFFSET_Y), line_thickness)
            pygame.draw.line(self.screen, (0, 0, 0), (i * gap + GRID_OFFSET_X, GRID_OFFSET_Y),
                             (i * gap + GRID_OFFSET_X, self.height + GRID_OFFSET_Y), line_thickness)

    def get_line_thickness(self, index):
        """
        Returns the line thickness based on the given index.

        Args:
            - index (int): The index of the grid line.

        Returns:
            - int: The thickness of the grid line.
        """
        return 6 if index % 3 == 0 else 1

    def draw_all_cubes(self):
        """
        Draws all cubes of the Sudoku grid.
        """
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].draw_cube(
                    self.screen, GRID_OFFSET_X, GRID_OFFSET_Y)

    def reset_all_cubes_selection(self):
        """
        Deselect all cubes on the board.
        """
        for i, j in itertools.product(range(self.rows), range(self.cols)):
            self.cubes[i][j].selected = False

    def clear_current_cube(self):
        """
        Clear the selected cube if it's value is 0.
        """
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].update_temp_value(0)

    def get_clicked_cube_position(self, pos):
        """
        Return the position of the cube that was clicked.

        Args:
            - pos (tuple): The screen position where the click occurred.

        Returns:
            - tuple: The position of the clicked cube as a tuple (row, col), or None if the click was outside the grid.
        """
        if self.is_within_grid(pos):
            # Considering the grid as square (rows = columns).
            gap = self.width / self.rows
            x = self.get_grid_coordinate(pos[0], GRID_OFFSET_X, gap)
            y = self.get_grid_coordinate(pos[1], GRID_OFFSET_Y, gap)
            return int(y), int(x)
        else:
            return None

    def is_within_grid(self, pos):
        """
        Check if the given position is within the Sudoku grid.

        Args:
            - pos (tuple): The screen position to be checked.

        Returns:
            - bool: Whether the position is within the grid.
        """
        return (GRID_OFFSET_X <= pos[0] < self.width + GRID_OFFSET_X) and (GRID_OFFSET_Y <= pos[1] < self.height + GRID_OFFSET_Y)

    def get_grid_coordinate(self, pos_val, offset, gap):
        """
        Return the grid coordinate corresponding to a position.

        Args:
            - pos_val (float): The screen position to be converted.
            - offset (int): The offset of the grid from the edge of the screen.
            - gap (float): The distance between grid lines.

        Returns:
            - int: The coordinate of the grid line closest to the given position.
        """
        return (pos_val - offset) // gap

    def is_sudoku_solved(self):
        """
        Check if the Sudoku puzzle is solved (i.e., no empty cells).

        Returns:
            - bool: Whether the Sudoku puzzle is solved.
        """
        return all(self.cubes[i][j].value != 0 for i, j in itertools.product(range(self.rows), range(self.cols)))

    def solve_sudoku(self):
        """
        Wrapper function for backtracking solve method.

        Returns:
            - bool: Whether a solution for the Sudoku puzzle was found.
        """
        return self.solve_with_backtrack()

    def solve_with_backtrack(self):
        """
        Solve the Sudoku board using a backtracking algorithm.

        The method finds an empty slot, and then tries all possible values (1-9) in that slot. 
        If the chosen value is valid and leads to a solution, the method returns True. 
        If not, it resets the slot and tries the next value. 
        If no values lead to a solution, the method returns False.

        Returns:
            - bool: True if a solution was found, False otherwise.
        """
        empty_slot = find_empty_slot(self.model)
        if not empty_slot:
            return True  # If no empty slots, puzzle is solved

        row, col = empty_slot
        for i in range(1, 10):
            if is_move_valid(self.model, i, (row, col)):
                self.set_value_in_model(row, col, i)

                if self.solve_with_backtrack():  # Recurse with new board
                    return True

                # If the recursion didn't find a solution, reset the slot
                self.set_value_in_model(row, col, 0)

        return False  # If no solution found for this slot, return False

    def set_value_in_model(self, row, col, value):
        """
        Set a value in the model at the specified row and col.

        Args:
            - row (int): The row index.
            - col (int): The column index.
            - value (int): The value to be set.
        """
        self.model[row][col] = value

    def solve_with_gui(self):
        """
        Wrapper function for backtracking solve method with GUI.

        This function updates the model to the current state, sets the solved_by_solver attribute to True, 
        records the current time as the start time, and then calls the solve_with_backtracking_gui method.

        Returns:
            - bool: The result of the solve_with_backtracking_gui method.
        """
        self.update_model()
        self.solved_by_solver = True
        self.start_time = time.time()
        return self.solve_with_backtracking_gui()

    def solve_with_backtracking_gui(self):
        """
        Solve the Sudoku board using a backtracking algorithm with GUI.

        This method is similar to the solve_with_backtrack method, but it also updates the GUI 
        with each attempted value.

        Returns:
            - bool: True if a solution was found, False otherwise.
        """
        empty_slot = find_empty_slot(self.model)
        if not empty_slot:
            return True  # If no empty slots, puzzle is solved

        row, col = empty_slot
        for i in range(1, 10):
            if is_move_valid(self.model, i, (row, col)):
                self.set_value_in_model(row, col, i)
                self.update_cube_and_gui(row, col, i, True)

                if self.solve_with_backtracking_gui():  # Recurse with new board
                    return True

                self.set_value_in_model(row, col, 0)
                # If the recursion didn't find a solution, reset the slot
                self.update_cube_and_gui(row, col, 0, False)

        return False  # If no solution found for this slot, return False

    def update_cube_and_gui(self, row, col, value, is_permanent):
        """
        Update a cube's value and redraw the cube in the GUI.

        Args:
            - row (int): The row index of the cube.
            - col (int): The column index of the cube.
            - value (int): The new value to be set in the cube.
            - is_permanent (bool): Whether the change is permanent.
        """
        self.cubes[row][col].update_value(value)
        self.cubes[row][col].draw_updated_value(self.screen, is_permanent)
        self.update_model()
        pygame.display.update()
        pygame.time.delay(10)

    def calculate_score(self):
        """
        Calculate the final score of the game.

        The score is calculated based on the difficulty level, the number of wrong attempts, 
        and the time taken to solve the puzzle. 
        If the puzzle was solved by the solver, the previously calculated final score is returned, i.e. 0.

        Returns:
            - int: The final score.
        """
        if self.solved_by_solver or self.start_time is None or self.game_over:
            return self.final_score

        time_taken = time.time() - self.start_time
        base_score = DIFFICULTY_SCORES[self.difficulty]
        penalty_for_wrong_attempts = self.wrong_inputs * 5
        penalty_for_time_taken = int(time_taken / 5)

        self.final_score = max(
            base_score - penalty_for_wrong_attempts - penalty_for_time_taken, 0)
        self.game_over = True
        return self.final_score

    def draw_score(self):
        """
        Draw the current score on the screen.

        This method first calculates the current score, then creates a Pygame surface with the score text, 
        and finally draws it to the screen at the specified position.
        """
        font = pygame.font.SysFont("monospace", 30)
        score = self.calculate_score()
        text = font.render(f"Your Score: {score}", True, (0, 0, 0))
        self.screen.blit(text, (320 - text.get_width() / 2, 870))


class Sudoku_Cube:
    rows = 9
    cols = 9

    def __init__(self, value: int, row: int, col: int, width: int, height: int) -> None:
        """Constructor for Sudoku_Cube.

        Args:
            - value (int): The initial value of the cube.
            - row (int): The row position of the cube.
            - col (int): The column position of the cube.
            - width (int): The width of the cube.
            - height (int): The height of the cube.
        """
        self.value = value
        self.temp = 0
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False
        self.original = bool(value)

    def draw_cube(self, screen: pygame.Surface, grid_offset_x: int, grid_offset_y: int) -> None:
        """
        Draws the cube on the given screen.

        Args:
            - screen (pygame.Surface): The Pygame surface to draw the cube on.
            - grid_offset_x (int): The x-coordinate of the top-left corner of the Sudoku grid.
            - grid_offset_y (int): The y-coordinate of the top-left corner of the Sudoku grid.
        """
        fnt = pygame.font.SysFont("monospace", 40 if self.original else 25)
        gap = self.width / 9
        x = self.col * gap + grid_offset_x
        y = self.row * gap + grid_offset_y

        self.draw_text_in_cube(screen, fnt, x, y)
        if self.selected:
            pygame.draw.rect(screen, (255, 0, 255),
                             (x, y, gap + 2, gap + 2), 2)

    def draw_text_in_cube(self, screen: pygame.Surface, fnt: pygame.font.Font, x: float, y: float) -> None:
        """
        Draws the cube's value as text on the screen at the specified coordinates.

        Args:
            - screen (pygame.Surface): The Pygame surface to draw the text on.
            - fnt (pygame.font.Font): The Pygame font object to use for the text.
            - x (float): The x-coordinate where the text will be drawn.
            - y (float): The y-coordinate where the text will be drawn.
        """
        if self.temp != 0 and self.value == 0:
            text = fnt.render(str(self.temp), 1, (128, 128, 128))
            screen.blit(text, (x+5, y+5))
        elif self.value != 0:
            text_color = (0, 0, 255) if self.original else (0, 0, 0)
            text = fnt.render(str(self.value), 1, text_color)
            screen.blit(text, (x + (self.width / 18 - text.get_width()/2),
                               y + (self.width / 18 - text.get_height()/2)))

    def update_value(self, val: int) -> None:
        """
        Sets the value of the cube.

        Args:
            - val (int): The value to set. If it's not 0, the cube will be considered not original.
        """
        self.value = val
        if val != 0:
            self.original = False

    def draw_updated_value(self, screen: pygame.Surface, green: bool = True) -> None:
        """
        Redraws the cube on the screen to indicate a change.

        Args:
            - screen (pygame.Surface): The Pygame surface to draw the cube on.
            - green (bool, optional): Whether to draw a green or red rectangle around the cube. Defaults to True (green).
        """
        fnt = pygame.font.SysFont("monospace", 25)
        gap = self.width / 9
        x = self.col * gap + GRID_OFFSET_X
        y = self.row * gap + GRID_OFFSET_Y

        pygame.draw.rect(screen, (255, 255, 255), (x, y, gap + 2, gap + 2), 0)

        self.draw_text_with_change(screen, fnt, x, y, green)

    def draw_text_with_change(self, screen: pygame.Surface, fnt: pygame.font.Font, x: float, y: float, green: bool) -> None:
        """
        Draws the cube's value as text on the screen with change indicator.

        Args:
            - screen (pygame.Surface): The Pygame surface to draw the text on.
            - fnt (pygame.font.Font): The Pygame font object to use for the text.
            - x (float): The x-coordinate where the text will be drawn.
            - y (float): The y-coordinate where the text will be drawn.
            - green (bool): Indicates if the change is valid (green) or not (red).
        """
        text = fnt.render(str(self.value), 1, (0, 0, 0))
        screen.blit(text, (x + (self.width / 18 - text.get_width() / 2),
                           y + (self.width / 18 - text.get_height() / 2)))
        pygame.draw.rect(screen, (0, 255, 0) if green else (255, 0, 0),
                         (x, y, self.width / 9 + 1, self.width / 9 + 1), 2)

    def update_temp_value(self, val: int) -> None:
        """
        Sets the temporary value of the cube.

        Args:
            - val (int): The temporary value to set.
        """
        self.temp = val
