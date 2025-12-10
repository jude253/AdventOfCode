from collections import defaultdict, deque

import pulp
from rich.console import Console

console = Console()


def get_input_file_contents(file_path="input/day_10/input.txt"):
    input_file_contents = None
    with open(file_path) as f:
        input_file_contents = f.read()
    return input_file_contents


def find_min_flip_switches_part_one(initialization_info):
    start_state, target_state, wiring_schematics_dict, _joltage_requirements = (
        initialization_info
    )
    seen_set = set()
    to_process = deque([])

    for _key, key_switch_group in wiring_schematics_dict.items():
        for switch_group in key_switch_group:
            current_state = start_state
            current_switches_to_flip = switch_group
            current_flipped_switch_count = 0
            current_step = (
                current_state,
                current_switches_to_flip,
                current_flipped_switch_count,
            )
            to_process.append(current_step)
            # console.log(current_step)

    seen_set.add(start_state)
    min_switches_flipped = float("inf")

    def get_new_state(current_switches_to_flip: set[int], current_state: str):
        new_state = list(current_state)
        for switch_to_flip in current_switches_to_flip:
            new_state[switch_to_flip] = (
                "." if current_state[switch_to_flip] == "#" else "#"
            )
        return "".join(new_state)

    while to_process:
        current_to_process_state = to_process.popleft()
        current_state, current_switches_to_flip, current_flipped_switch_count = (
            current_to_process_state
        )

        new_state = get_new_state(current_switches_to_flip, current_state)

        new_flipped_switch_count = current_flipped_switch_count + 1

        seen_set.add(new_state)
        if new_state == target_state:
            min_switches_flipped = min(new_flipped_switch_count, min_switches_flipped)
            return min_switches_flipped

        for _key, key_switch_group in wiring_schematics_dict.items():
            for switch_group in key_switch_group:
                next_switches_to_flip = switch_group
                next_to_process_state = (
                    new_state,
                    next_switches_to_flip,
                    new_flipped_switch_count,
                )
                new_new_state = get_new_state(next_switches_to_flip, new_state)
                if new_new_state not in seen_set:
                    to_process.append(next_to_process_state)
                    seen_set.add(new_new_state)
        ## Log diff for debugging
        # console.log(
        #     (current_to_process_state, (new_state, {}, new_flipped_switch_count))
        # )


def part_one(input_file_contents: str):
    """
    Idea: treat "current_state" as path taken to get to target as seen
    set elements.  Stop iterating when it gets to end state or already
    seen "state"

    NOTE: I over complicated this a bunch-- shouldn't have stored the
    switches in a dict-- just a plain list.
    """

    console.log("part_one")
    input_file_contents = input_file_contents.splitlines()
    input_file_contents = [line.split() for line in input_file_contents]
    initialization_info_list = []
    for line in input_file_contents:
        target_state, wiring_schematics, joltage_requirements = (
            line[0],
            line[1:-1],
            line[-1],
        )
        target_state = target_state.strip("[]")
        start_state = "." * len(target_state)
        wiring_schematics = [
            eval(element.replace("(", "{").replace(")", "}"))
            for element in wiring_schematics
        ]
        wiring_schematics_dict = defaultdict(list)
        for switches_flipped_together in wiring_schematics:
            for switch_number in switches_flipped_together:
                wiring_schematics_dict[switch_number].append(switches_flipped_together)

        joltage_requirements = eval(
            joltage_requirements.replace("{", "[").replace("}", "]")
        )
        initialization_info_list.append(
            (
                start_state,
                target_state,
                dict(wiring_schematics_dict),
                joltage_requirements,
            )
        )

    # initialization_info = initialization_info_list[19]
    # console.log(find_min_flip_switches_part_one(initialization_info))

    min_flip_switches_total = 0
    for i, initialization_info in enumerate(initialization_info_list):
        min_flip_switches_step = find_min_flip_switches_part_one(initialization_info)
        console.log(i, min_flip_switches_step)
        min_flip_switches_total += min_flip_switches_step

    console.log(min_flip_switches_total)


def solve_row_part_two(
    start_state: str,
    target_state: str,
    wiring_schematics_list: list[list[int]],
    target_joltage: list[int],
):
    # console.log(wiring_schematics_list, target_joltage)

    num_switches = len(wiring_schematics_list)
    num_positions = len(target_joltage)

    # Create the linear programming problem
    # Minimize sum(X) where X are the number of times each switch group is activated
    problem = pulp.LpProblem("MinimizeSwitchActivations", pulp.LpMinimize)

    # Create decision variables (non-negative integers)
    X = [
        pulp.LpVariable(f"x_{i}", lowBound=0, cat=pulp.LpInteger)
        for i in range(num_switches)
    ]

    # Objective: minimize sum of all X values
    problem += pulp.lpSum(X), "TotalActivations"

    # Constraints: for each position, sum of activations must equal target joltage
    for pos in range(num_positions):
        constraint_sum = pulp.lpSum(
            X[i] for i, switches in enumerate(wiring_schematics_list) if pos in switches
        )
        problem += constraint_sum == target_joltage[pos], f"Position_{pos}_Constraint"

    # Solve the problem
    problem.solve(pulp.PULP_CBC_CMD(msg=0))

    # Extract solution
    solution = [int(var.varValue) for var in X]

    # console.log("Solution X:", solution)
    # console.log("Sum of X:", sum(solution))

    # Verify solution
    verification = [0] * num_positions
    for i, switches in enumerate(wiring_schematics_list):
        for switch in switches:
            verification[switch] += solution[i]

    # console.log("Verification:", verification)
    # console.log("Should equal target_joltage:", target_joltage)
    # console.log("Status:", pulp.LpStatus[problem.status])

    return sum(solution)


def part_two(input_file_contents: str):
    console.log("part_two")
    input_file_contents = input_file_contents.splitlines()
    input_file_contents = [line.split() for line in input_file_contents]
    initialization_info_list = []
    for line in input_file_contents:
        target_state, wiring_schematics, target_joltage = (
            line[0],
            line[1:-1],
            line[-1],
        )
        target_state = target_state.strip("[]")
        start_state = "." * len(target_state)
        wiring_schematics_list = [
            eval(element.replace("(", "[").replace(")", "]"))
            for element in wiring_schematics
        ]
        target_joltage = eval(target_joltage.replace("{", "[").replace("}", "]"))
        initialization_info_list.append(
            (
                start_state,
                target_state,
                wiring_schematics_list,
                target_joltage,
            )
        )

    # initialization_info = initialization_info_list[0]

    # solve_row_part_two(*initialization_info)

    total = 0

    for initialization_info in initialization_info_list:
        total += solve_row_part_two(*initialization_info)
    console.log(total)


if __name__ == "__main__":
    input_file_contents = get_input_file_contents(file_path="input/day_10/test.txt")
    input_file_contents = get_input_file_contents(file_path="input/day_10/input.txt")
    part_one(input_file_contents)
    part_two(input_file_contents)
