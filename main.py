# 8/29/2020


from time import time, sleep
from colorama import Fore

import readchar
import random
import sys


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
    text = []

    start = time()

    for i in range(len(paragraph)):
        print('\033c' + Fore.GREEN + "".join(text) + Fore.WHITE + paragraph[i:])

        try:
            button = readchar.readchar().decode("utf-8")
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
    paragraph = random_paragraph()
    
    print("\033c" + Fore.YELLOW + "Typing Speed Test: Press" + Fore.LIGHTYELLOW_EX + " any button " + Fore.YELLOW + "to begin." + Fore.WHITE)
    readchar.readkey()

    time_delta, is_complete = body(paragraph)

    if is_complete is False:
        wpm = len(paragraph) / 5 / time_delta * 60
        print('\033c' + Fore.RED + "Incorrect. " + Fore.GREEN + str(round(wpm)) + Fore.WHITE + " words per minute.")
        sleep(2)

    else:
        wpm = len(paragraph) / 5 / time_delta * 60
        print("\033c" + f"Sentence completed at {Fore.GREEN + str(round(wpm)) + Fore.WHITE} words per minute")
        sleep(2)


if __name__ == "__main__":
    while True:
        menu()
