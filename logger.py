from datetime import datetime
from platform import system
from time import time


def logger(body="Test", file_name=None, starting_time=None): # Starting time expects Unix Timestamp (time.time()) Float
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
        os = system()
        
        if os == "Windows":
            file_name = "log-" + __main__.__file__.split("\\")[-1].replace(".py", ".txt") # Windows
        else:
            file_name = "log-" + __main__.__file__.split("/")[-1].replace(".py", ".txt") # Linux/MacOS

    with open(f"logs/{file_name}","a") as file:
        file.write(log)

    return log[:-1]


if __name__ == "__main__":
    t1 = time()
    logger("Testing 123", starting_time=t1)
