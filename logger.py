from datetime import datetime
from time import time
import os

def logger(body="Test", file_name=None, starting_time=None): # Starting time in uts
    tstamp = str(datetime.now())[:-4]
    log = [f'[{tstamp}]']

    if starting_time is not None:
        now = time()
        float_time_diff = round((now - starting_time), 2)
        
        if float_time_diff < 10:
            time_diff = "0" + str(float_time_diff)
        else:
            time_diff = str(float_time_diff)

        if len(time_diff) < 5:
            time_diff += "0"

        log.append(f"({time_diff}s) -")
    else:
        log.append("-")

    log.append(body + "\n")
    log = " ".join(log)

    if file_name is None:   
        import __main__
        
        txt_file = __main__.__file__.split("/")[-1].replace(".py", ".txt")

        file_name = "log-" + txt_file

    try:
        with open(f"logs/{file_name}","a") as file:
            file.write(log)
    except:
        os.system(f"mkdir logs")
        with open(f"logs/{file_name}","a") as file:
            file.write(log)
    
    return log[:-1]
