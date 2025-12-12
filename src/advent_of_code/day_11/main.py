from collections import defaultdict

from rich.console import Console

console = Console()


def get_input_file_contents(file_path="input/day_11/input.txt"):
    input_file_contents = None
    with open(file_path) as f:
        input_file_contents = f.read()
    return input_file_contents


def part_one(input_file_contents: str):
    console.log("part_one")
    input_file_contents = input_file_contents.splitlines()
    neighbors_lookup = defaultdict(set)

    for line in input_file_contents:
        parts = line.split()
        cur_node = parts[0].strip(":")
        neighbors_lookup[cur_node].update(set(parts[1:]))

    start = "you"
    end = "out"
    stack = [(start, (start,))]
    all_paths_count = 0
    while stack:
        current_node, current_path = stack.pop()
        # console.log(current_node, current_path)
        if current_node == end:
            all_paths_count += 1
            continue

        for neighbor in neighbors_lookup[current_node]:
            if neighbor not in current_path:
                stack.append((neighbor, [*current_path, neighbor]))

    console.log(all_paths_count)


def count_paths_between_dp(
    neighbors_lookup: dict, start: str, end: str, excluded_nodes: set[str] | None = None
) -> int:
    """
    Count all paths from start to end using dynamic programming.

    This approach is MUCH faster for large graphs with many paths
    because it avoids tracking individual paths.

    The key insight: we can count paths WITHOUT enumerating them
    by using DP where memo[node] = number of ways to reach 'end' from 'node'.
    """
    if excluded_nodes is None:
        excluded_nodes = set()

    # Try DAG optimization first: assume no cycles, use simple memoization
    memo = {}

    def count_paths_from(node: str) -> int:
        """Count paths from node to end (assumes DAG)."""
        if node == end:
            return 1

        if node in memo:
            return memo[node]

        total = 0
        for neighbor in neighbors_lookup.get(node, []):
            if neighbor not in excluded_nodes:
                total += count_paths_from(neighbor)

        memo[node] = total
        return total

    return count_paths_from(start)


def part_two(input_file_contents: str):
    """
    Count paths from 'svr' to 'out' that visit both 'dac' and 'fft'.

    Strategy: Decompose into ordered segments and use multiplication principle

    The key insight is that paths visiting both dac and fft must visit them
    in some order. We can partition all valid paths into two types:

    Type 1: svr -> ... -> dac -> ... -> fft -> ... -> out
    Type 2: svr -> ... -> fft -> ... -> dac -> ... -> out

    For each type, we count path segments independently and multiply:
    - Type 1: count(svr->dac, excluding fft) x count(dac->fft) x count(fft->out)
    - Type 2: count(svr->fft, excluding dac) x count(fft->dac) x count(dac->out)

    The exclusions prevent double-counting paths that visit both checkpoints early.

    The multiplication works because each segment choice is independent:
    - Any path svr->dac can combine with any path dac->fft
    - Any path dac->fft can combine with any path fft->out
    - Together they form unique complete paths

    Performance optimizations:
    1. Decomposition reduces search space from exponential to manageable segments
    2. DAG memoization: assumes graph is acyclic, so we can cache results per node
       without tracking visited nodes in the path
    3. This changes complexity from O(exponential) to O(nodes x edges)

    Example:
        If there are 5 paths svr->dac, 3 paths dac->fft, 2 paths fft->out,
        then there are 5 x 3 x 2 = 30 complete paths of type 1.
    """
    console.log("part_two")
    input_file_contents = input_file_contents.splitlines()

    neighbors_lookup = defaultdict(set)

    for line in input_file_contents:
        parts = line.split()
        cur_node = parts[0].strip(":")
        neighbors_lookup[cur_node].update(set(parts[1:]))

    # Strategy: decompose into ordered segments
    # Paths that visit both dac and fft can be:
    # 1. svr -> ... -> dac -> ... -> fft -> ... -> out
    # 2. svr -> ... -> fft -> ... -> dac -> ... -> out

    # For path type 1: svr->dac, dac->fft, fft->out
    # We need to multiply the counts because each combination is valid

    console.log("Counting paths: svr -> dac (excluding fft)")
    paths_svr_to_dac = count_paths_between_dp(
        neighbors_lookup, "svr", "dac", excluded_nodes={"fft"}
    )
    console.log(f"  Found {paths_svr_to_dac} paths")

    console.log("Counting paths: dac -> fft")
    paths_dac_to_fft = count_paths_between_dp(neighbors_lookup, "dac", "fft")
    console.log(f"  Found {paths_dac_to_fft} paths")

    console.log("Counting paths: fft -> out")
    paths_fft_to_out = count_paths_between_dp(neighbors_lookup, "fft", "out")
    console.log(f"  Found {paths_fft_to_out} paths")

    # Total for order: svr -> dac -> fft -> out
    total_dac_then_fft = paths_svr_to_dac * paths_dac_to_fft * paths_fft_to_out
    console.log(f"Total paths (svr->dac->fft->out): {total_dac_then_fft}")

    console.log("Counting paths: svr -> fft (excluding dac)")
    paths_svr_to_fft = count_paths_between_dp(
        neighbors_lookup, "svr", "fft", excluded_nodes={"dac"}
    )
    console.log(f"  Found {paths_svr_to_fft} paths")

    console.log("Counting paths: fft -> dac")
    paths_fft_to_dac = count_paths_between_dp(neighbors_lookup, "fft", "dac")
    console.log(f"  Found {paths_fft_to_dac} paths")

    console.log("Counting paths: dac -> out")
    paths_dac_to_out = count_paths_between_dp(neighbors_lookup, "dac", "out")
    console.log(f"  Found {paths_dac_to_out} paths")

    # Total for order: svr -> fft -> dac -> out
    total_fft_then_dac = paths_svr_to_fft * paths_fft_to_dac * paths_dac_to_out
    console.log(f"Total paths (svr->fft->dac->out): {total_fft_then_dac}")

    total_paths = total_dac_then_fft + total_fft_then_dac
    console.log(f"TOTAL: {total_paths}")


if __name__ == "__main__":
    input_file_contents = get_input_file_contents(file_path="input/day_11/test.txt")
    input_file_contents = get_input_file_contents(file_path="input/day_11/test2.txt")
    input_file_contents = get_input_file_contents(file_path="input/day_11/input.txt")
    part_one(input_file_contents)
    part_two(input_file_contents)
