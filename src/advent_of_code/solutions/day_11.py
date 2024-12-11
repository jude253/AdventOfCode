from collections import defaultdict

from advent_of_code.utils.daily_code_utils import Solution


def process_stone(stone):
    str_stone = str(stone)
    len_stone = len(str_stone)
    if stone == 0:
        return [1]
    elif len_stone % 2 == 0:
        half = len(str_stone) // 2
        stone1, stone2 = int(str_stone[:half]), int(str_stone[half:])
        return [stone1, stone2]
    else:
        return [stone * 2024]


def blink(stones_map):
    new_stones_map = defaultdict(int)
    for stone, count in stones_map.items():
        new_stones = process_stone(stone)
        for new_stone in new_stones:
            new_stones_map[new_stone] += count
    return new_stones_map


class Day_11(Solution):
    def part_one(self):
        stones_map = defaultdict(int)
        for stone in self.input_file.split():
            stones_map[int(stone)] += 1
        for _ in range(25):
            stones_map = blink(stones_map)
        return sum(list(stones_map.values()))

    def part_two(self):
        stones_map = defaultdict(int)
        for stone in self.input_file.split():
            stones_map[int(stone)] += 1
        for _ in range(75):
            stones_map = blink(stones_map)
        return sum(list(stones_map.values()))


if __name__ == "__main__":
    solution = Day_11()
    solution.execute_part_one()
    solution.execute_part_two()
