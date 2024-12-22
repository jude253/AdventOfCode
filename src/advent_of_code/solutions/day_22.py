from collections import defaultdict, deque

from advent_of_code.utils.daily_code_utils import Solution


def mix(a, b):
    return a ^ b


def prune(a):
    return a % 16777216


def process(secret_number):
    step1 = prune(mix(secret_number, secret_number * 64))
    step2 = prune(mix(step1, step1 // 32))
    step3 = prune(mix(step2, step2 * 2048))
    return step3


def get_ones(a):
    return a % 10


class Day_22(Solution):
    def part_one(self):
        secret_numbers = [int(line) for line in self.input_file.splitlines()]
        total = 0
        secret_processes = 2_000
        for secret_number in secret_numbers:
            for _ in range(secret_processes):
                secret_number = process(secret_number)
            total += secret_number

        return total

    def part_two(self):
        secret_numbers = [int(line) for line in self.input_file.splitlines()]
        secret_processes = 2_000

        all_sequences = set()
        sequence_value_lookup_list = []
        for secret_number in secret_numbers:
            prev_ones = None
            diff = None
            diffs = deque(maxlen=4)
            sequence_value_lookup = defaultdict(int)
            for _ in range(secret_processes):
                cur_ones = get_ones(secret_number)
                if prev_ones is not None:
                    diff = cur_ones - prev_ones
                    diffs.append(diff)
                diffs_tuple = tuple(diffs)
                if len(diffs_tuple) == 4 and diffs_tuple not in sequence_value_lookup:
                    all_sequences.add(diffs_tuple)
                    sequence_value_lookup[diffs_tuple] = cur_ones
                secret_number = process(secret_number)
                prev_ones = cur_ones
            sequence_value_lookup_list.append(sequence_value_lookup.copy())

        max_bananas = -float("inf")
        for sequence in all_sequences:
            total_bananas = 0
            for sequence_value_lookup in sequence_value_lookup_list:
                total_bananas += sequence_value_lookup[sequence]
            max_bananas = max(total_bananas, max_bananas)
        return max_bananas


if __name__ == "__main__":
    solution = Day_22()
    solution.execute_part_one()
    solution.execute_part_two()
