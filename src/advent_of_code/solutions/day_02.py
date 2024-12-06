import logging

from advent_of_code.utils.daily_code_utils import Solution

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

GOOD_DIFFERENCES = (1, 2, 3)


def parse_input(input_file_str):
    lines = input_file_str.split("\n")
    reports = [[int(x) for x in line.split()] for line in lines]
    return reports


def is_safe_decreasing(levels):
    i = 1
    while i < len(levels):
        prev = levels[i - 1]
        cur = levels[i]
        if prev - cur not in GOOD_DIFFERENCES:
            return False
        else:
            i += 1
    return True


def is_safe_decreasing_with_tolerance(levels_orig):
    levels = levels_orig[:]
    i = 1
    while i < len(levels):
        prev = levels[i - 1]
        cur = levels[i]
        if prev - cur not in GOOD_DIFFERENCES:
            safe_pop_cur = is_safe_decreasing(levels[:i] + levels[i + 1 :])
            safe_pop_prev = is_safe_decreasing(levels[: i - 1] + levels[i:])
            return safe_pop_cur or safe_pop_prev
        i += 1
    return True


class Day_02(Solution):
    def part_one(self):
        reports = parse_input(self.input_file)
        safe_count = 0
        for levels in reports:
            if is_safe_decreasing(levels) or is_safe_decreasing(levels[::-1]):
                safe_count += 1
        return safe_count

    def part_two(self):
        reports = parse_input(self.input_file)
        safe_count = 0
        for levels in reports:
            safe_forwards = False
            safe_reverse = False
            safe_forwards = is_safe_decreasing_with_tolerance(levels)
            safe_reverse = is_safe_decreasing_with_tolerance(levels[::-1])
            if safe_forwards or safe_reverse:
                safe_count += 1
        return safe_count


if __name__ == "__main__":
    solution = Day_02()
    logger.info(f"Part 1: {solution.part_one()}")
    logger.info(f"Part 2: {solution.part_two()}")
