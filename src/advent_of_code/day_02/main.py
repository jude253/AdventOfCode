from rich.console import Console

console = Console()


def get_input_file_contents(file_path="input/day_02/input.txt"):
    input_file_contents = None
    with open(file_path) as f:
        input_file_contents = f.read()
    return input_file_contents


def part_one_invalid_id(id: int) -> bool:
    str_id = str(id)
    half_len = len(str_id) // 2
    return str_id[:half_len] == str_id[half_len:]


def part_one():
    console.log("part_one")
    input_file_contents = get_input_file_contents("input/day_02/input.txt")
    invalid_id_ranges = "".join(input_file_contents.split()).split(",")
    invalid_id_ranges = [
        (int(item.split("-")[0]), int(item.split("-")[1])) for item in invalid_id_ranges
    ]
    invalid_id_sum = 0
    for invalid_id_range in invalid_id_ranges:
        start, end = invalid_id_range
        for invalid_id in range(start, end + 1):
            if part_one_invalid_id(invalid_id):
                invalid_id_sum += invalid_id

    console.log(invalid_id_sum)


def part_two_invalid_id(id: int) -> bool:
    str_id = str(id)
    # Check every possible sequence length from 1 up to half the string length.
    # A valid repeating pattern must divide the total length and repeat at least twice.
    n = len(str_id)
    for seq_len in range(1, n // 2 + 1):
        if n % seq_len != 0:
            continue
        repeat_count = n // seq_len
        if repeat_count < 2:
            continue
        seq = str_id[:seq_len]
        if seq * repeat_count == str_id:
            return True
    return False


def part_two_invalid_id_readible(id: int) -> bool:
    str_id = str(id)
    # Check every possible sequence length from 1 up to half the string length.
    # A valid repeating pattern must divide the total length and repeat at least twice.
    str_len = len(str_id)
    for compare_str_len in range(1, str_len):
        if str_len % compare_str_len == 0:
            substr_set = set()
            for substr_start_index in range(0, str_len, compare_str_len):
                substr_end_index = substr_start_index + compare_str_len
                substr = str_id[substr_start_index:substr_end_index]
                substr_set.add(substr)

                # Speed up by exiting early if already not repeating.
                if len(substr_set) > 1:
                    break

            # Ensure all substrs are the same b/c set size is exactly 1.
            if len(substr_set) == 1:
                return True
    return False


def part_two():
    console.log("part_two")
    input_file_contents = get_input_file_contents("input/day_02/input.txt")
    invalid_id_ranges = "".join(input_file_contents.split()).split(",")
    invalid_id_ranges = [
        (int(item.split("-")[0]), int(item.split("-")[1])) for item in invalid_id_ranges
    ]
    invalid_id_sum = 0
    for invalid_id_range in invalid_id_ranges:
        start, end = invalid_id_range
        for invalid_id in range(start, end + 1):
            if part_two_invalid_id_readible(invalid_id):
                invalid_id_sum += invalid_id

    console.log(invalid_id_sum)


if __name__ == "__main__":
    part_one()
    part_two()
