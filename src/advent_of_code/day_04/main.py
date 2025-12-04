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


def get_input_file_contents(file_path="input/day_04/input.txt"):
    input_file_contents = None
    with open(file_path) as f:
        input_file_contents = f.read()
    return input_file_contents


def in_grid(grid: list[list[str]], vector: tuple[int, int]):
    return -1 < vector[0] < len(grid) and -1 < vector[1] < len(grid[0])


def part_one(input_file_contents: str):
    console.log("part_one")
    grid = [list(line) for line in input_file_contents.split()]

    can_be_accessed_by_forklift_count = 0

    for row_index in range(len(grid)):
        for col_index in range(len(grid[0])):
            cur_vector = (row_index, col_index)

            if grid[cur_vector[0]][cur_vector[1]] != "@":
                continue

            surrounding_positions_have_paper_count = 0

            for d in ALL_DIRECTIONS:
                cur_surrounding_point = add_vectors(cur_vector, d)

                if (
                    in_grid(grid, cur_surrounding_point)
                    and grid[cur_surrounding_point[0]][cur_surrounding_point[1]] == "@"
                ):
                    surrounding_positions_have_paper_count += 1

            if surrounding_positions_have_paper_count < 4:
                can_be_accessed_by_forklift_count += 1

    console.log(can_be_accessed_by_forklift_count)


def count_number_of_accessible_rolls(grid: list[list[str]]):
    can_be_accessed_by_forklift_count = 0
    points_that_can_be_accessed_by_forklift = list()

    for row_index in range(len(grid)):
        for col_index in range(len(grid[0])):
            cur_vector = (row_index, col_index)

            if grid[cur_vector[0]][cur_vector[1]] != "@":
                continue

            surrounding_positions_have_paper_count = 0

            for d in ALL_DIRECTIONS:
                cur_surrounding_point = add_vectors(cur_vector, d)

                if (
                    in_grid(grid, cur_surrounding_point)
                    and grid[cur_surrounding_point[0]][cur_surrounding_point[1]] == "@"
                ):
                    surrounding_positions_have_paper_count += 1

            if surrounding_positions_have_paper_count < 4:
                points_that_can_be_accessed_by_forklift.append(cur_vector)
                can_be_accessed_by_forklift_count += 1

    for cur_vector in points_that_can_be_accessed_by_forklift:
        grid[cur_vector[0]][cur_vector[1]] = "x"

    return can_be_accessed_by_forklift_count


def clear_x_from_grid(grid: list[list[str]]):
    for row_index in range(len(grid)):
        for col_index in range(len(grid[0])):
            if grid[row_index][col_index].lower() == "x":
                grid[row_index][col_index] = "."


def print_grid(grid: list[list[str]]):
    for line in grid:
        console.log("".join(line))
    console.log("")


def part_two(input_file_contents: str):
    console.log("part_two")
    grid = [list(line) for line in input_file_contents.split()]
    can_be_accessed_by_forklift_count = 0
    can_be_accessed_by_forklift_count_step = None

    # console.log("Initial state:")
    # print_grid(grid)

    while can_be_accessed_by_forklift_count_step != 0:
        can_be_accessed_by_forklift_count_step = count_number_of_accessible_rolls(grid)
        can_be_accessed_by_forklift_count += can_be_accessed_by_forklift_count_step
        # console.log(
        #     f"Remove {can_be_accessed_by_forklift_count_step} rolls of paper:"
        # )

        # print_grid(grid)
        # clear_x_from_grid(grid)

    console.log(can_be_accessed_by_forklift_count)


if __name__ == "__main__":
    input_file_contents = get_input_file_contents(file_path="input/day_04/test.txt")
    input_file_contents = get_input_file_contents(file_path="input/day_04/input.txt")
    part_one(input_file_contents)
    part_two(input_file_contents)
