from advent_of_code.utils.daily_code_utils import Solution
from advent_of_code.utils.grid import DOWN, LEFT, RIGHT, UP, Grid

DIRS_MAP = {
    "^": UP,
    ">": RIGHT,
    "v": DOWN,
    "<": LEFT,
}


def get_box_val(row, col):
    return 100 * row + col


class Day_15(Solution):
    def part_one(self):
        grid_str, moves = self.input_file.split("\n\n")
        moves = moves.replace("\n", "")

        grid = Grid(grid_str)

        cur_loc = None
        for row, col in grid.nodes_indicies():
            if grid.get_node_val(row, col) == "@":
                cur_loc = (row, col)
                break

        for i in range(len(moves)):
            cur_dir_arrow = moves[i % len(moves)]
            cur_dir = DIRS_MAP[cur_dir_arrow]
            new_loc = (cur_loc[0] + cur_dir[0], cur_loc[1] + cur_dir[1])
            if grid.get_node_val(new_loc[0], new_loc[1]) != "#":
                if grid.get_node_val(new_loc[0], new_loc[1]) == ".":
                    grid.set_node_val(cur_loc[0], cur_loc[1], ".")
                    grid.set_node_val(new_loc[0], new_loc[1], "@")
                    cur_loc = new_loc
                elif grid.get_node_val(new_loc[0], new_loc[1]) == "O":
                    next_O_loc = new_loc
                    stack = [next_O_loc]
                    while grid.get_node_val(next_O_loc[0], next_O_loc[1]) == "O":
                        next_O_loc = (
                            next_O_loc[0] + cur_dir[0],
                            next_O_loc[1] + cur_dir[1],
                        )
                        stack.append(next_O_loc)

                    if grid.get_node_val(next_O_loc[0], next_O_loc[1]) == ".":
                        grid.set_node_val(cur_loc[0], cur_loc[1], ".")
                        while stack:
                            cur_update = stack.pop()
                            grid.set_node_val(cur_update[0], cur_update[1], "O")
                        grid.set_node_val(new_loc[0], new_loc[1], "@")
                        cur_loc = new_loc

        total_box_val = 0
        for row, col in grid.nodes_indicies():
            if grid.get_node_val(row, col) == "O":
                total_box_val += get_box_val(row, col)
        return total_box_val

    def part_two(self):
        grid_str, moves = self.input_file.split("\n\n")
        grid_str = grid_str.replace("#", "##")
        grid_str = grid_str.replace(".", "..")
        grid_str = grid_str.replace("O", "[]")
        grid_str = grid_str.replace("@", "@.")
        moves = moves.replace("\n", "")

        grid = Grid(grid_str)

        cur_loc = None
        for row, col in grid.nodes_indicies():
            if grid.get_node_val(row, col) == "@":
                cur_loc = (row, col)
                break

        def get_other_loc(cur_brac_loc, grid):
            if grid.get_node_val(cur_brac_loc[0], cur_brac_loc[1]) == "[":
                return (cur_brac_loc[0] + RIGHT[0], cur_brac_loc[1] + RIGHT[1])
            return (cur_brac_loc[0] + LEFT[0], cur_brac_loc[1] + LEFT[1])

        def can_update_lr(cur_loc, cur_dir, grid):
            if grid.get_node_val(*cur_loc) == ".":
                return True
            if grid.get_node_val(*cur_loc) == "#":
                return False
            new_loc = (cur_loc[0] + cur_dir[0], cur_loc[1] + cur_dir[1])
            return can_update_lr(new_loc, cur_dir, grid)

        def get_nodes_to_update_lr(cur_loc, cur_dir, grid, nodes, depth):
            if grid.get_node_val(*cur_loc) == ".":
                return
            if grid.get_node_val(*cur_loc) == "#":
                return
            nodes.add((depth, cur_loc))
            new_loc = (cur_loc[0] + cur_dir[0], cur_loc[1] + cur_dir[1])
            get_nodes_to_update_lr(new_loc, cur_dir, grid, nodes, depth + 1)
            return

        def can_update_ud(cur_loc, cur_dir, grid):
            if grid.get_node_val(*cur_loc) == ".":
                return True
            if grid.get_node_val(*cur_loc) == "#":
                return False

            other_loc = get_other_loc(cur_loc, grid)
            new_loc1 = (cur_loc[0] + cur_dir[0], cur_loc[1] + cur_dir[1])
            new_loc2 = (other_loc[0] + cur_dir[0], other_loc[1] + cur_dir[1])
            return can_update_ud(new_loc1, cur_dir, grid) and can_update_ud(
                new_loc2, cur_dir, grid
            )

        def get_nodes_to_update_ud(cur_loc, cur_dir, grid, nodes, depth):
            if grid.get_node_val(*cur_loc) == ".":
                return
            if grid.get_node_val(*cur_loc) == "#":
                return

            other_loc = get_other_loc(cur_loc, grid)
            nodes.add((depth, cur_loc))
            nodes.add((depth, other_loc))
            new_loc1 = (cur_loc[0] + cur_dir[0], cur_loc[1] + cur_dir[1])
            new_loc2 = (other_loc[0] + cur_dir[0], other_loc[1] + cur_dir[1])
            get_nodes_to_update_ud(new_loc1, cur_dir, grid, nodes, depth + 1)
            get_nodes_to_update_ud(new_loc2, cur_dir, grid, nodes, depth + 1)
            return

        for i in range(len(moves)):
            cur_dir_arrow = moves[i % len(moves)]
            cur_dir = DIRS_MAP[cur_dir_arrow]
            new_loc = (cur_loc[0] + cur_dir[0], cur_loc[1] + cur_dir[1])
            new_loc_val = grid.get_node_val(new_loc[0], new_loc[1])
            if grid.get_node_val(new_loc[0], new_loc[1]) != "#":
                if grid.get_node_val(new_loc[0], new_loc[1]) == ".":
                    grid.set_node_val(cur_loc[0], cur_loc[1], ".")
                    grid.set_node_val(new_loc[0], new_loc[1], "@")
                    cur_loc = new_loc
                elif new_loc_val in ("[", "]") and cur_dir in (LEFT, RIGHT):
                    if not can_update_lr(new_loc, cur_dir, grid):
                        continue
                    nodes_to_update = set()
                    get_nodes_to_update_lr(new_loc, cur_dir, grid, nodes_to_update, 0)
                    nodes_to_update = sorted(list(nodes_to_update), reverse=True)
                    for _depth, node in nodes_to_update:
                        replace_loc = (node[0] + cur_dir[0], node[1] + cur_dir[1])
                        replace_val = grid.get_node_val(*replace_loc)
                        node_val = grid.get_node_val(*node)
                        grid.set_node_val(*replace_loc, node_val)
                        grid.set_node_val(*node, replace_val)
                    grid.set_node_val(cur_loc[0], cur_loc[1], ".")
                    grid.set_node_val(new_loc[0], new_loc[1], "@")
                    cur_loc = new_loc

                elif new_loc_val in ("[", "]") and cur_dir in (UP, DOWN):
                    if not can_update_ud(new_loc, cur_dir, grid):
                        continue
                    nodes_to_update = set()
                    get_nodes_to_update_ud(new_loc, cur_dir, grid, nodes_to_update, 0)
                    nodes_to_update = sorted(list(nodes_to_update), reverse=True)
                    for _depth, node in nodes_to_update:
                        replace_loc = (node[0] + cur_dir[0], node[1] + cur_dir[1])
                        replace_val = grid.get_node_val(*replace_loc)
                        node_val = grid.get_node_val(*node)
                        grid.set_node_val(*replace_loc, node_val)
                        grid.set_node_val(*node, replace_val)
                    grid.set_node_val(cur_loc[0], cur_loc[1], ".")
                    grid.set_node_val(new_loc[0], new_loc[1], "@")
                    cur_loc = new_loc

        total_box_val = 0
        for row, col in grid.nodes_indicies():
            if grid.get_node_val(row, col) == "[":
                total_box_val += get_box_val(row, col)
        return total_box_val


if __name__ == "__main__":
    solution = Day_15()
    solution.execute_part_one()
    solution.execute_part_two()
