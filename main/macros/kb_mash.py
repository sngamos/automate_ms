from pynput.keyboard import Key, Controller
import random
import time
import math

from .utils.rand_pauser import random_pauser
# Initialize the keyboard controller
keyboard_controller = Controller()

def npc_interact(keyboard_listener,harvest_interact_button='j', button_press_delay=1):
    print("starting press loop")
    while True:
        if keyboard_listener.check_stop_key():
            print("Stop key pressed, exiting loop.")
            break            
        random_pauser(keyboard_listener,0,button_press_delay,add_random=True)
        keyboard_controller.press(harvest_interact_button)
        random_pauser(keyboard_listener,0,button_press_delay,add_random=True)
        keyboard_controller.release(harvest_interact_button)
    keyboard_controller.release(harvest_interact_button)
    return 1
