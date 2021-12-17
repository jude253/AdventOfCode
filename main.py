import os
import numpy as np
from collections import Counter
import heapq


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
    map = np.zeros((max_val + 1, max_val + 1))

    # for each line create list of points on line and mark map:

    for line in lines:
        x = line[0, 0], line[1, 0]
        y = line[0, 1], line[1, 1]
        x_step = 1 if x[1] - x[0] <= 0 else -1
        y_step = 1 if y[1] - y[0] <= 0 else -1
        x_vals = np.arange(x[1], x[0] + x_step * 1, x_step)
        y_vals = np.arange(y[1], y[0] + y_step * 1, y_step)
        # print(x_vals, y_vals)
        if len(x_vals) == 1:
            x_vals = np.ones_like(y_vals) * x_vals[0]
        if len(y_vals) == 1:
            y_vals = np.ones_like(x_vals) * y_vals[0]
        line_points = list(zip(x_vals, y_vals))
        for line_point in line_points:
            map[line_point[0], line_point[1]] += 1

    print(np.sum(map > 1))


# part 1: 80 days; part 2: 256
def day6():
    input, normal_cycle, _8, _7 = np.array([int(x) for x in read_file('day6.txt').rstrip().split(',')]), [0] * 7, 0, 0
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
        digit_map, len_5, len_6 = [None] * 10, [], []
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


def day9():
    input = [list(x) for x in read_file('day9.txt').rstrip().split('\n')]
    # risk level of a low point is 1 plus its height
    # What is the sum of the risk levels of all low points on your heightmap?
    sum_of_risk_levels = 0
    n, m = len(input), len(input[0])

    for i in range(n):
        for j in range(m):
            cur = int(input[i][j])
            up = 10 if i - 1 < 0 else int(input[i - 1][j])
            down = 10 if i + 1 >= n else int(input[i + 1][j])
            left = 10 if j - 1 < 0 else int(input[i][j - 1])
            right = 10 if j + 1 >= m else int(input[i][j + 1])
            if cur < up and cur < down and cur < left and cur < right:
                sum_of_risk_levels += cur + 1
    print(sum_of_risk_levels)


def day9_part2():
    """
    strategy:
        - for each low point
            - keep counting up down left right if it is bigger until 9 or edge of board reached

    """
    input = [list(x) for x in read_file('day9.txt').rstrip().split('\n')]
    n, m, total = len(input), len(input[0]), 1
    directions, basin_sizes = [[-1, 0], [1, 0], [0, -1], [0, 1]], []

    def is_low_point(i, j):
        for direction in directions:
            i1, j1 = i + direction[0], j + direction[1]
            # for adjacent point that's not an edge, if current point is greater than or equal to adjacent return false
            if 0 <= i1 < n and 0 <= j1 < m and int(input[i][j]) >= int(input[i1][j1]):
                return False
        return True

    def find_size_of_basin(i, j):
        cur, count, input[i][j] = int(input[i][j]), 1, 9  # count current, change already seen ones to 9
        # for adjacent point that's not an edge
        for direction in directions:
            i1, j1 = i + direction[0], j + direction[1]
            # if adjacent point that's not an edge and current point < adjacent point < 9 add basin from there to count
            if 0 <= i1 < n and 0 <= j1 < m and cur < int(input[i1][j1]) < 9:
                count += find_size_of_basin(i1, j1)
        return count

    # for each point, if it is a low point, calculate the size of the basin
    for i in range(n):
        for j in range(m):
            if is_low_point(i, j):
                basin_sizes.append(find_size_of_basin(i, j))

    # get top 3 basins
    basin_sizes.sort(reverse=True)
    basin_sizes = basin_sizes[:3]

    # multiply together the top 3 basins
    for basin_size in basin_sizes:
        total *= basin_size
    print(total)


def day10():
    input = [list(x) for x in read_file('day10.txt').rstrip().split('\n')]
    opposite = {'(': ')', '{': '}', '[': ']', '<': '>'}
    char_score = {')': 3, ']': 57, '}': 1197, '>': 25137}
    total = 0

    # if it is an opener (in  opposites), add its opposite to closers stack, else pop closers stack and see if matches
    for line in input:
        closers = []
        for char in line:
            if char in opposite:
                closers.append(opposite[char])
            else:
                if len(closers) == 0:
                    total += char_score[char]
                    break
                elif closers[-1] != char:
                    total += char_score[char]
                    break
                else:
                    closers.pop(-1)
    print(total)


def day10_part2():
    input = [list(x) for x in read_file('day10.txt').rstrip().split('\n')]
    opposite = {'(': ')', '{': '}', '[': ']', '<': '>'}
    char_score = {')': 1, ']': 2, '}': 3, '>': 4}
    line_totals = []

    # if it is an opener (in  opposites), add its opposite to closers stack, else pop closers stack and see if matches
    # if there are closers left over at end of line, reverse closers stack and calc score of line
    for line in input:
        closers, ignore_line, line_total = [], False, 0
        for char in line:
            if char in opposite:
                closers.append(opposite[char])
            else:
                if len(closers) == 0:
                    ignore_line = True
                    break
                elif closers[-1] != char:
                    ignore_line = True
                    break
                else:
                    closers.pop(-1)

        if not ignore_line:
            closers = closers[::-1]
            for char in closers:
                line_total = 5 * line_total + char_score[char]
            line_totals.append(line_total)

    # sort line totals
    line_totals.sort()
    # middle value:
    print(line_totals[len(line_totals) // 2])


def day11():
    number_of_steps = 100
    input = [list(x) for x in read_file('day11.txt').strip().split('\n')]
    input = np.array([[int(x) for x in line] for line in input])
    increment_step, flash_count = np.ones_like(input), 0
    surrounding_points = np.array([[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]])
    n, m = input.shape
    for step in range(number_of_steps):
        input += increment_step
        # where this is true, add 1 to surrounding window as long as there are new flashpoints
        prev_flash_points_coordinates, flash_points_coordinates = set([]), set(
            [tuple(x) for x in np.argwhere(input > 9)])
        while len(prev_flash_points_coordinates) < len(flash_points_coordinates):
            for fp_coor in flash_points_coordinates:
                if fp_coor not in prev_flash_points_coordinates:
                    for surrounding_point in surrounding_points:
                        surrounding_coor = fp_coor + surrounding_point
                        if -1 < surrounding_coor[0] < n and -1 < surrounding_coor[1] < m:
                            input[surrounding_coor[0], surrounding_coor[1]] += 1
            prev_flash_points_coordinates = flash_points_coordinates
            flash_points_coordinates = set([tuple(x) for x in np.argwhere(input > 9)])
        flash_count += np.sum(input > 9)
        input[input > 9] = 0

    print(flash_count)


def day11_part2():
    step = 0
    input = [list(x) for x in read_file('day11.txt').strip().split('\n')]
    input = np.array([[int(x) for x in line] for line in input])
    increment_step = np.ones_like(input)
    surrounding_points = np.array([[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]])
    n, m = input.shape
    while np.sum(input == 0) != np.sum(increment_step):
        input += increment_step
        # where this is true, add 1 to surrounding window as long as there are new flashpoints
        prev_flash_points_coordinates, flash_points_coordinates = set([]), set(
            [tuple(x) for x in np.argwhere(input > 9)])
        while len(prev_flash_points_coordinates) < len(flash_points_coordinates):
            for fp_coor in flash_points_coordinates:
                if fp_coor not in prev_flash_points_coordinates:
                    for surrounding_point in surrounding_points:
                        surrounding_coor = fp_coor + surrounding_point
                        if -1 < surrounding_coor[0] < n and -1 < surrounding_coor[1] < m:
                            input[surrounding_coor[0], surrounding_coor[1]] += 1
            prev_flash_points_coordinates = flash_points_coordinates
            flash_points_coordinates = set([tuple(x) for x in np.argwhere(input > 9)])
        input[input > 9] = 0
        step += 1

    print(step)


def day12():
    input, graph = [x.split('-') for x in read_file('day12.txt').strip().split('\n')], {}
    small_tunnels, tunnels_left = set(), set()
    for tunnels in input:
        for i, tunnel in enumerate(tunnels):
            other_tunnel = tunnels[(i + 1) % 2]
            tunnels_left.add(tunnel)
            small_tunnels.add(tunnel) if tunnel.islower() else None
            if tunnel in graph:
                graph[tunnel].append(other_tunnel)
            else:
                graph[tunnel] = [other_tunnel]
    tunnels_left.remove('start')

    def find_all_paths(graph, start, end, tunnels_left, path=[]):
        path = path + [start]
        if start == end:
            return [path]
        if start not in graph:
            return []
        paths = []
        for node in graph[start]:
            if node in tunnels_left:
                if node in small_tunnels:
                    tunnels_left.remove(node)
                    newpaths = find_all_paths(graph, node, end, tunnels_left, path)
                    tunnels_left.add(node)
                else:
                    newpaths = find_all_paths(graph, node, end, tunnels_left, path)
                for newpath in newpaths:
                    paths.append(newpath)
        return paths

    all_paths = find_all_paths(graph, 'start', 'end', tunnels_left)
    print(len(all_paths))


def day12_part2():
    input, graph = [x.split('-') for x in read_file('day12.txt').strip().split('\n')], {}
    small_tunnels, tunnels_left = set(), set()
    for tunnels in input:
        for i, tunnel in enumerate(tunnels):
            other_tunnel = tunnels[(i + 1) % 2]
            tunnels_left.add(tunnel)
            small_tunnels.add(tunnel) if tunnel.islower() else None
            if tunnel in graph:
                graph[tunnel].append(other_tunnel)
            else:
                graph[tunnel] = [other_tunnel]
    tunnels_left.remove('start')

    def find_all_paths(graph, start, end, tunnels_left, visited_small_2x, path=[]):
        path = path + [start]
        if start == end:
            return [path]
        if start not in graph:
            return []
        paths = []
        for node in graph[start]:
            if node in tunnels_left:
                if node in small_tunnels and visited_small_2x == False:
                    newpaths = find_all_paths(graph, node, end, tunnels_left, True, path)
                    tunnels_left.remove(node)
                    newpaths.extend(find_all_paths(graph, node, end, tunnels_left, visited_small_2x, path))
                    tunnels_left.add(node)
                elif node in small_tunnels and visited_small_2x == True:
                    tunnels_left.remove(node)
                    newpaths = find_all_paths(graph, node, end, tunnels_left, visited_small_2x, path)
                    tunnels_left.add(node)
                else:
                    newpaths = find_all_paths(graph, node, end, tunnels_left, visited_small_2x, path)
                for newpath in newpaths:
                    paths.append(newpath)
        return paths

    all_paths = set([','.join(path) for path in find_all_paths(graph, 'start', 'end', tunnels_left, False)])
    print(len(all_paths))


def day13():
    coords, folds = [x.split('\n') for x in read_file('day13.txt').strip().split('\n\n')]
    coords = np.array([[int(x) for x in coord.split(',')] for coord in coords])
    orig_board_shape = tuple(np.array([1, 1]) + np.max(coords, axis=0))
    folds = [[fold[fold.find('=') - 1:fold.find('=')], int(fold[fold.find('=') + 1:])] for fold in folds]

    # create board
    board = np.zeros(orig_board_shape)
    # mark board
    for coord in coords: board[coord[0], coord[1]] = 1

    # transpose board so that it has same orientation as example
    board = board.T

    # fold board
    def fold_board(board, fold):
        # if the fold is on "x=" transpose matrix, then transpose back at end
        board = board.T if fold[0] == 'x' else board
        upper, lower = board[:fold[1]], np.flipud(board[fold[1] + 1:])
        board = upper + lower
        board[board > 1] = 1
        board = board.T if fold[0] == 'x' else board
        return board

    board = fold_board(board, folds[0])

    print(int(np.sum(board)))


def day13_part2():
    coords, folds = [x.split('\n') for x in read_file('day13.txt').strip().split('\n\n')]
    coords = np.array([[int(x) for x in coord.split(',')] for coord in coords])
    orig_board_shape = tuple(np.array([1, 1]) + np.max(coords, axis=0))
    folds = [[fold[fold.find('=') - 1:fold.find('=')], int(fold[fold.find('=') + 1:])] for fold in folds]

    # create board
    board = np.zeros(orig_board_shape)
    # mark board
    for coord in coords: board[coord[0], coord[1]] = 1

    # transpose board so that it has same orientation as example
    board = board.T

    def fold_board(board, fold):
        board = board.T if fold[0] == 'x' else board
        upper, lower = board[:fold[1]], np.flipud(board[fold[1] + 1:])
        board = upper + lower
        board[board > 1] = 1
        board = board.T if fold[0] == 'x' else board
        return board

    # perform all folds
    for fold in folds:
        board = fold_board(board, fold)

    # print output in readable way
    for line in board:
        line_readable = ' '.join(['#' if x == 1 else '.' for x in line])
        print(line_readable)


def day14():
    number_of_steps = 10
    input = read_file('day14.txt')
    polymer_template, pair_insertion_rules = [x.split('\n') for x in input.strip().split('\n\n')]
    # set up conversion dictionary
    conversion_dict = {k: k[0] + v + k[1] for (k, v) in [x.split(' -> ') for x in pair_insertion_rules]}

    # iterate through pairs and replace with new insertion
    polymer_template = polymer_template[0]
    for step in range(number_of_steps):
        converted_polymer_pairs = []
        for i in range(len(polymer_template[:-1])):
            pair = polymer_template[i:i + 2]
            if pair in conversion_dict:
                converted_polymer_pairs.append(conversion_dict[pair])
            else:
                converted_polymer_pairs.append(pair)
        polymer_template = ''
        for i, chain in enumerate(converted_polymer_pairs):
            # if not last element:
            if i != len(converted_polymer_pairs) - 1:
                polymer_template += chain[:2]
            else:
                polymer_template += chain

    letter_counts = Counter(polymer_template)
    min_count, max_count = float('inf'), -float('inf')
    for letter, count in letter_counts.items():
        if count < min_count: min_count = count
        if count > max_count: max_count = count

    print(max_count - min_count)


def day14_part2():
    number_of_steps = 40
    input = read_file('day14.txt')

    polymer_template, pair_insertion_rules = [x.split('\n') for x in input.strip().split('\n\n')]
    # set up conversion dictionary
    conversion_dict = {k: [k[0] + v, v + k[1]] for (k, v) in [x.split(' -> ') for x in pair_insertion_rules]}
    # iterate through pairs and replace with new insertion
    polymer_template = polymer_template[0]

    # set up pairs_counter
    pairs_counter, new_pairs_counter = {k: 0 for k in conversion_dict.keys()}, {k: 0 for k in conversion_dict.keys()}
    for i in range(len(polymer_template)-1): pairs_counter[polymer_template[i:i + 2]] += 1
    for step in range(number_of_steps):
        new_pairs_counter = {k: 0 for k in conversion_dict.keys()}
        for pair, count in pairs_counter.items():
            if count > 0:
                new1, new2 = conversion_dict[pair]
                new_pairs_counter[new1] += count
                new_pairs_counter[new2] += count
        pairs_counter = new_pairs_counter

    letter_counts, max_count, min_count = {polymer_template[-1]:1}, -float('inf'), float('inf')
    for pair, count in pairs_counter.items():
        if pair[0] in letter_counts:
            letter_counts[pair[0]] += count
        else:
            letter_counts[pair[0]] = count

    min_count, max_count = float('inf'), -float('inf')
    for letter, count in letter_counts.items():
        if count < min_count: min_count = count
        if count > max_count: max_count = count
    print(max_count - min_count)


def day15():
    """
        function dijkstra(G, S)
        distance[V] <- infinite
        previous[V] <- NULL
        distance[S] <- 0
        while there unvisited verticies:
            add neighbors to current node to pq with dist to there

        while Q IS NOT EMPTY
            U <- Extract MIN from Q
            for each unvisited neighbour V of U
                tempDistance <- distance[U] + edge_weight(U, V)
                if tempDistance < distance[V]
                    distance[V] <- tempDistance
                    previous[V] <- U
        return distance[], previous[]
    """
    input = read_file('day15.txt')
    graph = np.array([[int(x) for x in list(line)] for line in input.strip().split('\n')])
    visited, distance, pqueue = np.zeros_like(graph), np.ones_like(graph)*np.inf, []
    distance[0, 0], count, all_visited = 0, 0, np.sum(np.ones_like(visited))
    n, m = graph.shape
    heapq.heappush(pqueue, (0, count, np.array([0, 0])))
    directions = np.array([[0, 1], [1, 0], [-1, 0], [0, -1]])
    while np.sum(visited) < all_visited:
        current_node = heapq.heappop(pqueue)
        dist, _, coords = current_node
        for direction in directions:
            new_coords, count = coords + direction, count + 1
            if -1 < new_coords[0] < n and -1 < new_coords[1] < m and visited[new_coords[0], new_coords[1]] == 0:
                dist_to_new_coords = dist + graph[new_coords[0], new_coords[1]]
                if dist_to_new_coords < distance[new_coords[0], new_coords[1]]:
                    distance[new_coords[0], new_coords[1]] = dist_to_new_coords
                    heapq.heappush(pqueue, (dist_to_new_coords, count, new_coords))
        visited[coords[0], coords[1]] = 1

    print(int(distance[-1, -1]))


def day15():
    input = read_file('day15.txt')
    graph = np.array([[int(x) for x in list(line)] for line in input.strip().split('\n')])
    one, new = np.ones_like(graph), np.copy(graph)
    # create new bigger graph:
    for i in range(4):
        new += one
        new[new > 9] = 1
        graph = np.hstack((graph, new))

    one, new = np.ones_like(graph), np.copy(graph)
    for i in range(4):
        new += one
        new[new > 9] = 1
        graph = np.vstack((graph, new))

    visited, distance, pqueue = np.zeros_like(graph), np.ones_like(graph)*np.inf, []
    distance[0, 0], count, all_visited = 0, 0, np.sum(np.ones_like(visited))
    n, m = graph.shape
    heapq.heappush(pqueue, (0, count, np.array([0, 0])))
    directions = np.array([[0, 1], [1, 0], [-1, 0], [0, -1]])
    while np.sum(visited) < all_visited:
        current_node = heapq.heappop(pqueue)
        dist, _, coords = current_node
        for direction in directions:
            new_coords, count = coords + direction, count + 1
            if -1 < new_coords[0] < n and -1 < new_coords[1] < m and visited[new_coords[0], new_coords[1]] == 0:
                dist_to_new_coords = dist + graph[new_coords[0], new_coords[1]]
                if dist_to_new_coords < distance[new_coords[0], new_coords[1]]:
                    distance[new_coords[0], new_coords[1]] = dist_to_new_coords
                    heapq.heappush(pqueue, (dist_to_new_coords, count, new_coords))
        visited[coords[0], coords[1]] = 1

    print(int(distance[-1, -1]))

if __name__ == '__main__':
    day15()
