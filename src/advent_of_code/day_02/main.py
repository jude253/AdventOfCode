from rich.console import Console

console = Console()


def get_input_file_contents(file_path="input/day_02/input.txt"):
    input_file_contents = None
    with open(file_path) as f:
        input_file_contents = f.read()
    return input_file_contents


part_one_to_rps = {
    "A": "ROCK",
    "B": "PAPER",
    "C": "SCISSORS",
    "X": "ROCK",
    "Y": "PAPER",
    "Z": "SCISSORS",
}

part_one_shape_score = {
    "X": 1,
    "Y": 2,
    "Z": 3,
}

outcome_score = {
    "WIN": 6,
    "DRAW": 3,
    "LOSS": 0,
}


def get_player_outcome(abc: str, xyz: str):
    abc_rps = part_one_to_rps[abc]
    xyz_rps = part_one_to_rps[xyz]
    if abc_rps == xyz_rps:
        return "DRAW"

    if abc_rps == "ROCK" and xyz_rps == "SCISSORS":
        return "LOSS"
    if abc_rps == "SCISSORS" and xyz_rps == "PAPER":
        return "LOSS"
    if abc_rps == "PAPER" and xyz_rps == "ROCK":
        return "LOSS"

    if xyz_rps == "ROCK" and abc_rps == "SCISSORS":
        return "WIN"
    if xyz_rps == "SCISSORS" and abc_rps == "PAPER":
        return "WIN"
    if xyz_rps == "PAPER" and abc_rps == "ROCK":
        return "WIN"


def part_one(input_file_contents: str):
    input_file_lines = input_file_contents.split("\n")
    total_player_score = 0
    for line in input_file_lines:
        abc, xyz = line.split()
        player_outcome = get_player_outcome(abc, xyz)
        player_shape_score, player_outcome_score = (
            part_one_shape_score[xyz],
            outcome_score[player_outcome],
        )
        total_round_player_score = player_shape_score + player_outcome_score
        total_player_score += total_round_player_score

    console.log(total_player_score)


part_two_xyz_lookup = {
    "X": "LOSS",
    "Y": "DRAW",
    "Z": "WIN",
}

part_two_shape_score = {
    "ROCK": 1,
    "PAPER": 2,
    "SCISSORS": 3,
}


def get_player_move(abc: str, xyz: str):
    abc_rps = part_one_to_rps[abc]
    xyz_outcome = part_two_xyz_lookup[xyz]
    if xyz_outcome == "DRAW":
        return abc_rps

    if xyz_outcome == "WIN":
        if abc_rps == "ROCK":
            return "PAPER"
        if abc_rps == "SCISSORS":
            return "ROCK"
        if abc_rps == "PAPER":
            return "SCISSORS"

    if xyz_outcome == "LOSS":
        if abc_rps == "ROCK":
            return "SCISSORS"
        if abc_rps == "SCISSORS":
            return "PAPER"
        if abc_rps == "PAPER":
            return "ROCK"


def part_two(input_file_contents: str):
    input_file_lines = input_file_contents.split("\n")
    total_player_score = 0
    for line in input_file_lines:
        abc, xyz = line.split()
        player_move = get_player_move(abc, xyz)
        xyz_outcome = part_two_xyz_lookup[xyz]
        player_shape_score, player_outcome_score = (
            part_two_shape_score[player_move],
            outcome_score[xyz_outcome],
        )
        total_round_player_score = player_shape_score + player_outcome_score
        total_player_score += total_round_player_score

    console.log(total_player_score)


if __name__ == "__main__":
    input_file_contents = get_input_file_contents("input/day_02/test.txt")
    input_file_contents = get_input_file_contents()
    console.print("Part 1:")
    part_one(input_file_contents)
    console.print("Part 2:")
    part_two(input_file_contents)
