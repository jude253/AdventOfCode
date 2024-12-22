from collections import OrderedDict, defaultdict, deque

from advent_of_code.utils.daily_code_utils import Solution
from advent_of_code.utils.grid import CLOCKWISE_DIRS, Grid


def get_min_honest_dist(start_ind, end_ind, grid):
    queue = deque([start_ind])
    cur_dist = 0
    seen_honest = OrderedDict()
    seen_honest[start_ind] = cur_dist
    while queue:
        nodes_at_cur_dist = len(queue)
        for _ in range(nodes_at_cur_dist):
            cur_row, cur_col = queue.popleft()
            if (cur_row, cur_col) == end_ind:
                return cur_dist, seen_honest
            for d in CLOCKWISE_DIRS:
                new_row, new_col = cur_row + d[0], cur_col + d[1]
                if not grid.is_inbounds(new_row, new_col):
                    continue
                new_val = grid.get_node_val(new_row, new_col)

                if (new_row, new_col) not in seen_honest and (new_val != "#"):
                    seen_honest[(new_row, new_col)] = cur_dist + 1
                    queue.append((new_row, new_col))
        cur_dist += 1


def get_dists_from_end(end_ind, grid):
    queue = deque([end_ind])
    cur_dist = 0
    dists_from_end = {}
    dists_from_end[end_ind] = cur_dist
    while queue:
        nodes_at_cur_dist = len(queue)
        for _ in range(nodes_at_cur_dist):
            cur_row, cur_col = queue.popleft()
            dists_from_end[(cur_row, cur_col)] = cur_dist
            for d in CLOCKWISE_DIRS:
                new_row, new_col = cur_row + d[0], cur_col + d[1]
                if not grid.is_inbounds(new_row, new_col):
                    continue
                new_val = grid.get_node_val(new_row, new_col)

                if (new_row, new_col) not in dists_from_end and (new_val != "#"):
                    queue.append((new_row, new_col))
        cur_dist += 1
    return dists_from_end


def get_cheats_from_start_location(start_ind, grid, max_cheat_picoseconds):
    queue = deque([(start_ind, 0)])
    seen = set([(start_ind)])
    cheats_from_location = dict()
    while queue:
        num_nodes_in_count = len(queue)
        for _ in range(num_nodes_in_count):
            cur_ind, cur_path_len = queue.popleft()
            cur_val = grid.get_node_val(*cur_ind)
            if cur_val != "#":
                if (start_ind, cur_ind) not in cheats_from_location:
                    cheats_from_location[(start_ind, cur_ind)] = cur_path_len
                else:
                    cheats_from_location[(start_ind, cur_ind)] = min(
                        cheats_from_location[(start_ind, cur_ind)], cur_path_len
                    )
            for d in CLOCKWISE_DIRS:
                new_row, new_col = cur_ind[0] + d[0], cur_ind[1] + d[1]
                new_path_len = cur_path_len + 1
                if (
                    grid.is_inbounds(new_row, new_col)
                    and ((new_row, new_col)) not in seen
                    and new_path_len <= max_cheat_picoseconds
                ):
                    seen.add((new_row, new_col))
                    queue.append(((new_row, new_col), new_path_len))

    return cheats_from_location


class Day_20(Solution):
    def part_one(self):
        grid = Grid(self.input_file)
        for row, col in grid.nodes_indicies():
            if grid.get_node_val(row, col) == "S":
                start_ind = (row, col)
            if grid.get_node_val(row, col) == "E":
                end_ind = (row, col)
        max_cheat_picoseconds = 2
        dists_from_end = get_dists_from_end(end_ind, grid)
        min_honest_dist, seen_honest = get_min_honest_dist(start_ind, end_ind, grid)
        cheat_dists = defaultdict(int)
        used_cheats = set()
        for cur_ind, cur_dist in seen_honest.items():
            cheats = get_cheats_from_start_location(
                cur_ind, grid, max_cheat_picoseconds
            )
            for (s, e), d in cheats.items():
                if (s, e) in used_cheats:
                    continue
                min_dist_to_end = dists_from_end[e]
                total_dist = min_dist_to_end + cur_dist + d
                cheat_dists[min_honest_dist - total_dist] += 1
            used_cheats.update(set(cheats.keys()))

        cheats_save_100_pico_seconds = 0

        for saved_picoseconds, count in sorted(
            cheat_dists.items(), key=lambda x: x[0], reverse=False
        ):
            if saved_picoseconds >= 100:
                cheats_save_100_pico_seconds += count

        return cheats_save_100_pico_seconds

    def part_two(self):
        grid = Grid(self.input_file)
        for row, col in grid.nodes_indicies():
            if grid.get_node_val(row, col) == "S":
                start_ind = (row, col)
            if grid.get_node_val(row, col) == "E":
                end_ind = (row, col)

        dists_from_end = get_dists_from_end(end_ind, grid)
        min_honest_dist, seen_honest = get_min_honest_dist(start_ind, end_ind, grid)
        max_cheat_picoseconds = 20
        cheat_dists = defaultdict(int)
        used_cheats = set()
        for cur_ind, cur_dist in seen_honest.items():
            cheats = get_cheats_from_start_location(
                cur_ind, grid, max_cheat_picoseconds
            )
            for (s, e), d in cheats.items():
                if (s, e) in used_cheats:
                    continue
                min_dist_to_end = dists_from_end[e]
                total_dist = min_dist_to_end + cur_dist + d
                cheat_dists[min_honest_dist - total_dist] += 1
            used_cheats.update(set(cheats.keys()))

        cheats_save_100_pico_seconds = 0

        for saved_picoseconds, count in sorted(
            cheat_dists.items(), key=lambda x: x[0], reverse=False
        ):
            if saved_picoseconds >= 100:
                cheats_save_100_pico_seconds += count

        return cheats_save_100_pico_seconds


if __name__ == "__main__":
    solution = Day_20()
    solution.execute_part_one()
    solution.execute_part_two()
