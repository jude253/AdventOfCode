from advent_of_code.utils.daily_code_utils import Solution
from advent_of_code.utils.grid import Grid


def make_grid(height, width):
    return "\n".join(["0" * width for _ in range(height)])


def set_state(robots, grid):
    for i in range(len(robots)):
        p, v = robots[i]
        grid.set_node_val(p[1], p[0], int(grid.get_node_val(p[1], p[0])) + 1)


def clear(grid):
    for row, col in grid.nodes_indicies():
        grid.set_node_val(row, col, 0)


def no_overlaps(grid):
    for row, col in grid.nodes_indicies():
        if int(grid.get_node_val(row, col)) not in (1, 0):
            return False
    return True


def parse_input(input_file_str):
    robots = []
    lines = input_file_str.splitlines()
    for line in lines:
        p_temp, v_temp = line.split()
        p_temp, v_temp = p_temp.split(","), v_temp.split(",")
        p = (int(p_temp[0][2:]), int(p_temp[1]))
        v = (int(v_temp[0][2:]), int(v_temp[1]))
        robots.append([p, v])
    return robots


class Day_14(Solution):
    def part_one(self):
        robots = parse_input(self.input_file)
        # HEIGHT, WIDTH = 7, 11
        HEIGHT, WIDTH = 103, 101
        MID_HEIGHT, MID_WIDTH = HEIGHT // 2, WIDTH // 2
        grid = Grid(make_grid(HEIGHT, WIDTH))

        for row, col in grid.nodes_indicies():
            grid.set_node_val(row, col, int(grid.get_node_val(row, col)))

        num_seconds = 100

        for _ in range(num_seconds):
            for j in range(len(robots)):
                p, v = robots[j]
                new_p = ((p[0] + v[0]) % grid.num_cols, (p[1] + v[1]) % grid.num_rows)
                robots[j][0] = new_p

        set_state(robots, grid)

        upper_left = 0
        upper_right = 0
        lower_left = 0
        lower_right = 0

        for row, col in grid.nodes_indicies():
            if row < MID_HEIGHT and col < MID_WIDTH:
                upper_left += int(grid.get_node_val(row, col))
            if row < MID_HEIGHT and col > MID_WIDTH:
                upper_right += int(grid.get_node_val(row, col))
            if row > MID_HEIGHT and col < MID_WIDTH:
                lower_left += int(grid.get_node_val(row, col))
            if row > MID_HEIGHT and col > MID_WIDTH:
                lower_right += int(grid.get_node_val(row, col))

        return upper_left * upper_right * lower_left * lower_right

    def part_two(self):
        robots = parse_input(self.input_file)
        HEIGHT, WIDTH = 103, 101

        grid = Grid(make_grid(HEIGHT, WIDTH))

        num_seconds = 10000

        for _i in range(num_seconds):
            for j in range(len(robots)):
                p, v = robots[j]
                new_p = ((p[0] + v[0]) % grid.num_cols, (p[1] + v[1]) % grid.num_rows)
                robots[j][0] = new_p
            set_state(robots, grid)
            if no_overlaps(grid):
                grid.print()
                break
            clear(grid)

        return _i + 1


if __name__ == "__main__":
    solution = Day_14()
    solution.execute_part_one()
    solution.execute_part_two()
