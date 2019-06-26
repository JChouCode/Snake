import curses
import random
from collections import deque

LEFT = curses.KEY_LEFT
RIGHT = curses.KEY_RIGHT
UP = curses.KEY_UP
DOWN = curses.KEY_DOWN

cur = curses.initscr()
curses.curs_set(0)
curses.noecho()
curses.cbreak()

sh, sw = cur.getmaxyx()
win = curses.newwin(sh, sw, 0, 0)
win.timeout(100)
win.keypad(True)

# Initialize snake
# snake = [(1, 1), (1, 1)]
snake = deque()
snake.append((1, 1))


def check_lose():
    if snake[0][0] in [0, sh] or snake[0][1] in [0, sw]:
        # or snake[0] in snake[1:]
        curses.nocbreak()
        cur.keypad(False)
        curses.echo()
        win.keypad(False)
        curses.endwin()
        quit()


key = None

apple = (sh//2, sw//2)

win.addch(apple[0], apple[1], curses.ACS_DIAMOND)

while True:
    check_lose()

    next_key = win.getch()
    key = key if next_key == -1 else next_key

    check_lose()

    new_head = snake[0]

    if key == UP:
        new_head = (snake[0][0] - 1, snake[0][1])
    elif key == DOWN:
        new_head = (snake[0][0] + 1, snake[0][1])
    elif key == LEFT:
        new_head = (snake[0][0], snake[0][1] - 1)
    elif key == RIGHT:
        new_head = (snake[0][0], snake[0][1] + 1)
    elif key == None:
        continue

    snake.append(new_head)

    temp = (0, 0)

    if snake[0] == apple:
        while True:
            temp = (random.randint(1, sh), random.randint(1, sw))
            if temp not in snake:
                apple = temp
                break
        win.addch(apple[0], apple[1], curses.ACS_PI)
    else:
        tail = snake.popleft()
        win.delch(tail[0], tail[1])

    win.addch(snake[0][0], snake[0][1], curses.ACS_CKBOARD)
