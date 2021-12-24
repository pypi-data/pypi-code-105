import curses
import sys


def remove_prefix(text, prefix):
    if text.startswith(prefix):
        return text[len(prefix):]
    return text


def remove_suffix(text, suffix):
    if text.endswith(suffix):
        return text[:-len(suffix)]
    return text


def is_word(line, target_index):
    return line[target_index + 1].lower() not in ' \n' or line[target_index - 1].lower() not in ' \n'


def find_word_start_index(line, target_index):
    index = target_index - 1
    while index >= 0:
        if line[index].lower() in ' \n':
            return index
        index = index - 1
    return target_index


def find_word_end_index(line, target_index):
    index = target_index + 1
    while True:
        if line[index].lower() in ' \n':
            return index
        index = index + 1
    return target_index


def to_lines(line, length):
    lines = []
    while True:
        if len(line) <= length:
            lines.append(line)
            break

        if not is_word(line, length - 1):
            lines.append(line[:length - 1])
            sub_line = line[:length - 1]
            line = line[length - 1:].strip()
        else:
            index = find_word_start_index(line, length - 1)
            sub_line = line[:index]
            line = line[index:].strip()

        lines.append(sub_line)

    return lines


def read_file(file_path):
    with open(file_path) as f:
        return f.read()


def view_curses_colors():
    def print_color(stdscr):
        curses.start_color()
        curses.use_default_colors()
        for i in range(0, curses.COLORS):
            curses.init_pair(i + 1, i, -1)
        try:
            for i in range(0, 255):
                stdscr.addstr(str(i) + " ", curses.color_pair(i))
        except curses.ERR:
            # End of screen reached
            pass
        stdscr.getch()

    curses.wrapper(print_color)


def color_print(msg):
    def func(stdscr):
        stdscr.scrollok(True)  # enable scrolling, so it can print string with new lines

        curses.start_color()
        curses.use_default_colors()

        curses.init_pair(124, 123, -1)  # changes the definition of color pair 124
        curses.init_pair(197, 196, -1)  # changes the definition of color pair 197
        try:
            stdscr.addstr(msg + " ", curses.color_pair(124))
            stdscr.addstr("\n\npress any key to exit view", curses.color_pair(197))  # red text
        except curses.ERR:
            # End of screen reached
            pass
        stdscr.getch()

    curses.wrapper(func)


def proto_print(msg):
    sys.stdout.write(u"\u001b[38;5;" + str(229) + "m " + msg)
    print(u"\u001b[0m")


def print_info(msg):
    sys.stdout.write(u"\u001b[38;5;" + str(38) + "m " + msg)
    print(u"\u001b[0m")


def show_colors():
    for i in range(0, 16):
        for j in range(0, 16):
            code = str(i * 16 + j)
            sys.stdout.write(u"\u001b[38;5;" + code + "m " + code.ljust(4))
    print(u"\u001b[0m")  # clear
