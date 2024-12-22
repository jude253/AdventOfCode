from advent_of_code.utils.daily_code_utils import Solution


def parse_input(input_file_str):
    n = len(input_file_str)
    str_builder = []
    cur_index = 0
    for i in range(n):
        num = int(input_file_str[i])
        if i % 2 == 0:
            new_str_part = [str(cur_index)] * num
            str_builder.extend(new_str_part)
            cur_index += 1
        else:
            new_str_part = ["."] * num
            str_builder.extend(new_str_part)
    return str_builder


class Day_09(Solution):
    def part_one(self):
        str_builder = parse_input(self.input_file)

        # Loop over and move highest memory to lowest open spot
        i_left, i_right = 0, len(str_builder) - 1
        while i_left < i_right:
            while str_builder[i_left] != ".":
                i_left += 1
            while str_builder[i_right] == ".":
                i_right -= 1
            right = str_builder[i_right]
            left = str_builder[i_left]
            if i_left < i_right:
                str_builder[i_left] = right
                str_builder[i_right] = left
        check_sum = 0
        for i, char in enumerate(str_builder):
            if char == ".":
                break
            check_sum += i * int(char)

        return check_sum

    def part_two(self):
        str_builder = parse_input(self.input_file)
        self.smallest_dot = float("inf")

        def get_block_ends_inclusive_ltr(i_start, str_builder):
            i = i_start
            while i < len(str_builder) and str_builder[i] == str_builder[i_start]:
                i += 1
            return (i_start, i - 1), i - i_start

        def get_block_ends_inclusive_rtl(i_start, str_builder):
            i = i_start
            while i >= 0 and str_builder[i] == str_builder[i_start]:
                i -= 1
            return (i + 1, i_start), i_start - i

        def set_left_block_to_right(bl, bl_size, br, br_size, str_builder):
            if bl[0] == self.smallest_dot:
                self.smallest_dot = float("inf")
            for i in range(br_size):
                str_builder[bl[0] + i] = str_builder[br[0] + i]
                str_builder[br[0] + i] = "."

        seen = set()

        # Loop over and add block of memory to left-most open space, if possible
        # trying at most 1x per block
        i_left, i_right = 0, len(str_builder) - 1
        i_left_prev, i_right_prev = None, None
        while True:
            i_left_prev, i_right_prev = i_left, i_right
            # Find replacement and move right block if possible
            while i_left < i_right:
                while str_builder[i_right] == ".":
                    i_right -= 1
                while str_builder[i_left] != ".":
                    i_left += 1

                # Check if new i_left could be new smallest starting pt to speed
                # up execution time
                if i_left < self.smallest_dot:
                    self.smallest_dot = i_left

                b_left, bl_size = get_block_ends_inclusive_ltr(i_left, str_builder)
                b_right, br_size = get_block_ends_inclusive_rtl(i_right, str_builder)
                right = str_builder[i_right]

                # If seen already, return!
                if right in seen:
                    i_right = b_right[0] - 1
                    break

                if i_left < i_right:
                    if bl_size >= br_size:
                        set_left_block_to_right(
                            b_left, bl_size, b_right, br_size, str_builder
                        )
                        i_right = b_right[0] - 1
                        seen.add(right)
                        break
                else:
                    # Open memory block is higher than right, no place for it
                    i_right = b_right[0] - 1
                    seen.add(right)

                # Move to next left memory block if one can't be found
                i_left += 1

            # Start left from left most address again to get left-most open
            # block to replace
            i_left = self.smallest_dot if self.smallest_dot < len(str_builder) else 0
            if i_left_prev == i_left and i_right == i_right_prev:
                break

        check_sum = 0
        for i, char in enumerate(str_builder):
            if char != ".":
                check_sum += i * int(char)

        return check_sum


if __name__ == "__main__":
    solution = Day_09()
    solution.execute_part_one()
    solution.execute_part_two()
