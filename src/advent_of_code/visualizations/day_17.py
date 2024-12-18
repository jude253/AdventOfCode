# Example file showing a circle moving on screen
import pygame

from advent_of_code.solutions import day_17
from advent_of_code.utils.daily_code_utils import DailyInput

TARGET_FPS = 10
daily_input = DailyInput()
# pygame setup
pygame.font.init()
pygame.init()
font = pygame.font.SysFont("sfnsmono", 35, bold=True)
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

BG_COLOR = "black"

ITERATION_COUNT = 0

REGISTER, PROGRAM = day_17.parse_input(daily_input.input_file)

NUM_INSTRUCTIONS = len(PROGRAM)

PROGRAM_STR = ",".join([str(x) for x in PROGRAM])


def get_out_text(out):
    return ",".join([str(x) for x in out])


OUTPUT: list[int] = []

INSTRUCTION_POINTER = 0

ITERATION_STATES = []

while INSTRUCTION_POINTER < NUM_INSTRUCTIONS:
    instruction_val = PROGRAM[INSTRUCTION_POINTER]
    literal_operand = PROGRAM[INSTRUCTION_POINTER + 1]
    CURRENT_STATE = [INSTRUCTION_POINTER, REGISTER.copy()]

    combo_operand = day_17.combo_operand_lookup(REGISTER, literal_operand)
    if instruction_val == 0:
        day_17.adv(REGISTER, combo_operand)
        CURRENT_STATE.extend(["adv", literal_operand, OUTPUT.copy()])
        ITERATION_STATES.append(CURRENT_STATE)
    elif instruction_val == 1:
        day_17.bxl(REGISTER, literal_operand)
        CURRENT_STATE.extend(["bxl", literal_operand, OUTPUT.copy()])
        ITERATION_STATES.append(CURRENT_STATE)
    elif instruction_val == 2:
        day_17.bst(REGISTER, combo_operand)
        CURRENT_STATE.extend(["bst", literal_operand, OUTPUT.copy()])
        ITERATION_STATES.append(CURRENT_STATE)
    elif instruction_val == 3:
        INSTRUCTION_POINTER = day_17.jnz(REGISTER, literal_operand, INSTRUCTION_POINTER)
        CURRENT_STATE.extend(["jnz", literal_operand, OUTPUT.copy()])
        ITERATION_STATES.append(CURRENT_STATE)
        continue
    elif instruction_val == 4:
        day_17.bxc(REGISTER, literal_operand)
        CURRENT_STATE.extend(["bxc", literal_operand, OUTPUT.copy()])
        ITERATION_STATES.append(CURRENT_STATE)
    elif instruction_val == 5:
        day_17.out(REGISTER, OUTPUT, combo_operand)
        CURRENT_STATE.extend(["out", literal_operand, OUTPUT.copy()])
        ITERATION_STATES.append(CURRENT_STATE)
    elif instruction_val == 6:
        day_17.bdv(REGISTER, combo_operand)
        CURRENT_STATE.extend(["bdv", literal_operand, OUTPUT.copy()])
        ITERATION_STATES.append(CURRENT_STATE)
    elif instruction_val == 7:
        day_17.cdv(REGISTER, combo_operand)
        CURRENT_STATE.extend(["cdv", literal_operand, OUTPUT.copy()])
        ITERATION_STATES.append(CURRENT_STATE)
    INSTRUCTION_POINTER += 2


ITERATION_COUNT = 0

while running:
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    ip, r, fn, lo, output = ITERATION_STATES[
        min(ITERATION_COUNT, len(ITERATION_STATES) - 1)
    ]

    screen.fill(BG_COLOR)

    program = font.render(PROGRAM_STR, False, "blue")
    p_rect = screen.blit(program, (500, 50))
    w = (p_rect.topright[0] - p_rect.topleft[0]) // len(PROGRAM) + 1
    pygame.draw.rect(
        screen,
        "purple",
        pygame.Rect(
            p_rect.topleft[0] + w * ip,
            p_rect.topleft[1],
            w,
            p_rect.h,
        ),
    )
    screen.blit(program, (500, 50))

    register_a_surface = font.render(f"A: {r['A']}", False, "green")
    screen.blit(register_a_surface, (50, 50))
    register_b_surface = font.render(f"B: {r['B']}", False, "green")
    screen.blit(register_b_surface, (50, 100))
    register_c_surface = font.render(f"C: {r['C']}", False, "green")
    screen.blit(register_c_surface, (50, 150))

    fn_surface = font.render(f"{fn} {lo}", False, "purple")
    screen.blit(fn_surface, (500, 250))

    out_surface = font.render(f"OUT: {get_out_text(output)}", False, "yellow")
    screen.blit(out_surface, (50, 500))

    pygame.display.flip()

    dt = clock.tick(TARGET_FPS) // 1000
    ITERATION_COUNT += 1

pygame.quit()
