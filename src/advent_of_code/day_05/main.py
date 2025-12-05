from rich.console import Console

console = Console()


def get_input_file_contents(file_path="input/day_05/input.txt"):
    input_file_contents = None
    with open(file_path) as f:
        input_file_contents = f.read()
    return input_file_contents


def part_one(input_file_contents: str):
    console.log("part_one")
    input_file_contents = input_file_contents.splitlines()
    fresh_id_range_list: list[tuple[int]] = []
    id_list: list[int] = []
    passed_blank_line = False

    for line in input_file_contents:
        if line == "":
            passed_blank_line = True
        elif not passed_blank_line:
            range_ids = line.split("-")
            range_ids = tuple([int(x) for x in range_ids])
            fresh_id_range_list.append(range_ids)
        else:
            id_list.append(int(line))

    # console.log(fresh_id_range)
    # console.log(id_list)

    fresh_ingredient_set = set()
    for ingredient_id in id_list:
        for range_start, range_end in fresh_id_range_list:
            if range_start <= ingredient_id <= range_end:
                fresh_ingredient_set.add(ingredient_id)

    console.log(fresh_ingredient_set)
    console.log(len(fresh_ingredient_set))


def part_two(input_file_contents: str):
    """
    This doesn't work and not sure why.  It gives answer that is "too
    large". Looking at the output ranges, I see that there's some
    ranges that start and end one appart.  Wondering if this could be
    the issue?

    I think I will ask chatGPT later today.
    """
    console.log("part_two")
    input_file_contents = input_file_contents.splitlines()
    to_consolidate_id_range_stack: list[tuple[int]] = []
    passed_blank_line = False

    for line in input_file_contents:
        if line == "":
            passed_blank_line = True
        elif not passed_blank_line:
            range_ids = line.split("-")
            range_ids = tuple(sorted([int(x) for x in range_ids]))
            to_consolidate_id_range_stack.append(range_ids)

    consolidated_id_range_set: set[tuple[int, int]] = set()

    while len(to_consolidate_id_range_stack) > 0:
        cur_range_start, cur_range_end = to_consolidate_id_range_stack.pop(0)
        console.log(cur_range_start, cur_range_end)
        to_consolidated_ranges_step: list = []
        for existing_range in consolidated_id_range_set:
            existing_range_start, existing_range_end = existing_range
            if (existing_range_start <= cur_range_start <= existing_range_end) or (
                existing_range_start <= cur_range_end <= existing_range_end
            ):
                to_consolidated_ranges_step.append(existing_range)

        if len(to_consolidated_ranges_step) > 0:
            for id_range in to_consolidated_ranges_step:
                consolidated_id_range_set.remove(id_range)

            to_consolidated_ranges_step.append((cur_range_start, cur_range_end))
            min_start = min([id_range[0] for id_range in to_consolidated_ranges_step])
            max_end = max([id_range[1] for id_range in to_consolidated_ranges_step])
            to_consolidate_id_range_stack.append((min_start, max_end))
        else:
            consolidated_id_range_set.add((cur_range_start, cur_range_end))

    consolided_id_range_list = list(sorted(consolidated_id_range_set))
    console.log(consolided_id_range_list)

    total_number_of_ids = 0
    for range_start, range_end in consolidated_id_range_set:
        total_number_of_ids += (range_end - range_start) + 1

    console.log(total_number_of_ids)


if __name__ == "__main__":
    input_file_contents = get_input_file_contents(file_path="input/day_05/test.txt")
    input_file_contents = get_input_file_contents(file_path="input/day_05/input.txt")
    part_one(input_file_contents)
    part_two(input_file_contents)
