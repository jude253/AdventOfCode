from helper import read_file


def part_1():
    input_str = read_file('day7')
    lines = input_str.split('\n')
    race_times = [ int(x) for x in lines[0].split()[1:] ]
    race_distances = [ int(x) for x in lines[1].split()[1:] ]

    
    speed_increase = 1  # millimeters per millisecond held down
    ways_win_per_race = 1
    for race_time, race_distance in zip(race_times, race_distances):
        speed = hold_time = 0  # millimeters per millisecond
        count_ways_to_win = 0

        while hold_time < race_time:
            hold_time = speed*speed_increase  # sepearate speed from distance for clarity

            time_remaining_after_hold = race_time - hold_time
            traveled_distance = time_remaining_after_hold * speed

            if traveled_distance > race_distance:
                count_ways_to_win += 1

            speed += 1
        ways_win_per_race *= count_ways_to_win

    return ways_win_per_race


def part_2():
    input_str = read_file('day6')
    lines = input_str.split('\n')

    race_time = int(''.join(lines[0].split()[1:]))
    race_distance = int(''.join(lines[1].split()[1:]))

    speed_increase = 1  # millimeters per millisecond held down
    ways_win_per_race = 1
    
    speed = hold_time = 0  # millimeters per millisecond
    count_ways_to_win = 0

    while hold_time < race_time:
        hold_time = speed*speed_increase  # sepearate speed from distance for clarity

        time_remaining_after_hold = race_time - hold_time
        traveled_distance = time_remaining_after_hold * speed

        if traveled_distance > race_distance:
            count_ways_to_win += 1

        speed += 1
    ways_win_per_race *= count_ways_to_win

    return ways_win_per_race