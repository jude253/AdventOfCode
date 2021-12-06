import logging
import sys
from abc import ABC, abstractmethod
from dataclasses import dataclass
from importlib.resources import as_file, files
from pathlib import Path

from advent_of_code import input

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


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
    input_file: str

    def __init__(self):
        self.__daily_input = DailyInput()
        logger.info(f"Input loaded for '{self.__daily_input.current_day_name}'!")
        self.input_file = self.__daily_input.input_file

    @abstractmethod
    def part_one(self):
        """Implement this as part of the challenge"""
        pass

    @abstractmethod
    def part_two(self):
        """Implement this as part of the challenge"""
        pass
