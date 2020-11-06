from colorama import Fore, Back
from time import time, sleep
from logger import logger

import readchar
import random
import json
import os


"""Menu Hotkeys
l - open logs
o - open sentences
p - leaderboard
"""

# TODO
# Ctrl+Backspace
# letters stay same color changes

menu_speed = 1 # In seconds
countdown = 1 # Count down from

text = None
start = None


def time_check(starting_time):
    ending_time = time()
    time_diff = ending_time - starting_time

    return time_diff


def leaderboard():
    leaderboard_sorter()
    print("\033c========[ Leaderboard ]========")
    with open("leaderboard", "r") as file:
        lines = file.readlines()
    try:
        for i in range(9):
            print(" " + str(i+1) + ": " + lines[i][:-1])
        print("10: " + lines[10][:-1])
    except IndexError:
        pass
    
    print()
    input("Press enter to return to menu.\n")


def leaderboard_sorter():
    with open("leaderboard", "r+") as file:
        lines = file.readlines()

    lines.sort()
    safe = [int(x[:-1]) for x in lines]
    safe.sort()
    safe.reverse()
    safe = [str(x) for x in safe][:50]

    with open("leaderboard", "w") as file:
        file.write("\n".join(safe) + "\n")


def random_sentence():
    with open("sentences", "r") as file:
        lines = [x[:-1] for x in file.readlines()]
        number = random.randint(0, len(lines) - 1)
        line = lines[number]
    sentence, description = line.split("*")
    return sentence, description


def write_json(score: int):
    with open("leaderboard","r") as file:
        json_dict = json.load()


def body(sentence):
    for i in range(countdown, 0, -1):
        print("\033c" + sentence + Fore.LIGHTGREEN_EX +  f"\n\nStarting in {i} seconds...")
        sleep(1)
        
    global text, start
    text = []
    start = time()
    typed = []
    i = 0
    incorrect = 0
    
    while True:
        time_delta = time_check(start)
        
        try: accuracy = round((len(typed) - incorrect) / len(typed) * 100)
        except: accuracy = 100
        
        try: wpm = round(len(text) / 5 / time_delta * 60)
        except: wpm = 0
        
        if wpm < 60:
            color = Fore.YELLOW
        elif wpm < 100:
            color = Fore.LIGHTRED_EX
        else:
            color = Fore.RED
        string = "\033c" + "".join(text) + Fore.WHITE + Back.LIGHTBLACK_EX + sentence[i] + Back.BLACK + Fore.WHITE + sentence[i+1:] + "\n\nCurrent Speed: " + color + str(wpm) + Fore.WHITE + " wpm.\n" + f"Accuracy: {Fore.LIGHTCYAN_EX + str(accuracy)}%\n" + Fore.WHITE + f"Score: {Fore.LIGHTMAGENTA_EX + str(round(wpm * accuracy))}"
        print(string)
        button = readchar.readchar()
        letter = button.decode('utf-8')
        if button == b'\x17':
            if i == 0:
                continue
            j = 1
            while True:
                if typed[-j] == ' ':
                    break
                else:
                    j += 1
            i -= j
            text = text[:-j]
            typed = typed[:-j]
            text = text[:-1]; text.append(" ")
            typed = typed[:-1]; typed.append(" ")

        if button == b'\x08':
            if i == 0:
                continue
            i -= 1
            text = text[:-1]
            typed = typed[:-1]
            continue
        elif button == b'\r':
            return time_delta, False, accuracy
        
        if letter != sentence[i]:
            text.append(Fore.RED + letter)
            incorrect += 1
        elif letter == sentence[i]:
            text.append(Fore.GREEN + letter)
        typed.append(letter)
        i += 1
        if len(typed) == len(sentence):
            logger(f"Completed Successfully [{wpm}wpm, {accuracy}%] | {''.join(typed)}", "main.log", start)
            return time_delta, True, accuracy


def menu():
    sentence, description = random_sentence()
    print("\033c" + Fore.YELLOW + "Typing Speed Test: Press" + Fore.LIGHTYELLOW_EX + " any button " + Fore.YELLOW + "to begin, " + Fore.LIGHTYELLOW_EX + "")
    option = readchar.readchar().decode("utf-8")
    if option == "l":
        os.system("start logs/main.log")
        return
    elif option == "o":
        os.system("notepad sentences")
        return
    elif option == "p":
        leaderboard()
        return
    time_delta, is_complete, accuracy = body(sentence)
    try: 
        wpm = len(text) / 5 / time_delta * 60
    except ZeroDivisionError: 
        wpm = 0
    if not is_complete:
        print('\033c' + Fore.RED + "Incorrect" + Fore.WHITE + ". " + Fore.GREEN + str(round(wpm)) + Fore.WHITE + " words per minute. \nAccuracy: " + Fore.LIGHTCYAN_EX + str(accuracy) + "%" + Fore.WHITE + "\n\n" + description)
        sleep(menu_speed)
    else:
        print("\033c" + f"Sentence completed at {Fore.GREEN + str(round(wpm)) + Fore.WHITE} words per minute. \n\nAccuracy: " + Fore.LIGHTCYAN_EX + str(accuracy) + "%" + Fore.WHITE + "\n\n" + description)
        with open("leaderboard", "a") as file:
            score = round(wpm * accuracy)
            file.write(str(score) + "\n")
        sleep(menu_speed)
        

if __name__ == "__main__":
    while True:
        menu()
