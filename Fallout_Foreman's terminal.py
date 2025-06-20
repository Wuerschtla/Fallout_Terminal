import os
import time
import sys
import pygame
import time
from FO4Codes.modules.passwordgame import run_password_game

base_path = os.path.dirname(os.path.abspath(__file__))

DEVMODE = False
MAINVOL = 1   # dampening factor for all volume settings; default = 1
DOOR = "CLOSED"

# Leds und schalter schalter= leds_on ; taster= schortcutmenü 1,2,3



#================================================
# Sound system
#================================================

os.environ["SDL_AUDIODRIVER"] = "alsa"
#os.environ["SDL_VIDEODRIVER"] = "dummy"  # we don't use the pygame video driver. We just need to load it headlessly for the event system

Clack_path = "media/FalloutSoundClack.mp3"
Clicking_path = "media/FalloutSoundClicking.mp3"
Error_path = "media/FalloutSoundError.wav"
Unlocked_path = "media/FalloutSoundUnlocked.wav"
Complete_path = "media/FalloutSoundComplete.wav"
poweron_path = "media/sounds_poweron.mp3"


# Background Music for Snake

TRACKS = [
    "media/SnakeMusic/Level_1.ogg",
    "media/SnakeMusic/Level_2.ogg",
    "media/SnakeMusic/Level_3.ogg",
    "media/SnakeMusic/Level_4.ogg",
    "media/SnakeMusic/Level_5.ogg"
]

# Initialisiere Pygame-Mixer
pygame.mixer.pre_init(frequency=22050, size=-16, channels=2, buffer=1024)
pygame.mixer.init()
#pygame.display.init()    # brings up the event system

# volume for background music
pygame.mixer.music.set_volume(0.1*MAINVOL)

# # Custom events for background music
MUSIC_END_EVENT = pygame.USEREVENT + 1

# # Post MUSIC_END_EVENT when a track finishes
pygame.mixer.music.set_endevent(MUSIC_END_EVENT)

external_channel = pygame.mixer.Channel(0)
internal_channel = pygame.mixer.Channel(1)
#external_channel_2 = pygame.mixer.Channel(2)

current_track = 0       # defines the "level" of the current bg music
switch_pending = False  # if set to True, the next track will rise +1 on the next cycle

Clack = pygame.mixer.Sound(Clack_path)
Clicking = pygame.mixer.Sound(Clicking_path)
Error = pygame.mixer.Sound(Error_path)
Unlocked = pygame.mixer.Sound(Unlocked_path)
Complete = pygame.mixer.Sound(Complete_path)
poweron = pygame.mixer.Sound(poweron_path)

#first parameter = leftvol = internal, second = right_vol = external

def play_Clack():    
    global MAINVOL
    external_channel.stop()    
    external_channel.set_volume(0.15*MAINVOL, 0.15*MAINVOL)
    external_channel.play(Clack)

def play_Clicking():
    global MAINVOL
    internal_channel.stop()    
    internal_channel.set_volume(0.06*MAINVOL, 0.06*MAINVOL)
    internal_channel.play(Clicking)

def play_Error():
    global MAINVOL
    external_channel.stop()
    external_channel.set_volume(0.2*MAINVOL, 0.2*MAINVOL)
    external_channel.play(Error)

def play_Unlocked():
    global MAINVOL
    external_channel.stop()
    external_channel.set_volume(0.3*MAINVOL, 0.3*MAINVOL)
    external_channel.play(Unlocked)

def play_Complete():
    global MAINVOL
    external_channel.stop()
    external_channel.set_volume(0.1*MAINVOL, 0.1*MAINVOL)
    external_channel.play(Complete)

def play_poweron():
    global MAINVOL
    external_channel.stop()
    external_channel.set_volume(0.3*MAINVOL, 0.3*MAINVOL)
    external_channel.play(poweron)

#system defs#

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Global variable to manage created files
created_files = []

# Global variable to control current mode
current_mode = None


def print_green(text, end="\n"):
    print("\033[92m" + text, end=end)
    
def print_green_text(text):
    for char in text:
        sys.stdout.write("\033[92m" + char)
        sys.stdout.flush()
        if DEVMODE == False:
            time.sleep(0.008)  # Kurze Pause, um den Text schnell erscheinen zu lasse

def get_green_input(prompt):
    #return input("\033[92m" + prompt + "\033[0m")
    return input(prompt)

def open_menu():
    clear_screen()
    menu_text = """
========== ROBCO INDUSTRIES UNIFIED OPERATING SYSTEM ==========
============ COPYRIGHT 2075-2077 ROBCO INDUSTRIES =============

[1.   Financi§l Reßort§    ]
[2.   Saf»y Rep''rts       ]
[3.   Foreman's Log        ]
[4.   Security Door Control]
[5.   Close Terminal       ]

"""
    play_Clicking()
    print_green_text(menu_text)
    Clicking.stop()
    play_Clack()

    while True:
        try:
            command = get_green_input("> ").strip().lower()

            if command == "5":
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
            else:
                print_green_text("unknown command\nPress Enter...")
                input
                open_menu()

        except (EOFError, KeyboardInterrupt):
            break

def open_Foremans_Log_menu():
    while True:
        try:
            command = get_green_input("> ").strip().lower()

            if command == "openmenu":
                open_menu()
            elif command == "exit":
                break
            elif command == "1":
                open_3_1()
            elif command == "2":
                open_3_2()
            elif command == "3":
                open_3_3()
            elif command == "4":
                open_3_4()
            elif command == "":
                open_menu()
            elif command == "exit":
                break    
            else:
                print_green_text("unknown command\nPress Enter...")
                input()

        except (EOFError, KeyboardInterrupt):
            break

def open_door_control_menu():
    while True:
        try:
            command = get_green_input("> ").strip().lower()

            if command == "openmenu":
                open_menu()
            elif command == "exit":
                break
            elif command == "1":
                opendoor()
            elif command == "2":
                closedoor()
            elif command == "":
                open_menu()
            elif command == "exit":
                break    
            else:
                print_green_text("unknown command\nPress Enter...")
                input()

        except (EOFError, KeyboardInterrupt):
            break

def open_1():
    clear_screen()
    if DEVMODE == False:
        play_Clicking()
        print_green_text("Loading...")
        time.sleep(2)
        Clicking.stop()
    clear_screen()
    print_green_text("[1.   Financi§l Reßort§    ]\n")  
    print_green("\n")  
    filepath_menu1 = "FalloutDocuments/Financi§l Reßort§.md"
    try:
        with open(filepath_menu1, "r", encoding="utf-8") as file:
            content = file.read()
            print_green_text(content)
            print_green("\n")
            play_Clack()
            print_green_text("Press Enter to return to Menu...")
    except FileNotFoundError:
        print_green_text("file not found")

def open_2():
    clear_screen()
    if DEVMODE == False:
        play_Clicking()
        print_green_text("Loading...")
        time.sleep(2)
        Clicking.stop()
    clear_screen()
    print_green_text("[2.   Saf»y Rep''rts       ]\n")  
    print_green("\n") 
    filepath_menu2 = "FalloutDocuments/Saf»y Rep''rts.md"
    try:
        with open(filepath_menu2, "r", encoding="utf-8") as file:
            content = file.read()
            print_green_text(content)
            print_green("\n")
            play_Clack()
            print_green_text("Press Enter to return to Menu...")
    except FileNotFoundError:
        print_green_text(f"Datei '{filepath_menu2}' nicht gefunden.")

def open_3():
    clear_screen()
    if DEVMODE == False:
        play_Clicking()
        print_green_text("Loading...")
        time.sleep(2)
        Clicking.stop()
    clear_screen()
    Foremans_Log_menu_text = """
========== ROBCO INDUSTRIES UNIFIED OPERATING SYSTEM ==========
============ COPYRIGHT 2075-2077 ROBCO INDUSTRIES =============

[Foreman's Log]
    
    [1.   New Leaves   ]
    [2.   War...       ]
    [3.   Incoming?    ]
    [4.   The Day After]
    
    [Enter to return to Mainmenu]

"""
    play_Clicking()
    print_green_text(Foremans_Log_menu_text)
    Clicking.stop()
    play_Clack()
    open_Foremans_Log_menu()

def open_3_1():
    clear_screen()
    if DEVMODE == False:
        play_Clicking()
        print_green_text("Loading...")
        time.sleep(2)
        Clicking.stop()
    clear_screen()
    print_green_text("[1.   New Leaves   ]\n")  
    print_green("\n")  
    filepath_menu1 = "FalloutDocuments/Foreman's Log/New Leaves.md"
    try:
        with open(filepath_menu1, "r", encoding="utf-8") as file:
            content = file.read()
            print_green_text(content)
            print_green("\n")
            play_Clack()
            print_green_text("Press Enter to return...")
            input()
            open_3()
            
    except FileNotFoundError:
        print_green_text("file not found")

def open_3_2():
    clear_screen()
    if DEVMODE == False:
        play_Clicking()
        print_green_text("Loading...")
        time.sleep(2)
        Clicking.stop()
    clear_screen()
    print_green_text("[2.   War...       ]\n")  
    print_green("\n")  
    filepath_menu1 = "FalloutDocuments/Foreman's Log/War....md"
    try:
        with open(filepath_menu1, "r", encoding="utf-8") as file:
            content = file.read()
            print_green_text(content)
            print_green("\n")
            play_Clack()
            print_green_text("Press Enter to return...")
            input()
            open_3()
            
    except FileNotFoundError:
        print_green_text("file not found")

def open_3_3():
    clear_screen()
    if DEVMODE == False:
        play_Clicking()
        print_green_text("Loading...")
        time.sleep(2)
        Clicking.stop()
    clear_screen()
    print_green_text("[3.   Incoming?    ]\n")  
    print_green("\n")  
    filepath_menu1 = "FalloutDocuments/Foreman's Log/Incoming?.md"
    try:
        with open(filepath_menu1, "r", encoding="utf-8") as file:
            content = file.read()
            print_green_text(content)
            print_green("\n")
            play_Clack()
            print_green_text("Press Enter to return...")
            input()
            open_3()
            
    except FileNotFoundError:
        print_green_text("file not found")

def open_3_4():
    clear_screen()
    if DEVMODE == False:
        play_Clicking()
        print_green_text("Loading...")
        time.sleep(2)
        Clicking.stop()
    clear_screen()
    print_green_text("[4.   The Day After]\n")  
    print_green("\n")  
    filepath_menu1 = "FalloutDocuments/Foreman's Log/The Day After.md"
    try:
        with open(filepath_menu1, "r", encoding="utf-8") as file:
            content = file.read()
            print_green_text(content)
            print_green("\n")
            play_Clack()
            print_green_text("Press Enter to return...")
            input()
            open_3()
            
    except FileNotFoundError:
        print_green_text("file not found")

def open_4():
    clear_screen()
    if DEVMODE == False:
        play_Clicking()
        print_green_text("Loading...")
        time.sleep(2)
        Clicking.stop()
    clear_screen()
    Door_Control_menu = """
========== ROBCO INDUSTRIES UNIFIED OPERATING SYSTEM ==========
============ COPYRIGHT 2075-2077 ROBCO INDUSTRIES =============

[MaxLock Security Door Control Interface]

STATUS: """+DOOR+"""

    [1.   Open Door ]
    [2.   Close Door]

    [Enter to return to Mainmenu]

"""

    play_Clicking()
    print_green_text(Door_Control_menu)
    Clicking.stop()
    play_Clack()
    open_door_control_menu()

def opendoor():
    global DOOR
    clear_screen()
    DOOR = "OPEN"
    if DEVMODE == False:
        play_Clicking()
        print_green_text("Opening doors...\n")
        print_green("\n")
        time.sleep(2)
        Clicking.stop()
    print_green_text("Enter to return...\n")    
    
    open_door_control_menu()

def closedoor():
    global DOOR
    clear_screen()
    DOOR = "CLOSED"
    if DEVMODE == False:
        play_Clicking()
        print_green_text("Sealing doors...\n")
        print_green("\n")
        time.sleep(2)
        Clicking.stop()
    print_green_text("Enter to return...\n")    
    
    open_door_control_menu()


def main():
    
    global current_mode
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
    if DEVMODE == False:
        run_password_game()
    else:
        clear_screen()
        play_Clicking()
        print_green_text(terminal_text)
        if DEVMODE == False:
            time.sleep(2)
    open_menu()
    

if __name__ == "__main__":
    main()
