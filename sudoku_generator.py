"""Random Sudoku puzzles, built on the backtracking solver in the `Soduku` file.

What this adds to the original solver:

- generate(level): a random puzzle with exactly one solution
- count_solutions(bo): counts solutions, stopping at two, to test that a puzzle is fair
- solve_smart(bo): backtracking that fills the most constrained cell first, for puzzles
  where plain left-to-right backtracking takes too long
- check_answers(puzzle, answer, attempt): marks a player's wrong entries

Run it to print a puzzle and its answer:

    python sudoku_generator.py            # medium
    python sudoku_generator.py hard

The same logic runs in the browser at https://jamesquantai.com/projects/sudoku-solver.html
"""
import random
import sys

# Starting numbers left on the board at each level. Fewer numbers is a rough guide to
# difficulty, not an exact one.
CLUES = {"easy": 40, "medium": 32, "hard": 26}


def valid(bo, num, pos):
    """True if num can sit at pos (row, col) without repeating in its row, column or box."""
    # Check row
    for i in range(9):
        if bo[pos[0]][i] == num and pos[1] != i:
            return False

    # Check column
    for i in range(9):
        if bo[i][pos[1]] == num and pos[0] != i:
            return False

    # Check box
    box_x = pos[1] // 3
    box_y = pos[0] // 3

    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if bo[i][j] == num and (i, j) != pos:
                return False

    return True


def find_tightest(bo):
    """The empty cell with the fewest digits that fit, or None if the board is full."""
    best, best_count = None, 10
    for i in range(9):
        for j in range(9):
            if bo[i][j] != 0:
                continue
            count = sum(1 for n in range(1, 10) if valid(bo, n, (i, j)))
            if count < best_count:
                best, best_count = (i, j), count
                if count <= 1:
                    return best
    return best


def solve_smart(bo):
    """Backtracking that always fills the most constrained cell next. Solves bo in place."""
    find = find_tightest(bo)
    if not find:
        return True
    row, col = find

    for i in range(1, 10):
        if valid(bo, i, (row, col)):
            bo[row][col] = i

            if solve_smart(bo):
                return True

            bo[row][col] = 0

    return False


def full_grid():
    """A complete valid grid: backtracking with the digits tried in random order."""
    bo = [[0] * 9 for _ in range(9)]

    def fill():
        find = find_tightest(bo)
        if not find:
            return True
        row, col = find
        digits = list(range(1, 10))
        random.shuffle(digits)
        for num in digits:
            if valid(bo, num, (row, col)):
                bo[row][col] = num
                if fill():
                    return True
                bo[row][col] = 0
        return False

    fill()
    return bo


def count_solutions(bo, limit=2):
    """Number of solutions, stopping at limit. A fair puzzle has exactly one. Leaves bo unchanged."""
    found = 0

    def search():
        nonlocal found
        find = find_tightest(bo)
        if not find:
            found += 1
            return
        row, col = find
        for num in range(1, 10):
            if found >= limit:
                return
            if valid(bo, num, (row, col)):
                bo[row][col] = num
                search()
                bo[row][col] = 0

    search()
    return found


def generate(level="medium"):
    """Return (puzzle, answer). The puzzle has exactly one solution.

    Starts from a full grid and removes numbers one at a time in random order, keeping a
    removal only if the puzzle still has a single solution.
    """
    target = CLUES.get(level, CLUES["medium"])
    answer = full_grid()
    puzzle = [row[:] for row in answer]
    left = 81

    cells = [(i, j) for i in range(9) for j in range(9)]
    random.shuffle(cells)
    for row, col in cells:
        if left <= target:
            break
        keep = puzzle[row][col]
        puzzle[row][col] = 0
        if count_solutions(puzzle) == 1:
            left -= 1
        else:
            puzzle[row][col] = keep

    return puzzle, answer


def check_answers(puzzle, answer, attempt):
    """Compare a player's board with the answer.

    Returns (wrong, empty): the cells the player filled in wrongly, and the cells still empty.
    Starting numbers from the puzzle are skipped.
    """
    wrong, empty = [], []
    for i in range(9):
        for j in range(9):
            if puzzle[i][j] != 0:
                continue
            if attempt[i][j] == 0:
                empty.append((i, j))
            elif attempt[i][j] != answer[i][j]:
                wrong.append((i, j))
    return wrong, empty


def print_board(bo):
    for i in range(len(bo)):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - - - - ")

        for j in range(len(bo[0])):
            if j % 3 == 0 and j != 0:
                print(" | ", end="")

            if j == 8:
                print(bo[i][j])
            else:
                print(str(bo[i][j]) + " ", end="")


if __name__ == "__main__":
    level = sys.argv[1] if len(sys.argv) > 1 else "medium"
    if level not in CLUES:
        sys.exit("Level must be one of: " + ", ".join(CLUES))

    puzzle, answer = generate(level)
    clues = sum(1 for row in puzzle for n in row if n != 0)
    print(f"{level.capitalize()} puzzle with {clues} starting numbers (0 means empty):")
    print_board(puzzle)
    print("___________________")
    print("Answer:")
    print_board(answer)
