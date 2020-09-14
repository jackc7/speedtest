from colorama import Fore, init, Back
from time import time, sleep
from logger import logger

import readchar
import random
import sys
import os


"""
l - open logs
o - open sentences 
"""

menu_speed = 1 # In seconds
countdown = 1 # Count down from

text = None
start = None


def time_check(starting_time):
    ending_time = time()
    time_diff = ending_time - starting_time

    return time_diff

def random_paragraph():
    with open("sentences.txt", "r") as file:
        lines = file.readlines()
        
        number = random.randint(0, len(lines) - 1)
        
        sentence = lines[number]
    return sentence[:-1]

def body(paragraph):
    for i in range(countdown, 0, -1):
        print("\033c" + paragraph + Fore.LIGHTGREEN_EX +  f"\n\nStarting in {i} seconds...")
        sleep(1)

    global text
    text = []
    
    global start
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
        
        print("\033c" + "".join(text) + Fore.WHITE + Back.LIGHTBLACK_EX + paragraph[i] + Back.BLACK + Fore.WHITE + paragraph[i+1:] + "\n\nCurrent Speed: " + color + str(wpm) + Fore.WHITE + f" wpm.\nAccuracy: {Fore.LIGHTCYAN_EX + str(accuracy)}%" + Fore.WHITE)

        button = readchar.readchar()
        letter = button.decode('utf-8')
        
        if button == b'\x08':
            if i == 0:
                continue
            i -= 1
            text = text[:-1]
            typed = typed[:-1]
            continue
        elif button == b'\r':
            return time_delta, False, accuracy
        
        if letter != paragraph[i]:
            text.append(Fore.RED + letter)
            incorrect += 1
        elif letter == paragraph[i]:
            text.append(Fore.GREEN + letter)
        
        typed.append(letter)
        i += 1
            
        if len("".join(typed)) == len(paragraph):
            logger(f"Completed Successfully [{wpm}wpm, {accuracy}%] | {''.join(typed)}", "main.log", start)
            return time_delta, True, accuracy

def menu():
    paragraph = random_paragraph()
    
    print("\033c" + Fore.YELLOW + "Typing Speed Test: Press" + Fore.LIGHTYELLOW_EX + " any button " + Fore.YELLOW + "to begin, " + Fore.LIGHTYELLOW_EX + "")
    
    option = readchar.readchar().decode("utf-8")
    
    if option == "l":
        os.system("start logs/main.log")
        return
    elif option == "o":
        os.system("start sentences.txt")
        return
    
    time_delta, is_complete, accuracy = body(paragraph)
    wpm = len(text) / 5 / time_delta * 60

    if not is_complete:
        print('\033c' + Fore.RED + "Incorrect" + Fore.WHITE + ". " + Fore.GREEN + str(round(wpm)) + Fore.WHITE + " words per minute. \nAccuracy: " + Fore.LIGHTCYAN_EX + str(accuracy) + "%" + Fore.WHITE)
        sleep(menu_speed)
    else:
        print("\033c" + f"Sentence completed at {Fore.GREEN + str(round(wpm)) + Fore.WHITE} words per minute. \n\nAccuracy: " + Fore.LIGHTCYAN_EX + str(accuracy) + "%" + Fore.WHITE)
        sleep(menu_speed)

if __name__ == "__main__":
    while True:
        menu()
                   
