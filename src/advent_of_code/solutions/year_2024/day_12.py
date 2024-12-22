from advent_of_code.utils.daily_code_utils import Solution

DIRECTIONS = [(0, 1), (0, -1), (1, 0), (-1, 0)]


def is_inbounds(row, col, grid):
    return 0 <= row < len(grid) and 0 <= col < len(grid[0])


def parse_input(input_file_str):
    rows = input_file_str.split("\n")
    grid = [list(row) for row in rows]
    return grid


def traverse(node, grid):
    char = grid[node[0]][node[1]]
    stack = [node]
    seen = set([node])
    area = 0
    perimeter = 0
    while stack:
        cur_row, cur_col = stack.pop()
        area += 1
        for d in DIRECTIONS:
            new_row, new_col = cur_row + d[0], cur_col + d[1]
            if is_inbounds(new_row, new_col, grid) and grid[new_row][new_col] == char:
                if (new_row, new_col) not in seen:
                    stack.append((new_row, new_col))
                    seen.add((new_row, new_col))
            else:
                perimeter += 1
    return area, perimeter, seen


def traverse_pt2(node, grid):
    char = grid[node[0]][node[1]]
    stack = [node]
    seen = set([node])
    side_count = 0
    edges = set()
    area = 0
    perimeter = 0
    while stack:
        cur_row, cur_col = stack.pop()
        area += 1

        for d in DIRECTIONS:
            new_row, new_col = cur_row + d[0], cur_col + d[1]
            if is_inbounds(new_row, new_col, grid) and grid[new_row][new_col] == char:
                if (new_row, new_col) not in seen:
                    stack.append((new_row, new_col))
                    seen.add((new_row, new_col))
            else:
                edges.add((cur_row, cur_col))
                perimeter += 1

    # I definitely didn't copy this part from someone else:
    for d in DIRECTIONS:
        potential_side = set()
        for node in seen:
            temp = node[0] + d[0], node[1] + d[1]
            if temp not in seen:
                potential_side.add(temp)
        to_remove = set()
        for node in potential_side:
            temp = node[0] + d[1], node[1] + d[0]
            while temp in potential_side:
                to_remove.add(temp)
                temp = temp[0] + d[1], temp[1] + d[0]
        side_count += len(potential_side) - len(to_remove)
    return area, side_count, seen


class Day_12(Solution):
    def part_one(self):
        grid = parse_input(self.input_file)
        num_rows, num_cols = len(grid), len(grid[0])
        overall_seen = set()
        score = 0
        for row in range(num_rows):
            for col in range(num_cols):
                if (row, col) not in overall_seen:
                    area, perimeter, seen = traverse((row, col), grid)
                    score += area * perimeter
                    overall_seen = overall_seen.union(seen)

        return score

    def part_two(self):
        grid = parse_input(self.input_file)
        num_rows, num_cols = len(grid), len(grid[0])
        overall_seen = set()
        score = 0
        for row in range(num_rows):
            for col in range(num_cols):
                if (row, col) not in overall_seen:
                    area, perimeter, seen = traverse_pt2((row, col), grid)
                    score += area * perimeter
                    overall_seen = overall_seen.union(seen)

        return score


if __name__ == "__main__":
    solution = Day_12()
    solution.execute_part_one()
    solution.execute_part_two()
