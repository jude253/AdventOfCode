from advent_of_code.utils.daily_code_utils import Solution

XMAS_LEN = 4
XMAS = "XMAS"
XMAS_COUNT = 0

X_MAS_WORDS = set([tuple("MAS"), tuple("SAM")])
X_MAS_COUNT = 0


def is_valid(row, col, num_rows, num_cols):
    return -1 <= row <= num_rows and -1 <= col <= num_cols


def get_word(grid, start_row, start_col, end_row, end_col):
    word = []
    row_diff = (end_row - start_row) // XMAS_LEN
    col_diff = (end_col - start_col) // XMAS_LEN
    for i in range(XMAS_LEN):
        word.append(grid[start_row + (i * row_diff)][start_col + (i * col_diff)])
    return "".join(word)


def get_xmas_count_for_point(grid, row, col):
    xmas_count_for_point = 0
    num_rows, num_cols = len(grid), len(grid[0])

    right_end = (row, col + XMAS_LEN)
    left_end = (row, col - XMAS_LEN)
    down_end = (row + XMAS_LEN, col)
    up_end = (row - XMAS_LEN, col)
    diagonal_1 = (row + XMAS_LEN, col + XMAS_LEN)
    diagonal_2 = (row - XMAS_LEN, col + XMAS_LEN)
    diagonal_3 = (row - XMAS_LEN, col - XMAS_LEN)
    diagonal_4 = (row + XMAS_LEN, col - XMAS_LEN)

    endpoints = [
        right_end,
        left_end,
        down_end,
        up_end,
        diagonal_1,
        diagonal_2,
        diagonal_3,
        diagonal_4,
    ]

    for endpoint in endpoints:
        if (
            is_valid(*endpoint, num_rows, num_cols)
            and get_word(grid, row, col, *endpoint) == XMAS
        ):
            xmas_count_for_point += 1
    return xmas_count_for_point


def parse_input(input_file_str):
    return [list(line) for line in input_file_str.split("\n")]


class Day_04(Solution):
    def part_one(self):
        global XMAS_COUNT
        grid = parse_input(self.input_file)
        for row in range(len(grid)):
            for col in range(len(grid[0])):
                XMAS_COUNT += get_xmas_count_for_point(grid, row, col)
        return XMAS_COUNT

    def part_two(self):
        global X_MAS_COUNT
        grid = parse_input(self.input_file)
        for row in range(len(grid) - 2):
            for col in range(len(grid[0]) - 2):
                word_1 = (
                    grid[row][col],
                    grid[row + 1][col + 1],
                    grid[row + 2][col + 2],
                )
                word_2 = (
                    grid[row + 2][col],
                    grid[row + 1][col + 1],
                    grid[row][col + 2],
                )
                if word_1 in X_MAS_WORDS and word_2 in X_MAS_WORDS:
                    X_MAS_COUNT += 1

        return X_MAS_COUNT


if __name__ == "__main__":
    solution = Day_04()
    solution.execute_part_one()
    solution.execute_part_two()
