import curses

def wrapper(func, num_colors):
    curses.initscr()
    curses.curs_set(0)
    curses.start_color()
    curses.use_default_colors()
    for i in range(num_colors - 1):
        curses.init_pair(i + 1, i, -1)
    curses.wrapper(func)
    curses.curs_set(1)