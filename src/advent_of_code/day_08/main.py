import heapq
from collections import defaultdict

import numpy as np
from rich.console import Console

console = Console()


def get_input_file_contents(file_path="input/day_08/input.txt"):
    input_file_contents = None
    with open(file_path) as f:
        input_file_contents = f.read()
    return input_file_contents


def part_one(input_file_contents: str):
    console.log("part_one")
    input_file_contents = input_file_contents.splitlines()
    points = np.array(
        [[int(x) for x in line.strip().split(",")] for line in input_file_contents]
    )

    max_heap = []
    largest_cuircuit_limit = 3
    closest_pair_limit = 1_000
    # closest_pair_limit = 10

    # console.log(points)
    seen_pair_set = set()
    for cur_ind in range(points.shape[0]):
        # console.log(cur_ind)
        distances_from_cur_ind = np.linalg.norm(points - points[cur_ind], axis=1)
        for other_ind in range(points.shape[0]):
            cur_dist = distances_from_cur_ind[other_ind]
            if cur_ind == other_ind:
                continue

            cur_pair = tuple(sorted([cur_ind, other_ind]))

            if cur_pair not in seen_pair_set:
                heapq.heappush(max_heap, (-1 * cur_dist, cur_pair))
                seen_pair_set.add(cur_pair)

            if len(max_heap) > closest_pair_limit:
                heapq.heappop(max_heap)

    connections_list = []
    while max_heap:
        connections_list.append(heapq.heappop(max_heap)[1])
    connections_list = connections_list[::-1]

    # console.log(connections_list)

    neighbors_lookup = defaultdict(set)

    for lo, hi in connections_list:
        neighbors_lookup[lo].add(hi)
        neighbors_lookup[hi].add(lo)

    visited_index_set = set()
    cluster_count = 0
    cluster_sizes = []
    # console.log(neighbors_lookup)

    # Iterate over ALL points (0 to points.shape[0]-1)
    for index in range(points.shape[0]):
        if index not in visited_index_set:
            cur_cluster_size = 0
            cluster_count += 1
            indexes_to_visit = [index]

            while indexes_to_visit:
                cur_index = indexes_to_visit.pop()
                # Only process if not already visited
                if cur_index not in visited_index_set:
                    cur_cluster_size += 1
                    visited_index_set.add(cur_index)

                    # Get neighbors of the CURRENT index being processed
                    for neighbor_index in neighbors_lookup[cur_index]:
                        if neighbor_index not in visited_index_set:
                            indexes_to_visit.append(neighbor_index)

            cluster_sizes.append(cur_cluster_size)

    cluster_sizes.sort()
    total_clusters_size_product = 1

    # console.log(cluster_count, cluster_sizes)
    # console.log(sorted(cluster_sizes, reverse=True))

    for _ in range(largest_cuircuit_limit):
        total_clusters_size_product *= cluster_sizes.pop()

    console.log(total_clusters_size_product)


def part_two(input_file_contents: str):
    console.log("part_two")
    input_file_contents = input_file_contents.splitlines()


if __name__ == "__main__":
    input_file_contents = get_input_file_contents(file_path="input/day_08/test.txt")
    input_file_contents = get_input_file_contents(file_path="input/day_08/input.txt")
    # part_one(input_file_contents)
    part_two(input_file_contents)
