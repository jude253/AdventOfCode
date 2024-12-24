from collections import deque

from advent_of_code.utils.daily_code_utils import Solution


class Day_24(Solution):
    def part_one(self):
        existing_wires, output_wires = self.input_file.split("\n\n")
        existing_wires = {
            x.split(": ")[0]: int(x.split(": ")[1]) for x in existing_wires.splitlines()
        }
        output_wires = [line.split() for line in output_wires.splitlines()]
        output_wires_deque = deque(output_wires.copy())

        new_wires_list = [line[4] for line in output_wires]
        z_wires = reversed(
            sorted(
                [
                    (int(wire.replace("z", "")), wire)
                    for wire in new_wires_list
                    if "z" in wire
                ]
            )
        )
        while output_wires_deque:
            cur = output_wires_deque.pop()
            wire1, operator, wire2, _, new_wire = cur
            if wire1 in existing_wires and wire2 in existing_wires:
                wire1_val = existing_wires[wire1]
                wire2_val = existing_wires[wire2]
                new_wire_val = None
                if operator == "AND":
                    new_wire_val = wire1_val and wire2_val
                if operator == "OR":
                    new_wire_val = wire1_val or wire2_val
                if operator == "XOR":
                    new_wire_val = wire1_val ^ wire2_val
                existing_wires[new_wire] = new_wire_val
            else:
                output_wires_deque.appendleft(cur)

        output_binary_str = "".join([str(existing_wires[x[1]]) for x in z_wires])

        return int(output_binary_str, 2)

    def part_two(self):
        data = self.input_file.splitlines()
        wires = {}
        operations = []

        def process(op, op1, op2):
            if op == "AND":
                return op1 & op2
            elif op == "OR":
                return op1 | op2
            elif op == "XOR":
                return op1 ^ op2

        highest_z = "z00"
        for line in data:
            if ":" in line:
                wire, value = line.split(": ")
                wires[wire] = int(value)
            elif "->" in line:
                op1, op, op2, _, res = line.split(" ")
                operations.append((op1, op, op2, res))
                if res[0] == "z" and int(res[1:]) > int(highest_z[1:]):
                    highest_z = res

        wrong = set()
        for op1, op, op2, res in operations:
            if res[0] == "z" and op != "XOR" and res != highest_z:
                wrong.add(res)
            if (
                op == "XOR"
                and res[0] not in ["x", "y", "z"]
                and op1[0] not in ["x", "y", "z"]
                and op2[0] not in ["x", "y", "z"]
            ):
                wrong.add(res)
            if op == "AND" and "x00" not in [op1, op2]:
                for subop1, subop, subop2, _subres in operations:
                    if res in (subop1, subop2) and subop != "OR":
                        wrong.add(res)
            if op == "XOR":
                for subop1, subop, subop2, _subres in operations:
                    if res in (subop1, subop2) and subop == "OR":
                        wrong.add(res)

        while len(operations):
            op1, op, op2, res = operations.pop(0)
            if op1 in wires and op2 in wires:
                wires[res] = process(op, wires[op1], wires[op2])
            else:
                operations.append((op1, op, op2, res))

        return ",".join(sorted(wrong))


if __name__ == "__main__":
    solution = Day_24()
    solution.execute_part_one()
    solution.execute_part_two()
