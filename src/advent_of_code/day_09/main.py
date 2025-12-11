from rich.console import Console

console = Console()


def get_input_file_contents(file_path="input/day_09/input.txt"):
    input_file_contents = None
    with open(file_path) as f:
        input_file_contents = f.read()
    return input_file_contents


def part_one(input_file_contents: str, is_test=False):
    console.log("part_one")
    input_file_contents = input_file_contents.splitlines()

    points = [[int(x.strip()) for x in line.split(",")] for line in input_file_contents]

    num_points = len(points)
    max_rect_area = 0

    console.log(points)

    for fixed_point_index in range(num_points):
        fixed_point_value = points[fixed_point_index]
        for other_point_index in range(num_points):
            other_point_value = points[other_point_index]
            len_dir_0 = abs(fixed_point_value[0] - other_point_value[0]) + 1
            len_dir_1 = abs(fixed_point_value[1] - other_point_value[1]) + 1
            max_rect_area = max(max_rect_area, len_dir_0 * len_dir_1)

    console.log(max_rect_area)


def part_two(input_file_contents: str, is_test=False):
    console.log("part_two")
    input_file_contents = input_file_contents.splitlines()

    points = [[int(x.strip()) for x in line.split(",")] for line in input_file_contents]
    num_points = len(points)

    # Step 1: Coordinate compression with gaps
    console.log("Step 1: Compressing coordinates...")
    all_xs = sorted(set(p[0] for p in points))
    all_ys = sorted(set(p[1] for p in points))

    def compress_axis(all_t):
        """Compress coordinates, inserting gaps between non-adjacent values"""
        tt_by_t = {}
        tt_by_t[all_t[0]] = 0
        tt = 1
        for i in range(1, len(all_t)):
            prev_t = all_t[i - 1]
            t = all_t[i]
            if prev_t < t - 1:
                tt += 1  # Add gap
            tt_by_t[t] = tt
            tt += 1
        return tt_by_t

    xx_by_x = compress_axis(all_xs)
    yy_by_y = compress_axis(all_ys)
    width = xx_by_x[all_xs[-1]] + 1
    height = yy_by_y[all_ys[-1]] + 1

    console.log(f"Compressed grid size: {width}x{height}")

    # Step 2: Draw vertical lines with direction markers
    console.log("Step 2: Drawing polygon edges...")
    canvas = [[0] * width for _ in range(height)]

    for i in range(num_points):
        prev_pt = points[i]
        pt = points[(i + 1) % num_points]
        if prev_pt[0] == pt[0]:  # Vertical line
            xx = xx_by_x[pt[0]]
            yy0 = yy_by_y[prev_pt[1]]
            yy1 = yy_by_y[pt[1]]
            dyy = 1 if yy1 > yy0 else -1
            for yy in range(yy0, yy1 + dyy, dyy):
                canvas[yy][xx] = dyy

    # Step 3: Fill interior using scanline
    console.log("Step 3: Filling interior...")
    for yy in range(height):
        inside = 0
        for xx in range(width):
            v = canvas[yy][xx]
            if inside != v:
                inside += v
            if inside != 0 or v != 0:
                canvas[yy][xx] = 1

    # Step 4: Build prefix sum array for fast rectangle checks
    console.log("Step 4: Building prefix sum array...")
    prefix_sum = [[0] * (width + 1) for _ in range(height + 1)]
    for yy in range(1, height + 1):
        for xx in range(1, width + 1):
            prefix_sum[yy][xx] = (
                prefix_sum[yy][xx - 1]
                + prefix_sum[yy - 1][xx]
                - prefix_sum[yy - 1][xx - 1]
                + canvas[yy - 1][xx - 1]
            )

    def is_filled(x0, x1, y0, y1):
        """Check if rectangle is completely filled using prefix sum"""
        xx0 = xx_by_x[x0]
        xx1 = xx_by_x[x1]
        yy0 = yy_by_y[y0]
        yy1 = yy_by_y[y1]
        filled_count = (
            prefix_sum[yy1 + 1][xx1 + 1]
            - prefix_sum[yy0][xx1 + 1]
            - prefix_sum[yy1 + 1][xx0]
            + prefix_sum[yy0][xx0]
        )
        area = (yy1 - yy0 + 1) * (xx1 - xx0 + 1)
        return filled_count == area

    # Step 5: Find largest valid rectangle
    console.log("Step 5: Finding largest valid rectangle...")
    max_rect_area = 0

    for i in range(num_points):
        if i % 50 == 0:
            console.log(
                f"Progress: {i}/{num_points}, current max area: {max_rect_area}"
            )

        for j in range(i + 1, num_points):
            a = points[i]
            b = points[j]
            dx = abs(a[0] - b[0]) + 1
            dy = abs(a[1] - b[1]) + 1
            area = dx * dy

            if area > max_rect_area:
                x0, x1 = min(a[0], b[0]), max(a[0], b[0])
                y0, y1 = min(a[1], b[1]), max(a[1], b[1])
                if is_filled(x0, x1, y0, y1):
                    max_rect_area = area

    console.log(f"Final max area: {max_rect_area}")


if __name__ == "__main__":
    test_input = get_input_file_contents(file_path="input/day_09/test.txt")
    input_file_contents = get_input_file_contents(file_path="input/day_09/input.txt")

    # console.log("=== Testing with example ===")
    # part_one(test_input, is_test=True)

    # console.log("=== Running with actual input ===")
    # part_one(input_file_contents)

    console.log("=== Testing with example ===")
    part_two(test_input, is_test=True)

    console.log("\n=== Running with actual input ===")
    part_two(input_file_contents)
