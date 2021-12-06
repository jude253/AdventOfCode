import logging

from advent_of_code.utils.daily_code_utils import Solution

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class Day_14(Solution):
    def part_one(self):
        print(self.input_file)
        return

    def part_two(self):
        return


if __name__ == "__main__":
    solution = Day_14()
    logger.info(f"Part 1: {solution.part_one()}")
    logger.info(f"Part 2: {solution.part_two()}")
