# 8/29/2020

from time import time, sleep
from logger import logger
from colorama import Fore, init

import readchar
import random
import sys
import ahk

"""
l - open logs
o - open sentences 
"""

menu_speed = 1 # sleep() seconds
countdown = 1 # start countdown at this number

text = None
start = None

log_loc = "C://Users//jack7//Desktop//Python//SpeedTest//logs//log.txt"

def time_check(starting_time):
    ending_time = time()
    time_diff = ending_time - starting_time

    return time_diff

def random_paragraph():
    with open("sentences.txt", "r") as file:
        number = random.randint(0, 301)
        sentence = file.readlines()[number]
    return sentence[:-1]

def body(paragraph):
    for i in range(countdown, 0, -1):
        print("\033c" + paragraph + Fore.LIGHTGREEN_EX +  f"\n\nStarting in {i} seconds...")
        sleep(1)

    global text
    text = []

    global start
    start = time()

    sleep(.1)
    for i in range(len(paragraph)):
        time_delta = time_check(start)

        wpm = str(round(len(text) / 5 / time_delta * 60))
        print("\033c" + Fore.GREEN + "".join(text) + Fore.WHITE + paragraph[i:] + "\n\nCurrent Speed: " + Fore.GREEN + wpm + Fore.WHITE + " wpm.")

        try:
            button = readchar.readchar().decode("utf-8")                

            # Checks if typed letter is wrong.
            if button != paragraph[i]:
                time_delta = time_check(start)

                wpm = round(len(text) / 5 / time_delta * 60)
                logger(f"Typo [{wpm} wpm] | {''.join(text)} <- Here | Typed '{button}' instead of '{paragraph[i]}'", "log.txt", start)

                return time_delta, False

            text.append(button)
            
        except: # If invalid key pressed.
            time_delta = time_check(start)

            wpm = round(len(text) / 5 / time_delta * 60)
            logger(f"Invalid Keypress [{wpm}wpm] | {''.join(text)} <- Here", "log.txt", start)

            return time_delta, False

        if "".join(text) == paragraph: # Checks if what you typed is the same as the given paragraph.
            time_delta = time_check(start)

            wpm = round(len(text) / 5 / time_delta * 60)
            logger(f"Completed Successfully [{wpm}wpm] | {''.join(text)}", "log.txt", start)

            return time_delta, True

def menu():
    paragraph = random_paragraph()
    
    print("\033c" + Fore.YELLOW + "Typing Speed Test: Press" + Fore.LIGHTYELLOW_EX + " any button " + Fore.YELLOW + "to begin." + Fore.WHITE)
    
    option = readchar.readchar().decode("utf-8")
    
    if option == "l":
        ahk.run_file(log_loc)
        return
    if option == "o":
        ahk.run_file("C:/Users/jack7/Desktop/Python/typeracer/SpeedTest/sentences.txt")
        return
    
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
