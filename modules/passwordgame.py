import os
import time
import sys
import pygame
import random
import time

DEVMODE = False  # Set to True for faster output
MAINVOL = 1   # dampening factor for all volume settings; default = 1

#================================================
# Sound system
#================================================

# Set SDL audio driver to coreaudio for macOS
os.environ["SDL_AUDIODRIVER"] = "coreaudio"
#os.environ["SDL_VIDEODRIVER"] = "dummy"  # we don't use the pygame video driver. We just need to load it headlessly for the event system

Clack_path = "media/FalloutSoundClack.mp3"
Clicking_path = "media/FalloutSoundClicking.mp3"
Error_path = "media/FalloutSoundError.wav"
Unlocked_path = "media/FalloutSoundUnlocked.wav"
Complete_path = "media/FalloutSoundComplete.wav"

# Initialisiere Pygame-Mixer
try:
    pygame.mixer.pre_init(frequency=11025, size=-16, channels=1, buffer=2048)
    pygame.mixer.init()
except pygame.error as e:
    print(f"⚠️  Sound konnte nicht initialisiert werden (passwordgame): {e}")
#pygame.display.init()    # brings up the event system

external_channel = pygame.mixer.Channel(0)
internal_channel = pygame.mixer.Channel(1)

Clack = pygame.mixer.Sound(Clack_path)
Clicking = pygame.mixer.Sound(Clicking_path)
Error = pygame.mixer.Sound(Error_path)
Unlocked = pygame.mixer.Sound(Unlocked_path)
Complete = pygame.mixer.Sound(Complete_path)

def play_Clack():    
    global MAINVOL
    external_channel.stop()    
    external_channel.set_volume(0.15*MAINVOL)
    external_channel.play(Clack)

def play_Clicking():
    global MAINVOL
    internal_channel.stop()    
    internal_channel.set_volume(0.03*MAINVOL)
    internal_channel.play(Clicking)

def play_Error():
    global MAINVOL
    external_channel.stop()
    external_channel.set_volume(0.2*MAINVOL)
    external_channel.play(Error)

def play_Unlocked():
    global MAINVOL
    external_channel.stop()
    external_channel.set_volume(0.3*MAINVOL)
    external_channel.play(Unlocked)

def play_Complete():
    global MAINVOL
    external_channel.stop()
    external_channel.set_volume(0.1*MAINVOL)
    external_channel.play(Complete)
    sys.stdout.write("\033[1A")  # Cursor eine Zeile nach oben
    sys.stdout.flush()



def print_green_text(text):
    for char in text:
        sys.stdout.write("\033[92m" + char)
        sys.stdout.flush()
        if not DEVMODE:
            time.sleep(0.008)

def print_fast(text):
    sys.stdout.write("\033[92m" + text)
    sys.stdout.flush()

WORD_BANK = [
    "CONSIST", "ROAMING", "GAINING", "FARMING", "STERILE", "ENGLISH",
    "FENCING", "MANKIND", "MORNING", "HEALING", "LEAVING", "CORRECT",
    "JESSICA", "CONTACT", "NUCLEAR", "SCIENCE", "CONTROL", "FALLOUT",
    "DISABLE", "UPGRADE", "SYSTEMS", "NETWORK", "PROCESS", "PROGRAM",
    "DIGITAL", "MACHINE", "KEYCARD", "SCANNER", "CHAMBER", "REACTOR",
    "TESTING", "HUNTING", "COOKING", "WALKING", "SITTING", "TALKING",
    "WRITING", "READING", "WORKING", "PLAYING", "WINNING", "RUNNING"
]

def generate_random_chars(length):
    special_chars = "+#*$&)(=!?<>-_.,;:/"
    return ''.join(random.choice(special_chars) for _ in range(length))

from collections import Counter

def calculate_matches(guess, correct):
    guess = guess.upper()
    correct = correct.upper()
    guess_counter = Counter(guess)
    correct_counter = Counter(correct)
    return sum(min(guess_counter[char], correct_counter[char]) for char in guess_counter)

def generate_terminal_display(passwords):
    display = []
    display.append("")
    display.append("ENTER PASSWORD NOW")
    display.append("")  # Extra newline before address block
    
    # Ungefähr 16 Wörter (Passwörter + Füllwörter), der Rest wird mit Random Chars gefüllt
    filler_words = [
        "LOADING", "NETWORK", "SYSTEMS", "UPGRADE", "PROCESS",
        "CONTROL", "REACTOR", "SCANNER", "MACHINE", "DIGITAL",
        "PROGRAM", "CHAMBER", "TESTING", "HEALTH", "CONTACT"
    ]

    passwords = list(set(passwords))  # Duplikate vermeiden
    passwords = [w for w in passwords if w != ""]  # leere Wörter filtern
    correct = [w for w in passwords if w in WORD_BANK]  # nur echte Wörter
    used_words = random.sample(correct, min(len(correct), 16))

    word_count = min(16, len(used_words) + len(filler_words))
    used_words += random.sample(filler_words, max(0, word_count - len(used_words)))
    all_content = [("word", (w + generate_random_chars(12 - len(w)))[:12]) for w in used_words]

    # Garantiert zwei Bonuszeichenfolgen in all_content einfügen
    special_chars = "+#*$&)(=!?<>-_.,;:/"
    bonus_codes = []
    while len(bonus_codes) < 2:
        c = random.choice(special_chars)
        if c * 3 not in bonus_codes:
            bonus_codes.append(c * 3)

    for code in bonus_codes:
        entry = code + generate_random_chars(9)
        all_content.append(("random", entry[:12]))

    active_bonus_inputs = []
    for entry in all_content:
        if entry[0] == "random":
            for i in range(len(entry[1]) - 2):
                if entry[1][i] == entry[1][i+1] == entry[1][i+2]:
                    sequence = entry[1][i]*3
                    if sequence not in active_bonus_inputs:
                        active_bonus_inputs.append(sequence)

    # Fülle den Rest auf 32 mit Random Chars, ohne dass drei gleiche Zeichen hintereinander sind
    def is_valid_random_string(s):
        return all(s[i] != s[i+1] or s[i] != s[i+2] for i in range(len(s) - 2))

    while len(all_content) < 32:
        s = generate_random_chars(12)
        while not is_valid_random_string(s):
            s = generate_random_chars(12)
        all_content.append(("random", s))

    random.shuffle(all_content)

    content_index = 0
    for line in range(16):
        addr1 = f"0x{0xF4F0 + line * 20:04X}"
        addr2 = f"0x{0xF4F0 + line * 20 + 14:04X}"
        # Ensure passwords are exactly 12 chars long, already padded above
        content1 = all_content[content_index][1][:12]
        content_index += 1
        content2 = all_content[content_index][1][:12]
        content_index += 1
        display.append(f"{addr1} {content1.ljust(12)}  {addr2} {content2}")

    display.append("")
    return display, active_bonus_inputs, all_content

def overlay_guess_feedback(display_lines, attempts_left, guess_history):
    overlay = display_lines[:]
    overlay[2] = f"{attempts_left} ATTEMPT(S) LEFT: " + "■ " * attempts_left + "\n"
    overlay.insert(3, "")

    # Stelle sicher, dass genug Platz vorhanden ist für alle Versuche (2 Zeilen pro Versuch)
    required_lines = 4 + len(guess_history) * 2
    while len(overlay) < required_lines:
        overlay.append("")

    start_line = len(overlay) - (len(guess_history) * 2) - 1

    for i, (guess, match) in enumerate(guess_history[-16:]):  # maximal 8 Versuche sichtbar
        line_index = start_line + i * 2
        overlay[line_index] = overlay[line_index][:43].rstrip().ljust(43) + f">{guess}"
        if line_index + 1 < len(overlay):
            overlay[line_index + 1] = overlay[line_index + 1][:43].rstrip().ljust(43) + f">{match}/{len(guess)} correct"

    if attempts_left == 0:
        overlay.append("".ljust(43) + ">Entry denied")
        overlay.append("".ljust(43) + ">TERMINAL LOCKED")
        overlay.append("".ljust(43) + f">Correct password was: {guess_history[-1][0]}")

    return overlay


def play_terminal_game():
    while True:
        correct_password = random.choice(WORD_BANK)
        others = [w for w in WORD_BANK if w != correct_password]
        display_passwords = random.sample(others, random.randint(5, 9)) + [correct_password]
        random.shuffle(display_passwords)

        attempts = 4
        guess_history = []
        display_cache, bonus_codes, all_content = generate_terminal_display(display_passwords)

        def generate_new_bonus_string():
            special_chars = "+#*$&)(=!?<>-_.,;:/"
            while True:
                s = ''.join(random.choice(special_chars) for _ in range(12))
                # Check no three identical chars in a row
                if all(s[i] != s[i+1] or s[i] != s[i+2] for i in range(len(s)-2)):
                    return s

        while attempts > 0:
            print("\033[2J\033[H", end="")

            full_display = overlay_guess_feedback(display_cache, attempts, guess_history)
            if not guess_history:
                play_Clicking()
                print_green_text("\n".join(full_display))
                Clicking.stop()
            else:
                print_fast("\n".join(full_display))
            print_fast("\n")
            print_fast("\n")
            print_fast(">")
            play_Clack()
            user_input = input().strip().upper()

            # Auch mit dem versteckten Befehl "SUDO CONTINUE" kann das Spiel gewonnen werden
            if user_input == correct_password or user_input == "ROBCO":
                matches = calculate_matches(user_input, correct_password)
                guess_history.append((user_input, matches))
                print("\033[2J\033[H", end="")  # Bildschirm löschen vor Anzeige
                full_display = overlay_guess_feedback(display_cache, attempts, guess_history)
                full_display[-4] = full_display[-4][:43].rstrip().ljust(43) + f">{user_input}"
                full_display[-3] = full_display[-3][:43].rstrip().ljust(43) + f">{matches}/{len(correct_password)} correct."
                full_display[-2] = full_display[-2][:43].rstrip().ljust(43) + ">Entry accepted"
                print_fast("\n".join(full_display))
                play_Unlocked()
                time.sleep(2)
                print_green_text("\n>Press Enter to continue...")
                time.sleep(0.8)
                input()
                return
            elif user_input in bonus_codes:
                attempts += 1
                external_channel.stop()
                external_channel.set_volume(0.1*MAINVOL)
                external_channel.play(Complete)
                bonus_codes.remove(user_input)
                # Replace the matching bonus string in display_cache with a new random 12-char string without triple repeats
                for i in range(len(display_cache)):
                    line = display_cache[i]
                    parts = line.split()
                    if len(parts) >= 4:
                        if parts[1].startswith(user_input):
                            new_str = generate_new_bonus_string()
                            parts[1] = new_str.ljust(12)
                            display_cache[i] = f"{parts[0]} {parts[1]}  {parts[2]} {parts[3]}"
                            break
                        elif parts[3].startswith(user_input):
                            new_str = generate_new_bonus_string()
                            parts[3] = new_str.ljust(12)
                            display_cache[i] = f"{parts[0]} {parts[1]}  {parts[2]} {parts[3]}"
                            break
            else:
                matches = calculate_matches(user_input, correct_password)
                guess_history.append((user_input, matches))
                attempts -= 1

                if attempts == 0:
                    print("\033[2J\033[H", end="")
                    play_Error()
                    # Diese Infos sind bereits im Overlay
                    print_green_text("Entry denied!\n")
                    print_green_text("next attempt in 5 sec")
                    time.sleep(0.7)
                    print("\033[2J\033[H", end="")
                    print_green_text("Entry denied!\n")
                    print_green_text("next attempt in 4 sec")
                    time.sleep(0.7)
                    print("\033[2J\033[H", end="")
                    print_green_text("Entry denied!\n")
                    print_green_text("next attempt in 3 sec")
                    time.sleep(0.7)
                    print("\033[2J\033[H", end="")
                    print_green_text("Entry denied!\n")
                    print_green_text("next attempt in 2 sec")
                    time.sleep(0.7)
                    print("\033[2J\033[H", end="")
                    print_green_text("Entry denied!\n")
                    print_green_text("next attempt in 1 sec")
                    time.sleep(0.7)
                    continue

def run_password_game():
    play_terminal_game()


# >>> einfügen wenn starten ohne Hauptprogramm <<<
#if __name__ == "__main__":
#    run_password_game()