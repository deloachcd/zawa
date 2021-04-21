import curses
import time

BIG_CARD_WIDTH = 13
BIG_CARD_HEIGHT = 9


def new_curses_window(width, height, begin_x, begin_y):
    return curses.newwin(height, width, begin_y, begin_x)


def main(stdscr):
    # Initialize curses environment
    curses.noecho()
    curses.cbreak()

    # Clear the screen
    stdscr.clear()
    stdscr.addstr(0, 0, "here's some text")
    time.sleep(1)

    # End curses environment
    stdscr.keypad(False)
    curses.echo()


if __name__ == "__main__":
    curses.wrapper(main)
