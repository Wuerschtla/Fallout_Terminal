import curses
import random
import time
import pygame

pygame.mixer.init()
pygame.mixer.music.load("media/wanderer.mp3")
pygame.mixer.music.play(-1)  

shapes = [
    [[1, 1, 1],
     [0, 1, 0]],

    [[0, 2, 2],
     [2, 2, 0]],

    [[3, 3, 0],
     [0, 3, 3]],

    [[4, 4],
     [4, 4]],

    [[5, 5, 5, 5]],

    [[6, 0, 0],
     [6, 6, 6]],

    [[0, 0, 7],
     [7, 7, 7]]
]

class Tetris:
    def __init__(self, stdscr, color):
        self.stdscr = stdscr
        self.color = color
        self.board = [[0 for _ in range(10)] for _ in range(20)]
        self.shape = None
        self.x = 0
        self.y = 0
        self.gameover = False
        self.score = 0
        self.new_shape()

    def new_shape(self):
        self.shape = random.choice(shapes)
        self.x = 3
        self.y = 0
        if self.check_collision():
            self.gameover = True

    def check_collision(self):
        for i in range(len(self.shape)):
            for j in range(len(self.shape[0])):
                if self.shape[i][j]:
                    if i + self.y >= 20 or \
                       j + self.x < 0 or \
                       j + self.x >= 10 or \
                       self.board[i + self.y][j + self.x]:
                        return True
        return False

    def freeze(self):
        for i in range(len(self.shape)):
            for j in range(len(self.shape[0])):
                if self.shape[i][j]:
                    self.board[i + self.y][j + self.x] = self.shape[i][j]
        self.clear_lines()
        self.new_shape()

    def clear_lines(self):
        new_board = [row for row in self.board if any(cell == 0 for cell in row)]
        cleared = 20 - len(new_board)
        self.score += cleared * 100
        while len(new_board) < 20:
            new_board.insert(0, [0 for _ in range(10)])
        self.board = new_board

    def rotate(self):
        rotated = [ [ self.shape[y][x] for y in range(len(self.shape)) ] for x in range(len(self.shape[0])-1, -1, -1) ]
        old_shape = self.shape
        self.shape = rotated
        if self.check_collision():
            self.shape = old_shape

    def move(self, dx):
        self.x += dx
        if self.check_collision():
            self.x -= dx

    def drop(self):
        self.y += 1
        if self.check_collision():
            self.y -= 1
            self.freeze()

    def draw(self):
        self.stdscr.clear()
        max_y, max_x = self.stdscr.getmaxyx()

        try:
            self.stdscr.addstr(0, 0, "Fallout Tetris - ENTER to quit", self.color)
            self.stdscr.addstr(1, 0, f"Score: {self.score}", self.color)
        except curses.error:
            pass

        for i in range(20):
            for j in range(10):
                if i+2 < max_y and j*2+1 < max_x:
                    try:
                        if self.board[i][j]:
                            self.stdscr.addstr(i+2, j*2, "[]", self.color)
                        else:
                            self.stdscr.addstr(i+2, j*2, "  ", self.color)
                    except curses.error:
                        pass

        for i in range(len(self.shape)):
            for j in range(len(self.shape[0])):
                if self.shape[i][j]:
                    y = self.y + i + 2
                    x = (self.x + j) * 2
                    if y < max_y and x+1 < max_x:
                        try:
                            self.stdscr.addstr(y, x, "[]", self.color)
                        except curses.error:
                            pass

        self.stdscr.refresh()

def main(stdscr):
    curses.curs_set(0)
    curses.start_color()
    curses.use_default_colors()

    try:
        curses.init_pair(1, 10, -1)  
    except curses.error:
        curses.init_pair(1, curses.COLOR_GREEN, -1)  

    green = curses.color_pair(1)

    stdscr.nodelay(True)
    tetris = Tetris(stdscr, green)
    last_drop = time.time()

    while not tetris.gameover:
        tetris.draw()
        time.sleep(0.05)
        key = stdscr.getch()

        if key in [10, 13]:
            break
        elif key == curses.KEY_LEFT:
            tetris.move(-1)
        elif key == curses.KEY_RIGHT:
            tetris.move(1)
        elif key == curses.KEY_DOWN:
            tetris.drop()
        elif key == curses.KEY_UP:
            tetris.rotate()

        if time.time() - last_drop > 0.5:
            tetris.drop()
            last_drop = time.time()

    stdscr.nodelay(False)
    stdscr.clear()
    stdscr.addstr(10, 10, "Game Over! Press any key to return to Terminal.", green)
    stdscr.refresh()
    stdscr.getch()

if __name__ == "__main__":
    curses.wrapper(main)
    pygame.mixer.music.stop()
