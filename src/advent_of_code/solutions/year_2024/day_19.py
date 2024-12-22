from functools import lru_cache

from advent_of_code.utils.daily_code_utils import Solution


def is_possible(cur, display, towels):
    if len(cur) > len(display):
        return False

    if tuple(cur) != display[: len(cur)]:
        return False

    if tuple(cur) == display:
        return True

    for towel in towels:
        next = is_possible(cur + list(towel), display, towels)
        if next is True:
            return True
    return False


def parse_input(input_file_str):
    towels, displays = input_file_str.split("\n\n")
    towels = [tuple(towel) for towel in towels.split(", ")]
    displays = [tuple(display) for display in displays.splitlines()]
    return towels, displays


class Day_19(Solution):
    def part_one(self):
        towels, displays = parse_input(self.input_file)

        total_possible = 0
        for display in displays:
            display_possible = is_possible([], display, towels)
            if display_possible:
                total_possible += 1
        return total_possible

    def part_two(self):
        towels, displays = parse_input(self.input_file)

        @lru_cache(maxsize=2000)
        def num_ways(cur):
            if len(cur) == 0:
                return 1
            total_num_ways = 0
            for towel in towels:
                l_towel = len(towel)
                if towel == cur[-l_towel:]:
                    total_num_ways += num_ways(cur[:-l_towel])

            return total_num_ways

        total_num_ways = 0
        for display in displays:
            total_num_ways += num_ways(display)

        return total_num_ways


if __name__ == "__main__":
    solution = Day_19()
    solution.execute_part_one()
    solution.execute_part_two()
