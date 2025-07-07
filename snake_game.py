import pygame
import pygame.mixer
import random
import time
import curses
import json
from collections import deque

def open_snake():
    """Snake-Spiel-Hauptfunktion"""
    # Sound initialisieren
    pygame.mixer.init()
    pygame.mixer.music.load("media/maybe.mp3")  # Stelle sicher, dass die Datei im gleichen Ordner liegt
    pygame.mixer.music.play(-1)  # -1 = Endlosschleife
    # Konstanten
    DELAY = 150  # Verzögerung in Millisekunden
    HIGHSCORE_FILE = "snake_highscores.json"

    # Richtungen
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
            # Curses initialisieren
            curses.curs_set(0)  # Cursor unsichtbar machen
            curses.start_color()
            curses.use_default_colors()
            curses.init_pair(1, curses.COLOR_GREEN, -1)
            curses.init_pair(2, curses.COLOR_GREEN, -1)
            curses.init_pair(3, curses.COLOR_GREEN, -1)
            curses.init_pair(4, curses.COLOR_GREEN, -1)
            
            # Bildschirmgröße ermitteln
            self.max_y, self.max_x = self.stdscr.getmaxyx()
            
            # 16:9 Format berechnen (innerhalb der verfügbaren Größe)
            height = min(self.max_y - 6, 45)  # Höhe minus Statuszeilen
            width = min(int(height * 16/9), self.max_x - 2)  # 16:9 Verhältnis, begrenzt durch Bildschirmbreite
            
            # Spielfenster erstellen mit Umrandung
            self.height = height
            self.width = width
            
            # Position des Spielfelds berechnen (zentriert)
            self.start_y = (self.max_y - height) // 2
            self.start_x = (self.max_x - width) // 2
            
            # Spielfeld erstellen
            self.win = curses.newwin(height, width, self.start_y, self.start_x)
            self.win.keypad(True)  # Ermöglicht Pfeiltasten
            self.win.timeout(DELAY)  # Aktualisierungsrate
            
            # Status-Fenster für Score
            self.status_win = curses.newwin(3, width, self.start_y - 3, self.start_x)

        def reset_game(self):
            # Spielfeld-Größe berechnen (innen)
            self.play_height = self.height - 2
            self.play_width = self.width - 2
            
            # Schlange in der Mitte starten
            start_x = self.play_width // 4 + 1
            start_y = self.play_height // 2 + 1
            
            self.snake = deque([(start_y, start_x)])  # Koordinaten als (y, x) für curses
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
                # Standardhighscores, wenn keine Datei existiert
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
            # Neue Highscore-Einträge hinzufügen
            self.highscores.append({"name": name, "score": self.score})
            # Nach Score sortieren
            self.highscores.sort(key=lambda x: x["score"], reverse=True)
            # Auf Top 5 begrenzen
            self.highscores = self.highscores[:5]
            self.save_highscores()

        def place_food(self):
            while True:
                # Zufällige Position innerhalb des Spielfelds (Grenzen ausgeschlossen)
                y = random.randint(1, self.play_height)
                x = random.randint(1, self.play_width)
                
                # Prüfen, ob Position nicht von Schlange belegt ist
                if (y, x) not in self.snake:
                    self.food = (y, x)
                    break

        def get_input(self):
            key = self.win.getch()
            
            if key == curses.KEY_LEFT or key == ord('a'):   #links
                if self.direction != DOWN:
                    return UP
            elif key == curses.KEY_RIGHT or key == ord('d'):   #rechts
                if self.direction != UP:
                    return DOWN
            elif key == curses.KEY_UP or key == ord('w'): #hoch
                if self.direction != RIGHT:
                    return LEFT
            elif key == curses.KEY_DOWN or key == ord('s'):   #unten
                if self.direction != LEFT:
                    return RIGHT
            elif key == ord('q'):
                self.running = False
                
            return self.direction

        def move_snake(self):
            head_y, head_x = self.snake[0]
            dy, dx = self.direction
            new_head = (head_y + dy, head_x + dx)
            
            # Kollisionsprüfungen
            # Prüfen auf Kollisionen mit der Wand
            if (new_head[0] <= 0 or new_head[0] > self.play_height or
                new_head[1] <= 0 or new_head[1] > self.play_width or
                new_head in self.snake):
                self.game_over = True
                return

            # Schlangenkopf bewegen
            self.snake.appendleft(new_head)
            
            # Prüfen, ob Futter gefressen wurde
            if new_head == self.food:
                self.score += 10
                self.place_food()
            else:
                # Wenn kein Futter gefressen wurde, entferne das letzte Segment
                self.snake.pop()

        def draw_status(self):
            self.status_win.clear()
            # Score fett und grün in der Statusleiste anzeigen
            self.status_win.attron(curses.color_pair(3) | curses.A_BOLD)
            self.status_win.addstr(1, 2, f"Score: {self.score}")
            self.status_win.addstr(1, self.width - 30, "Snake | WASD / Pfeiltasten")
            self.status_win.attroff(curses.color_pair(3) | curses.A_BOLD)
            self.status_win.refresh()

        def draw_game(self):
            self.win.clear()
            # Score-Anzeige aus dem Spielfeld entfernt, da sie in draw_status angezeigt wird
            # Rand zeichnen (grün)
            self.win.attron(curses.color_pair(3))
            self.win.border()
            self.win.attroff(curses.color_pair(3))
            
            # Schlange zeichnen (grün)
            for segment in self.snake:
                y, x = segment
                self.win.addch(y, x, '0', curses.color_pair(1))
            
            # Futter zeichnen (rot)
            if self.food:
                y, x = self.food
                self.win.addch(y, x, '*', curses.color_pair(2))
            
            self.win.refresh()

        def show_highscores(self):
            # Highscore-Fenster
            hs_height = 15
            hs_width = 40
            hs_y = (self.max_y - hs_height) // 2
            hs_x = (self.max_x - hs_width) // 2

            hs_win = curses.newwin(hs_height, hs_width, hs_y, hs_x)
            hs_win.keypad(True)
            hs_win.attron(curses.color_pair(3))
            hs_win.border()
            hs_win.attroff(curses.color_pair(3))

            # Highscores überschrift
            hs_win.addstr(2, (hs_width - 10) // 2, "HIGHSCORES", curses.A_BOLD | curses.color_pair(4))

            # Highscores anzeigen
            for i, hs in enumerate(self.highscores[:5]):
                hs_win.addstr(4 + i, 5, f"{i+1}. {hs['name']}: {hs['score']}", curses.color_pair(4))

            # Rückkehr-Nachricht
            hs_win.addstr(hs_height - 2, 5, "Drücke eine Taste für zurück...", curses.color_pair(4))
            hs_win.refresh()

            # Auf Tastendruck warten
            hs_win.getch()

        def show_game_over(self):
            # Game Over-Fenster
            game_over_height = 15
            game_over_width = 40
            game_over_y = (self.max_y - game_over_height) // 2
            game_over_x = (self.max_x - game_over_width) // 2
            
            game_over_win = curses.newwin(game_over_height, game_over_width, game_over_y, game_over_x)
            game_over_win.keypad(True)
            game_over_win.attron(curses.color_pair(3))
            game_over_win.border()
            game_over_win.attroff(curses.color_pair(3))
            # Aktiviere Farbpaar 4 dauerhaft für den Inhalt
            game_over_win.attron(curses.color_pair(4))
            
            # Game Over Text
            game_over_win.addstr(2, (game_over_width - 9) // 2, "GAME OVER", curses.A_BOLD | curses.color_pair(4))
            game_over_win.addstr(4, 2, f"Dein Score: {self.score}", curses.color_pair(4))
            
            # Neuer Highscore?
            if self.is_highscore():
                game_over_win.addstr(6, 2, "Neuer Highscore! Dein Name (3 Zeichen):", curses.color_pair(4))
                game_over_win.refresh()
                
                # Namenseingabe
                curses.echo()  # Eingabe anzeigen
                curses.curs_set(1)  # Cursor sichtbar
                name = game_over_win.getstr(6, 38, 3).decode('utf-8').upper()
                curses.curs_set(0)  # Cursor wieder unsichtbar
                curses.noecho()  # Keine Eingabe anzeigen
                
                # Highscore hinzufügen
                self.add_highscore(name)
            
            # Optionen nach Game Over
            game_over_win.addstr(9, 2, "Was möchtest du tun?", curses.color_pair(4))
            game_over_win.addstr(11, 4, "H - Highscores anzeigen", curses.color_pair(4))
            game_over_win.addstr(12, 4, "R - Spiel erneut starten", curses.color_pair(4))
            game_over_win.addstr(13, 4, "ENTER - Zurück zum Menü", curses.color_pair(4))
            game_over_win.attroff(curses.color_pair(4))
            game_over_win.refresh()
            
            # Auf Eingabe warten
            while True:
                key = game_over_win.getch()
                if key == ord('h') or key == ord('H'):
                    self.show_highscores()
                    # Nach Highscores wieder Game-Over-Fenster anzeigen
                    game_over_win.clear()
                    game_over_win.attron(curses.color_pair(3))
                    game_over_win.border()
                    game_over_win.attroff(curses.color_pair(3))
                    game_over_win.attron(curses.color_pair(4))
                    game_over_win.addstr(2, (game_over_width - 9) // 2, "GAME OVER", curses.A_BOLD | curses.color_pair(4))
                    game_over_win.addstr(4, 2, f"Dein Score: {self.score}", curses.color_pair(4))
                    game_over_win.addstr(9, 2, "Was möchtest du tun?", curses.color_pair(4))
                    game_over_win.addstr(11, 4, "H - Highscores anzeigen", curses.color_pair(4))
                    game_over_win.addstr(12, 4, "R - Spiel erneut starten", curses.color_pair(4))
                    game_over_win.addstr(13, 4, "ENTER - Zurück zum Menü", curses.color_pair(4))
                    game_over_win.attroff(curses.color_pair(4))
                    game_over_win.refresh()
                elif key == curses.KEY_ENTER or key in [10, 12]:
                    break
                elif key == ord('r') or key == ord('R'):  # <--- NEU!
                    self.reset_game()

        def run(self):
            while self.running:
                # Status anzeigen
                self.draw_status()
                
                # Tastatureingabe
                new_direction = self.get_input()
                if new_direction and new_direction != self.direction:
                    self.direction = new_direction
                
                if not self.game_over:
                    # Schlange bewegen
                    self.move_snake()
                    
                    # Spielfeld zeichnen
                    self.draw_game()
                else:
                    # Game Over anzeigen
                    self.show_game_over()
                    # Zurück zum Hauptmenü
                    return

    # Snake-Spiel mit curses starten
    def start_game(stdscr):
        game = SnakeGame(stdscr)
        game.run()
        # Zurück zum Hauptmenü - hier kann die Verbindung zu open_menu() hergestellt werden
    
    # Curses starten und danach zurück zu open_menu() kehren
    curses.wrapper(start_game)
    # Nach dem Spiel sollte open_menu() aufgerufen werden
    # Dies würde außerhalb dieser Funktion passieren

    pygame.mixer.music.stop()

if __name__ == "__main__":
    open_snake()  # Direkt startbar, unabhängig vom Menü