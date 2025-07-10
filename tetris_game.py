import curses
import random
import time
import pygame
import json
import os

pygame.mixer.init()
pygame.mixer.music.set_volume(0.2)
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
        start_x = 2  # offset for left border

        try:
            self.stdscr.addstr(0, 0, "Fallout Tetris - ENTER to quit", self.color)
            self.stdscr.addstr(1, 0, f"Score: {self.score}", self.color)
            # Draw border around the board
            for i in range(21):  # 20 rows + bottom border
                self.stdscr.addstr(i + 2, start_x - 2, "||", self.color)
                self.stdscr.addstr(i + 2, start_x + 20, "||", self.color)
            self.stdscr.addstr(22, start_x - 2, "=" * 22, self.color)
        except curses.error:
            pass

        for i in range(20):
            for j in range(10):
                if i+2 < max_y and (start_x + j*2) < max_x:
                    try:
                        if self.board[i][j]:
                            self.stdscr.addstr(i+2, start_x + j*2, "[]", self.color)
                        else:
                            self.stdscr.addstr(i+2, start_x + j*2, "  ", self.color)
                    except curses.error:
                        pass

        for i in range(len(self.shape)):
            for j in range(len(self.shape[0])):
                if self.shape[i][j]:
                    y = self.y + i + 2
                    x = start_x + (self.x + j) * 2
                    if y < max_y and x+1 < max_x:
                        try:
                            self.stdscr.addstr(y, x, "[]", self.color)
                        except curses.error:
                            pass

        self.stdscr.refresh()

    def load_highscores(self, file="tetris_highscores.json"):
        if not os.path.exists(file):
            default_scores = [
                {"name": "AAA", "score": 50},
                {"name": "BBB", "score": 40},
                {"name": "CCC", "score": 30},
                {"name": "DDD", "score": 20},
                {"name": "EEE", "score": 10}
            ]
            with open(file, "w") as f:
                json.dump(default_scores, f)
            return default_scores
        with open(file, "r") as f:
            return json.load(f)

    def save_highscores(self, highscores, file="tetris_highscores.json"):
        with open(file, "w") as f:
            json.dump(highscores, f)

    def update_highscores(self):
        highscores = self.load_highscores()
        if len(highscores) < 5 or self.score > highscores[-1]["score"]:
            name = self.get_player_name()
            highscores.append({"name": name, "score": self.score})
            highscores = sorted(highscores, key=lambda x: x["score"], reverse=True)[:5]
            self.save_highscores(highscores)
            return True
        return False

    def show_highscores(self):
        highscores = self.load_highscores()
        self.stdscr.clear()
        self.stdscr.addstr(1, 2, "Highscores:", self.color | curses.A_BOLD)
        for idx, entry in enumerate(highscores):
            self.stdscr.addstr(3 + idx, 4, f"{idx + 1}. {entry['name']}: {entry['score']}", self.color)
        self.stdscr.addstr(10, 2, "Press any key to return...", self.color)
        self.stdscr.refresh()
        key = self.stdscr.getch()
        if key:
            self.stdscr.clear()
            self.stdscr.addstr(8, 10, "Game Over!", self.color | curses.A_BOLD)
            self.stdscr.addstr(10, 10, "Press 'R' to restart, 'H' for highscores, or any other key to exit.", self.color)
            self.stdscr.refresh()
            key = self.stdscr.getch()
            if key in [ord('r'), ord('R')]:
                main(self.stdscr)
            elif key in [ord('h'), ord('H')]:
                self.show_highscores()

    def get_player_name(self):
        curses.echo()
        self.stdscr.clear()
        self.stdscr.addstr(5, 2, f"Your score: {self.score}", self.color)
        self.stdscr.addstr(7, 2, "Enter your name: ", self.color)
        self.stdscr.refresh()
        self.stdscr.attron(self.color)
        raw = self.stdscr.getstr(7, 20, 3)
        try:
            name = raw.decode("utf-8").upper()
        except UnicodeDecodeError:
            name = "???"
        if not name:
            name = "???"
        self.stdscr.attroff(self.color)
        curses.noecho()
        return name

def main(stdscr):
    curses.curs_set(0)
    curses.mousemask(0)
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
    was_highscore = tetris.update_highscores()
    if was_highscore:
        tetris.show_highscores()
    stdscr.clear()
    stdscr.addstr(8, 10, "Game Over!", green | curses.A_BOLD)
    stdscr.addstr(10, 10, "Press 'R' to restart, 'H' for highscores, or ENTER to exit.", green)
    stdscr.refresh()
    key = stdscr.getch()
    if key in [ord('r'), ord('R')]:
        main(stdscr)
    elif key in [ord('h'), ord('H')]:
        tetris.show_highscores()

if __name__ == "__main__":
    curses.wrapper(main)
    pygame.mixer.music.stop()
