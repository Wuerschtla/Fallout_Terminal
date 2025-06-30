import os
import time
import sys
import pygame
from modules.passwordgame import run_password_game

base_path = os.path.dirname(os.path.abspath(__file__))

DEVMODE = False
MAINVOL = 1
DOOR = "CLOSED"

# Paths
FOREMANS_LOG_PATH = os.path.join("FalloutDocuments", "Foreman's Log")

# ================ Sound system =================

if os.name == "nt":
    os.environ["SDL_AUDIODRIVER"] = "directsound"

Clack_path = "media/FalloutSoundClack.mp3"
Clicking_path = "media/FalloutSoundClicking.mp3"
Error_path = "media/FalloutSoundError.wav"
Unlocked_path = "media/FalloutSoundUnlocked.wav"
Complete_path = "media/FalloutSoundComplete.wav"
poweron_path = "media/sounds_poweron.mp3"

SOUND_ENABLED = True

try:
    pygame.mixer.pre_init(frequency=22050, size=-16, channels=1, buffer=1024)
    pygame.mixer.init()
except pygame.error as e:
    print(f"⚠️  Sound could not be initialized: {e}")
    SOUND_ENABLED = False

if SOUND_ENABLED:
    external_channel = pygame.mixer.Channel(0)
    internal_channel = pygame.mixer.Channel(1)

    Clack = pygame.mixer.Sound(Clack_path)
    Clicking = pygame.mixer.Sound(Clicking_path)
    Error = pygame.mixer.Sound(Error_path)
    Unlocked = pygame.mixer.Sound(Unlocked_path)
    Complete = pygame.mixer.Sound(Complete_path)
    poweron = pygame.mixer.Sound(poweron_path)

# =============== Sound functions ===============
def play_Clack():
    if SOUND_ENABLED:
        external_channel.stop()
        external_channel.set_volume(0.15 * MAINVOL)
        external_channel.play(Clack)

def play_Clicking():
    if SOUND_ENABLED:
        internal_channel.stop()
        internal_channel.set_volume(0.03 * MAINVOL)
        internal_channel.play(Clicking)

def play_Error():
    if SOUND_ENABLED:
        external_channel.stop()
        external_channel.set_volume(0.2 * MAINVOL)
        external_channel.play(Error)

def play_Unlocked():
    if SOUND_ENABLED:
        external_channel.stop()
        external_channel.set_volume(0.3 * MAINVOL)
        external_channel.play(Unlocked)

def play_Complete():
    if SOUND_ENABLED:
        external_channel.stop()
        external_channel.set_volume(0.1 * MAINVOL)
        external_channel.play(Complete)

def play_poweron():
    if SOUND_ENABLED:
        external_channel.stop()
        external_channel.set_volume(0.3 * MAINVOL)
        external_channel.play(poweron)

# =============== System defs ===================
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_green(text, end="\n"):
    print("\033[92m" + text, end=end)

def print_green_text(text):
    for char in text:
        sys.stdout.write("\033[92m" + char)
        sys.stdout.flush()
        if not DEVMODE:
            time.sleep(0.008)

def get_green_input(prompt):
    return input(prompt)

# =============== Main Menus ====================
def open_menu():
    clear_screen()
    menu_text = """
========== ROBCO INDUSTRIES UNIFIED OPERATING SYSTEM ==========
============ COPYRIGHT 2075-2077 ROBCO INDUSTRIES =============

[1.   Financi§l Reßort§    ]
[2.   Saf»y Rep''rts       ]
[3.   Foreman's Log        ]
[4.   Security Door Control]
[5.   Play Tetris          ]
[6.   Close Terminal       ]

"""
    play_Clicking()
    print_green_text(menu_text)
    Clicking.stop()
    play_Clack()

    while True:
        try:
            command = get_green_input("> ").strip().lower()
            if command == "6":
                print_green_text("closing Terminal...")
                time.sleep(2)
                exit()
            elif command == "1":
                open_1()
            elif command == "2":
                open_2()
            elif command == "3":
                open_3()
            elif command == "4":
                open_4()
            elif command == "5":
                play_tetris()

            else:
                print_green_text("unknown command\nPress Enter...")
                input()
                open_menu()
        except (EOFError, KeyboardInterrupt):
            break

def open_1():
    load_and_display_md("FalloutDocuments/Financi§l Reßort§.md")

def open_2():
    load_and_display_md("FalloutDocuments/Saf»y Rep''rts.md")

def open_4():
    clear_screen()
    if not DEVMODE:
        play_Clicking()
        print_green_text("Loading...")
        time.sleep(2)
        Clicking.stop()
    clear_screen()
    Door_Control_menu = f"""
========== ROBCO INDUSTRIES UNIFIED OPERATING SYSTEM ==========
============ COPYRIGHT 2075-2077 ROBCO INDUSTRIES =============

[MaxLock Security Door Control Interface]

STATUS: {DOOR}

    [1.   Open Door ]
    [2.   Close Door]

    [Enter to return to Mainmenu]

"""
    play_Clicking()
    print_green_text(Door_Control_menu)
    Clicking.stop()
    play_Clack()
    open_door_control_menu()

def open_door_control_menu():
    while True:
        try:
            command = get_green_input("> ").strip().lower()
            if command == "openmenu" or command == "":
                open_menu()
            elif command == "1":
                opendoor()
            elif command == "2":
                closedoor()
            elif command == "exit":
                break
            else:
                print_green_text("unknown command\nPress Enter...")
                input()
        except (EOFError, KeyboardInterrupt):
            break

def opendoor():
    global DOOR
    clear_screen()
    DOOR = "OPEN"
    if not DEVMODE:
        play_Clicking()
        print_green_text("Opening doors...\n")
        time.sleep(2)
        Clicking.stop()
    print_green_text("Enter to return...\n")    
    open_door_control_menu()

def closedoor():
    global DOOR
    clear_screen()
    DOOR = "CLOSED"
    if not DEVMODE:
        play_Clicking()
        print_green_text("Sealing doors...\n")
        time.sleep(2)
        Clicking.stop()
    print_green_text("Enter to return...\n")    
    open_door_control_menu()

# ============ Foreman's Log ====================
def open_3():
    clear_screen()
    if not DEVMODE:
        play_Clicking()
        print_green_text("Loading...")
        time.sleep(2)
        Clicking.stop()
    clear_screen()

    try:
        entries = [f for f in os.listdir(FOREMANS_LOG_PATH) if f.lower().endswith(".md")]
        entries.sort()
    except FileNotFoundError:
        entries = []

    Foremans_Log_menu_text = """
========== ROBCO INDUSTRIES UNIFIED OPERATING SYSTEM ==========
============ COPYRIGHT 2075-2077 ROBCO INDUSTRIES =============

[Foreman's Log]
"""
    for i, entry in enumerate(entries, 1):
        name = os.path.splitext(entry)[0]
        Foremans_Log_menu_text += f"\n    [{i}.   {name}]"

    Foremans_Log_menu_text += f"\n    [{len(entries)+1}.   Create new log entry]"
    Foremans_Log_menu_text += "\n\n    [Enter to return to Mainmenu]\n"

    play_Clicking()
    print_green_text(Foremans_Log_menu_text)
    Clicking.stop()
    play_Clack()
    open_Foremans_Log_menu(entries)

def open_Foremans_Log_menu(entries):
    while True:
        try:
            command = get_green_input("> ").strip().lower()

            if command == "" or command == "openmenu":
                open_menu()
            elif command.isdigit():
                choice = int(command)
                if 1 <= choice <= len(entries):
                    filename = entries[choice - 1]
                    open_log_entry(filename)
                elif choice == len(entries) + 1:
                    create_new_log_entry()
                else:
                    print_green_text("Unknown command\nPress Enter...")
                    input()
            elif command == "exit":
                break
            else:
                print_green_text("Unknown command\nPress Enter...")
                input()
        except (EOFError, KeyboardInterrupt):
            break

def open_log_entry(filename):
    clear_screen()
    if not DEVMODE:
        play_Clicking()
        print_green_text("Loading...")
        time.sleep(2)
    clear_screen()
    print_green_text(f"[{filename}]\n\n")
    path = os.path.join(FOREMANS_LOG_PATH, filename)
    try:
        with open(path, "r", encoding="utf-8") as file:
            content = file.read()
            print_green_text(content)
            print_green("\n")
            Clicking.stop()
            play_Clack()
            print_green_text("Press Enter to return...")
            input()
            open_3()
    except FileNotFoundError:
        print_green_text("File not found")

def create_new_log_entry():
    clear_screen()
    print_green_text("=== Create New Foreman's Log Entry ===\n")
    title = get_green_input("Entry title: ").strip()
    if not title:
        print_green_text("Cancelled. Returning to Foreman's Log Menu...")
        time.sleep(2)
        open_3()
        return
    safe_title = "".join(c for c in title if c.isalnum() or c in (" ", "-", "_")).rstrip()
    filename = f"{safe_title}.md"
    filepath = os.path.join(FOREMANS_LOG_PATH, filename)
    print_green_text("\nEnter content (type 'END' on its own line to finish):\n")
    lines = []
    while True:
        line = input()
        if line.strip().upper() == "END":
            break
        lines.append(line)
    content = "\n".join(lines)
    if not content.strip():
        print_green_text("No content entered. Returning...")
        time.sleep(2)
        open_3()
        return
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print_green_text(f"\nEntry saved as '{filename}'!")
    except Exception as e:
        print_green_text(f"\nError saving entry: {e}")
    time.sleep(2)
    open_3()

def load_and_display_md(filepath):
    clear_screen()
    if not DEVMODE:
        play_Clicking()
        print_green_text("Loading...")
        time.sleep(2)
    clear_screen()
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            content = file.read()
            print_green_text(content)
            print_green("\n")
            Clicking.stop()
            play_Clack()
            print_green_text("Press Enter to return to Menu...")
            input()
            open_menu()
    except FileNotFoundError:
        print_green_text(f"File '{filepath}' not found.")

def main():
    clear_screen()
    welcome_message = """
Welcome to ROBCO Industries (TM) Termlink

-----------------
Password required
-----------------

Press Enter to continue...
"""
    terminal_text = """
Initializing...

[Initializing]
[Loading System...]
[Starting Protocol...]
[Connecting to Database...]

CONNECTED
"""
    play_poweron()
    print_green_text(welcome_message)
    input()
    if not DEVMODE:
        run_password_game()
    else:
        clear_screen()
        play_Clicking()
        print_green_text(terminal_text)
        if not DEVMODE:
            time.sleep(2)
    open_menu()

def play_tetris():
    clear_screen()
    print_green_text("Launching Tetris...\n")
    time.sleep(1)
    os.system(f"{sys.executable} tetris_game.py")
    print_green_text("\nReturning to ROBCO Terminal...")
    time.sleep(2)
    open_menu()

if __name__ == "__main__":
    main()
