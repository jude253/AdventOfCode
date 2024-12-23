from collections import defaultdict, deque

from advent_of_code.utils.daily_code_utils import Solution


class Day_23(Solution):
    def part_one(self):
        connections_lookup = defaultdict(set)
        for row in self.input_file.splitlines():
            comp1, comp2 = row.split("-")
            connections_lookup[comp1].add(comp2)
            connections_lookup[comp2].add(comp1)

        three_interconnected_computers_set = set()

        def find_three_interconnected_computers(start_node, connections_lookup):
            queue = deque([(start_node, set([start_node]))])
            length = 0
            seen = set([])
            connected_computers_set = set()
            while queue:
                num_nodes_at_length = len(queue)
                length += 1
                if length == 4:
                    break
                for _ in range(num_nodes_at_length):
                    cur_node, cur_path_nodes = queue.popleft()
                    seen.add(cur_node)
                    for next_node in connections_lookup[cur_node]:
                        # print(cur_node, length, next_node, length+1, cur_path_nodes)

                        if next_node == start_node and length == 3:
                            connected_computers_set.add(tuple(sorted(cur_path_nodes)))

                        if next_node not in seen:
                            next_path_nodes = cur_path_nodes.copy()
                            next_path_nodes.add(next_node)
                            queue.append((next_node, next_path_nodes))

            return connected_computers_set

        for node in connections_lookup:
            three_interconnected_computers = find_three_interconnected_computers(
                node, connections_lookup
            )
            three_interconnected_computers_set.update(three_interconnected_computers)

        total_start_with_t = 0
        for row in three_interconnected_computers_set:
            has_comp_starts_with_t = any([e.startswith("t") for e in row])

            if has_comp_starts_with_t:
                total_start_with_t += 1

        return total_start_with_t

    def part_two(self):
        all_connections_lookup = defaultdict(set)
        for row in self.input_file.splitlines():
            comp1, comp2 = row.split("-")
            all_connections_lookup[comp1].add(comp1)
            all_connections_lookup[comp1].add(comp2)
            all_connections_lookup[comp2].add(comp1)
            all_connections_lookup[comp2].add(comp2)

        def get_all_connected_nodes(node, all_connections_lookup):
            all_connections = all_connections_lookup[node].copy()
            connections_counts = defaultdict(int)
            for t_node in all_connections_lookup[node]:
                if t_node == node:
                    continue
                intersection_connections = all_connections.intersection(
                    all_connections_lookup[t_node]
                )
                intersection_connections = tuple(sorted(list(intersection_connections)))
                connections_counts[intersection_connections] += 1
            return set(
                [
                    k
                    for k, v in connections_counts.items()
                    if len(k) == v + 1 and v == max(connections_counts.values())
                ]
            )

        all_connected_nodes_set = set()
        for node in all_connections_lookup:
            all_connected_nodes_set.update(
                get_all_connected_nodes(node, all_connections_lookup)
            )

        max_all_connected_node_tuple_size = 0
        max_all_connected_node_tuple = ()

        for all_connected_node_tuple in all_connected_nodes_set:
            if len(all_connected_node_tuple) > max_all_connected_node_tuple_size:
                max_all_connected_node_tuple_size = len(all_connected_node_tuple)
                max_all_connected_node_tuple = all_connected_node_tuple
        return ",".join(max_all_connected_node_tuple)


if __name__ == "__main__":
    solution = Day_23()
    solution.execute_part_one()
    solution.execute_part_two()
