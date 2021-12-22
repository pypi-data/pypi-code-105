import curses

def wrapper(num_colors):
    def __inner(func):
        curses.initscr()
        curses.curs_set(0)
        curses.start_color()
        curses.use_default_colors()
        for i in range(num_colors - 2):
            curses.init_pair(i + 1, i, -1)
        curses.wrapper(func)
        curses.curs_set(1)