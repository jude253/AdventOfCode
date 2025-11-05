from rich.console import Console

console = Console()


def get_input_file_contents(file_path="input/day_01/input.txt"):
    input_file_contents = None
    with open(file_path) as f:
        input_file_contents = f.read()
    return input_file_contents


def part_one(input_file_contents: str):
    input_file_lines = input_file_contents.split("\n")

    # console.out(input_file_lines)

    elves_food_carry = []
    cur_elf_food_carry = []
    for line in input_file_lines:
        if line == "":
            elves_food_carry.append(cur_elf_food_carry)
            cur_elf_food_carry = []
        else:
            cur_elf_food_carry.append(int(line))

    elves_total_calories = [sum(elf_food_carry) for elf_food_carry in elves_food_carry]
    # console.print(elves_total_calories)
    console.print(max(elves_total_calories))


def part_two(input_file_contents: str):
    input_file_lines = input_file_contents.split("\n")

    # console.out(input_file_lines)

    elves_food_carry = []
    cur_elf_food_carry = []
    for line in input_file_lines:
        if line == "":
            elves_food_carry.append(cur_elf_food_carry)
            cur_elf_food_carry = []
        else:
            cur_elf_food_carry.append(int(line))

    elves_total_calories = [sum(elf_food_carry) for elf_food_carry in elves_food_carry]
    # console.print(elves_total_calories)
    elves_total_calories.sort(reverse=True)
    console.print(sum(elves_total_calories[:3]))


if __name__ == "__main__":
    input_file_contents = get_input_file_contents()
    console.print("Part 1:")
    part_one(input_file_contents)
    console.print("Part 2:")
    part_two(input_file_contents)
