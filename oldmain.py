# 8/28/2020

import sys

from colorama import Fore
from readchar import readchar


paragraph = "But she wasn't sure she actually preferred it."
letters = list(paragraph)

letters_typed = []

for i in range(len(letters)):
    print('\033c')

    body = Fore.GREEN + "".join(letters_typed) + Fore.WHITE +  paragraph[i:]
    sys.stdout.write(body)
    
    
    try:
        button = readchar().decode("utf-8")
    except:
        letters_typed.pop()
        continue
    else:
        letters_typed = []
    
    if button == letters[i]:
        letters.append(button)
    else:
        to_append = Fore.RED + button
        letters_typed.append(to_append)

    sys.stdout.write(letters[i])
