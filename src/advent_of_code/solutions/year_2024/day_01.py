import heapq
from collections import Counter, defaultdict

from advent_of_code.utils.daily_code_utils import Solution


def parse_input(input_file_str):
    input_lines = input_file_str.split("\n")
    input_lines = [[int(x) for x in line.split()] for line in input_lines]
    left = [line[0] for line in input_lines]
    right = [line[1] for line in input_lines]
    return left, right


class Day_01(Solution):
    def part_one(self):
        left, right = parse_input(self.input_file)
        n = len(left)

        heapq.heapify(left)
        heapq.heapify(right)

        running_sum = 0
        for _ in range(n):
            left_min, right_min = heapq.heappop(left), heapq.heappop(right)
            running_sum += abs(left_min - right_min)
        return running_sum

    def part_two(self):
        left, right = parse_input(self.input_file)

        similarity_score = 0
        right_counts = defaultdict(int, Counter(right))
        for element in left:
            similarity_score += element * right_counts[element]

        return similarity_score


if __name__ == "__main__":
    solution = Day_01()
    solution.execute_part_one()
    solution.execute_part_two()
