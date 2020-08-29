# 8/29/2020

from readchar import readchar
from colorama import Fore
from time import time

import random
import sys


paragraph = None
text = None


def end(starting_time):
    ending_time = time()
    time_diff = ending_time - starting_time
    return time_diff

def random_paragraph():
    with open("sentences.txt", "r") as file:
        random_number = random.randint(0, 49)
        lines = file.readlines()
        the_paragraph = lines[random_number][:-1]
    return the_paragraph

def body(body):
    global paragraph
    paragraph = body
    
    global text
    text = []

    start = time()

    for i in range(len(paragraph)):
        print('\033c' + Fore.GREEN + "".join(text) + Fore.WHITE + paragraph[i:])

        try:
            button = readchar().decode("utf-8")
            if button != paragraph[i]:
                time_delta = end(start)
                return time_delta, False
            text.append(button)
        except:
            time_delta = end(start)
            return time_delta, False

        if "".join(text) == paragraph:
            time_delta = end(start)
            return time_delta, True

def menu():
    print(Fore.YELLOW + "Typing Speed Test: Press Enter to Begin" + Fore.WHITE)
    input()
    time_delta, is_complete = body()
    if is_complete is False:
        wpm = len(paragraph) / 5 / time_delta * 60
        print('\033c' + Fore.RED + "Incorrect." + Fore.GREEN + str(round(wpm)) + Fore.WHITE + "words per minute.")
    else:
        wpm = len(paragraph) / 5 / time_delta * 60
        print(f"Sentence completed at {Fore.GREEN + str(round(wpm)) + Fore.WHITE} words per minute")

if __name__ == "__main__":
    menu()
