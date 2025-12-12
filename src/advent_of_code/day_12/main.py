from rich.console import Console

console = Console()


def get_input_file_contents(file_path="input/day_12/input.txt"):
    input_file_contents = None
    with open(file_path) as f:
        input_file_contents = f.read()
    return input_file_contents


def part_one(input_file_contents: str):
    console.log("part_one")
    input_file_contents = input_file_contents.split("\n\n")

    presents = [
        tuple([row for row in line.splitlines() if ":" not in row])
        for line in input_file_contents[:-1]
    ]
    grids = [
        [
            tuple(map(int, part.split("x")))
            if "x" in part
            else list(map(int, part.split()))
            for part in line.split(": ")
        ]
        for line in input_file_contents[-1].splitlines()
    ]

    present_density = [
        sum([sum([char == "#" for char in row]) for row in present])
        for present in presents
    ]
    NO, Maybe, Definitely = range(3)
    results = []
    for grid in grids:
        grid_x, grid_y = grid[0]
        present_counts = grid[1]
        min_space = sum(
            a * b for a, b in zip(present_counts, present_density, strict=True)
        )
        total_presents = sum(present_counts)
        if min_space > grid_x * grid_y:
            results.append(NO)
        elif total_presents <= (grid_x // 3) * (grid_y // 3):
            results.append(Definitely)
        else:
            results.append(Maybe)

    console.log(f"{results.count(NO)=}")
    console.log(f"{results.count(Definitely)=}")
    console.log(f"{results.count(Maybe)=}")


if __name__ == "__main__":
    input_file_contents = get_input_file_contents(file_path="input/day_12/test.txt")
    input_file_contents = get_input_file_contents(file_path="input/day_12/input.txt")
    part_one(input_file_contents)
