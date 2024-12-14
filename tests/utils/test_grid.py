from advent_of_code.utils.grid import Grid, GridNode

TEST_GRID_1 = """
AAABBBCCC
AAABBBCCC
AAABBBCCC
""".strip()

TEST_GRID_2 = """
...BBBCCC
...BBBCCC
...BBBCCC
""".strip()


def test_no_error():
    g = Grid(TEST_GRID_1)
    g.get_str()


def test_set_node():
    g = Grid(TEST_GRID_1)
    for row, col in g.nodes_indicies():
        val = g.get_node_val(row, col)
        if val == "A":
            g.set_node(row, col, GridNode("."))
    assert g.get_str() == TEST_GRID_2


def test_is_inbounds():
    g = Grid(TEST_GRID_1)
    assert g.is_inbounds(-1, -1) is False
    assert g.is_inbounds(0, 0) is True
    assert g.is_inbounds(g.num_rows, g.num_cols) is False
