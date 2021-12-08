import os
import numpy as np


def read_file(filename):
    path = os.path.join(os.getcwd(), 'inputs', filename)
    f = open(path, 'r')
    return f.read()


def day1():
    input = read_file('day1.txt').split()
    input = [int(val) for val in input]
    prev = input[0]
    count = 0
    for i in range(1, len(input)):
        cur = input[i]
        if cur - prev > 0:
            count += 1

        prev = cur
    print(count)


def day1_part2():
    input = read_file('day1.txt').split()
    input = [int(val) for val in input]
    prev = input[0]
    count = 0
    # create new list:
    input_3 = []
    for i in range(len(input) - 2):
        input_3.append(input[i] + input[i + 1] + input[i + 2])

    # print(len(input_3), input_3)

    for i in range(1, len(input_3)):
        cur = input_3[i]
        if cur - prev > 0:
            count += 1

        prev = cur
    print(count)


def day2():
    input = read_file('day2.txt').rstrip().split('\n')
    horizontal_pos, depth = 0, 0

    for command in input:
        direction, magnitude = command.split()[0], int(command.split()[1])
        if direction == 'forward':
            horizontal_pos += magnitude
        if direction == 'down':
            depth += magnitude
        if direction == 'up':
            depth -= magnitude
    print(horizontal_pos * depth)


def day2_part2():
    """
    - down X increases your aim by X units.
    - up X decreases your aim by X units.
    - forward X does two things:
        - It increases your horizontal position by X units.
        - It increases your depth by your aim multiplied by X.

    """
    input = read_file('day2.txt').rstrip().split('\n')
    horizontal_pos, depth, aim = 0, 0, 0

    for command in input:
        direction, magnitude = command.split()[0], int(command.split()[1])

        if direction == 'down':
            aim += magnitude
        if direction == 'up':
            aim -= magnitude

        if direction == 'forward':
            horizontal_pos += magnitude
            depth += aim * magnitude
    print(horizontal_pos * depth)


def day3():
    input = read_file('day3.txt').split()
    n = len(input)
    big_list = []
    out = [0] * 12
    for i in range(n):
        for j, digit in enumerate(input[i]):
            out[j] = int(digit)
        big_list.append(out[:])
    big_list = np.array(big_list)

    bool_list = big_list.sum(axis=0) / n > .5
    gamma_rate, epsilon_rate = [], []
    for val in bool_list:
        if val == True:
            gamma_rate.append('1')
            epsilon_rate.append('0')
        else:
            gamma_rate.append('0')
            epsilon_rate.append('1')

    gamma_rate, epsilon_rate = int(''.join(gamma_rate), 2), int(''.join(epsilon_rate), 2)
    print(gamma_rate * epsilon_rate)


def day3_part2():
    input = read_file('day3.txt').split()
    n = len(input)
    big_list = []
    out = [0] * 12
    for i in range(n):
        for j, digit in enumerate(input[i]):
            out[j] = int(digit)
        big_list.append(out[:])
    big_list = np.array(big_list)

    bool_list = big_list.sum(axis=0) / n >= .5
    gamma_rate, epsilon_rate = [], []
    for val in bool_list:
        if val == True:
            gamma_rate.append('1')
            epsilon_rate.append('0')
        else:
            gamma_rate.append('0')
            epsilon_rate.append('1')

    gamma_rate, epsilon_rate = ''.join(gamma_rate), ''.join(epsilon_rate)

    print(gamma_rate, epsilon_rate)

    oxygen_list, CO2_list = np.unique(big_list, axis=0), np.unique(big_list, axis=0)
    oxygen_generator_rating, CO2_scrubber_rating = 0, 0
    for i in range(12):
        o = int(oxygen_list[:, i].sum(axis=0) / oxygen_list.shape[0] >= .5)
        c = int(CO2_list[:, i].sum(axis=0) / CO2_list.shape[0] < .5)

        oxygen_list = oxygen_list[oxygen_list[:, i] == o]
        CO2_list = CO2_list[CO2_list[:, i] == c]

        if oxygen_list.shape[0] == 1:
            oxygen_generator_rating = oxygen_list[0]
        if CO2_list.shape[0] == 1:
            CO2_scrubber_rating = CO2_list[0]

    oxygen_generator_rating, CO2_scrubber_rating = [str(i) for i in oxygen_generator_rating], [str(i) for i in
                                                                                               CO2_scrubber_rating]
    oxygen_generator_rating, CO2_scrubber_rating = int(''.join(oxygen_generator_rating), 2), int(
        ''.join(CO2_scrubber_rating), 2)
    print(oxygen_generator_rating, CO2_scrubber_rating)
    print(oxygen_generator_rating * CO2_scrubber_rating)
    return


def day4():
    input = read_file('day4.txt').rstrip().split('\n\n')
    numbers = [int(num) for num in input[0].split(',')]
    boards_raw = [board.split('\n') for board in input[1:]]
    boards = []
    for board_raw in boards_raw:
        board = []
        for row_raw in board_raw:
            row = row_raw.split()
            row = [int(num) for num in row]
            board.append(row)
        boards.append(np.array(board))
    # print(boards)

    number = numbers[0]

    def mark_boards(number):
        for i, board in enumerate(boards):
            board[board == number] = 0
            boards[i] = board

    for number in numbers:
        mark_boards(number)

        # score boards:
        for i, board in enumerate(boards):
            axis_0, axis_1, total = np.sum(board, axis=0), np.sum(board, axis=1), np.sum(board)
            if 0 in axis_0 or 0 in axis_1:
                print(total * number)
                # return
    # print(boards)

    mark_boards(number)

    # print(numbers, boards)


def day4_part2():
    input = read_file('day4.txt').rstrip().split('\n\n')
    numbers = [int(num) for num in input[0].split(',')]
    boards_raw = [board.split('\n') for board in input[1:]]
    boards = {}
    for i, board_raw in enumerate(boards_raw):
        board = []
        for row_raw in board_raw:
            row = row_raw.split()
            row = [int(num) for num in row]
            board.append(row)
        boards[i] = np.array(board)
    # print(boards)

    number = numbers[0]

    def mark_boards(number):
        for i, board in boards.items():
            board[board == number] = 0
            boards[i] = board

    for number in numbers:
        mark_boards(number)
        remove_list = []

        # score boards:
        for i, board in boards.items():
            axis_0, axis_1, total = np.sum(board, axis=0), np.sum(board, axis=1), np.sum(board)
            if 0 in axis_0 or 0 in axis_1:
                if len(boards) != 1:
                    remove_list.append(i)
                else:
                    print(total * number)
                    return
        for j in remove_list:
            boards.pop(j)

    mark_boards(number)

    # print(numbers, boards)


def day5():
    """
    Strategy:
    - parse input to beginning and end of lines in pair
        - find max value too
    - create board that is max by max
        - potentially dictionary
    - for each line end point pair:
        - if vertical or horizontal line
            - create list of points on line, increment board locations for each point
    - Count how many points have two or more
    """
    input, lines, max_val = read_file('day5.txt').rstrip().split('\n'), [], 0
    for line_raw in input:
        line = np.array([int(num) for num in line_raw.replace(' -> ', ',').split(',')]).reshape((2, 2))
        max_line_val = np.max(line)

        # find max to create board
        if max_val < max_line_val:
            max_val = max_line_val

        # only keep vertical or horizontal lines
        if 0 in line[0] - line[1]:
            lines.append(line)

    # create map:
    map = np.zeros((max_val, max_val))
    # mark map for each line:
    for line in lines:
        s, e, diff = line[0], line[1], line[0] - line[1]

        if diff[0] == 0:
            x = s[0]
            y1, y2 = min(s[1], e[1]), max(s[1], e[1]) + 1
            map[x, y1:y2] += 1
        else:
            x1, x2 = min(s[0], e[0]), max(s[0], e[0]) + 1
            y = s[1]
            map[x1:x2, y] += 1
    print(np.sum(map > 1))


def day5_part2():
    """
    Strategy:
    - parse input to beginning and end of lines in pair
        - find max value too
    - create board that is max by max
        - potentially dictionary
    - for each line end point pair:
        - create list of points on line, increment board locations for each point iteratively
    - Count how many points have two or more
    """
    input, lines, max_val = read_file('day5.txt').rstrip().split('\n'), [], 0
    for line_raw in input:
        line = np.array([int(num) for num in line_raw.replace(' -> ', ',').split(',')]).reshape((2, 2))
        max_line_val = np.max(line)

        # find max to create board
        if max_val < max_line_val:
            max_val = max_line_val

        lines.append(line)

    # create map:
    map = np.zeros((max_val+1, max_val+1))

    # for each line create list of points on line and mark map:

    for line in lines:
        x = line[0, 0], line[1, 0]
        y = line[0, 1], line[1, 1]
        x_step = 1 if x[1] - x[0] <= 0 else -1
        y_step = 1 if y[1] - y[0] <= 0 else -1
        x_vals = np.arange(x[1], x[0] + x_step*1, x_step)
        y_vals = np.arange(y[1], y[0] + y_step*1, y_step)
        # print(x_vals, y_vals)
        if len(x_vals) == 1:
            x_vals = np.ones_like(y_vals)*x_vals[0]
        if len(y_vals) == 1:
            y_vals = np.ones_like(x_vals) * y_vals[0]
        line_points = list(zip(x_vals, y_vals))
        for line_point in line_points:
            map[line_point[0], line_point[1]] += 1

    print(np.sum(map > 1))


# part 1: 80 days; part 2: 256
def day6():
    input, normal_cycle, _8, _7 = np.array([int(x) for x in read_file('day6.txt').rstrip().split(',')]), [0]*7, 0, 0
    number_of_days = 256
    for i in range(7):
        normal_cycle[i] = np.sum(input == i)

    for i in range(number_of_days):

        # decrement days:
        _0 = normal_cycle.pop(0)
        normal_cycle.append(_0)
        # add prev 7's too normal cycle six:
        normal_cycle[6] += _7

        # decrement 8 and add all that are currently 0 to new 8:
        _7, _8 = _8, _0

    all_fish = normal_cycle[:]
    all_fish.extend([_7, _8])
    all_fish = np.array(all_fish)
    print(np.sum(all_fish))


def day7():
    input = np.array([int(x) for x in read_file('day7.txt').rstrip().split(',')])
    median = np.median(input)
    fuel = int(np.sum(np.abs(input - median)))
    print(fuel)


def day7_part2():
    """
    brute force approach:
    """
    input = np.array([int(x) for x in read_file('day7.txt').rstrip().split(',')])
    # input = np.array([16,1,2,0,4,2,7,1,2,14]) # test input
    max_pos = np.max(input)
    past_fuel_costs = {}
    possible_aligns_fuel = np.zeros(max_pos + 1)
    def fuel_cost(x):
        if x in past_fuel_costs:
            return past_fuel_costs[x]
        else:
            past_fuel_costs[x] = np.sum(np.array(range(x + 1)))
        return past_fuel_costs[x]

    for align in range(len(possible_aligns_fuel)):
        dists_from_align = np.abs(input - align)
        running_fuel_total = 0
        for crab_dist in dists_from_align:
            running_fuel_total += fuel_cost(crab_dist)
        possible_aligns_fuel[align] = running_fuel_total
    print(int(np.min(possible_aligns_fuel)))


def day8():
    input = [x for x in read_file('day8.txt').rstrip().split('\n')]
    count, digit_lens = 0, set([2, 4, 3, 7])
    for line in input:
        # take the output (part after |)
        output = line.split(' | ')[1]

        # split the output string on spaces
        output = output.split(' ')

        # count if 1,4,7, or 8 in output
        for seven_segment_digit in output:
            if len(seven_segment_digit) in digit_lens:
                count += 1

    print(count)

def day8_part2():
    input = [x for x in read_file('day8.txt').rstrip().split('\n')]
    total = 0
    for line in input:
        # take the output (part after |)
        all_digits, output = line.split(' | ')

        # split the output string on spaces
        all_digits, output, output_digits = all_digits.split(' '), [set(digit) for digit in output.split(' ')], []
        digit_map, len_5, len_6 = [None]*10, [], []
        for digit in all_digits:
            if len(digit) == 2:
                digit_map[1] = set(digit)
            if len(digit) == 4:
                digit_map[4] = set(digit)
            if len(digit) == 3:
                digit_map[7] = set(digit)
            if len(digit) == 7:
                digit_map[8] = set(digit)
            if len(digit) == 5:
                len_5.append(set(digit))
            if len(digit) == 6:
                len_6.append(set(digit))

        # len 5:
        for digit in len_5:
            # find 3:
            # if 1 in digit, digit is 3
            if digit_map[1].issubset(digit):
                digit_map[3] = digit
            # if len(digit minus 4) = 2, digit is 5
            elif len(digit - digit_map[4]) == 2:
                digit_map[5] = digit
            # if len(digit minus 4) = 3, digit is 2
            elif len(digit - digit_map[4]) == 3:
                digit_map[2] = digit

        # find middle segment:
        middle = digit_map[2].intersection(digit_map[5], digit_map[4])

        # len 6:
        for digit in len_6:
            # if middle not in digit, digit is 0
            if not middle.issubset(digit):
                digit_map[0] = digit
            # if len(digit minus 3) = 1, digit is 9
            elif len(digit - digit_map[3]) == 1:
                digit_map[9] = digit
            # if len(digit minus 3) = 2, digit is 6
            elif len(digit - digit_map[3]) == 2:
                digit_map[6] = digit

        # convert output digits to integer:
        for digit in output:
            output_digits.append(str(digit_map.index(digit)))
        output_digits = int(''.join(output_digits))

        # add output digits to total:
        total += output_digits
    print(total)




if __name__ == '__main__':
    day8_part2()
