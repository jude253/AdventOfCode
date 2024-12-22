from collections import deque

from advent_of_code.utils.daily_code_utils import Solution
from advent_of_code.utils.grid import CLOCKWISE_DIRS, Grid


def is_valid(row, col, grid):
    return grid.get_node_val(row, col) != "#"


class Day_16(Solution):
    def part_one(self):
        grid = Grid(self.input_file)
        grid.print()

        start_ind = None
        start_dir = 1
        for row, col in grid.nodes_indicies():
            if grid.get_node_val(row, col) == "S":
                start_ind = (row, col)

        min_score = float("inf")
        overall_seen = {}
        queue = deque([(start_ind[0], start_ind[1], start_dir, 0)])

        while queue:
            cur_row, cur_col, cur_dir_ind, cur_score = queue.popleft()
            overall_seen[(cur_row, cur_col, cur_dir_ind)] = min(
                cur_score,
                overall_seen.get((cur_row, cur_col, cur_dir_ind), float("inf")),
            )
            if grid.get_node_val(cur_row, cur_col) == "E":
                min_score = min(min_score, cur_score)

            next_row_straight = cur_row + CLOCKWISE_DIRS[cur_dir_ind][0]
            next_col_straight = cur_col + CLOCKWISE_DIRS[cur_dir_ind][1]
            next_score_straight = cur_score + 1
            if is_valid(
                next_row_straight, next_col_straight, grid
            ) and next_score_straight < overall_seen.get(
                (next_row_straight, next_col_straight, cur_dir_ind), float("inf")
            ):
                overall_seen[(next_row_straight, next_col_straight, cur_dir_ind)] = (
                    next_score_straight
                )
                queue.append(
                    (
                        next_row_straight,
                        next_col_straight,
                        cur_dir_ind,
                        next_score_straight,
                    )
                )

            for turn_dir_ind in (
                (cur_dir_ind + 1) % len(CLOCKWISE_DIRS),
                (cur_dir_ind - 1) % len(CLOCKWISE_DIRS),
            ):
                next_row_turn = cur_row + CLOCKWISE_DIRS[turn_dir_ind][0]
                next_col_turn = cur_col + CLOCKWISE_DIRS[turn_dir_ind][1]
                next_score_turn = cur_score + 1001
                if is_valid(
                    next_row_turn, next_col_turn, grid
                ) and next_score_turn < overall_seen.get(
                    (next_row_turn, next_col_turn, turn_dir_ind), float("inf")
                ):
                    overall_seen[(next_row_turn, next_col_turn, turn_dir_ind)] = (
                        next_score_turn
                    )
                    queue.append(
                        (next_row_turn, next_col_turn, turn_dir_ind, next_score_turn)
                    )

        return min_score

    def part_two(self):
        grid = Grid(self.input_file)
        grid.print()

        start_ind = None
        start_dir = 1
        for row, col in grid.nodes_indicies():
            if grid.get_node_val(row, col) == "S":
                start_ind = (row, col)

        min_score = float("inf")
        overall_seen = {}
        queue = deque([(start_ind[0], start_ind[1], start_dir, 0, set())])

        nodes_seen_by_score = {}

        while queue:
            cur_row, cur_col, cur_dir_ind, cur_score, path_seen = queue.popleft()
            path_seen.add((cur_row, cur_col))
            overall_seen[(cur_row, cur_col, cur_dir_ind)] = min(
                cur_score,
                overall_seen.get((cur_row, cur_col, cur_dir_ind), float("inf")),
            )

            if grid.get_node_val(cur_row, cur_col) == "E":
                nodes_seen_by_score[cur_score] = path_seen.union(
                    nodes_seen_by_score.get(cur_score, set())
                )
                min_score = min(min_score, cur_score)

            next_row_straight = cur_row + CLOCKWISE_DIRS[cur_dir_ind][0]
            next_col_straight = cur_col + CLOCKWISE_DIRS[cur_dir_ind][1]
            next_score_straight = cur_score + 1
            if is_valid(
                next_row_straight, next_col_straight, grid
            ) and next_score_straight <= overall_seen.get(
                (next_row_straight, next_col_straight, cur_dir_ind), float("inf")
            ):
                new_path_seen = path_seen.copy()
                overall_seen[(next_row_straight, next_col_straight, cur_dir_ind)] = (
                    next_score_straight
                )
                queue.append(
                    (
                        next_row_straight,
                        next_col_straight,
                        cur_dir_ind,
                        next_score_straight,
                        new_path_seen,
                    )
                )

            for turn_dir_ind in (
                (cur_dir_ind + 1) % len(CLOCKWISE_DIRS),
                (cur_dir_ind - 1) % len(CLOCKWISE_DIRS),
            ):
                next_row_turn = cur_row + CLOCKWISE_DIRS[turn_dir_ind][0]
                next_col_turn = cur_col + CLOCKWISE_DIRS[turn_dir_ind][1]
                next_score_turn = cur_score + 1001
                if is_valid(
                    next_row_turn, next_col_turn, grid
                ) and next_score_turn <= overall_seen.get(
                    (next_row_turn, next_col_turn, turn_dir_ind), float("inf")
                ):
                    new_path_seen = path_seen.copy()
                    overall_seen[(next_row_turn, next_col_turn, turn_dir_ind)] = (
                        next_score_turn
                    )
                    queue.append(
                        (
                            next_row_turn,
                            next_col_turn,
                            turn_dir_ind,
                            next_score_turn,
                            new_path_seen,
                        )
                    )

        return len(nodes_seen_by_score[min_score])


if __name__ == "__main__":
    solution = Day_16()
    solution.execute_part_one()
    solution.execute_part_two()
