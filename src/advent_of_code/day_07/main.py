from rich.console import Console

console = Console()


def add_vectors(vector1: tuple[int, int], vector2: tuple[int, int]):
    return (vector1[0] + vector2[0], vector1[1] + vector2[1])


UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)
UP_LEFT = add_vectors(UP, LEFT)
UP_RIGHT = add_vectors(UP, RIGHT)
DOWN_LEFT = add_vectors(DOWN, LEFT)
DOWN_RIGHT = add_vectors(DOWN, RIGHT)

ALL_DIRECTIONS = [
    UP,
    DOWN,
    LEFT,
    RIGHT,
    UP_LEFT,
    UP_RIGHT,
    DOWN_LEFT,
    DOWN_RIGHT,
]


def get_input_file_contents(file_path="input/day_07/input.txt"):
    input_file_contents = None
    with open(file_path) as f:
        input_file_contents = f.read()
    return input_file_contents


def part_one(input_file_contents: str):
    console.log("part_one")
    input_file_contents = input_file_contents.splitlines()
    grid = [list(line) for line in input_file_contents]
    # console.log(grid)

    num_rows, num_cols = len(grid), len(grid[0])
    start_vector = (0, 0)
    for row_ind in range(num_rows):
        for col_ind in range(num_cols):
            if grid[row_ind][col_ind] == "S":
                start_vector = (row_ind, col_ind)

    cur_row = start_vector[0]
    seen_set = set()
    points_to_update = [start_vector]
    split_count = 0
    while cur_row < num_rows - 1:
        cur_points_to_update = points_to_update.copy()
        points_to_update.clear()

        while cur_points_to_update:
            point = cur_points_to_update.pop()
            potential_new_point = add_vectors(point, DOWN)
            potential_new_point_value = grid[potential_new_point[0]][
                potential_new_point[1]
            ]
            if potential_new_point_value == ".":
                grid[potential_new_point[0]][potential_new_point[1]] = "|"
                if potential_new_point not in seen_set:
                    points_to_update.append(potential_new_point)
                    seen_set.add(potential_new_point)
            elif potential_new_point_value == "^":
                split_count += 1
                new_point_left = add_vectors(point, LEFT)
                new_point_right = add_vectors(point, RIGHT)
                if new_point_left not in seen_set:
                    cur_points_to_update.append(new_point_left)
                    seen_set.add(new_point_left)
                if new_point_right not in seen_set:
                    cur_points_to_update.append(new_point_right)
                    seen_set.add(new_point_right)

        # console.log(grid)

        cur_row += 1

    console.log(split_count)


def part_two(input_file_contents: str):
    """
    Count unique timelines using dynamic programming.

    Key insight: We don't need to track full paths, just count how many
    timelines reach each column at each row. When a particle hits a splitter,
    the timeline count doubles (one goes left, one goes right).
    """
    console.log("part_two")
    input_file_contents = input_file_contents.splitlines()
    grid = [list(line) for line in input_file_contents]

    num_rows, num_cols = len(grid), len(grid[0])
    start_vector = (0, 0)
    for row_ind in range(num_rows):
        for col_ind in range(num_cols):
            if grid[row_ind][col_ind] == "S":
                start_vector = (row_ind, col_ind)

    # Track timeline counts per column position
    # Key: (row, col), Value: number of timelines at that position
    current_positions = {start_vector: 1}

    cur_row = start_vector[0]

    while cur_row < num_rows - 1:
        next_positions = {}

        for (row, col), timeline_count in current_positions.items():
            # Move down
            next_row = row + 1
            next_col = col

            cell_value = grid[next_row][next_col]

            if cell_value in (".", "|", "S"):
                # Continue straight - add timeline count to this position
                key = (next_row, next_col)
                next_positions[key] = next_positions.get(key, 0) + timeline_count

            elif cell_value == "^":
                # Split: go down-left and down-right
                # Each timeline that hits the splitter creates 2 timelines

                # Down-left
                left_pos = (next_row, next_col - 1)
                next_positions[left_pos] = (
                    next_positions.get(left_pos, 0) + timeline_count
                )

                # Down-right
                right_pos = (next_row, next_col + 1)
                next_positions[right_pos] = (
                    next_positions.get(right_pos, 0) + timeline_count
                )

        current_positions = next_positions
        cur_row += 1

    # Total number of timelines is the sum of all timeline counts
    total_timelines = sum(current_positions.values())
    console.log(f"Total timelines: {total_timelines}")


if __name__ == "__main__":
    input_file_contents = get_input_file_contents(file_path="input/day_07/test.txt")
    input_file_contents = get_input_file_contents(file_path="input/day_07/input.txt")
    # part_one(input_file_contents)
    part_two(input_file_contents)
