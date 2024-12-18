from collections import deque

from advent_of_code.utils.daily_code_utils import Solution
from advent_of_code.utils.grid import CLOCKWISE_DIRS, Grid


def make_grid(height, width):
    return "\n".join(["." * width for _ in range(height)])


class Day_18(Solution):
    def part_one(self):
        coords = []
        for line in self.input_file.splitlines():
            coords.append(tuple(int(x) for x in line.split(",")))
        grid_len = 70
        first_bytes_count = 1024
        start = (0, 0)
        end = (grid_len, grid_len)
        grid = Grid(make_grid(grid_len + 1, grid_len + 1))
        for col, row in coords[:first_bytes_count]:
            grid.set_node_val(row, col, "#")
        queue = deque([start])
        seen = set([start])
        cur_dist = 0
        while queue:
            num_nodes_at_level = len(queue)
            for _ in range(num_nodes_at_level):
                cur_col, cur_row = queue.popleft()
                if (cur_col, cur_row) == end:
                    return cur_dist
                for d in CLOCKWISE_DIRS:
                    new_col, new_row = cur_col + d[0], cur_row + d[1]
                    if (
                        grid.is_inbounds(new_row, new_col)
                        and grid.get_node_val(new_row, new_col) != "#"
                        and (new_col, new_row) not in seen
                    ):
                        seen.add((new_col, new_row))
                        queue.append((new_col, new_row))
            cur_dist += 1

        return cur_dist

    def part_two(self):
        coords = []
        for line in self.input_file.splitlines():
            coords.append(tuple(int(x) for x in line.split(",")))
        grid_len = 70
        first_bytes_count = 1024
        start = (0, 0)
        end = (grid_len, grid_len)
        grid = Grid(make_grid(grid_len + 1, grid_len + 1))
        for col, row in coords[:first_bytes_count]:
            grid.set_node_val(row, col, "#")

        def reaches_exit(start, end, grid):
            queue = deque([start])
            seen = set([start])
            cur_dist = 0

            while queue:
                num_nodes_at_level = len(queue)
                for _ in range(num_nodes_at_level):
                    cur_col, cur_row = queue.popleft()
                    if (cur_col, cur_row) == end:
                        return True
                    for d in CLOCKWISE_DIRS:
                        new_col, new_row = cur_col + d[0], cur_row + d[1]
                        if (
                            grid.is_inbounds(new_row, new_col)
                            and grid.get_node_val(new_row, new_col) != "#"
                            and (new_col, new_row) not in seen
                        ):
                            seen.add((new_col, new_row))
                            queue.append((new_col, new_row))
                cur_dist += 1
            return False

        i = 1
        while reaches_exit(start, end, grid):
            col, row = coords[first_bytes_count + i]
            grid.set_node_val(row, col, "#")
            i += 1

        return ",".join([str(x) for x in coords[first_bytes_count + i - 1]])


if __name__ == "__main__":
    solution = Day_18()
    solution.execute_part_one()
    solution.execute_part_two()
