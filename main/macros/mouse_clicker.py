from pynput.keyboard import Key, Controller, Listener
from pynput.mouse import Button, Controller as MouseController
import random
import time

from utils.kbListener import KeyboardListener
from utils.rand_pauser import random_pauser

def cubing_click(kb_listener,mouse_controller, button= Button.left):
    #simulate mouse click
    mouse_controller.press(button)
    random_pauser(kb_listener,0.1,0.3)
    mouse_controller.release(button)
    random_pauser(kb_listener,0.1,0.3)

def blind_cubing_loop(kb_listener,mouse_controller,keyboard_controller):
    print("starting blind cubing loop")
    time.sleep(1)
    print("3")
    time.sleep(1)
    print("2")
    time.sleep(1)
    print("1")
    time.sleep(1)
    while True:
        if kb_listener.check_stop_key():
            print("Stop key pressed, exiting loop.")
            break
        cubing_click(kb_listener,mouse_controller)
        random_pauser(kb_listener,0.5,0.7)
        keyboard_controller.press(Key.enter)
        random_pauser(kb_listener,0.5,0.7)
        keyboard_controller.release(Key.enter)
        random_pauser(kb_listener,0.5,0.7)
        keyboard_controller.press(Key.enter)
        random_pauser(kb_listener,1.5,2)
    return 1

if __name__ == "__main__":
    # Initialize the keyboard controller
    keyboard_controller = Controller()
    mouse_controller = MouseController()
    # Create a global KeyboardListener instance
    global_keyboard_listener = KeyboardListener()
    # Start the pynput Listener on the main thread
    global_listener = Listener(on_press=global_keyboard_listener.on_press)
    global_listener.start()  # This starts the listener non-blocking on the main thread
    blind_cubing_loop(global_keyboard_listener,mouse_controller,keyboard_controller)