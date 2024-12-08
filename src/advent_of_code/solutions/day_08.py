from collections import defaultdict, deque

from advent_of_code.utils.daily_code_utils import Solution


def is_inbounds(row, col, grid):
    num_rows, num_cols = len(grid), len(grid[0])
    return 0 <= row < num_rows and 0 <= col < num_cols


class Day_08(Solution):
    def part_one(self):
        antenna_map = defaultdict(list)
        grid = [list(line) for line in self.input_file.split("\n")]
        num_rows, num_cols = len(grid), len(grid[0])

        for row in range(num_rows):
            for col in range(num_cols):
                char = grid[row][col]
                if char != "." and char != "#":
                    antenna_map[char].append((row, col))
        antinodes_set = set()
        for char, points in antenna_map.items():
            num_points = len(points)
            for i in range(num_points - 1):
                for j in range(i + 1, num_points):
                    diff = (points[i][0] - points[j][0], points[i][1] - points[j][1])
                    for pt in (points[i], points[j]):
                        new_pt_pos = (pt[0] + diff[0], pt[1] + diff[1])
                        new_pt_neg = (pt[0] - diff[0], pt[1] - diff[1])
                        if (
                            is_inbounds(*new_pt_pos, grid)
                            and grid[new_pt_pos[0]][new_pt_pos[1]] != char
                        ):
                            antinodes_set.add(new_pt_pos)
                            grid[new_pt_pos[0]][new_pt_pos[1]] = "#"
                        if (
                            is_inbounds(*new_pt_neg, grid)
                            and grid[new_pt_neg[0]][new_pt_neg[1]] != char
                        ):
                            antinodes_set.add(new_pt_neg)
                            grid[new_pt_neg[0]][new_pt_neg[1]] = "#"

        return len(antinodes_set)

    def part_two(self):
        antenna_map = defaultdict(list)
        grid = [list(line) for line in self.input_file.split("\n")]
        num_rows, num_cols = len(grid), len(grid[0])

        for row in range(num_rows):
            for col in range(num_cols):
                char = grid[row][col]
                if char != "." and char != "#":
                    antenna_map[char].append((row, col))
        antinodes_set = set()
        for _char, points in antenna_map.items():
            num_points = len(points)
            for i in range(num_points - 1):
                for j in range(i + 1, num_points):
                    diff = (points[i][0] - points[j][0], points[i][1] - points[j][1])
                    seen = set()
                    queue = deque([points[i], points[j]])
                    while queue:
                        pt = queue.popleft()
                        new_pt_pos = (pt[0] + diff[0], pt[1] + diff[1])
                        new_pt_neg = (pt[0] - diff[0], pt[1] - diff[1])
                        if is_inbounds(*new_pt_pos, grid) and new_pt_pos not in seen:
                            seen.add(new_pt_pos)
                            queue.append(new_pt_pos)
                            antinodes_set.add(new_pt_pos)
                            grid[new_pt_pos[0]][new_pt_pos[1]] = "#"
                        if is_inbounds(*new_pt_neg, grid) and new_pt_neg not in seen:
                            seen.add(new_pt_neg)
                            queue.append(new_pt_neg)
                            antinodes_set.add(new_pt_neg)
                            grid[new_pt_neg[0]][new_pt_neg[1]] = "#"

        return len(antinodes_set)


if __name__ == "__main__":
    solution = Day_08()
    solution.execute_part_one()
    solution.execute_part_two()
