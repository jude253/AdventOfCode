from helper import read_file

NUMBER_STRS = [
    'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine'
]

            
def part_2():
    input_str = read_file('day1')
    sum = 0
    for line in input_str.split('\n'):
        if line is not None:
            # print('----------------------------------')
            # print(line)

            number_str = ''
            for i, char in enumerate(line):
                # print("searching", char)
                if char.isdigit():
                    number_str += char
                    # print("found", number_str)
                else:
                    for j, word in enumerate(NUMBER_STRS):
                        if 0 == line[i:].find(word):
                            # print("found", str(j+1))
                            number_str += str(j+1)

            number_str = number_str[0] + number_str[-1]

            sum += int(number_str)

    print(sum)