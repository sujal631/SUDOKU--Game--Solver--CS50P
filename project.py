# Import necessary modules
from import_module import *
from sudoku import *
from helper_functions import *
from game_messages import *

# Game parameters
SCREEN_SIZE = (640, 950)
CAPTION = "Sudoku - Game & Solver"
DIFFICULTY_LEVELS = {
    1: ("EASY", (30, 49)),
    2: ("MEDIUM", (50, 69)),
    3: ("HARD", (70, 89)),
    4: ("EXTREME", (100, 120))
}

#Keys used for entering numbers in the game
KEYS = [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9, pygame.K_KP1, pygame.K_KP2, pygame.K_KP3, pygame.K_KP4, pygame.K_KP5, pygame.K_KP6, pygame.K_KP7, pygame.K_KP8, pygame.K_KP9]

# File for sorting rankings
RANKING_FILE = 'ranking.csv'
# Field names for the ranking file
FIELDNAMES = ['Rank', 'Username', 'Difficulty', 'Time Taken', 'Wrong Inputs', 'Total Score']

def clear_screen():
    """
    Clears the console.
    """
    os.system("clear||cls")

def get_username():
    """ Prompts user for a username until a valid one is provided 
    
    Returns:
        - str: A validated username
    """
    while True:
        console.print("[gold3]\nEnter your name: [/gold3]", end="")
        name = input()
        if validate_name(name):
            return name
        else:
            print(f"[red1]\n\tInvalid name. Must be 4-10 alphanumeric characters.\n\tTry again.[/red1]")
        
def validate_name(name):
    """
    Checks if the provided name is valid.

    Args:
        - name (str): User input name.

    Returns:
        - bool: True if name is valid, False otherwise.
    """
    return bool((10 >= len(name) >= 4) and name.isalnum())

def get_difficulty():
    """
    Prompts the user to enter a difficulty level until a valid one is provided.

    Returns:
        - tuple: A tuple containing the chosen difficulty and a random number within the range of average rank for the difficulty level.
    """
    while True:
        try:
            console.print(f"[gold3]{DIFF}\n[/gold3]")
            difficulty_level = int(input())

            if difficulty_level in DIFFICULTY_LEVELS:
                difficulty, avg_rank_range = DIFFICULTY_LEVELS[difficulty_level]
                avg_rank = random.randint(*avg_rank_range)
                return difficulty, avg_rank
            else:
                print(f"[red1]\n\tInvalid difficulty level. Should be either 1 or 2 or 3 or 4.\n\tTry again.[/red1]")
        except Exception:
            print(f"[red1]\n\tInvalid difficulty level. Should be either 1 or 2 or 3 or 4.\n\tTry again.[/red1]")


def get_replay_input():
    """
    Prompts the user to enter if they want to replay the game.

    Returns:
        - str: User's response to the replay prompt.
    """
    console.print(f"[gold3]{DIV}\nDo you want to replay the game? (Yes/Y to replay): [/gold3]", end="")
    return input()

def draw_welcome_message(screen, default_font):
    """
    Renders and displays the welcome message on the screen.
    
    Args:
        - screen (pygame.Surface): The game screen.
        - default_font (pygame.font.Font): The font to be used for the message.
    """
    text = default_font.render("Welcome to SUDOKU - Game & Solver", True, (0, 0, 0))
    screen.blit(text, (320 - text.get_width() / 2, 10))

def draw_instructions(screen, instructions_font, user_name, difficulty):
    """
    Renders and displays the game instructions on the screen.
    
    Args:
        - screen (pygame.Surface): The game screen.
        - instructions_font (pygame.font.Font): The font to be used for the instructions.
        - user_name (str): The name of the user.
        - difficulty (str): The selected difficulty level.
    """
    instructions = [
        f"Hello {user_name}, you chose {difficulty} difficulty.",
        "How to play?",
        "1. Select a box by clicking it.",
        "2. Use number keys to fill the box.",
        "3. Hit 'DELETE' to clear a box.",
        "4. Hit 'ENTER' to confirm the digit.",
        "5. Stuck? Hit 'SPACEBAR' to auto complete the puzzle.",
        "Note: No points for auto completing the puzzle."
    ]
    coordinates = [(20, 60), (20, 90), (60, 110), (60, 130), (60, 150), (60, 170), (60, 190), (20, 220)]
    colors = [(1, 155, 32)] + [(0, 0, 0) for _ in range(1, 7)] + [(255, 0, 0)]

    for instruction, coord, color in zip(instructions, coordinates, colors):
        text = instructions_font.render(instruction, True, color)
        screen.blit(text, coord)

def draw_time_and_wrong_inputs(screen, instructions_font, time, wrong_inputs):
    """
    Renders and displays the time elapsed and number of wrong inputs on the screen.
    
    Args:
        - screen (pygame.Surface): The game screen.
        - instructions_font (pygame.font.Font): The font to be used for the information.
        - time (int): The elapsed time in seconds.
        - wrong_inputs (int): The number of wrong inputs made by the user.
    """
    text = instructions_font.render(f"Wrong Inputs: {wrong_inputs}", True, (255, 0, 0))
    screen.blit(text, (20, 920))
    text = instructions_font.render(f"Time Elapsed: {format_time(time)}", True, (255, 0, 0))
    screen.blit(text, (640 - 200, 920))

def redraw_screen(screen, board, time, wrong_inputs, user_name, difficulty):
    """
    Refreshes and redraws the entire game screen.
    
    Args:
        - screen (pygame.Surface): The game screen.
        - board (Sudoku_Grid): The Sudoku board.
        - time (int): The elapsed time in seconds.
        - wrong_inputs (int): The number of wrong inputs made by the user.
        - user_name (str): The name of the user.
        - difficulty (str): The selected difficulty level.
    """
    screen.fill((255, 255, 255))
    default_font = pygame.font.SysFont("comicsans", 30)
    instructions_font = pygame.font.SysFont("comicsans", 16)

    draw_welcome_message(screen, default_font)
    draw_instructions(screen, instructions_font, user_name, difficulty)
    draw_time_and_wrong_inputs(screen, instructions_font, time, wrong_inputs)
    
    # Draw grid and board
    board.draw_grid_and_cubes()

def format_time(seconds):
    """
    Converts seconds into a formatted string in 'minutes:seconds' format.
    
    Args:
        - seconds (int): The time in seconds.

    Returns:
        - str: The formatted time string.
    """
    minutes, seconds = divmod(seconds, 60)
    return f"{int(minutes)}:{round(seconds)}"
    
def print_game_summary(board, user_name):
    """
    Prints a formatted summary of the game to the console.
    
    Args:
        - board (Sudoku_Grid): The Sudoku board.
        - user_name (str): The name of the user.
    """
    
    print(f"\n[gold3][bright_green]{user_name}[/bright_green], here is your game summary:[/gold3]\n")
    print(f"\t[gold3]Game difficulty:                    [bright_green]{board.difficulty}[/bright_green][/gold3]" )

    total_time_taken = time.time() - board.start_time
    print(f"\t[gold3]Time taken to solve the puzzle:     [bright_green]{format_time(total_time_taken)}[/bright_green][/gold3]")

    print(f"\t[gold3]Number of wrong inputs:             [bright_green]{board.wrong_inputs}[/bright_green][/gold3]")

    print(f"\t[gold3]Was puzzle auto-solved?:            [bright_green]{'Yes' if board.solved_by_solver else 'No'}[/bright_green][/gold3]")

    print(f"[gold3]{DIV}\n\tTotal Score:                        [bright_green]{board.calculate_score()}[/bright_green]\n{DIV}[/gold3]" )
    
    if not board.solved_by_solver:
        write_to_csv(user_name, board, total_time_taken)
        sort_rankings()

def write_to_csv(user_name, board, total_time_taken):
    """
    Writes the game data into a CSV file.
    
    Args:
        - user_name (str): The name of the user.
        - board (Sudoku_Grid): The Sudoku board.
        - total_time_taken (float): The total time taken to solve the puzzle in seconds.
    """
    new_row = {
        'Rank': '',
        'Username': user_name,
        'Difficulty': board.difficulty,
        'Time Taken': format_time(total_time_taken),
        'Wrong Inputs': board.wrong_inputs,
        'Total Score': board.calculate_score()
    }
    if not os.path.isfile(RANKING_FILE):
        write_csv_header(RANKING_FILE)
    append_to_csv(RANKING_FILE, new_row)
    
def write_csv_header(file):
    """
    Writes the header into a CSV file.
    
    The header fields are defined by the global FIELDNAMES variable.
    """
    with open(file, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=FIELDNAMES)
        writer.writeheader()

def append_to_csv(file, new_row):
    """
    Appends a new row into an existing CSV file.
    
    Args:
        - new_row (dict): The row to be appended. It must be a dictionary where the keys match the FIELDNAMES.
    """
    with open(file, 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=FIELDNAMES)
        writer.writerow(new_row)

def sort_rankings():
    """
    Sorts the rankings in the CSV file based on total score.
    
    The rankings are sorted in descending order and the rank field is updated accordingly.
    """
    with open(RANKING_FILE, 'r') as csvfile:
        data = list(csv.DictReader(csvfile))

    for row in data:
        row['Total Score'] = int(row['Total Score'])

    sorted_data = sorted(data, key=lambda row: row['Total Score'], reverse=True)

    for rank, row in enumerate(sorted_data, start=1):
        row['Rank'] = rank

    rewrite_csv(sorted_data)

def rewrite_csv(data):
    """
    Rewrites the CSV file with the provided data.
    
    Args:
        - data (list): A list of dictionaries representing the rows of data. Each dictionary must have keys matching FIELDNAMES.
    """
    with open(RANKING_FILE, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=FIELDNAMES)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

def display_ranking(board):
    """
    Prints the leader board to the console. The leader board is read from a CSV file.
    
    If the board was solved by the solver, the user is notified that they are not included in the rankings.
    
    Args:
        - board (Sudoku_Grid): The Sudoku board.
    """
    with open('ranking.csv', 'r') as csvfile:
        data = list(csv.DictReader(csvfile))
        if board.solved_by_solver:
            print("\n[red1]Since you used the solver, you are not included in the rankings.[/red1]")
            print("[red1]Please try attempting the puzzle independently next time.[/red1]\n")
        print("\n[yellow1]🏆LEADER BOARD🏆[/yellow1]")
        print(tb(data, headers="keys", tablefmt='grid'))

def game_loop(screen, board, start, game_over, final_time, wrong_inputs, user_name, difficulty):
    """
    Contains the main game loop where all game actions are performed.

    Args:
        - screen (pygame.Surface): The game window.
        - board (Sudoku_Grid): The Sudoku board.
        - start (float): Start time of the game.
        - game_over (bool): Flag indicating if the game is over.
        - final_time (float): The time at which the game finished.
        - wrong_inputs (int): Count of wrong inputs made by the user.
        - user_name (str): The name of the user.
        - difficulty (str): The chosen difficulty of the game.
    """
    run = True
    key = None
    while run:
        if not game_over:
            play_time = round(time.time() - start)
        else:
            final_time = play_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key in KEYS:
                    key = event.key - 48 if event.key < 58 else event.key - 256
                elif event.key == pygame.K_DELETE:
                    board.clear_current_cube()
                    key = None
                elif event.key == pygame.K_SPACE:
                    board.solve_with_gui()
                elif event.key == pygame.K_RETURN:
                    i, j = board.selected
                    if board.cubes[i][j].temp != 0:
                        if board.place_value_in_selected_cube(board.cubes[i][j].temp):
                            print("\t✅ [bright_green]Correct input![/bright_green]")
                        else:
                            print("\t❌ [red1]Wrong input![/red1]")
                            wrong_inputs += 1
                        key = None

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if clicked := board.get_clicked_cube_position(pos):
                    board.select_cube(clicked[0], clicked[1])
                    key = None

        if not game_over:
            if board.selected and key is not None:
                board.sketch_temp_value(key)

            redraw_screen(screen, board, final_time if game_over else play_time, wrong_inputs, user_name, difficulty)
            if board.is_sudoku_solved():
                clear_screen()
                print(f"[bright_green]{DIV}\nGreat! You solved the puzzle. 💪\n{DIV}[bright_green]")
                print_game_summary(board, user_name)
                display_ranking(board)
                game_over = True
                pygame.display.update()

        if game_over:
            board.draw_score()
        pygame.display.update()
                
def main():
    """
    The main function of the game, which is responsible for running the game.
    """
    
    while True:
        clear_screen()
        print(f"[bold bright_blue]{DIV}\n\t\t\t🕹️ ~~ Welcome to SUDOKU- Game & Solver ~~  🕹️\n{DIV}[/bold bright_blue]")

        user_name = get_username()
        clear_screen()
        print(f"[gold3]{DIV}\nHello [bright_green]{user_name}[/bright_green], let's play SUDOKU.\n{DIV}[/gold3]")

        print(f"[gold3]{RULES}\n{DIV}[gold3]")

        difficulty, avg_rank = get_difficulty()
        clear_screen()
        print(f"[gold3]{DIV}\nLoading Puzzle...\n{DIV}[/gold3]")
        pygame.time.wait(3000)
        clear_screen()
        print(f"[gold3]{DIV}\nYour timer starts now...\n{DIV}[/gold3]")

        screen = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption(CAPTION)
        board = Sudoku_Grid(9, 9, 600, 600, screen, avg_rank, difficulty)
        start = time.time()
        game_over = False
        wrong_inputs = 0
        final_time = None

        game_loop(screen, board, start, game_over, final_time, wrong_inputs, user_name, difficulty)

        clear_screen()
        replay = get_replay_input()
        if replay.lower() not in ['yes', 'y']:
            cowsay.cow("Sad to see you go. Thank you for playing. ❤️")
            print(f"[gold3]{DIV}[/gold3]")
            break
        else:
            print(f"[bright_green]Restarting the game...[/bright_green]\n[gold3]{DIV}[/gold3]")

if __name__ == "__main__":
    main()
pygame.quit()