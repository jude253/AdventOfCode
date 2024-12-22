from collections import defaultdict

from advent_of_code.utils.daily_code_utils import Solution


def parse_input(input_file_str):
    lines = input_file_str.split("\n")
    pages_after_lookup = defaultdict(set)
    page_orderings = []
    for line in lines:
        if "|" in line:
            before, after = line.split("|")
            pages_after_lookup[before].add(after)
        elif len(line) != 0:
            page_orderings.append(line.split(","))
    return pages_after_lookup, page_orderings


def get_page_ordering_correct(page_ordering, pages_after_lookup):
    for i in range(len(page_ordering)):
        prev_page_nums, cur_page_num = page_ordering[:i], page_ordering[i]
        for prev_page_num in prev_page_nums:
            if prev_page_num in pages_after_lookup[cur_page_num]:
                return False
    return True


def get_middle_page_num(page_ordering):
    """
    Q: What to do if input has even # of elements?

    A: Looks like none of the input has even # of elements.
    """
    n = len(page_ordering)
    return int(page_ordering[n // 2])


def get_corrected_page_orderings(incorrect_page_orderings, pages_after_lookup):
    """
    Bubble-sort kind of approach.  This hinges on there only being one
    correct answer for each page_ordering and not doing some sort of
    optimal re-ordering with the least number of swaps or something.
    """
    corrected_page_orderings = []
    for page_ordering in incorrect_page_orderings:
        new_page_ordefing = page_ordering[:]
        cur_page_i = 0
        while cur_page_i < len(new_page_ordefing):
            page_order_corrected_in_pass = False
            prev_page_nums, cur_page_num = (
                new_page_ordefing[:cur_page_i],
                new_page_ordefing[cur_page_i],
            )
            for prev_page_i, prev_page_num in enumerate(prev_page_nums):
                if prev_page_num in pages_after_lookup[cur_page_num]:
                    new_page_ordefing[cur_page_i] = prev_page_num
                    new_page_ordefing[prev_page_i] = cur_page_num
                    cur_page_i = 0
                    page_order_corrected_in_pass = True
                    break
            if not page_order_corrected_in_pass:
                cur_page_i += 1
        corrected_page_orderings.append(new_page_ordefing)
    return corrected_page_orderings


class Day_05(Solution):
    def part_one(self):
        pages_after_lookup, page_orderings = parse_input(self.input_file)
        middle_page_sum = 0
        for page_ordering in page_orderings:
            page_ordering_correct = get_page_ordering_correct(
                page_ordering, pages_after_lookup
            )
            if page_ordering_correct:
                middle_page_sum += get_middle_page_num(page_ordering)
        return middle_page_sum

    def part_two(self):
        pages_after_lookup, page_orderings = parse_input(self.input_file)
        incorrect_page_orderings = []
        for page_ordering in page_orderings:
            page_ordering_correct = get_page_ordering_correct(
                page_ordering, pages_after_lookup
            )
            if not page_ordering_correct:
                incorrect_page_orderings.append(page_ordering)

        corrected_page_orderings = get_corrected_page_orderings(
            incorrect_page_orderings, pages_after_lookup
        )
        corrected_middle_page_sum = 0
        for page_ordering in corrected_page_orderings:
            corrected_middle_page_sum += get_middle_page_num(page_ordering)
        return corrected_middle_page_sum


if __name__ == "__main__":
    solution = Day_05()
    solution.execute_part_one()
    solution.execute_part_two()
