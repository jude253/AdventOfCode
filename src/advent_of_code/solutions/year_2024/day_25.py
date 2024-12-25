from advent_of_code.utils.daily_code_utils import Solution

FILLED_IN_ROW = "#####"


def get_column_heights(grid):
    column_heights = [-1] * len(grid[0])
    for col in range(len(grid[0])):
        for row in range(len(grid)):
            if grid[row][col] == "#":
                column_heights[col] += 1
    return column_heights


def sum_column_heights(a, b):
    out = [0] * len(a)
    for col in range(len(a)):
        out[col] = a[col] + b[col]
    return out


class Day_25(Solution):
    def part_one(self):
        locks_and_keys = [x.splitlines() for x in self.input_file.split("\n\n")]
        max_height = len(locks_and_keys[0]) - 1
        locks = [get_column_heights(x) for x in locks_and_keys if x[0] == FILLED_IN_ROW]
        keys = [get_column_heights(x) for x in locks_and_keys if x[-1] == FILLED_IN_ROW]

        unique_combinations_count = 0
        for lock in locks:
            for key in keys:
                summed_key_and_lock = sum_column_heights(lock, key)
                if not any([val >= max_height for val in summed_key_and_lock]):
                    unique_combinations_count += 1
        return unique_combinations_count

    def part_two(self):
        return


if __name__ == "__main__":
    solution = Day_25()
    solution.execute_part_one()
    solution.execute_part_two()
