# **SUDOKU - Solver & Game**

### **Video Demo:** https://youtu.be/kTVGgUepPJ4

## **Description:**

SUDOKU - Game & Solver is my final project for CS50's Introduction to Programming with Python.
This project is a Python-based SUDOKU game that uses Pygame for the GUI. It allows users to interactively solve randomly generated SUDOKU puzzles and, if necessary, get help from a built-in SUDOKU Solver, which utilizes a backtracking algorithm to solve the puzzle.

## **Project Repository Contents:**

This repository contains the following items:

- **project.py:** This file is the heart of the project and includes the game loop and main function along with other utility functions.
- **sudoku.py:** This file contains the classes 'SUDOKU_Grid' and 'SUDOKU_Cube', which are essential for the functionality of the SUDOKU game.
- **helper_functions.py:** This file consists of helper functions, 'find_empty_slot()' and 'is_move_valid()' that assist in the operations and manipulation throughout the project.
- **import_module.py:** This file includes all the necessary imports for this project.
- **ranking.csv:** This file contains the game ranking data in CSV format. It is updated every time a game is completed.
- **requirements.txt:** This file lists all the Python dependencies that must be installed for the project to run.
- **test_project.py**, **test_sudoku.py** and **test_helper_functions.py:** These are testing files written to ensure the proper functioning of the 'project.py' , 'sudoku,py' and 'helper_functions.py' files respectively.

## **Libraries and Dependencies:**

To run the project, the following Python libraries and modules are required:

- **pygame:** Used for creating the GUI for the SUDOKU game.
- **itertools:** Used for efficient looping and iterations.
- **time:** Used for operations involving time.
- **random:** Used for generating random number within the range of average rank for the difficulty level.
- **os:** Provides functions for interacting with the OS.
- **csv:** Used for reading and writing data in CSV format.
- **tabulate:** Used for printing LEADER BOARD data in table format.
- **rich:** Used to produce rich text and beautiful formatting in the terminal.
- **cowsay:** Used to display goodbye text in the terminal with ASCII art of a talking cow.
- **dokusan:** Used to generate SUDOKU puzzle.
- **pytest:** Used to test functions.

## **Installation:**

You will need Python3.7 or newer and above mentioned packages installed in your machine to run this project. You can download Python from [here](https://www.python.org/downloads/).
Install the project dependencies by running following code in your terminal:

```
pip install -r requirements.txt
```

## **Running the Game:**

To run the game, navigate to the directory containing '**project.py**' in your terminal or command prompt and enter the following command:

```
python project.py
```

This will start the game, and a new window will open where you can play SUDOKU.

## **Game Mechanics:**

The game starts by prompting you to enter your username, which should be alphanumeric characters and should be between 4 and 10 characters.

```
Enter your name:
```

Choose your difficulty level by entering the corresponding number:

1. EASY
2. MEDIUM
3. HARD
4. EXTREME

```
Now, let's pick a difficulty level. Press:

    [1] for EASY
    [2] for MEDIUM
    [3] for HARD
    [4] for EXTREME
```

Each difficulty level corresponds to a range of average ranks, and a difficulty number will be randomly chosen from the corresponding range.
| Difficulty | Range of Average Ranks **(avg_rank)** |
|------------|---------------------------------------|
| EASY | 30 - 49 |
| MEDIUM | 50 - 69 |
| HARD | 70 - 89 |
| EXTREME |100 - 120 |

## **Game Instructions:**

Once username and difficulty level is chosen, you will see a SUDOKU board on the screen with a greeting message, a 'HOW TO PLAY' instructions and a SUDOKU board generated with your choice of difficulty.

1. **Select a box by clicking it.** The selected box will be highlighted.
2. **Use number keys to fill the box.** This will be a temporary entry.
3. **Hit 'DELETE' to clear a box.** This will delete the number in a box.
4. **Hit 'ENTER' to confirm the digit.** If the digit is correct, it stays, else it gets deleted. The count of wrong inputs is maintained.
5. **Stuck? Hit 'SPACEBAR' to auto complete the puzzle.** This will automatically solve the puzzle for you, but beware, using this option will not earn you any points.

   ![SUDOKU display](https://github.com/sujal631/SUDOKU--Game--Solver--CS50P/blob/master/example_SUDOKU_display.png)

## **Game Summary:**

After completing the game, a summary is printed out on the console. It shows the chosen difficulty, time taken to solve the puzzle, number of wrong inputs, whether the puzzle was auto-solved or not, and the total score.

```
JoshiDai07, here is your game summary:

        Game difficulty:                    EASY
        Time taken to solve the puzzle:     3:33
        Number of wrong inputs:             0
        Was puzzle auto-solved?:            No
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        Total Score:                        108
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
```

The total score is calculated in the following way:

```python
def calculate_score(self):
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
```

The total score is calculated by subtracting penalties for wrong inputs and time taken from a base score associated with the game's difficulty level. Each wrong input costs 5 points, and each 5 seconds taken costs 1 point. If a game is auto-solved, the score isn't calculated further. The final score can't go below zero.

| Difficulty | Base Score |
| ---------- | ---------- |
| EASY       | 150        |
| MEDIUM     | 250        |
| HARD       | 350        |
| EXTREME    | 500        |

## **Game Ranking:**

If you didn't use the solver to auto-solve the game, your details (username, difficulty, time taken, wrong inputs, total score) are saved to a CSV file, **'ranking.csv'**, and you will be included in the rankings, which is sorted by total score in descending order. The rankings are then displayed on the console after every game.

![LEADER BOARD](https://github.com/sujal631/SUDOKU--Game--Solver--CS50P/blob/master/example_LEADERBOARD.png)

## **Exiting the Game:**

If you want to exit the game, simply click `❌` on the Pygame application. Upon doing this, a prompt will appear on your console screen:

```
Do you want to replay the game? (Yes/Y to replay):
```

- If you wish to replay the game, input either 'Y' or 'Yes' in the console. This will restart the game.

- If you desire to exit the game, enter any response other than 'Y' or 'Yes'. Upon doing so, the game will terminate, and you'll be greeted with the following farewell message:

```
  ____________________________________________
| Sad to see you go. Thank you for playing. ❤️ |
  ============================================
                                            \
                                             \
                                               ^__^
                                               (oo)\_______
                                               (__)\       )\/\
                                                   ||----w |
                                                   ||     ||

```
