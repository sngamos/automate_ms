from pynput.keyboard import Key

# Listener for the 'q' key to exit
class KeyboardListener:
    def __init__(self):
        self.stop_key_pressed = False

    def on_press(self, key):
        if key == Key.esc or (hasattr(key, 'char') and key.char == 'q'):
            self.stop_key_pressed = True

    def check_stop_key(self):
        return self.stop_key_pressed
    def unchecked_stop_key(self):
        self.stop_key_pressed = False
        return self.stop_key_pressed