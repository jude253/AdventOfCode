from advent_of_code.utils.daily_code_utils import Solution


def add(a, b):
    return (a[0] + b[0], a[1] + b[1])


def sub(a, b):
    return (a[0] - b[0], a[1] - b[1])


def extract_int(s):
    return int("".join([c for c in s if c.isnumeric()]))


def get_min_cost(prize, A, B):
    min_cost = float("inf")
    stack = [(prize, 0)]
    seen = set([(prize, 0)])
    while stack:
        cur_dist, cost = stack.pop()
        for i, d in enumerate([A, B]):
            next_dist = sub(cur_dist, d)
            next_cost = cost + 3 if i == 0 else cost + 1
            if next_dist == (0, 0):
                min_cost = min(min_cost, next_cost)
            elif (
                (next_dist, next_cost) not in seen
                and next_dist[0] >= 0
                and next_dist[1] >= 0
            ):
                stack.append((next_dist, next_cost))
                seen.add((next_dist, next_cost))
    return 0 if min_cost == float("inf") else min_cost


def parse_input(input_file_str):
    games = []
    for game in input_file_str.split("\n\n"):
        lines = game.splitlines()
        game_map = {}
        A = lines[0].split()
        B = lines[1].split()
        P = lines[2].split()
        X_A, Y_A = extract_int(A[2]), extract_int(A[3])
        X_B, Y_B = extract_int(B[2]), extract_int(B[3])
        X_P, Y_P = extract_int(P[1]), extract_int(P[2])
        game_map["A"] = (X_A, Y_A)
        game_map["B"] = (X_B, Y_B)
        game_map["Prize"] = (X_P, Y_P)
        games.append(game_map)
    return games


def solve_system(A, B, P):
    y = (P[1] * A[0] - P[0] * A[1]) / (A[0] * B[1] - A[1] * B[0])
    x = (P[0] - B[0] * y) / A[0]
    return x, y


class Day_13(Solution):
    def part_one(self):
        games = parse_input(self.input_file)
        min_cost = 0
        for game in games:
            prize, A, B = game["Prize"], game["A"], game["B"]
            # min_cost += get_min_cost(prize, A, B)
            x, y = solve_system(A, B, prize)
            if x == int(x) and y == int(y):
                min_cost += x * 3 + y

        return int(min_cost)

    def part_two(self):
        games = parse_input(self.input_file)

        min_cost = 0
        for game in games:
            prize, A, B = game["Prize"], game["A"], game["B"]
            prize = add(prize, (10000000000000, 10000000000000))
            x, y = solve_system(A, B, prize)
            if x == int(x) and y == int(y):
                min_cost += x * 3 + y

        return int(min_cost)


if __name__ == "__main__":
    solution = Day_13()
    solution.execute_part_one()
    solution.execute_part_two()
