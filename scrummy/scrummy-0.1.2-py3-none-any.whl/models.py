from __future__ import annotations
from datetime import datetime

import re

from scrummy.config import conf
from scrummy.constants import Constants
from scrummy.utils import leading_spaces, parse_line


class Epic:
    filepath: str
    frontmatter: dict
    todos: list[Todo]
    todos_dict: dict
    miscellanea: str

    def __init__(self):
        self.filepath = ""
        self.frontmatter = {}
        self.todos = []
        self.todos_dict = {}
        self.miscellanea = ""

    def __getitem__(self, key: str) -> Todo:
        return self.todos_dict[key]

    def __setitem__(self, key, value):
        self.todos_dict[key] = value

    def __str__(self) -> str:
        return self.render()

    def __repr__(self) -> str:
        return f"<Epic {self.filepath}>"

    def parse_frontmatter(self, frontmatter: list[str]) -> None:
        for line in frontmatter:
            key, value = parse_line(line, sep=":")
            self.frontmatter[key] = value

    def render(self, render_frontmatter: bool = True, render_miscellanea: bool = True) -> str:
        lines: list[str] = []
        if self.frontmatter and render_frontmatter:
            lines.append(f"---")
            for key, value in self.frontmatter.items():
                lines.append(f"{key}: {value}")
            lines.append("---")
            lines.append('\n')
        for todo in self.todos:
            lines.append(str(todo))
        lines.append(Constants.line_ending)
        if render_miscellanea:
            lines.append(self.miscellanea)
        return Constants.line_ending.join(lines)

    def update(self, todo: Todo, date: datetime) -> None:
        todo.date = date
        self[todo.id].completed = todo.completed
        self[todo.id].date = date

    def last_of_depth(self, depth: int) -> Todo | None:
        if depth <= 0:
            if self.todos:
                return self.todos[-1]
            else:
                return None
        todo = self.todos[-1]
        while depth > todo.depth:
            if todo.children:
                todo = todo.children[-1]
            else:
                break
        return todo


class Todo:
    id: str = ""
    epic_id: int | None = None
    content: str = ""
    date: datetime | None = None
    completed: bool = False
    parent: Todo = None
    depth: int = 0
    children: list[Todo]

    def __init__(self, lines: list[str]):
        """
        Parses a multi-line todo of the form:

        ```
        * [ ] 234-4 <content>
        ```
        Parameters
        ----------
        lines: List[str]
        """
        self.children = []
        if lines[0].startswith("  "):
            pass
        self.depth = leading_spaces(lines[0]) // conf.indent_size
        self.completed = bool(re.search(r'\[x]', lines[0]))
        ident = re.search(r'\d+-\d+', lines[0])
        if ident:
            self.id = ident.group()
            self.epic_id = int(self.id.split('-')[0])
            end_of_id = ident.span()[-1]
        else:
            end_of_id = Constants.opener_length
        content: str = ''.join([lines[0][end_of_id:], *lines[1:]]).replace('\n', '')
        self.content = re.sub(r' +', ' ', content)

    def __str__(self):
        return self.render()

    def __repr__(self):
        return f"<Todo {self.id}>"

    def count_parents(self) -> int:
        """
        Counts the number of parents (i.e., the count of indentations to prepend)

        Returns
        -------
        int
        """
        if self.parent:
            return self.parent.count_parents() + 1
        return 0

    def render(self):
        """
        Renders a single todo to a string.

        Produces a string of the form:

        `- [ ] 234-4 <content>` if completed is False
        `- [x] 234-4 <content>` if completed is True

        The dash is replaced by configured list_indicator

        The indentation is determined by the depth of the todo (i.e., how many parents it has).

        The string is broken into multiple lines if it is too long (configured by indent_size).

        Returns
        -------
        str
        """
        completed: str = 'x' if self.completed else ' '
        ident: str = self.id if self.id else ''
        date: str = f' ({self.date.strftime(conf.date_format)})' if self.date else ''

        # '- [ ] 234-4 <content>'
        if self.completed:
            single_line: str = f'{conf.list_indicator} [{completed}] {ident}{self.content}{date}'
        else:
            single_line: str = f'{conf.list_indicator} [{completed}] {ident}{self.content}'

        indentation: str = ' ' * conf.indent_size * self.count_parents()
        split_strings: list[str] = []
        idx: int = 0
        first_line: bool = True
        while single_line[idx:].strip():
            end = idx + conf.max_line_length - len(indentation)
            if len(single_line[idx:end]) == end - idx:
                end = single_line[idx:end].rfind(' ')
            if first_line:
                split_strings.append(indentation + single_line[idx:end].strip())
                first_line = False
            else:
                split_strings.append(indentation + ' ' * Constants.opener_length + single_line[idx:end].strip())
            idx = end
        for child in self.children:
            split_strings.append(child.render())
        return Constants.line_ending.join(split_strings)
