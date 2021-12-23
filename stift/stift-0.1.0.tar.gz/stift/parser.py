from typing import List, Union

from stift.exceptions import ParserError

TokenResponse = List[List[dict]]


class ParseTypes:
    function = "function"
    array = "array"
    variable = "variable"


class Token:
    """A token member of a perser."""

    def __init__(self, type=ParseTypes.variable) -> None:
        self.type = type
        self.value = ""

    def set_val(self, val) -> None:
        self.value = val.strip()

    def to_dict(self) -> dict:
        return self.__dict__

    def __repr__(self) -> str:
        return f'Token "{self.value}" [{self.type}]'

    def __str__(self) -> str:
        return f'"{self.value}" [{self.type}]'


class Parser:
    """Class used to parse strings with functions, array elements, strings, and variables.

    The main method is "parse"
    """

    def __init__(self, s: str = None) -> Union[None, TokenResponse]:
        self.tokens = [[]]
        self.level = 0
        self.token_index = 0

        if s is not None:
            self.parsed_data = self.parse(s)

    def parse(self, s: str) -> TokenResponse:
        """Parse a string with functions, strings, variables, and arrays.

        A tool to use these arguments should start at the end of the returned array (lowest level)
        and work upwards. Anything of type "str", "int", or "float" can be used as-is.

        :param s: String to be parsed
        :type s: str
        :raises ParserError: Issue with parsing somewhere along the line
        :return: Returns a nested list of "Token" dictionaries. These always include a value and a type.
            For functions, there will also be an argc and argv element (see example)
            For arrays, there will also be an index element (See example)
            {
                type: ParseTypes.function,  # Type can be str, int, float, or a ParseTypes element
                value: "ceiling"            # Variable value or function/array name
                argc: 2,                    # (Functions only) number of arguments
                argv: [(1,2), (1,3)],       # (Functions only) pointer to arg locations e.g. parsed[1][2]
            }
        :rtype: List[List[dict]]
        """

        self.s = s
        self.tokens = [[]]
        self.level = 0
        self.token_index = 0
        strindex = 0

        escape_active = False
        str_active = False

        # Left ([,(,") will increase level
        # Right ([,(,") will finalize current token and decrease level

        # Iterate through string and handle possible characters in order of precedence
        for c in s:
            if self.current_token is None:
                self.create_token()

            if c == "\\":
                # Escape character
                escape_active = True

            elif escape_active:
                escape_active = False
                self.current_token.value += c

            elif c == '"':
                # End a string
                if str_active:
                    str_active = False
                else:
                    self.current_token.type = str
                    str_active = True

            elif str_active:
                self.current_token.value += c

            elif c == "(":
                self.finalize_current_token(identifier=True)
                self.increase_level()
                self.parent_token.type = ParseTypes.function
                self.parent_token.argc = 1
                self.parent_token.argv = [(self.level, self.token_index)]

            elif c == ")":
                self.decrease_level()

            elif c == "[":
                self.increase_level()
                self.parent_token.index = (self.level, self.token_index)
                self.parent_token.type = ParseTypes.array

            elif c == "]":
                self.decrease_level()

            elif c == "," and self.parent_token.type == ParseTypes.function:
                self.finalize_current_token()
                self.increase_token_index()
                self.parent_token.argc += 1
                self.parent_token.argv.append((self.level, self.token_index))

            else:
                self.current_token.value += c

            strindex += 1

        if self.level != 0:
            raise ParserError("Unmatched bracket or quote somewhere along the line")

        self.parsed_data = self.dump_tokens()
        return self.parsed_data

    def finalize_current_token(self, identifier=False) -> None:
        """Convert numeric values if possible. Also verify identifiers"""
        self.current_token.value = self.current_token.value.strip()
        if identifier:
            testval = self.current_token.value.replace("@@", "")
            if not testval.isidentifier():
                raise ParserError(f"Not a valid identifier: {self.current_token.value}")
            return

        if self.current_token.type == ParseTypes.variable:
            try:
                v = float(self.current_token.value)
                v = int(self.current_token.value)
            except ValueError:
                # Default type is variable / identifier
                return self.finalize_current_token(identifier=True)

            else:
                self.current_token.value = v
                self.current_token.type = type(v)

    def increase_level(self) -> None:
        """Add an empty level and set us to that depth."""
        self.level += 1
        self.tokens.append([Token()])
        self.token_index = len(self.tokens[self.level]) - 1

    def decrease_level(self) -> None:
        """Decrease the depth level and set index properly."""
        self.finalize_current_token()
        self.level -= 1
        self.token_index = len(self.tokens[self.level]) - 1

    def increase_token_index(self) -> None:
        """Increase token index, nothing special."""
        self.token_index += 1

    def decrease_token_index(self) -> None:
        """Decrease token index, nothing special."""
        self.token_index -= 1

    def dump_tokens(self) -> list:
        """Go through two levels of nesting to get a dict."""
        return [[i.to_dict() for i in l] for l in self.tokens]

    def create_token(self) -> None:
        """Add a token to the current level."""
        self.tokens[self.level].append(Token())

    @property
    def current_token(self) -> Token:
        """Return the currently active token"""
        if len(self.tokens[self.level]) < self.token_index + 1:
            return None
        return self.tokens[self.level][self.token_index]

    @current_token.setter
    def current_token(self, val) -> None:
        self.tokens[self.level][self.token_index] = val

    @property
    def parent_token(self) -> Token:
        """Return parent token if it exists. Otherwise, create one with no type."""
        try:
            parent_level = self.tokens[self.level - 1]
            return self.tokens[self.level - 1][len(parent_level) - 1]
        except IndexError:
            return Token(type=None)

    def __repr__(self) -> str:
        return f"Parser {self.s}"

    def __str__(self) -> str:
        return f"{self.s}"
