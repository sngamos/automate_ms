from pynput.keyboard import Key, Controller, Listener
import random
import time
import math
# Initialize the keyboard controller
keyboard_controller = Controller()


# Listener for the 'q' key to exit
class KeyboardListener:
    def __init__(self, stop_key='q'):
        self.stop_key_pressed = False
        self.stop_key = stop_key

    def on_press(self, key):
        if key == Key.esc or (hasattr(key, 'char') and key.char == self.stop_key):
            self.stop_key_pressed = True

    def check_stop_key(self):
        return self.stop_key_pressed

def random_pauser(keyboard_listener,lower_bound=None, upper_bound=None, add_random=False):
    """
    Pause execution for a random duration, checking frequently for a stop signal.
    
    If no bounds are provided, it sleeps for a random time between 0 and 10 second.
    Otherwise, it sleeps for a random time between the provided bounds.

    If add_random is True, the sleep time is increased by a random amount by a 0-25% of the bound provided.
    """
    if lower_bound is None and upper_bound is None:
        total_sleep = random.random()
    else:
        if lower_bound is None:
            lower_bound = 0.0
        if upper_bound is None:
            upper_bound = 10.0
        if upper_bound < lower_bound:
            raise ValueError("upper_bound must be greater than lower_bound")
        total_sleep = random.uniform(lower_bound, upper_bound)
        if add_random:
            total_sleep += random.uniform(0, 0.25 * (upper_bound - lower_bound))
    print(f"Sleeping for {total_sleep} seconds.")
    sleep_increment = 0.01  # Check every 10ms
    elapsed = 0.0
    while elapsed < total_sleep:
        if keyboard_listener.check_stop_key():
            raise KeyboardInterrupt("Stop key pressed, exiting sleep early.")
        time.sleep(sleep_increment)
        elapsed += sleep_increment

def npc_interact(keyboard_listener,harvest_interact_button='j',hold_down_button=False, button_press_delay=1):
    if hold_down_button:
        print("Holding down button...")
        keyboard_controller.press(harvest_interact_button)
        # Continue holding until q or esc is pressed
        while not keyboard_listener.check_stop_key():
            time.sleep(0.1)  # Check every 100ms
        keyboard_controller.release(harvest_interact_button)
        print("Released button due to stop key press.")
        return 2

    else:
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
