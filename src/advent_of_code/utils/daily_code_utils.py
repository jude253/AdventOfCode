import logging
import sys
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass
from importlib.resources import as_file, files
from pathlib import Path

from advent_of_code import input

logging.basicConfig(level=logging.INFO)


class TText:
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    END = "\033[0m"

    @classmethod
    def bold_and_green(cls, s):
        return TText.GREEN + TText.BOLD + str(s) + TText.END + TText.END


@dataclass
class DailyInput:
    """
    This reads the input file for a day.  The input file is expected to
    have the same name as the python file running the code for the
    challenge, but without any extension in the `/input` sub directory.
    """

    current_day_name: str
    input_file: str

    def __init__(self):
        self.current_day_name = Path(sys.argv[0]).stem
        self.__get_input_for_current_day()

    def __get_input_for_current_day(self):
        input_dir_files = files(input)
        with as_file(input_dir_files) as input_dir:
            cur_day_file_path = input_dir.joinpath(self.current_day_name)
            if not cur_day_file_path.exists():
                raise FileNotFoundError(
                    f"'{cur_day_file_path}' not found."
                    f"\n\nPlease add the correct input file "
                    f"from 'https://adventofcode.com/'!\n\n"
                )
            self.input_file = cur_day_file_path.read_text()


@dataclass
class Solution(ABC):
    __daily_input: DailyInput
    current_day_name: str
    input_file: str

    def __init__(self):
        self.__daily_input = DailyInput()
        self.current_day_name = self.__daily_input.current_day_name
        self.logger = logging.getLogger(self.current_day_name)
        self.logger.info(f"Input loaded for '{self.current_day_name}'!")
        self.input_file = self.__daily_input.input_file

    @abstractmethod
    def part_one(self):
        """Implement this as part of the challenge"""
        pass

    @abstractmethod
    def part_two(self):
        """Implement this as part of the challenge"""
        pass

    def __print_title(self, title):
        print()
        print(TText.bold_and_green("-" * 80))
        print(TText.bold_and_green(f"{title:-^80}"))
        print(TText.bold_and_green("-" * 80))
        print()

    def __format_answer(self, answer, seconds_to_run):
        return (
            f"{TText.YELLOW + TText.BOLD}"
            f"{answer}"
            f"{TText.END + TText.END} "
            f"({TText.CYAN}{seconds_to_run} sec{TText.END})"
        )

    def execute_part_one(self):
        title = f" {self.current_day_name} - part one "
        self.__print_title(f" START: {title}")

        start = time.time()
        part_one_solution = self.part_one()
        end = time.time()
        seconds_to_run = end - start
        self.logger.info(
            f"Part 1: {self.__format_answer(part_one_solution, seconds_to_run)}"
        )
        self.__print_title(f"-- END: {title}")

    def execute_part_two(self):
        title = f" {self.current_day_name} - part two "
        self.__print_title(f" START: {title}")

        start = time.time()
        part_two_solution = self.part_two()
        end = time.time()
        seconds_to_run = end - start
        self.logger.info(
            f"Part 2: {self.__format_answer(part_two_solution, seconds_to_run)}"
        )

        self.__print_title(f"-- END: {title}")
