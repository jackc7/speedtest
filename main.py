# 8/29/2020

from time import time, sleep
from logger import logger
from colorama import Fore

import readchar
import random
import sys


text = None

menu_speed = 1 # sleep() seconds
countdown = 5 # 3 = 3, 2, 1 go. 2 = 2, 1 go.


def end(starting_time):
    ending_time = time()
    time_diff = ending_time - starting_time

    return time_diff


def random_paragraph():
    with open("sentences.txt", "r") as file:
        random_number = random.randint(0, 49)
        lines = file.readlines()
        random_paragraph = lines[random_number][:-1]

    return random_paragraph


def body(paragraph):
    for i in range(countdown, 0, -1):
        print("\033c" + paragraph + Fore.LIGHTGREEN_EX +  f"\n\nStarting in {i} seconds...")
        sleep(1)

    global text
    text = []

    start = time()

    for i in range(len(paragraph)):
        print('\033c' + Fore.GREEN + "".join(text) + Fore.WHITE + paragraph[i:])

        try:
            button = readchar.readchar().decode("utf-8")

            # Checks if typed letter is wrong.
            if button != paragraph[i]:
                time_delta = end(start)

                wpm = round(len(text) / 5 / time_delta * 60)
                logger(f"Typo [{wpm}wpm] | {''.join(text)} <- Here | Typed '{button}' instead of '{paragraph[i]}'", "log.txt", start)

                return time_delta, False

            text.append(button)
            
        except: # If invalid key pressed.
            time_delta = end(start)

            wpm = round(len(text) / 5 / time_delta * 60)
            logger(f"Invalid Keypress [{wpm}wpm] | {''.join(text)} <- Here", "log.txt", start)

            return time_delta, False

        if "".join(text) == paragraph: # Checks if what you typed is the same as the given paragraph.
            time_delta = end(start)

            wpm = round(len(text) / 5 / time_delta * 60)
            logger(f"Completed Successfully [{wpm}wpm] | {''.join(text)}", "log.txt", start)

            return time_delta, True


def menu():
    paragraph = random_paragraph()
    
    print("\033c" + Fore.YELLOW + "Typing Speed Test: Press" + Fore.LIGHTYELLOW_EX + " any button " + Fore.YELLOW + "to begin." + Fore.WHITE)
    readchar.readkey()

    time_delta, is_complete = body(paragraph)

    if is_complete is False:
        wpm = len(text) / 5 / time_delta * 60
        print('\033c' + Fore.RED + "Incorrect" + Fore.WHITE + ". " + Fore.GREEN + str(round(wpm)) + Fore.WHITE + " words per minute.")
        sleep(menu_speed)

    else:
        wpm = len(text) / 5 / time_delta * 60
        print("\033c" + f"Sentence completed at {Fore.GREEN + str(round(wpm)) + Fore.WHITE} words per minute")
        sleep(menu_speed)


if __name__ == "__main__":
    while True:
        menu()
