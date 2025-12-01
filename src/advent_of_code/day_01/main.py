from rich.console import Console

console = Console()

DIAL_START = 50


def get_input_file_contents(file_path="input/day_01/input.txt"):
    input_file_contents = None
    with open(file_path) as f:
        input_file_contents = f.read()
    return input_file_contents


def get_rotated_dial_pointer(dial_pointer: int, rotation: tuple[str, int]) -> int:
    rotation_direction, rotation_amount = rotation
    if rotation_direction == "L":
        rotation_amount *= -1
    return (dial_pointer + rotation_amount) % 100


def part_one():
    console.log("part_one")
    input_file_contents = get_input_file_contents("input/day_01/input.txt")

    dial_pointer = DIAL_START

    rotations = input_file_contents.split()
    rotations = [(item[0], int(item[1:])) for item in rotations]

    zero_count = 0

    for rotation in rotations:
        dial_pointer = get_rotated_dial_pointer(dial_pointer, rotation)
        if dial_pointer == 0:
            zero_count += 1
    console.log(zero_count)


def part_two():
    console.log("part_two")
    input_file_contents = get_input_file_contents("input/day_01/input.txt")

    dial_pointer = DIAL_START

    rotations = input_file_contents.split()
    rotations = [(item[0], int(item[1:])) for item in rotations]

    zero_count = 0

    for rotation in rotations:
        rotation_direction, rotation_amount = rotation

        rotation_one = (rotation_direction, 1)

        while rotation_amount > 0:
            dial_pointer = get_rotated_dial_pointer(dial_pointer, rotation_one)
            if dial_pointer == 0:
                zero_count += 1

            rotation_amount -= 1

    console.log(zero_count)


if __name__ == "__main__":
    part_one()
    part_two()
