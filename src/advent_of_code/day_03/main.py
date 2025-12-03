from rich.console import Console

console = Console()


def get_input_file_contents(file_path="input/day_03/input.txt"):
    input_file_contents = None
    with open(file_path) as f:
        input_file_contents = f.read()
    return input_file_contents


def part_one():
    console.log("part_one")
    input_file_contents = get_input_file_contents("input/day_03/input.txt")
    banks = [
        [(int(item), i) for i, item in enumerate(line)]
        for line in input_file_contents.split()
    ]

    top2_list = [sorted(bank, reverse=True)[:2] for bank in banks]
    total = 0

    for bank_index, top2 in enumerate(top2_list):
        largest_2_digit_num = 0
        cur_bank = banks[bank_index]
        largest_num, largest_index = top2[0]
        second_largest_num, second_largest_index = top2[1]

        for i in range(largest_index + 1, len(cur_bank)):
            potential_largest_2_digit_num = int(f"{largest_num}{cur_bank[i][0]}")
            largest_2_digit_num = max(
                potential_largest_2_digit_num, largest_2_digit_num
            )

        for i in range(second_largest_index + 1, len(cur_bank)):
            potential_largest_2_digit_num = int(f"{second_largest_num}{cur_bank[i][0]}")
            largest_2_digit_num = max(
                potential_largest_2_digit_num, largest_2_digit_num
            )

        total += largest_2_digit_num

    console.log(total)


def part_two():
    console.log("part_two")
    input_file_contents = get_input_file_contents("input/day_03/input.txt")

    banks = [line for line in input_file_contents.split()]

    total = 0
    for i, bank in enumerate(banks):
        console.log(i)
        total += get_max_int_greedy_2(bank)
    console.log(total)


def get_max_int_greedy(digits: str, keep: int = 12) -> int:
    """
    **From ChatGPT:**

    Find the maximum number possible by selecting exactly 'keep' digits
    from the input string while maintaining their relative order.

    Greedy Algorithm Explanation:
    ------------------------------
    The key insight is that to maximize the resulting number, we want larger
    digits to appear as early as possible in our result. At each step, we
    greedily pick the largest available digit from a valid "window" of positions.

    The "valid window" is constrained by:
    1. We can't look before our current position (must maintain order)
    2. We can't look too far ahead, or we won't have enough digits left
       to complete our selection

    Example: digits="234234234234278", keep=12 (remove 3)

    Step 1: Need 12 more digits, can search positions 0-3 (leave 12 remaining)
            Window "2342" → max is '4' at index 3
            Pick '4', next start = 4

    Step 2: Need 11 more digits, can search positions 4-4 (leave 11 remaining)
            Window "2" → max is '3' at index 5
            Pick '3', next start = 6

    Step 3: Continue this process...
            Result: "434234234278"

    Why this works:
    ---------------
    By always picking the largest digit available in the valid window, we ensure
    that high-value digits appear as early as possible in the result, which
    maximizes the final number's value.

    Args:
        digits: String of digit characters to select from
        keep: Number of digits to keep in the result

    Returns:
        Integer representing the maximum number possible

    Time Complexity: O(n * keep) where n = len(digits)
    Space Complexity: O(keep) for storing the result
    """
    n = len(digits)
    result = []
    start = 0

    for digits_needed in range(keep, 0, -1):
        # Calculate the valid search window for this iteration
        # We need to leave at least (digits_needed - 1) digits after our choice
        # So the furthest we can look is: n - digits_needed + 1
        end = n - digits_needed + 1

        # Find the maximum digit character in the valid window
        max_digit = max(digits[start:end])

        # Find the first occurrence of this maximum digit in the window
        # We take the first occurrence to leave maximum flexibility for future picks
        for i in range(start, end):
            if digits[i] == max_digit:
                result.append(max_digit)

                # Next iteration must start after this position to maintain order
                start = i + 1
                break

    return int("".join(result))


def get_max_int_greedy_2(digits: str, keep: int = 12) -> int:
    """
    Get the largest number in the range of next numbers that will allow
    still filling all slots.
    """

    digits: list[int] = [int(x) for x in digits]

    len_digits = len(digits)

    max_greed_int_output = []

    current_window_start_index = 0
    current_window_end_index = 0  # Set in loop-- here for clarity.

    while len(max_greed_int_output) < keep:
        # Current window end index is the end of the range of the length
        # of digits minus the current number of digits need to fill
        # max_greed_int_output (+1 b/c not inclusive)
        current_window_end_index = len_digits - (keep - len(max_greed_int_output)) + 1
        current_window = digits[current_window_start_index:current_window_end_index]

        # Get max in current window
        current_window_max = max(current_window)

        # Get index of max in current window in reference to whole digit list
        current_window_max_index = digits.index(
            value=current_window_max,
            start=current_window_start_index,
            stop=current_window_end_index,
        )

        # Add max to max_greed_int_output
        max_greed_int_output.append(current_window_max)

        # Set next current_window_start_index to the index after current
        # max in digits list.
        current_window_start_index = current_window_max_index + 1

    return int("".join([str(x) for x in max_greed_int_output]))


def get_max_int(input_str: str):
    """Use greedy algorithm to find max by keeping 12 digits"""
    return get_max_int_greedy(input_str)


if __name__ == "__main__":
    part_one()
    part_two()
