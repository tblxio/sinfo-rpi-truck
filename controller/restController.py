import Tkinter as tk
import sys
import requests
import time
from decimal import Decimal, getcontext

URL = "http://127.0.0.1:8080/motors/drive"
getcontext().prec = 2


def generate_params(direction, power):
    return{
        'motion': direction,
        'power': power
    }

# Handles the behavior expected from each key press
def key_input(event):

    stri = event.keysym.lower()
    print("Press w,s,a,d to drive, b to break and q to quit")

    if stri == 'd':
        print("[{}] Drive right ").format(Decimal(time.time() * 1000))
        requests.get(url=URL, params=generate_params("angular", 255))
    elif stri == 'b':
        requests.get(url=URL, params=generate_params("angular", 0))
        requests.get(url=URL, params=generate_params("linear", 0))
        print("[{}] Stop ").format(Decimal(time.time() * 1000))
    elif stri == 'a':
        requests.get(url=URL, params=generate_params("angular", -125))
        print("[{}] Drive left ").format(Decimal(time.time() * 1000))
    elif stri == 'w':
        requests.get(url=URL, params=generate_params("linear", 255))
        print("[{}] Drive forward ").format(Decimal(time.time() * 1000))
    elif stri == 's':
        requests.get(url=URL, params=generate_params("linear", -255))
        print("[{}] Drive back ").format(Decimal(time.time() * 1000))
    elif stri == 'q':
        requests.get(url=URL, params=generate_params("angular", 0))
        requests.get(url=URL, params=generate_params("linear", 0))
        print("[{}] Quit ").format(Decimal(time.time() * 1000))
        sys.exit()
    elif stri == 'p':
        pass


# Simple Tkinter program to monitor key presses and act on them
if __name__ == "__main__":
    command = tk.Tk()
    command.bind_all('<KeyPress>', key_input)
    command.mainloop()
