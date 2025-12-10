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


def part_one(input_file_contents: str, is_test=False):
    console.log("part_one")
    input_file_contents = input_file_contents.splitlines()
    points = np.array(
        [[int(x) for x in line.strip().split(",")] for line in input_file_contents]
    )

    max_heap = []
    largest_cuircuit_limit = 3
    closest_pair_limit = 1_000
    if is_test:
        closest_pair_limit = 10

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
    points = np.array(
        [[int(x) for x in line.strip().split(",")] for line in input_file_contents]
    )

    # Build a min heap of all pairs sorted by distance
    min_heap = []
    seen_pair_set = set()

    for cur_ind in range(points.shape[0]):
        distances_from_cur_ind = np.linalg.norm(points - points[cur_ind], axis=1)
        for other_ind in range(points.shape[0]):
            if cur_ind == other_ind:
                continue

            cur_pair = tuple(sorted([cur_ind, other_ind]))

            if cur_pair not in seen_pair_set:
                cur_dist = distances_from_cur_ind[other_ind]
                heapq.heappush(min_heap, (cur_dist, cur_pair))
                seen_pair_set.add(cur_pair)

    # Union-Find parent array: each node starts as its own parent
    parent = list(range(points.shape[0]))

    def find_root(index):
        """Find the root parent of a cluster (with path compression)"""
        if parent[index] != index:
            parent[index] = find_root(parent[index])
        return parent[index]

    def union_clusters(index_a, index_b):
        """Union two clusters, return True if they were in different clusters"""
        root_a = find_root(index_a)
        root_b = find_root(index_b)

        if root_a == root_b:
            return False

        parent[root_b] = root_a
        return True

    def count_clusters():
        """Count how many unique clusters exist"""
        unique_roots = set()
        for i in range(points.shape[0]):
            unique_roots.add(find_root(i))
        return len(unique_roots)

    # Connect pairs in order of increasing distance until all in one cluster
    last_connection = None

    while min_heap:
        cur_dist, (index_a, index_b) = heapq.heappop(min_heap)

        # Try to union these two clusters
        if union_clusters(index_a, index_b):
            last_connection = (index_a, index_b)

            # Check if we're done (all in one cluster)
            if count_clusters() == 1:
                break

    # Calculate the product of X coordinates
    if last_connection:
        index_a, index_b = last_connection
        x_coord_a = points[index_a][0]
        x_coord_b = points[index_b][0]
        result = x_coord_a * x_coord_b

        console.log(f"Last connection: {points[index_a]} and {points[index_b]}")
        console.log(f"X coordinates: {x_coord_a} * {x_coord_b} = {result}")
    else:
        console.log("No connections needed or something went wrong")


if __name__ == "__main__":
    test_input = get_input_file_contents(file_path="input/day_08/test.txt")
    input_file_contents = get_input_file_contents(file_path="input/day_08/input.txt")

    console.log("=== Testing with example ===")
    part_one(test_input, is_test=True)

    console.log("\n=== Running with actual input ===")
    part_one(input_file_contents)

    console.log("=== Testing with example ===")
    part_two(test_input)

    console.log("\n=== Running with actual input ===")
    part_two(input_file_contents)
