from typing import List, IO

from csvgen.random_utils import RandUtils, RandomBase


class CsvGenerator:

    _RAND_UTILS = RandUtils()

    def __init__(
            self,
            separator: str,
            delimiter: str,
            headers: bool,
            schema: List[dict],
            delimit_all: bool = False,
            randutils_override: RandUtils or None = None
    ):
        self.separator = separator
        self.delimiter = delimiter
        self.headers = headers
        self.schema = schema
        self.delimit_all = delimit_all
        self._schema_string = self._get_schema_string()
        self._schema_args = self._get_schema_args()
        self.lines: List[str] = []
        if randutils_override:
            self._RAND_UTILS = randutils_override

    def _get_schema_string(self) -> str:
        if self.delimit_all:
            temp_list: List[str] = []
            for _ in self.schema:
                temp_list.append(f"{self.delimiter}{{}}{self.delimiter}")
            return f"{self.separator}".join(temp_list) + "\n"
        return f"{self.separator}".join("{}" for _ in range(len(self.schema))) + "\n"

    def _get_schema_args(self) -> List[RandomBase]:
        result: List[RandomBase] = []
        for element in self.schema:
            element_type = element["type"]
            if element_type in self._RAND_UTILS.__dict__:
                result.append(self._RAND_UTILS.__dict__[element_type])
            else:
                result.append(self._RAND_UTILS.string)
        return result

    def _write_headers(self) -> str:
        result = ""
        for schema_element, arg in zip(self.schema, self._schema_args):
            if "header" in schema_element:
                result += f"{schema_element['header']}{self.separator}"
            else:
                result += f"{arg.header()}{self.separator}"
        return result[:-1] + "\n"

    def _write_line(self) -> str:
        return self._schema_string.format(*[f.generate() for f in self._schema_args])

    def generate(self, lines: int):
        """ generates the desired amount of lines for the CSV file """
        if self.headers:
            self.lines.append(self._write_headers())
        for _ in range(lines):
            self.lines.append(self._write_line())

    def clear(self):
        """ clears the generated lines """
        self.lines.clear()

    def write(self, result: IO):
        """ writes the lines of the CSV file into an IO buffer """
        for line in self.lines:
            result.write(line.encode())

    def __str__(self):
        result: str = f"CSV Generator {self.__hash__()}:\n"
        for element in self.__dict__:
            if element[0] != "_":
                result += f"{element}: {self.__dict__[element]}\n"
        return result + f"schema string: {self._schema_string}"
