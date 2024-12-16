import pygame

from advent_of_code.solutions import day_14
from advent_of_code.utils.daily_code_utils import DailyInput
from advent_of_code.utils.grid import Grid

TARGET_FPS = 0.5
daily_input = DailyInput()
robots = day_14.parse_input(daily_input.input_file)
HEIGHT, WIDTH = 103, 101

grid = Grid(day_14.make_grid(HEIGHT, WIDTH))
NUM_ROWS, NUM_COLS = grid.num_rows, grid.num_cols

COLORS = ["white", "green", "yellow", "red"]

GRIDS = []

num_seconds = 10000

for _i in range(7344):
    for j in range(len(robots)):
        p, v = robots[j]
        new_p = ((p[0] + v[0]) % grid.num_cols, (p[1] + v[1]) % grid.num_rows)
        robots[j][0] = new_p
    day_14.set_state(robots, grid)
    if _i in range(7340, 7344):
        GRIDS.append(Grid(grid.get_str()))
    day_14.clear(grid)

pygame.font.init()
pygame.init()
font = pygame.font.SysFont("Arial", 8)
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

BG_COLOR = "black"

H = screen.get_width() / NUM_COLS
W = screen.get_height() / NUM_ROWS


dt = 0

ITERATION_COUNT = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BG_COLOR)

    for row, col in grid.nodes_indicies():
        color = None
        i = min(ITERATION_COUNT, len(GRIDS) - 1)
        char = str(GRIDS[i].get_node_val(row, col))
        color = COLORS[int(char) % len(COLORS)]
        text_surface = font.render(char, False, color)
        text_surface.get_width()
        screen.blit(text_surface, (H * col, W * row))

    pygame.display.flip()
    dt = clock.tick(TARGET_FPS) // 1000
    ITERATION_COUNT += 1

pygame.quit()
