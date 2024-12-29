import argparse
import os
from importlib.resources import as_file, files

from advent_of_code import solutions

if __name__ == "__main__":
    """
    This file is a super simple CLI to run the advent of code python
    code with a CLI interface.  It is is to allow an easy way to run
    this code with bazel or hatch.  (I am having trouble understanding
    how to use th "py_runtime" python rule with bazel b/c I don't know
    how to get the python interpreter set up with bazel, so I made this
    little cli wrapper instead.)

    Example bazel command:
    ```
    bazel run main 2024 01
    ```
    """

    parser = argparse.ArgumentParser(
        prog="AdventOfCodeCLI",
        description=(
            "This allows running the advent of code python code with a CLI interface."
        ),
    )

    parser.add_argument("year")  # positional argument
    parser.add_argument("day")  # positional argument
    args = parser.parse_args()

    if (
        len(args.year) != 4
        or not args.year.startswith("20")
        or not args.year.isnumeric()
    ):
        raise ValueError("year must be length 4, start with '20', and be a number!")
    if len(args.day) != 2 or not args.day.isnumeric():
        raise ValueError("day must be length 2 and be a number!")
    solutions_dir_files = files(solutions)
    try:
        with as_file(solutions_dir_files) as solutions_dir:
            fp = solutions_dir.joinpath(f"year_{args.year}")
            fp = fp.joinpath(f"day_{args.day}.py")
            fp_str = str(fp)
            if not fp.exists():
                raise FileNotFoundError(f"File not found: {fp_str}!")
            os.environ["__PY_DAILY_SOLUTION_FILE_PATH"] = fp_str
            exec(fp.read_bytes())
    finally:
        os.environ["__PY_DAILY_SOLUTION_FILE_PATH"] = ""
