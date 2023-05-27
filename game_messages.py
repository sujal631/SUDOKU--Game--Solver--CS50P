"""
str: A string consisting of 100 '~' characters.

This constant is used to print divider lines for UI separation in console output.
"""
DIV = "~" * 100


"""
str: A multi-line string outlining the rules of the game Sudoku.

This constant is used to print the rules of the game to the console.
"""
RULES = f"""
Here are some key rules for playing SUDOKU:

\t1. Sudoku is a 9x9 grid divided into nine 3x3 boxes. Each box, row, and 
\t   column must contain all numbers 1-9 with no repetition.
\t2. The game begins with certain cells pre-filled. Your task is to complete
\t   the grid following the above rule.
\t3. Difficulty varies with the number and position of the starting numbers.
\t   More filled-in numbers typically means easier puzzles.
\t4. Notations or pencil marks can be used to track potential numbers.
\t5. Time is a crucial factor; quicker solutions result in higher rankings.
"""


"""
str: A multi-line string detailing the difficulty options for the game.

This constant is used to present the difficulty options to the user and request their input.
"""
DIFF = f"""
Now, let's pick a difficulty level. Press:

\t[1] for EASY
\t[2] for MEDIUM
\t[3] for HARD
\t[4] for EXTREME
"""
