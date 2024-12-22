# Example file showing a circle moving on screen
import pygame

from advent_of_code.solutions.year_2024 import day_11
from advent_of_code.utils.daily_code_utils import DailyInput

daily_input = DailyInput()
# pygame setup
pygame.font.init()
pygame.init()
font = pygame.font.SysFont("Arial", 8)
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

BG_COLOR = pygame.Color(39, 60, 92)
RED = pygame.Color(163, 0, 0)
GREEN = pygame.Color(18, 143, 1)
PART_2_TOTAL = day_11.Day_11().part_two()
STONES = day_11.parse_input(daily_input.input_file)
LEN_STONES = []
for _ in range(76):
    LEN_STONES.append(day_11.get_stone_count(STONES))
    STONES = day_11.blink(STONES)


print(day_11.get_stone_count(STONES))

dt = 0

START_HEIGHT = screen.get_height() / 10
HEIGHT_CHUNK = screen.get_height() / 100
WIDTH_CHUNK = screen.get_width() / 10
ITERATION_COUNT = -50

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill(BG_COLOR)
    if ITERATION_COUNT >= 0:
        limit = min(ITERATION_COUNT, 75)
        MAX_LEN = LEN_STONES[limit]
        for i, len_stones in enumerate(LEN_STONES[:limit]):
            text_surface = font.render(f"{i}:", False, "grey")
            screen.blit(
                text_surface, (WIDTH_CHUNK - 20, START_HEIGHT + HEIGHT_CHUNK * i)
            )
            if 0 <= i <= 25:
                pygame.draw.rect(
                    screen,
                    RED,
                    pygame.Rect(
                        WIDTH_CHUNK,
                        START_HEIGHT + HEIGHT_CHUNK * i,
                        max(1, len_stones / MAX_LEN * 500),
                        10,
                    ),
                )
            screen.blit(
                text_surface,
                (
                    screen.get_width() - 4 * WIDTH_CHUNK - 20,
                    START_HEIGHT + HEIGHT_CHUNK * i,
                ),
            )
            pygame.draw.rect(
                screen,
                GREEN,
                pygame.Rect(
                    screen.get_width() - 4 * WIDTH_CHUNK,
                    START_HEIGHT + HEIGHT_CHUNK * i,
                    max(1, len_stones / MAX_LEN * 500),
                    10,
                ),
            )

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(20) // 1000
    ITERATION_COUNT += 1

pygame.quit()
