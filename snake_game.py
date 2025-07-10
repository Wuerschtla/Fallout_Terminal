import pygame
import pygame.mixer
import random
import curses
import json
from collections import deque

def open_snake():
    """Main Snake game function"""
    # Initialize sound
    pygame.mixer.init()
    pygame.mixer.music.set_volume(1)  # Set volume 0.0 to 1.0
    pygame.mixer.music.load("media/maybe.mp3")  # Make sure the file is in the same folder
    pygame.mixer.music.play(-1)  # -1 = loop indefinitely
    # Constants
    DELAY = 150  # Delay in milliseconds
    HIGHSCORE_FILE = "snake_highscores.json"

    # Directions
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

    class SnakeGame:
        def __init__(self, stdscr):
            self.stdscr = stdscr
            self.setup_screen()
            self.reset_game()
            self.load_highscores()
            self.running = True

        def setup_screen(self):
            # Initialize curses
            curses.curs_set(0)  # Make cursor invisible
            curses.start_color()
            curses.use_default_colors()
            curses.init_pair(1, curses.COLOR_GREEN, -1)
            curses.init_pair(2, curses.COLOR_GREEN, -1)
            curses.init_pair(3, curses.COLOR_GREEN, -1)
            curses.init_pair(4, curses.COLOR_GREEN, -1)
            
            # Get screen size
            self.max_y, self.max_x = self.stdscr.getmaxyx()
            
            # Calculate 16:9 format (within available size)
            height = min(self.max_y - 6, 45)  # Height minus status lines
            width = min(int(height * 16/9), self.max_x - 2)  # 16:9 ratio, limited by screen width
            
            # Create game window with border
            self.height = height
            self.width = width
            
            # Calculate position of game field (left-aligned)
            self.start_y = (self.max_y - height) // 2
            self.start_x = 1
            
            # Create game field
            self.win = curses.newwin(height, width, self.start_y, self.start_x)
            self.win.keypad(True)  # Enable arrow keys
            self.win.timeout(DELAY)  # Refresh rate
            
            # Status window for score
            self.status_win = curses.newwin(3, width, self.start_y - 3, 1)

        def reset_game(self):
            # Calculate game field size (inside)
            self.play_height = self.height - 2
            self.play_width = self.width - 2
            
            # Start snake in center
            start_x = self.play_width // 4 + 1
            start_y = self.play_height // 2 + 1
            
            self.snake = deque([(start_y, start_x)])  # Coordinates as (y, x) for curses
            self.direction = RIGHT
            self.food = None
            self.score = 0
            self.game_over = False
            self.place_food()

        def load_highscores(self):
            try:
                with open(HIGHSCORE_FILE, 'r') as f:
                    self.highscores = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                # Default highscores if no file exists
                self.highscores = [
                    {"name": "AAA", "score": 50},
                    {"name": "BBB", "score": 40},
                    {"name": "CCC", "score": 30},
                    {"name": "DDD", "score": 20},
                    {"name": "EEE", "score": 10}
                ]

        def save_highscores(self):
            with open(HIGHSCORE_FILE, 'w') as f:
                json.dump(self.highscores, f)

        def is_highscore(self):
            return self.score > min(hs["score"] for hs in self.highscores) if self.highscores else True

        def add_highscore(self, name):
            # Add new highscore entries
            self.highscores.append({"name": name, "score": self.score})
            # Sort by score
            self.highscores.sort(key=lambda x: x["score"], reverse=True)
            # Limit to top 5
            self.highscores = self.highscores[:5]
            self.save_highscores()

        def place_food(self):
            while True:
                # Random position inside the game field (excluding borders)
                y = random.randint(1, self.play_height)
                x = random.randint(1, self.play_width)
                
                # Check if position is not occupied by snake
                if (y, x) not in self.snake:
                    self.food = (y, x)
                    break

        def get_input(self):
            key = self.win.getch()
            
            if key == curses.KEY_LEFT or key == ord('a'):   # left
                if self.direction != DOWN:
                    return UP
            elif key == curses.KEY_RIGHT or key == ord('d'):   # right
                if self.direction != UP:
                    return DOWN
            elif key == curses.KEY_UP or key == ord('w'): # up
                if self.direction != RIGHT:
                    return LEFT
            elif key == curses.KEY_DOWN or key == ord('s'):   # down
                if self.direction != LEFT:
                    return RIGHT
            elif key == ord('q'):
                self.running = False
                
            return self.direction

        def move_snake(self):
            head_y, head_x = self.snake[0]
            dy, dx = self.direction
            new_head = (head_y + dy, head_x + dx)
            
            # Collision checks
            # Check for collisions with wall
            if (new_head[0] <= 0 or new_head[0] > self.play_height or
                new_head[1] <= 0 or new_head[1] > self.play_width or
                new_head in self.snake):
                self.game_over = True
                return

            # Move snake head
            self.snake.appendleft(new_head)
            
            # Check if food was eaten
            if new_head == self.food:
                self.score += 10
                self.place_food()
            else:
                # If no food eaten, remove last segment
                self.snake.pop()

        def draw_status(self):
            self.status_win.clear()
            # Display score bold and green in status bar
            self.status_win.attron(curses.color_pair(3) | curses.A_BOLD)
            self.status_win.addstr(1, 2, f"Score: {self.score}")
            self.status_win.addstr(1, 20, "Snake | WASD / Arrow keys")
            self.status_win.attroff(curses.color_pair(3) | curses.A_BOLD)
            self.status_win.refresh()

        def draw_game(self):
            self.win.clear()
            # Score display removed from game field as it is shown in draw_status
            # Draw border (green)
            self.win.attron(curses.color_pair(3))
            self.win.border()
            self.win.attroff(curses.color_pair(3))
            
            # Draw snake (green)
            for segment in self.snake:
                y, x = segment
                self.win.addch(y, x, '0', curses.color_pair(1))
            
            # Draw food (red)
            if self.food:
                y, x = self.food
                self.win.addch(y, x, '*', curses.color_pair(2))
            
            self.win.refresh()

        def show_highscores(self):
            # Highscore window
            hs_height = 15
            hs_width = 40
            hs_y = (self.max_y - hs_height) // 2
            hs_x = 1

            hs_win = curses.newwin(hs_height, hs_width, hs_y, hs_x)
            hs_win.keypad(True)
            hs_win.attron(curses.color_pair(3))
            hs_win.border()
            hs_win.attroff(curses.color_pair(3))

            # Highscores title
            hs_win.addstr(2, (hs_width - 10) // 2, "HIGHSCORES", curses.A_BOLD | curses.color_pair(4))

            # Display highscores
            for i, hs in enumerate(self.highscores[:5]):
                hs_win.addstr(4 + i, 5, f"{i+1}. {hs['name']}: {hs['score']}", curses.color_pair(4))

            # Return message
            hs_win.addstr(hs_height - 2, 5, "Press any key to return...", curses.color_pair(4))
            hs_win.refresh()

            # Wait for key press
            hs_win.getch()

        def show_game_over(self):
            # Game Over window
            game_over_height = 15
            game_over_width = 40
            game_over_y = (self.max_y - game_over_height) // 2
            game_over_x = 1
            
            game_over_win = curses.newwin(game_over_height, game_over_width, game_over_y, game_over_x)
            game_over_win.keypad(True)
            game_over_win.attron(curses.color_pair(3))
            game_over_win.border()
            game_over_win.attroff(curses.color_pair(3))
            # Enable color pair 4 permanently for content
            game_over_win.attron(curses.color_pair(4))
            
            # Game Over text
            game_over_win.addstr(2, (game_over_width - 9) // 2, "GAME OVER", curses.A_BOLD | curses.color_pair(4))
            game_over_win.addstr(4, 2, f"Your score: {self.score}", curses.color_pair(4))
            
            # New highscore?
            if self.is_highscore():
                game_over_win.addstr(6, 2, "New highscore!", curses.color_pair(4))
                game_over_win.refresh()
                
                # Name input
                curses.echo()  # Show input
                curses.curs_set(1)  # Cursor visible
                name = game_over_win.getstr(6, 20, 3).decode('utf-8').upper()
                curses.curs_set(0)  # Cursor invisible again
                curses.noecho()  # Hide input
                
                # Add highscore
                self.add_highscore(name)
            
            # Options after Game Over
            game_over_win.addstr(9, 2, "What would you like to do?", curses.color_pair(4))
            game_over_win.addstr(11, 4, "H - Show highscores", curses.color_pair(4))
            game_over_win.addstr(12, 4, "R - Restart game", curses.color_pair(4))
            game_over_win.addstr(13, 4, "ENTER - Return to menu", curses.color_pair(4))
            game_over_win.attroff(curses.color_pair(4))
            game_over_win.refresh()
            
            # Wait for input
            while True:
                key = game_over_win.getch()
                if key == ord('h') or key == ord('H'):
                    self.show_highscores()
                    # After highscores, show Game Over window again
                    game_over_win.clear()
                    game_over_win.attron(curses.color_pair(3))
                    game_over_win.border()
                    game_over_win.attroff(curses.color_pair(3))
                    game_over_win.attron(curses.color_pair(4))
                    game_over_win.addstr(2, (game_over_width - 9) // 2, "GAME OVER", curses.A_BOLD | curses.color_pair(4))
                    game_over_win.addstr(4, 2, f"Your score: {self.score}", curses.color_pair(4))
                    game_over_win.addstr(9, 2, "What would you like to do?", curses.color_pair(4))
                    game_over_win.addstr(11, 4, "H - Show highscores", curses.color_pair(4))
                    game_over_win.addstr(12, 4, "R - Restart game", curses.color_pair(4))
                    game_over_win.addstr(13, 4, "ENTER - Return to menu", curses.color_pair(4))
                    game_over_win.attroff(curses.color_pair(4))
                    game_over_win.refresh()
                elif key == curses.KEY_ENTER or key in [10, 12]:
                    break
                elif key == ord('r') or key == ord('R'):  # <--- NEW!
                    open_snake()  # Restart game

        def run(self):
            while self.running:
                # Display status
                self.draw_status()
                
                # Keyboard input
                new_direction = self.get_input()
                if new_direction and new_direction != self.direction:
                    self.direction = new_direction
                
                if not self.game_over:
                    # Move snake
                    self.move_snake()
                    
                    # Draw game field
                    self.draw_game()
                else:
                    # Show Game Over
                    self.show_game_over()
                    # Return to main menu
                    return

    # Start snake game with curses
    def start_game(stdscr):
        game = SnakeGame(stdscr)
        game.run()
        # Return to main menu - here connection to open_menu() can be made
    
    # Start curses and then return to open_menu()
    curses.wrapper(start_game)
    # After the game, open_menu() should be called
    # This would happen outside this function

    pygame.mixer.music.stop()

if __name__ == "__main__":
    open_snake()  # Can be started directly, independent of menu