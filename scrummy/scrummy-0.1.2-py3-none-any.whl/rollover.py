"""
1. Read in todo.md.
2. All numbered done tasks are marked done in scrum/.
3. All undone tasks are kept in the new todo.md.
4. All done tasks are deleted from todo.md.
5. Everything else is ignored.
"""
import os
import re
import shutil
from datetime import datetime, timedelta
from pathlib import Path

import dateutil as du
from dateutil.parser import ParserError

from scrummy.config import conf
from scrummy.constants import Constants
from scrummy.models import Todo, Epic


def link_todo(todo: Todo, epic: Epic):
    last_todo = epic.last_of_depth(todo.depth-1)
    if last_todo and last_todo.depth < todo.depth:
        last_todo.children.append(todo)
        todo.parent = last_todo
    else:
        epic.todos.append(todo)
    if todo.id:
        epic[todo.id] = todo


def parse_todofile(filename: Path) -> tuple[datetime | None, Epic]:
    """
    Parse a todo file into a list of Todo objects.

    Parameters
    ----------
    filename: str | Path

    Returns
    -------
    tuple[datetime|None, Epic]
    """
    with open(filename, 'rt') as f:
        items = f.readlines()
    current_line: list[str] = []
    is_todo: bool = False
    is_frontmatter: bool = False
    file_date: datetime | None = None
    frontmatter: list[str] = []
    miscellanea: list[str] = []
    have_date: bool = False

    epic = Epic()
    epic.filepath = filename

    for line in items:
        # getting frontmatter
        if line.strip() == '---':
            is_frontmatter = not is_frontmatter
        elif is_frontmatter:
            frontmatter.append(line)
        # trying to get the date, assuming we're above the todo list.
        elif line.startswith('#') and not have_date:
            try:
                file_date = du.parser.parse(line[1:].strip())
                have_date = True
            except ParserError:
                pass
        elif re.match(Constants.opener_regex, line.lstrip()):
            have_date = True  # We assume that the first todo is after the date (in case it doesn't exist)
            if current_line:
                link_todo(Todo(current_line), epic)
                current_line = []
            current_line.append(line)
            is_todo = True
            if line.strip() == items[-1].strip():
                link_todo(Todo(current_line), epic)
                current_line = []
        elif is_todo:
            if not line.strip():
                link_todo(Todo(current_line), epic)
                current_line = []
                is_todo = False
            else:
                current_line.append(line)
        elif have_date:
            miscellanea.append(line)
    epic.parse_frontmatter(frontmatter)
    epic.miscellanea = ''.join(miscellanea)
    epic.filepath = filename
    return file_date, epic


def update_epics(epics: dict[str, Epic], sprint: Epic, date: datetime | None):
    keep = []
    for todo in sprint.todos:
        if todo.epic_id in epics:
            epics[todo.epic_id].update(todo, date)
        if not todo.completed:
            keep.append(todo)
    sprint.todos = keep
    sprint.todos_dict = {todo.id: todo for todo in sprint.todos}


def rollover_todo():
    date, sprint = parse_todofile(Path(conf.todo_file))
    epics: dict[str, Epic] = {}
    for path in Path(os.path.join(conf.home, 'scrum')).glob('*.md'):
        _, epic = parse_todofile(path)
        epics[epic.frontmatter['id']] = epic
    update_epics(epics, sprint, date)
    for epic in epics.values():
        with open(epic.filepath, 'wt') as f:
            f.write(str(epic))
    shutil.move(sprint.filepath, os.path.join(conf.home, 'sprints', date.strftime('%Y-%m-%d') + '.md'))
    with open(Path(conf.todo_file), 'wt') as f:
        # write the date as a top headline
        f.write('# ' + (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d') + '\n\n')
        f.write(sprint.render(render_frontmatter=False, render_miscellanea=False))


if __name__ == '__main__':
    rollover_todo()
