import logging

from advent_of_code.utils.daily_code_utils import Solution

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


OPERATORS = ['||', '*', '+']


class Day_07(Solution):
    def part_one(self):
        lines = self.input_file.split('\n')
        answer_list = []
        operands_list = []
        for line in lines:
            s = line.split(':')
            answer_list.append(int(s[0]))
            operands_list.append([int(x) for x in s[1].split()])
        total_sum = 0
        for answer, operands in zip(answer_list, operands_list):
            stack = [(0, operands[0])]
            while stack:
                cur_index, cur_total = stack.pop()
                if cur_index < len(operands) - 1:
                    next_index = cur_index + 1
                    next_val = operands[next_index]
                    for operator in OPERATORS:
                        if operator == '+':
                            stack.append((next_index, cur_total+next_val))
                        if operator == '*':
                            stack.append((next_index, cur_total*next_val))
                elif cur_index == len(operands) - 1 and cur_total == answer:
                    total_sum += answer
                    break
        return total_sum

    def part_two(self):
        lines = self.input_file.split('\n')
        answer_list = []
        operands_list = []
        for line in lines:
            s = line.split(':')
            answer_list.append(int(s[0]))
            operands_list.append([int(x) for x in s[1].split()])
        total_sum = 0
        for answer, operands in zip(answer_list, operands_list):
            stack = [(0, operands[0])]
            while stack:
                cur_index, cur_total = stack.pop()
                if cur_index < len(operands) - 1:
                    next_index = cur_index + 1
                    next_val = operands[next_index]
                    for operator in OPERATORS:
                        if operator == '||':
                            stack.append((next_index, int(str(cur_total)+str(next_val))))
                        if operator == '+':
                            stack.append((next_index, cur_total+next_val))
                        if operator == '*':
                            stack.append((next_index, cur_total*next_val))
                elif cur_index == len(operands) - 1 and cur_total == answer:
                    total_sum += answer
                    break

        return total_sum


if __name__ == "__main__":
    solution = Day_07()
    logger.info(f"Part 1: {solution.part_one()}")
    logger.info(f"Part 2: {solution.part_two()}")
