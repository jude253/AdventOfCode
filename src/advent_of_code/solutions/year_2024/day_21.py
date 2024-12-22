import math
from collections import deque
from functools import cache

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
        direction = {(0, 1): ">", (-1, 0): "^", (0, -1): "<", (1, 0): "v"}

        def valid(mat, x, y):
            return (
                x >= 0
                and x < len(mat)
                and y >= 0
                and y < len(mat[x])
                and mat[x][y] != "#"
            )

        def precalc(mat):
            resp = {}
            for i in range(len(mat)):
                for j in range(len(mat[i])):
                    if mat[i][j] == "#":
                        continue
                    for k in range(len(mat)):
                        for a in range(len(mat[k])):
                            if k == i and a == j:
                                continue
                            resp[(i, j, k, a)] = paths(mat, (i, j), (k, a))
            return resp

        def paths(mat, start, end):
            q = deque([(*start, [start])])
            result = []
            m = math.inf
            while q:
                x, y, path = q.popleft()
                if (x, y) == end and len(path) <= m:
                    if len(path) < m:
                        result.clear()
                    m = len(path)
                    result.append(path)
                    continue
                for d in direction:
                    u = (x + d[0], y + d[1])
                    if valid(mat, *u) and u not in path:
                        q.append((*u, path + [u]))
            final = []
            for r in result:
                f = []
                for i in range(1, len(r)):
                    mov = (r[i][0] - r[i - 1][0], r[i][1] - r[i - 1][1])
                    f.append(direction[mov])
                f.append("A")
                final.append(f)
            return final

        def toCord(mat):
            result = {}
            for i in range(len(mat)):
                for j in range(len(mat[i])):
                    result[mat[i][j]] = (i, j)
            return result

        pad = ["789", "456", "123", "#0A"]
        pad2cord = toCord(pad)

        padpaths = precalc(pad)

        dpad = ["#^A", "<v>"]
        dpad2cord = toCord(dpad)
        dpadpaths = precalc(dpad)

        def genericpad(c, p2cord, allpaths, mat, start="A"):
            current = p2cord[start]
            options = []
            for i in c:
                target = p2cord[i]

                paths = allpaths[(*current, *target)] if current != target else [["A"]]
                response = []
                if len(options) == 0:
                    response = [] + paths
                else:
                    for o in options:
                        for p in paths:
                            response.append(o + p)
                options = response
                current = target
            m = min([len(o) for o in options])
            return ["".join(o) for o in options if len(o) == m]

        def numpad(c):
            return genericpad(c, pad2cord, padpaths, pad)

        @cache
        def dp(c, d):
            response = 0
            c = "A" + c
            for i in range(1, len(c)):
                paths = genericpad(c[i], dpad2cord, dpadpaths, dpad, c[i - 1])
                if d == 0:
                    response += min([len(path) for path in paths])
                else:
                    response += min(dp(path, d - 1) for path in paths)
            return response

        def solve_part2(c):
            return min([dp(x, 24) for x in numpad(c)])

        lines = [line.strip() for line in self.input_file.splitlines()]

        total = 0
        for code in lines:
            numeric_code = int("".join(x for x in code if x.isdecimal()))
            size = solve_part2(code)
            total += size * numeric_code

        return total


if __name__ == "__main__":
    solution = Day_21()
    solution.execute_part_one()
    solution.execute_part_two()
