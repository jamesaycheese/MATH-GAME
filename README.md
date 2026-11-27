# math-game

#Game 1 
The game provides 1- 9 digits. all digits can be used only once 
You random pick a number from the 1-9 digits list and the 1st number that you pick has to be able to divide by 1 
The second number you pick has to be a number that you have not picked previously. 
For example you picked 2 as your first number then your second number cannot be 2 again. 
The only option you have is 1,3,4,5,6,7,8,9. 
Let's say you pick 4.
so first number is 2 , and second number is 4. 

First number 2 can be divided by 1
First number 2 + second number 4 = 24 can be divided by 2 

lets pick number 3 as 3 
First number 2 + second number 4 +third number= 243 can be divided by 3
.
.
.
etc

so far so good 

The final goal is to use all 9 digits 


# Sudoku

`Soduku` is a backtracking solver. It finds the first empty cell, tries the digits 1 to 9, keeps a digit that does not repeat in its row, column or 3 by 3 box, and steps back when no digit fits.

`sudoku_generator.py` builds on it:

- `generate(level)` makes a random puzzle with exactly one solution, at easy, medium or hard
- `count_solutions(bo)` counts solutions, stopping at two, to test that a puzzle is fair
- `solve_smart(bo)` fills the most constrained cell first, for puzzles where plain backtracking is slow
- `check_answers(puzzle, answer, attempt)` marks a player's wrong entries

Run `python sudoku_generator.py hard` to print a puzzle and its answer.

Play it in the browser: https://jamesquantai.com/projects/sudoku-solver.html
