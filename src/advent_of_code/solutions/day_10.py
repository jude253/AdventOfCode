from advent_of_code.utils.daily_code_utils import Solution

DIRECTIONS = [(0, 1), (0, -1), (1, 0), (-1, 0)]


def is_inbounds(row, col, grid):
    return 0 <= row < len(grid) and 0 <= col < len(grid[0])


def parse_input(input_file_str):
    rows = input_file_str.split("\n")
    grid = [[int(x) if x.isnumeric() else -1 for x in row] for row in rows]
    return grid


def get_trail_heads(grid):
    trail_heads = []
    num_rows, num_cols = len(grid), len(grid[0])
    for row in range(num_rows):
        for col in range(num_cols):
            if grid[row][col] == 0:
                trail_heads.append((row, col))
    return trail_heads


class Day_10(Solution):
    def part_one(self):
        grid = parse_input(self.input_file)
        trail_heads = get_trail_heads(grid)

        def count_score(trail_head):
            score = 0
            stack = [trail_head]
            seen = set([trail_head])
            while stack:
                cur_row, cur_col = stack.pop()
                for d in DIRECTIONS:
                    new_row, new_col = cur_row + d[0], cur_col + d[1]
                    if (
                        is_inbounds(new_row, new_col, grid)
                        and grid[cur_row][cur_col] + 1 == grid[new_row][new_col]
                        and (new_row, new_col) not in seen
                    ):
                        if grid[new_row][new_col] == 9:
                            score += 1
                            seen.add((new_row, new_col))
                        else:
                            stack.append((new_row, new_col))
                            seen.add((new_row, new_col))
            return score

        return sum([count_score(trail_head) for trail_head in trail_heads])

    def part_two(self):
        grid = parse_input(self.input_file)
        trail_heads = get_trail_heads(grid)

        def count_score(trail_head):
            score = 0
            stack = [trail_head]
            seen = set([trail_head])
            while stack:
                cur_row, cur_col = stack.pop()
                for d in DIRECTIONS:
                    new_row, new_col = cur_row + d[0], cur_col + d[1]
                    if (
                        is_inbounds(new_row, new_col, grid)
                        and grid[cur_row][cur_col] + 1 == grid[new_row][new_col]
                    ):
                        if grid[new_row][new_col] == 9:
                            score += 1
                        else:
                            stack.append((new_row, new_col))
                            seen.add((new_row, new_col))
            return score

        return sum([count_score(trail_head) for trail_head in trail_heads])


if __name__ == "__main__":
    solution = Day_10()
    solution.execute_part_one()
    solution.execute_part_two()
