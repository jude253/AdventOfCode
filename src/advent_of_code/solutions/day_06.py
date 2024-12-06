import logging

from advent_of_code.utils.daily_code_utils import Solution

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


UP = (-1, 0)
RIGHT = (0, 1)
DOWN = (1, 0)
LEFT = (0, -1)

DIRS = [UP, RIGHT, DOWN, LEFT]


def is_exit(row, col, graph):
    num_rows = len(graph)
    num_cols = len(graph[0])
    return row == -1 or row == num_rows or col == -1 or col == num_cols


def is_valid(row, col, graph):
    return graph[row][col] != "#"


class Day_06(Solution):
    """
    I went for speed on this one, so I didn't try to make the code
    pretty or readible.
    """
    def part_one(self):
        graph = [list(s) for s in self.input_file.split("\n")]
        num_rows = len(graph)
        num_cols = len(graph[0])
        start_row, start_col = 0, 0
        for row in range(num_rows):
            for col in range(num_cols):
                if graph[row][col] == "^":
                    start_row, start_col = row, col
        seen = set()
        step_count = 0
        cur_dir_idx = 0
        stack = [(start_row, start_col)]

        while stack:
            cur_row, cur_col = stack.pop()
            if (cur_row, cur_col) not in seen:
                step_count += 1
            seen.add((cur_row, cur_col))
            graph[cur_row][cur_col] = step_count
            cur_dir = DIRS[cur_dir_idx]
            new_row, new_col = cur_row + cur_dir[0], cur_col + cur_dir[1]
            if is_exit(new_row, new_col, graph):
                break
            if is_valid(new_row, new_col, graph):
                stack.append((new_row, new_col))
            else:
                while not is_valid(new_row, new_col, graph):
                    cur_dir_idx = (cur_dir_idx + 1) % 4
                    cur_dir = DIRS[cur_dir_idx]
                    new_row, new_col = cur_row + cur_dir[0], cur_col + cur_dir[1]
                stack.append((new_row, new_col))

        return step_count

    def part_two(self):
        graph = [list(s) for s in self.input_file.split("\n")]
        num_rows = len(graph)
        num_cols = len(graph[0])
        start_row, start_col = 0, 0
        skip_points = []
        for row in range(num_rows):
            for col in range(num_cols):
                if graph[row][col] == "^":
                    start_row, start_col = row, col
                if graph[row][col] == ".":
                    skip_points.append((row, col))

        def is_loop(start_row, start_col, skip_row, skip_col, graph):
            seen = set()
            cur_dir_idx = 0
            graph[skip_row][skip_col] = "#"
            stack = [(start_row, start_col)]
            retracking_prev_steps_count = 0

            while stack:
                cur_row, cur_col = stack.pop()
                if (cur_row, cur_col) in seen:
                    retracking_prev_steps_count += 1
                else:
                    retracking_prev_steps_count = 0
                if retracking_prev_steps_count > 1000:
                    graph[skip_row][skip_col] = "."
                    return True
                seen.add((cur_row, cur_col))
                cur_dir = DIRS[cur_dir_idx]
                new_row, new_col = cur_row + cur_dir[0], cur_col + cur_dir[1]
                if is_exit(new_row, new_col, graph):
                    graph[skip_row][skip_col] = "."
                    return False
                if is_valid(new_row, new_col, graph):
                    stack.append((new_row, new_col))
                else:
                    while not is_valid(new_row, new_col, graph):
                        cur_dir_idx = (cur_dir_idx + 1) % 4
                        cur_dir = DIRS[cur_dir_idx]
                        new_row, new_col = cur_row + cur_dir[0], cur_col + cur_dir[1]
                    stack.append((new_row, new_col))
            graph[skip_row][skip_col] = "."
            return False

        loop_count = 0
        for skip_row, skip_col in skip_points:
            creates_loop = is_loop(start_row, start_col, skip_row, skip_col, graph)
            if creates_loop:
                loop_count += 1

        return loop_count


if __name__ == "__main__":
    solution = Day_06()
    logger.info(f"Part 1: {solution.part_one()}")
    logger.info(f"Part 2: {solution.part_two()}")
