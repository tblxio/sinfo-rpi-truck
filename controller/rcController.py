import controllerMessages as messages
import Tkinter as tk
import sys
import json
sys.path.append('..')
from mqttClient import MqttClient

# Connect to the client and subscribe to the necessary topics
drive_topic = "sbrick/01/sp/drive"
stop_topic = "sbrick/01/sp/stop"
adc_topic = "sbrick/01/rr/get_adc"
my_client = MqttClient()
my_client.setup_client()

# Handles the behaviour expected from each key press
def key_input(event):
    
    stri = event.keysym.lower()
    print("Press w,s,a,d to drive, b to break and q to quit")

    if stri == 'd':
        print("Drive right")
        my_client.publish(drive_topic, json.dumps(messages.drive_msgd,  sort_keys=True))
    elif stri == 'b':
        my_client.publish(drive_topic, json.dumps(messages.stop_msg_l, sort_keys=True))
        my_client.publish(drive_topic, json.dumps(messages.stop_msg_a, sort_keys=True))
        print("Stop")
    elif stri == 'a':
        my_client.publish(drive_topic, json.dumps(messages.drive_msga, sort_keys=True))
        print("Drive left")
    elif stri == 'w':
        my_client.publish(drive_topic, json.dumps(messages.drive_msgw, sort_keys=True))
        print("Drive forward")
    elif stri == 's':
        my_client.publish(drive_topic, json.dumps(messages.drive_msgs, sort_keys=True))
        print("Drive back")
    elif stri == 'q':
        my_client.publish(drive_topic, json.dumps(messages.stop_msg_l, sort_keys=True))
        my_client.publish(drive_topic, json.dumps(messages.stop_msg_a, sort_keys=True))
        print("Stop and quit")
        sys.exit()
    elif stri == 'p':
        my_client.publish(adc_topic, json.dumps(messages.get_adc, sort_keys=True))


# Simple Tkinter program to monitor key presses and act on them
if __name__ == "__main__":
    command = tk.Tk()
    command.bind_all('<KeyPress>', key_input)
    command.mainloop()
