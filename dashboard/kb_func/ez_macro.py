from pynput.keyboard import Key, Controller, Listener
import random
import time
import math
# Initialize the keyboard controller
keyboard_controller = Controller()

# Listener for the 'q' key to exit
class KeyboardListener:
    def __init__(self):
        self.stop_key_pressed = False

    def on_press(self, key):
        if key == Key.esc or (hasattr(key, 'char') and key.char == 'q'):
            self.stop_key_pressed = True

    def check_stop_key(self):
        return self.stop_key_pressed

def random_pauser(lower_bound=None, upper_bound=None, add_random=False):
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
    
    sleep_increment = 0.01  # Check every 10ms
    elapsed = 0.0
    while elapsed < total_sleep:
        if keyboard_listener.check_stop_key():
            raise KeyboardInterrupt("Stop key pressed, exiting sleep early.")
        time.sleep(sleep_increment)
        elapsed += sleep_increment


def kb_mash():
    print("starting")
    time.sleep(1)
    print("3")
    time.sleep(1)
    print("2")
    time.sleep(1)
    print("1")
    time.sleep(1)
    counter = 0
    counter_limit = random.randint(10,20)
    print('counter limit: %s', counter_limit)  
    while True:
        # Simulate pressing and releasing the 'j' key
        random_pauser()
        keyboard_controller.press('x')
        random_pauser()
        keyboard_controller.release('x')
        random_pauser()
        counter +=1
        print("counter: %s", counter)   
        # Exit the loop if 'q' is pressed
        if keyboard_listener.check_stop_key():
            print("Stopping...")
            break
        # move after random n key presses
        if counter == counter_limit:
            print("moving after pressing %s keys", counter)
            random_pauser(1,1.5)
            keyboard_controller.press(Key.right)
            print("moving right")
            random_pauser(1,1.5)
            keyboard_controller.release(Key.right)
            print("stop moving right")
            random_pauser(0.1,0.3)
            keyboard_controller.press('c')
            print("attacking")
            random_pauser(1,1.5)
            keyboard_controller.release('c')
            print("stop attacking")
            random_pauser(1,1.5)
            keyboard_controller.press(Key.left)
            print('move left')
            random_pauser(1.2,1.4)
            keyboard_controller.release(Key.left)
            print('stop moving left')
            counter = 0 
            print('resetting counter')
            counter_limit = random.randint(10,20)
            print('new counter limit: %s', counter_limit)

# Initialize and start the keyboard listener
keyboard_listener = KeyboardListener()
with Listener(on_press=keyboard_listener.on_press) as listener:
    kb_mash()
