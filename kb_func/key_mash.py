from pynput.keyboard import Key, Controller, Listener
import random
import time

# Initialize the keyboard controller
keyboard_controller = Controller()


def random_pauser():
    time.sleep(random.random()*0.1)


def kb_mash():
    print("starting")
    time.sleep(1)
    print("3")
    time.sleep(1)
    print("2")
    time.sleep(1)
    print("1")
    time.sleep(1)

    while True:
        # Simulate pressing and releasing the 'j' key
        random_pauser()
        keyboard_controller.press('j')
        random_pauser()
        keyboard_controller.release('j')
        random_pauser()
        keyboard_controller.press('left')
        time.sleep(0.2)
        keyboard_controller.release('left')
        random_pauser()
        keyboard_controller.press('c')
        random_pauser()
        keyboard_controller.release('c')
        random_pauser()
        keyboard_controller.press('right')
        time.sleep(0.2)
        keyboard_controller.release('right')
        random_pauser()
        keyboard_controller.press('c')
        random_pauser()
        keyboard_controller.release('c')
        time.sleep(4)  # Adjust delay as needed

        # Exit the loop if 'q' is pressed
        if keyboard_listener.check_stop_key():
            print("Stopping...")
            break

# Listener for the 'q' key to exit
class KeyboardListener:
    def __init__(self):
        self.stop_key_pressed = False

    def on_press(self, key):
        if key == Key.esc or (hasattr(key, 'char') and key.char == 'q'):
            self.stop_key_pressed = True

    def check_stop_key(self):
        return self.stop_key_pressed

# Initialize and start the keyboard listener
keyboard_listener = KeyboardListener()
with Listener(on_press=keyboard_listener.on_press) as listener:
    kb_mash()
