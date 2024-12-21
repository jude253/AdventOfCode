from collections import deque

from advent_of_code.utils.daily_code_utils import Solution
from advent_of_code.utils.grid import DOWN, LEFT, RIGHT, UP, Grid

NUMERICAL_PAD = "789\n" "456\n" "123\n" "#0A"

"""
    +---+---+
    | ^ | A |
+---+---+---+
| < | v | > |
+---+---+---+
"""
DIRECTIONAL_PAD = "#^A\n" "<v>"

DIRS = {
    "^": UP,
    "v": DOWN,
    "<": LEFT,
    ">": RIGHT,
}


def _get_shortest_paths_between(start_val, end_val, grid: Grid):
    if start_val == end_val:
        return "A"

    for row, col in grid.nodes_indicies():
        if grid.get_node_val(row, col) == start_val:
            start_ind = (row, col)

    queue = deque([(*start_ind, 0, "")])
    seen = set([(*start_ind, 0, "")])
    out_seqs = set()
    dist = 0
    min_out_seq_len = float("inf")
    while queue:
        num_nodes_at_dist = len(queue)
        for _ in range(num_nodes_at_dist):
            cur_row, cur_col, find_ind, out_seq = queue.popleft()
            for arrow, d in DIRS.items():
                new_row, new_col = cur_row + d[0], cur_col + d[1]
                if not grid.is_inbounds(new_row, new_col):
                    continue
                new_val = grid.get_node_val(new_row, new_col)
                new_find_ind = find_ind
                new_out_seq = out_seq + arrow
                if new_val == "#":
                    continue
                if new_val == end_val:
                    new_find_ind += 1
                    new_out_seq = new_out_seq + "A"
                    if len(new_out_seq) <= min_out_seq_len:
                        min_out_seq_len = min(min_out_seq_len, len(new_out_seq))
                        out_seqs.add(new_out_seq)

                if len(new_out_seq) > min_out_seq_len:
                    continue

                seen.add((new_row, new_col, new_find_ind, new_out_seq))
                queue.append((new_row, new_col, new_find_ind, new_out_seq))
        dist += 1
    return list(out_seqs)


def get_shortest_paths(code, grid):
    out_seq_paths_list = []
    prev = "A"
    for i in range(len(code)):
        shortest_paths = _get_shortest_paths_between(prev, code[i], grid)
        out_seq_paths_list.append(shortest_paths)
        prev = code[i]
    stack = [(0, "")]
    seen = set((0, ""))
    out_paths = []
    while stack:
        cur_ind, cur_path = stack.pop()
        for new_path_seg in out_seq_paths_list[cur_ind]:
            new_ind = cur_ind + 1
            new_path = cur_path + new_path_seg
            seen.add((new_ind, new_path))
            if new_ind == len(out_seq_paths_list):
                out_paths.append(new_path)
            else:
                stack.append((new_ind, new_path))
    return out_paths


def get_shortest_human_path(code, num_pad, dir_pad):
    paths1 = get_shortest_paths(code, num_pad)
    shortestest_paths2 = []
    min_len_path2 = float("inf")
    for path1 in paths1:
        paths2 = get_shortest_paths(path1, dir_pad)
        cur_len_path2 = len(paths2[0])
        if cur_len_path2 < min_len_path2:
            min_len_path2 = cur_len_path2
            shortestest_paths2 = paths2[:]
        elif cur_len_path2 == min_len_path2:
            shortestest_paths2.extend(paths2)

    shortestest_paths3 = []
    min_len_path3 = float("inf")
    for path2 in shortestest_paths2:
        paths3 = get_shortest_paths(path2, dir_pad)
        cur_len_path3 = len(paths3[0])
        if cur_len_path3 < min_len_path3:
            min_len_path3 = cur_len_path3
            shortestest_paths3 = paths3[:]
        elif cur_len_path2 == min_len_path2:
            shortestest_paths3.extend(paths3)

    return shortestest_paths3


class Day_21(Solution):
    def part_one(self):
        codes = [line for line in self.input_file.splitlines()]
        num_pad = Grid(NUMERICAL_PAD)
        dir_pad = Grid(DIRECTIONAL_PAD)

        total = 0
        for code in codes:
            shortest_human_paths = get_shortest_human_path(code, num_pad, dir_pad)
            numeric_code = int("".join(x for x in code if x.isdecimal()))
            total += numeric_code * len(shortest_human_paths[0])

        return total

    def part_two(self):
        return


if __name__ == "__main__":
    solution = Day_21()
    solution.execute_part_one()
    solution.execute_part_two()
