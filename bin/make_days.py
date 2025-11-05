import os

NUM_DAYS = 25

PKG_NAME = "AdventOfCode"
GITKEEP_FILE_NAME = ".gitkeep"
WORKSPACE_ROOT = os.path.join(os.getcwd().split(PKG_NAME)[0], PKG_NAME)
SRC_REL_PATH = os.path.join("src", "advent_of_code")
INPUT_REL_PATH = "input"
SRC_FULL_PATH = os.path.join(WORKSPACE_ROOT, SRC_REL_PATH)
INPUT_FULL_PATH = os.path.join(WORKSPACE_ROOT, INPUT_REL_PATH)


def get_day_path_segments():
    day_path_segments = []
    for i in range(1, NUM_DAYS + 1):
        str_i = str(i)
        if len(str_i) == 1:
            str_i = f"0{str_i}"
        day_path_segment = f"day_{str_i}"
        day_path_segments.append(day_path_segment)
    return day_path_segments


if __name__ == "__main__":
    day_path_segments = get_day_path_segments()
    for day_path_segment in day_path_segments:
        gitkeep_full_path = os.path.join(
            SRC_FULL_PATH, day_path_segment, GITKEEP_FILE_NAME
        )
        os.makedirs(os.path.split(gitkeep_full_path)[0], exist_ok=True)
        with open(gitkeep_full_path, "w+") as f:
            f.write("")
    for day_path_segment in day_path_segments:
        gitkeep_full_path = os.path.join(
            INPUT_FULL_PATH, day_path_segment, GITKEEP_FILE_NAME
        )
        os.makedirs(os.path.split(gitkeep_full_path)[0], exist_ok=True)
        with open(gitkeep_full_path, "w+") as f:
            f.write("")
