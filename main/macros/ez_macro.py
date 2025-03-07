from pynput.keyboard import Key, Controller, Listener
import random
import time
import math

from utils.kbListener import KeyboardListener
from utils.rand_pauser import random_pauser
# Initialize the keyboard controller
keyboard_controller = Controller()

def kb_mash(kb_listener):
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
        random_pauser(kb_listener)
        keyboard_controller.press('x')
        random_pauser(kb_listener)
        keyboard_controller.release('x')
        random_pauser(kb_listener)
        counter +=1
        print("counter: %s", counter)   
        # Exit the loop if 'q' is pressed
        if keyboard_listener.check_stop_key():
            print("Stopping...")
            break
        # move after random n key presses
        if counter == counter_limit:
            print("moving after pressing %s keys", counter)
            random_pauser(kb_listener,1,1.5)
            keyboard_controller.press(Key.right)
            print("moving right")
            random_pauser(kb_listener,1,1.5)
            keyboard_controller.release(Key.right)
            print("stop moving right")
            random_pauser(kb_listener,0.1,0.3)
            keyboard_controller.press('c')
            print("attacking")
            random_pauser(kb_listener,1,1.5)
            keyboard_controller.release('c')
            print("stop attacking")
            random_pauser(kb_listener,1,1.5)
            keyboard_controller.press(Key.left)
            print('move left')
            random_pauser(kb_listener,1.2,1.4)
            keyboard_controller.release(Key.left)
            print('stop moving left')
            counter = 0 
            print('resetting counter')
            counter_limit = random.randint(10,20)
            print('new counter limit: %s', counter_limit)

# Initialize and start the keyboard listener
keyboard_listener = KeyboardListener()
with Listener(on_press=keyboard_listener.on_press) as listener:
    kb_mash(keyboard_listener)
