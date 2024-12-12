from random import randint

import pygame

from advent_of_code.solutions import day_12
from advent_of_code.utils.daily_code_utils import DailyInput

TARGET_FPS = 60
daily_input = DailyInput()
GRID = day_12.parse_input(daily_input.input_file)
NUM_ROWS, NUM_COLS = len(GRID), len(GRID[0])

# pygame setup
pygame.font.init()
pygame.init()
font = pygame.font.SysFont("Arial", 5)
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

BG_COLOR = pygame.Color(39, 60, 92)
RED = pygame.Color(163, 0, 0)
GREEN = pygame.Color(18, 143, 1)

W = screen.get_width() / NUM_ROWS
H = screen.get_height() / NUM_COLS

ALL_SEEN = set()
TRAVERSE_ORDER_LOOKUP = {}
TRAVERSE_ITERATION_COUNT = 0

RANDOM_COLORS = [
    pygame.Color(randint(0, 255), randint(0, 255), randint(0, 255)) for _ in range(100)
]


def traverse(node, grid):
    global TRAVERSE_ITERATION_COUNT
    char = grid[node[0]][node[1]]
    stack = [node]
    seen = set()
    while stack:
        cur_row, cur_col = stack.pop()
        seen.add((cur_row, cur_col))
        TRAVERSE_ORDER_LOOKUP[(cur_row, cur_col)] = TRAVERSE_ITERATION_COUNT
        TRAVERSE_ITERATION_COUNT += 1
        for d in day_12.DIRECTIONS:
            new_row, new_col = cur_row + d[0], cur_col + d[1]
            if (
                day_12.is_inbounds(new_row, new_col, grid)
                and grid[new_row][new_col] == char
                and (new_row, new_col) not in seen
            ):
                stack.append((new_row, new_col))
                ALL_SEEN.add((new_row, new_col))
    return seen


for row in range(NUM_ROWS):
    for col in range(NUM_COLS):
        if (row, col) not in ALL_SEEN:
            seen = traverse((row, col), GRID)
            ALL_SEEN = ALL_SEEN.union(seen)

dt = 0


ITERATION_COUNT = -50

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BG_COLOR)

    for row in range(NUM_ROWS):
        for col in range(NUM_COLS):
            color = None
            char = str(GRID[row][col])
            if TRAVERSE_ORDER_LOOKUP[(row, col)] < ITERATION_COUNT * 50:
                color = RANDOM_COLORS[ord(char) % len(RANDOM_COLORS)]
            text_surface = font.render(char, False, color if color else "black", color)
            text_surface.get_width()
            screen.blit(text_surface, (W * row, H * col))

    pygame.display.flip()
    dt = clock.tick(200) // 1000
    ITERATION_COUNT += 1

pygame.quit()
