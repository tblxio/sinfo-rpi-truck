from config.configuration import componentDic
from componentClass import Component
import multiprocessing as mp
import threading
import signal
import sys
import time


# CTRl+C handler to exit the program properly
def signal_handler(sig, frame):
    print('Bye Bye')
    sys.exit(0)

# Get components from the config file
def get_components():
    my_components = {}
    for key in componentDic:
        # Imports the name of the class and creates an object
        mod = __import__(key, fromlist=[componentDic.get(key)])
        klass = getattr(mod, componentDic.get(key))
        aux_component = klass()
        # Ignores objects which are not Components
        if isinstance(aux_component, Component):
            my_components[key] = klass()
        else:
            print("It's not a valid component")
    return my_components

# Create a thread to run each component
def start_components(my_components):
    p = {}

    for component in my_components:
        p[component] = threading.Thread(target=my_components[component].run)
        print("Starting", component)
        p[component].daemon = True
        p[component].start()
        time.sleep(1)
    return p

# Wait for all the proccesses to finish (shouldn't get here
# since they run in a loop)
def wait_components_finish(p):
    print("Waiting for threads to finish")
    for component in p:
        p.get(component).join()

# Main behaviour
def main():
    signal.signal(signal.SIGINT, signal_handler)
    my_components = get_components()
    proc = start_components(my_components)
    # Used for testing purpouses to kill the program with ctrl + c
    # by force (not ideal)
    # while True:
    #     time.sleep(3)
    wait_components_finish(proc)
    sys.exit(0)


if __name__ == "__main__":
    main()
