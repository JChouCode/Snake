import os
import sys
import curses
import random
import time
from enum import Enum
# from collections import deque
from curses import wrapper


def init_screen(stdscr):
    curses.curs_set(0)
    curses.nonl()
    sh, sw = stdscr.getmaxyx()
    win = curses.newwin(sh, sw, 0, 0)
    win.timeout(100)
    win.keypad(True)
    if sw//2 % 2 == 0:
        apple = (sh//2, sw//2 + 1)
    else:
        apple = (sh//2, sw//2)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
    return win, apple, sh, sw


class Key(Enum):
    LEFT = curses.KEY_LEFT
    RIGHT = curses.KEY_RIGHT
    UP = curses.KEY_UP
    DOWN = curses.KEY_DOWN

# Snake Object


class Snake(list):
    def __init__(self):
        list.__init__(self)
        self.append((1, 1))

    def get_x(self):
        return self[0][0]

    def get_y(self):
        return self[0][1]

    def get_pos(self):
        return self[0]

    def move(self, k):
        assert type(k) is Key
        if k == Key.UP:
            self.insert(0, (self[0][0] - 1, self[0][1]))
        elif k == Key.DOWN:
            self.insert(0, (self[0][0] + 1, self[0][1]))
        elif k == Key.LEFT:
            self.insert(0, (self[0][0], self[0][1] - 2))
        elif k == Key.RIGHT:
            self.insert(0, (self[0][0], self[0][1] + 2))


def check_lose(snake, sh, sw):
    return snake.get_x() in [0, sh] and snake.get_y() in [0, sw] and snake.get_pos() in snake[1:]


def gen_app(snake, apple, sh, sw):
    temp = snake.get_pos()
    while temp[1] % 2 == 0 or temp in snake:
        temp = (random.randint(1, sh - 1), random.randint(1, sw - 1))
    return temp


def main(stdscr):
    win, apple, sh, sw = init_screen(stdscr)

    snake = Snake()
    win.addch(snake.get_x(), snake.get_y(),
              '■', curses.color_pair(2))
    win.addch(apple[0], apple[1], curses.ACS_DIAMOND, curses.color_pair(1))

    key = None

    while True:

        next_key = win.getch()

        key = key if next_key == -1 else next_key

        if key == curses.KEY_UP:
            snake.move(Key.UP)
        elif key == curses.KEY_DOWN:
            snake.move(Key.DOWN)
        elif key == curses.KEY_LEFT:
            snake.move(Key.LEFT)
        elif key == curses.KEY_RIGHT:
            snake.move(Key.RIGHT)
        elif key == None:
            continue

        if check_lose(snake, sh, sw):
            win.keypad(False)
            return

        if snake.get_pos() == apple:
            apple = gen_app(snake, apple, sh, sw)
            win.addch(apple[0], apple[1], curses.ACS_DIAMOND,
                      curses.color_pair(1))
            win.refresh()
        else:
            tail = snake.pop()
            win.addch(tail[0], tail[1], ' ')

        pos_str = str(snake.get_pos())
        win.addstr(1, sw - 13, "Length: " + str(len(snake)))
        win.addstr(0, sw - 15, "               ")
        win.addstr(0, sw - 13, "Pos: " + pos_str)
        try:
            win.addch(snake.get_x(), snake.get_y(),
                      '■', curses.color_pair(2))
        except curses.error:
            win.clear()
            win.addstr(sh//2, sw//2 - 5, "Game Over")
            win.refresh()
            time.sleep(1.5)
            return


wrapper(main)
