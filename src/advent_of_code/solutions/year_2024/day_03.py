from advent_of_code.utils.daily_code_utils import Solution


def get_mul_args_list_list(mul_args_str_list):
    mul_args_list_list = []
    for mul_args_str in mul_args_str_list:
        lparen_ind = mul_args_str.find("(")
        comma_ind = mul_args_str.find(",")
        rparen_ind = mul_args_str.find(")")
        if lparen_ind == 0 and lparen_ind < comma_ind < rparen_ind:
            mul_args_str = mul_args_str[lparen_ind + 1 : rparen_ind]
            mul_args_list = mul_args_str.split(",")
            if len(mul_args_list) != 2:
                continue
            if not (mul_args_list[0].isnumeric() and mul_args_list[1].isnumeric()):
                continue
            if not (
                len(mul_args_list[0]) in (1, 2, 3)
                and len(mul_args_list[1]) in (1, 2, 3)
            ):
                continue
            mul_args = [int(num) for num in mul_args_list]
            mul_args_list_list.append(mul_args)
    return mul_args_list_list


class Day_03(Solution):
    def part_one(self):
        mul_args_str_list = self.input_file.split("mul")[1:]
        total = 0
        mul_args_list_list = get_mul_args_list_list(mul_args_str_list)
        for mul_args_list in mul_args_list_list:
            total += mul_args_list[0] * mul_args_list[1]
        return total

    def part_two(self):
        do_str_list = self.input_file.split("do()")
        do_str_list = [x.split("don't")[0] for x in do_str_list]
        do_str = "".join(do_str_list)
        mul_args_str_list = do_str.split("mul")[1:]
        total = 0
        mul_args_list_list = get_mul_args_list_list(mul_args_str_list)
        for mul_args_list in mul_args_list_list:
            total += mul_args_list[0] * mul_args_list[1]
        return total


if __name__ == "__main__":
    solution = Day_03()
    solution.execute_part_one()
    solution.execute_part_two()
