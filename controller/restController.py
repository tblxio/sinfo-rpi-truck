import Tkinter as tk
import sys
import requests

URL = "http://127.0.0.1:8080/drive"

def generate_params(direction,power):
    return{
        'direction':direction,
        'power': power
    }
    
# Handles the behaviour expected from each key press
def key_input(event):
    
    stri = event.keysym.lower()
    print("Press w,s,a,d to drive, b to break and q to quit")

    if stri == 'd':
        print("Drive right")
        requests.get(url=URL,params= generate_params("right",255))
    elif stri == 'b':
        requests.get(url=URL,params= generate_params("right",0))
        requests.get(url=URL,params= generate_params("back",0))
        print("Stop")
    elif stri == 'a':
        requests.get(url=URL,params= generate_params("left",255))
        print("Drive left")
    elif stri == 'w':
        requests.get(url=URL,params= generate_params("forward",255))
        print("Drive forward")
    elif stri == 's':
        requests.get(url=URL,params= generate_params("back",255))
        print("Drive back")
    elif stri == 'q':
        requests.get(url=URL,params= generate_params("right",0))
        requests.get(url=URL,params= generate_params("back",0))
        print("Stop and quit")
        sys.exit()
    elif stri == 'p':
        pass


# Simple Tkinter program to monitor key presses and act on them
if __name__ == "__main__":
    command = tk.Tk()
    command.bind_all('<KeyPress>', key_input)
    command.mainloop()