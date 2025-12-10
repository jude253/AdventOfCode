from rich.console import Console

console = Console()


def get_input_file_contents(file_path="input/day_06/input.txt"):
    input_file_contents = None
    with open(file_path) as f:
        input_file_contents = f.read()
    return input_file_contents


def part_one(input_file_contents: str):
    console.log("part_one")
    input_file_contents = input_file_contents.splitlines()
    input_file_contents = [line.split() for line in input_file_contents]

    number_rows = []
    operation_row = []
    for i, line in enumerate(input_file_contents):
        if i < len(input_file_contents) - 1:
            number_rows.append([int(x) for x in line])
        else:
            operation_row.extend(line)

    # console.log(number_rows)
    # console.log(operation_row)

    total = 0
    for i, operation in enumerate(operation_row):
        subtotal = 0

        operands = [row[i] for row in number_rows]

        if operation == "*":
            subtotal = 1
            for operand in operands:
                subtotal *= operand
        elif operation == "+":
            subtotal = sum(operands)

        # console.log((i, operands, subtotal))
        total += subtotal

    console.log(total)


def part_two(input_file_contents: str):
    console.log("part_two")
    input_file_contents = input_file_contents.splitlines()
    number_lines = input_file_contents[0:-1]
    operation_line = input_file_contents[-1]
    operations = operation_line.split()

    cephalopod_numbers = []
    start_i = 0
    for i, char in enumerate(operation_line):
        cur_cephalopod_number = []

        if i > 1 and char != " ":
            end_i = i
            for row in number_lines:
                cur_cephalopod_number.append(row[start_i:end_i])
            cephalopod_numbers.append(cur_cephalopod_number)
            start_i = end_i
        elif i == len(operation_line) - 1:
            end_i = len(operation_line)
            for row in number_lines:
                cur_cephalopod_number.append(row[start_i:end_i])
            cephalopod_numbers.append(cur_cephalopod_number)

    human_numbers_columns = []
    for cephalopod_number in cephalopod_numbers:
        cur_human_number_column = []
        for i in range(len(cephalopod_number[0])):
            cur_human_number = []
            for line in cephalopod_number:
                cur_human_number.append(line[i])

            cur_human_number = "".join(cur_human_number).strip()
            if len(cur_human_number) > 0:
                cur_human_number_column.append(int(cur_human_number))
        human_numbers_columns.append(cur_human_number_column)

    total = 0
    for i, operation in enumerate(operations):
        subtotal = 0
        operands = human_numbers_columns[i]

        if operation == "*":
            subtotal = 1
            for operand in operands:
                subtotal *= operand
        elif operation == "+":
            subtotal = sum(operands)
        total += subtotal

    # console.log(human_numbers_columns)
    console.log(total)


if __name__ == "__main__":
    input_file_contents = get_input_file_contents(file_path="input/day_06/test.txt")
    input_file_contents = get_input_file_contents(file_path="input/day_06/input.txt")
    part_one(input_file_contents)
    part_two(input_file_contents)
