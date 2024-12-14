from dataclasses import dataclass
from typing import Any

UP = (-1, 0)
RIGHT = (0, 1)
DOWN = (1, 0)
LEFT = (0, -1)

CLOCKWISE_DIRS = [UP, RIGHT, DOWN, LEFT]
COUNTERCLOCKWISE_DIRS = [UP, LEFT, DOWN, RIGHT]


@dataclass
class GridNode:
    val: Any
    other_attributes: Any = None


@dataclass
class Grid:
    _grid: list[list[GridNode]]
    num_rows: int
    num_cols: int

    def __init__(self, input_file_str: str):
        self._grid = []
        for row in input_file_str.splitlines():
            self._grid.append([GridNode(val) for val in row])
        self.num_rows, self.num_cols = len(self._grid), len(self._grid[0])

    def get_str(self):
        return "\n".join(["".join([str(g.val) for g in row]) for row in self._grid])

    def print(self, row_type=str):
        if row_type is str:
            for row in self._grid:
                print("".join([str(g.val) for g in row]))
        else:
            for row in self._grid:
                print([g.val for g in row])

    def is_inbounds(self, row: int, col: int):
        return 0 <= row < self.num_rows and 0 <= col < self.num_cols

    def get_node(self, row: int, col: int):
        return self._grid[row][col]

    def get_node_val(self, row: int, col: int):
        return self.get_node(row, col).val

    def set_node(self, row: int, col: int, node: GridNode):
        self._grid[row][col] = node

    def set_node_val(self, row: int, col: int, val: Any):
        self._grid[row][col].val = val

    def nodes(self):
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                yield self._grid[row][col]

    def nodes_indicies(self):
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                yield (row, col)
