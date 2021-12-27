"""
Module containing functionality for console output, such as color print and ProgressBar class.
"""

import time
import sys
import os


class Colors:
    """
    Static class for storing color ASCI representations.
    """
    # This get inserted before string
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    # This gets inserted after strings
    END = '\033[0m'

    convert = {
        "white": "",
        "green": OKGREEN,
        "orange": WARNING,
        "red": FAIL
    }


def color_print(to_print: any, color: str = "white") -> None:
    """
    Function prints passed argument (casted to string) in specified color.
    Error gets raised if color does not exist.

    Args:
        to_print (any): Object instance to output to console
        color (str, optional): Color passed as string. Defaults to "white".

    Raises:
        ValueError: If passed color does not exist
    """
    # Check if color implemented
    if color in Colors.convert:
        print(Colors.convert[color] + str(to_print) + Colors.END)
    else:
        raise ValueError(f"color_print: Color {color} does not yet exist.")


class ProgressBar:
    """
    Class for displaying and updating a progress bar on the console output.
    """
    def __init__(
        self,
        total: int,
        start: int = 0,
        prefix: str = "Start",
        suffix: str = "End",
        decimals: str = 1,
        length: int = 40,
        fill: str = '█'
    ):
        """
        Args:
            total (int): Total number of calls needed for 100% fill
            start (int, optional): Start at iteration. Defaults to 0.
            prefix (str, optional): String to display before bar. Defaults to "".
            suffix (str, optional): String to display after bar. Defaults to "".
            decimals (str, optional): Number of decimals to round progress percentage. Defaults to 1.
            length (int, optional): Visual length of progress bar. Defaults to 100.
            fill (str, optional): Filler string for completion. Defaults to '█'.
        """
        self.iteration = start
        self.total = total
        self.prefix = prefix
        self.suffix = suffix
        self.decimals = decimals
        self.length = length

        self.initial_fill = fill
        self.fill = fill

        self.start_time = time.time()

    def __output(self) -> None:
        """
        Method outputs bar into console.
        """
        percent = ("{0:." + str(self.decimals) + "f}").format(100 * (self.iteration / float(self.total)))
        filled_length = int(self.length * self.iteration // self.total)
        bar = self.fill * filled_length + '-' * (self.length - filled_length)

        out_line = f'{self.prefix} |{bar}| {percent}% {self.suffix}\r'
        print('\b' * len(out_line), end='')
        sys.stdout.write(f'{self.prefix} |{bar}| {percent}% {self.suffix}\r')  # )
        sys.stdout.flush()

    def __fill(self):
        """
        Method fills the bar to the end.
        """
        self.iteration = self.total

    def update(self, iteration: int = None) -> None:
        """
        Method updates bar either adding one to iteration (if not passed), or setting progress on passed iteration value.

        Args:
            iteration (int, optional): If passed progress will be set to iteration / total. Defaults to None.
        """
        if iteration:
            self.iteration = iteration
        else:
            self.iteration += 1
        self.__output()

    def complete(self, successful: bool = True, fill: bool = False) -> None:
        """
        Method completes progress, determines color of either Green (successful) or Red (Not successful).

        Args:
            successful (bool, optional): If completion was successful, output will be green. Defaults to True.
            fill (bool, optional): If bar should be filled to 100%. Defaults to False.
        """
        if fill:
            self.__fill()
        if successful:
            self.fill = Colors.OKGREEN + self.fill
            status = "Completed in "
        else:
            self.fill = Colors.FAIL + self.fill
            status = "Failed at "
        self.fill += Colors.ENDC

        # Set suffix
        total_time = time.time() - self.start_time
        self.suffix = status + f"{int(total_time // 60)}min {int(total_time % 60)}s"

        self.__output()
        print()

    def reset(self) -> None:
        """
        Method re-sets progress to 0, re-outputs bar.
        """
        self.iteration = 0
        self.fill = self.initial_fill
        self.update()
