from advent_of_code.utils.daily_code_utils import Solution


def adv(register, combo_operand):
    register["A"] = register["A"] // (2**combo_operand)


def bxl(register, literal_operand):
    register["B"] = register["B"] ^ literal_operand


def bst(register, combo_operand):
    register["B"] = combo_operand % 8


def jnz(register, literal_operand, instruction_pointer):
    """don't increment instruction_pointer after this"""
    if register["A"] == 0:
        return instruction_pointer + 2
    return literal_operand


def bxc(register, ignored_operand):
    register["B"] = register["B"] ^ register["C"]


def out(register, output, combo_operand):
    output.append(combo_operand % 8)


def bdv(register, combo_operand):
    register["B"] = register["A"] // (2**combo_operand)


def cdv(register, combo_operand):
    register["C"] = register["A"] // (2**combo_operand)


def combo_operand_lookup(register, literal_operand):
    d = {
        0: 0,
        1: 1,
        2: 2,
        3: 3,
        4: register["A"],
        5: register["B"],
        6: register["C"],
        7: None,
    }
    return d[literal_operand]


class Day_17(Solution):
    def part_one(self):
        register = {}
        program = []

        output = []

        for line in self.input_file.splitlines():
            if line.startswith("Register A: "):
                register["A"] = int(line.split("Register A: ")[1])
            if line.startswith("Register B: "):
                register["B"] = int(line.split("Register B: ")[1])
            if line.startswith("Register C: "):
                register["C"] = int(line.split("Register C: ")[1])
            if line.startswith("Program: "):
                tmp = line.split("Program: ")[1]
                program = [int(num) for num in tmp.split(",")]

        num_instructions = len(program)
        instruction_pointer = 0

        while instruction_pointer < num_instructions:
            instruction_val = program[instruction_pointer]
            literal_operand = program[instruction_pointer + 1]
            combo_operand = combo_operand_lookup(register, literal_operand)
            if instruction_val == 0:
                adv(register, combo_operand)
            elif instruction_val == 1:
                bxl(register, literal_operand)
            elif instruction_val == 2:
                bst(register, combo_operand)
            elif instruction_val == 3:
                instruction_pointer = jnz(
                    register, literal_operand, instruction_pointer
                )
                continue
            elif instruction_val == 4:
                bxc(register, literal_operand)
            elif instruction_val == 5:
                out(register, output, combo_operand)
            elif instruction_val == 6:
                bdv(register, combo_operand)
            elif instruction_val == 7:
                cdv(register, combo_operand)
            instruction_pointer += 2

        return ",".join([str(num) for num in output])

    def part_two(self):
        register = {}
        program = []

        for line in self.input_file.splitlines():
            if line.startswith("Register A: "):
                register["A"] = int(line.split("Register A: ")[1])
            if line.startswith("Register B: "):
                register["B"] = int(line.split("Register B: ")[1])
            if line.startswith("Register C: "):
                register["C"] = int(line.split("Register C: ")[1])
            if line.startswith("Program: "):
                tmp = line.split("Program: ")[1]
                program = [int(num) for num in tmp.split(",")]

        def execute_program(register, program):
            output = []
            num_instructions = len(program)
            instruction_pointer = 0

            while instruction_pointer < num_instructions:
                instruction_val = program[instruction_pointer]
                literal_operand = program[instruction_pointer + 1]
                combo_operand = combo_operand_lookup(register, literal_operand)
                if instruction_val == 0:
                    adv(register, combo_operand)
                elif instruction_val == 1:
                    bxl(register, literal_operand)
                elif instruction_val == 2:
                    bst(register, combo_operand)
                elif instruction_val == 3:
                    instruction_pointer = jnz(
                        register, literal_operand, instruction_pointer
                    )
                    continue
                elif instruction_val == 4:
                    bxc(register, literal_operand)
                elif instruction_val == 5:
                    out(register, output, combo_operand)
                elif instruction_val == 6:
                    bdv(register, combo_operand)
                elif instruction_val == 7:
                    cdv(register, combo_operand)
                instruction_pointer += 2

            return output

        A_val = 1
        comp_output = []

        A_val = 146876419701173  # 2,4,1,1,7,5,1,7,2,3,4,7,4,5,4,0  # 7 in common

        A_val = 175921605802421  # 2,4,1,1,7,5,1,5,4,5,4,4,4,7,3,0  # 9 in common
        # A_val = 160528443013557 # 2,4,1,1,7,5,1,5,4,5,4,0,7,7,1,0  # 10 in common
        # A_val = 162727722121653  # 2,4,1,1,7,1,0,4,4,4,4,4,4,0,3,0  5 in common

        # 164545579612597  # this it too high...
        # 164541154621877  # this is too low...

        # 8 in common, right next to the low. too high! 2,4,1,1,7,5,1,5,4,3,4,3,5,5,3,0
        A_val = 164542089951669

        # 2,4,1,1,7,5,2,7,4,0,0,3,5,5,3,0  - left:  2,4,1,1,7,5, right: ,4,0,0,3,5,5,3,0
        A_val = 164541158816181

        diff_comp_size = 4
        prev = 0

        diff_small = 1

        while program != comp_output:
            register["A"] = A_val
            comp_output = execute_program(register, program)
            if program[:diff_comp_size] == comp_output[:diff_comp_size]:
                diff = abs(A_val - prev)
                print(
                    ",".join([str(num) for num in comp_output]),
                    len(comp_output),
                    len(program),
                    A_val,
                    diff,
                )
                prev = A_val
            if A_val < 164_541_154_621_877:
                print("TOO LOW")
                break
            if A_val > 164_542_089_951_669:
                print("TOO HIGH")
                break
            A_val += diff_small
        return A_val - 1


if __name__ == "__main__":
    solution = Day_17()
    solution.execute_part_one()
    solution.execute_part_two()
