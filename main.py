from config.configuration import componentDic, rootTopic
from componentClass import Component
import multiprocessing as mp
import threading
import signal
import sys
import time
import math

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
        aux_component = klass(rootTopic)

        # Ignores objects which are not Components
        if isinstance(aux_component, Component):
            my_components[key] = aux_component
            my_components[key].setup()

            # The use of threads here is mainly in the case of components that should
            # run in a parallel loop, such as the camera, and they can do so by
            # implementing the run function. This shouldn't be the used for 
            # components such as sensors, since their data aquisition is done
            # in the main loop
            p = threading.Thread(
                target=my_components[key].run)
            p.daemon = True
            p.start()

        else:
            print("It's not a valid component")
    return my_components


# Get the slowest and fastest poll rates in order to define
# the cycle speed and the maximum number of cycles before resetting
# the counter
def get_max_min_sampling_interval(my_components):
    max_interval = -1.0
    min_interval = 1000.0
    for component in my_components:
        if my_components[component].sampInterval <= min_interval:
            min_interval = my_components[component].sampInterval

        if my_components[component].sampInterval >= max_interval:
            max_interval = my_components[component].sampInterval

    return max_interval, min_interval


# Update the number of cycles between measurements for
# each component based on the loop speed
def update_loop_cycles(my_components, loop_speed, timestamp):
    for key, component in my_components.iteritems():
        component.calculate_loop_cycles(loop_speed, timestamp)


# Main behaviour
def main():
    # Get components and setup CTRL+C handling
    signal.signal(signal.SIGINT, signal_handler)
    my_components = get_components()

    # Get the sampling ratios of all components in order to
    # define the cycle speed, the number of cycles
    # in between measurements for each component as well as
    # the number of cycles of the slowest component in order
    # to reset the counter
    max_rate, min_rate = get_max_min_sampling_interval(my_components)
    max_loops = math.ceil((max_rate/min_rate))
    update_loop_cycles(my_components, min_rate, time.time()*1000000)
    print "Loop speed: {} || Maximum number of cycles {} ".format(
        min_rate, max_loops)

    loopcount = 0
    # Get timestamp, call handle data for each component
    # sleep the rate - time_spent_on_loop
    while True:
        begin = time.time()
        timestamp = int(begin*1000000)  # microseconds

        for key, component in my_components.iteritems():
            if component.loopCycles <= loopcount:
                component.handleData(timestamp)
                # p = threading.Thread(
                #     target=component.handleData, args=(timestamp,))
                # p.daemon = True
                # p.start()

        loopcount += 1
        end = time.time()
        # Prevents errors in case the loop takes too long
        # Loop time is around 2ms with 2 components
        if (end-begin) < min_rate:
            time.sleep(min_rate-(end-begin))
        if loopcount > max_loops:
            loopcount = 0

    sys.exit(0)


if __name__ == "__main__":
    main()
