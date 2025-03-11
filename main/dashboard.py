from PySide6.QtWidgets import (QApplication, QMainWindow, QTabWidget, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QPushButton, QCheckBox, QTextEdit, QSpinBox, QLineEdit)
from PySide6.QtGui import QDesktopServices, QPixmap, QColor
from PySide6.QtCore import QUrl, Qt

import macros.kb_mash as kb_mash
from macros.utils.kbListener import KeyboardListener
from pynput.keyboard import Listener
import threading
# Create a global KeyboardListener instance
global_keyboard_listener = KeyboardListener()
# Start the pynput Listener on the main thread
global_listener = Listener(on_press=global_keyboard_listener.on_press)
global_listener.start()  # This starts the listener non-blocking on the main thread


class TutorialTab(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        layout = QVBoxLayout()
        self.setLayout(layout)
        # Landing page text
        self.text_box = QTextEdit()
        self.text_box.setReadOnly(True)
        self.text_box.setHtml(
            """<h1>Automate MS</h1>
            <h2>Introduction</h2>
            <p>A little tool to automate repetitive/boring tasks in MapleStory to enhance your gameplay experience.</p>
            <h3>Disclaimer</h3>
            <ol>
                <li>This software is <b>NOT</b> a substitute for playing the game. It is a tool to assist you in your gameplay.</li>
                <li>Use this software at your <b>OWN RISK</b>. </li>
                <li>The developers are <b>NOT</b> responsible for any bans or penalties incurred while using this software.</li>
            </ol>
            <h3>Features</h3>
            <ol>
                <li>Auto dialogue key pressing.</li>
                <li>Auto Miracle cubing.</li>
                <li>...More to come!<li>
            </ol>
            </h3>Credits</h3>
            <p>Developed by: <b>Openwide</b></p>

            """
        )
        layout.addWidget(self.text_box)
        
        # Add button to open YouTube video
        self.video_button = QPushButton("Click here to watch video tutorial")
        self.video_button.clicked.connect(self.open_video_tutorial)
        layout.addWidget(self.video_button, alignment=Qt.AlignmentFlag.AlignHCenter)

        # Checkbox for tutorial acknowledgment
        self.check_box = QCheckBox("I have read the tutorial")
        self.check_box.stateChanged.connect(self.enable_tabs)
        layout.addWidget(self.check_box, alignment=Qt.AlignmentFlag.AlignHCenter)

        

    def open_video_tutorial(self):
        youtube_url = QUrl("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        QDesktopServices.openUrl(youtube_url)

    def enable_tabs(self, state):
        state = int(state)  # Explicitly cast state to integer
        print(f"Checkbox state changed: {state}")  # Debugging statement
        if state == 2:  # Explicitly checking for Qt.Checked (2)
            print("Checkbox is checked. Enabling tabs...")
            self.main_window.enable_tabs()
        elif state == 0:  # Explicitly checking for Qt.Unchecked (0)
            print("Checkbox is unchecked. Disabling tabs...")
            self.main_window.disable_tabs()
        else:
            print(f"Unhandled state: {state}")

    

class Tab1(QWidget):
    def __init__(self):
        super().__init__()
        
        # Set up the layout
        layout = QVBoxLayout()
        
        # Label
        self.label = QLabel("Auto: Button Press")
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        # Horizontal layout for NPC interact button and its label
        interact_layout = QHBoxLayout()
        interact_label = QLabel("NPC Interact Button:")
        interact_layout.addWidget(interact_label)

        # LineEdit for NPC Interact
        self.character_input = QLineEdit()
        self.character_input.setMaxLength(1)
        self.character_input.setPlaceholderText("j")
        self.character_input.setText("j")  # Default value
        self.character_input.setFixedWidth(50)  # Align closely with label
        self.character_input.setAlignment(Qt.AlignCenter)
        interact_layout.addWidget(self.character_input)

        layout.addLayout(interact_layout)   

        # Horizontal layout for delay field and its label
        delay_layout = QHBoxLayout()
        delay_label = QLabel("Button Press Delay:")
        delay_layout.addWidget(delay_label)

        # SpinBox for Button Click Delay
        self.delay_spinbox = QSpinBox()
        self.delay_spinbox.setRange(0, 10000)  # Set range in milliseconds
        self.delay_spinbox.setValue(100)  # Default value
        self.delay_spinbox.setSuffix(" ms")
        self.delay_spinbox.setFixedWidth(80)  # Align closely with label
        delay_layout.addWidget(self.delay_spinbox)

        layout.addLayout(delay_layout)


        # Button to start auto button press
        self.external_btn = QPushButton("Start Auto Button Press")
        self.external_btn.clicked.connect(self.npc_interact)
        layout.addWidget(self.external_btn)

        # Set the layout for the widget
        self.setLayout(layout)


    def npc_interact(self):
        # Get parameters from the GUI
        interact_button = self.character_input.text()
        button_press_delay = self.delay_spinbox.value() / 1000  # Convert ms to seconds
        global_keyboard_listener.unchecked_stop_key()  # Reset the stop key state
        self.label.setText("NPC Interact macro started...\nPress 'q' to stop")
        
        # Define a function to run your macro logic in a background thread
        def run_macro():
            # Use the global_keyboard_listener created at startup
            macro_exit_code = kb_mash.npc_interact(global_keyboard_listener, interact_button, button_press_delay)
            # Optionally, update the UI after macro ends using signals/slots if needed:
            if macro_exit_code == 2:
                print("User Interrupted: NPC Interact Button Released")
            elif macro_exit_code == 1:
                print("User Interrupted: NPC Interact Button Loop Exited")
            else:
                print("NPC Interact Button Loop Exited")
        
        # Start the macro in a new thread
        threading.Thread(target=run_macro, daemon=True).start()
    

class Tab2(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        
        # 1. Image display area at the top
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # Create a placeholder pixmap (400x300, gray background)
        placeholder_pixmap = QPixmap(200, 150)
        placeholder_pixmap.fill(QColor('gray'))
        self.image_label.setPixmap(placeholder_pixmap)
        layout.addWidget(self.image_label)
        
        # 2. "Set Capture Frame" button below the image
        self.set_capture_frame_button = QPushButton("Set Capture Frame")
        self.set_capture_frame_button.clicked.connect(self.set_capture_frame)
        layout.addWidget(self.set_capture_frame_button, alignment=Qt.AlignHCenter)
        
        # 3. Existing UI elements
        self.label = QLabel("Auto: Miracle Cube")
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)
        
        self.external_btn = QPushButton("Open Keypress Script")
        self.external_btn.clicked.connect(self.open_keypress_script)
        layout.addWidget(self.external_btn)
        
        self.setLayout(layout)

    def set_capture_frame(self):
        # Placeholder function: in a real app, this would let the user snip a portion of the screen.
        print("Set Capture Frame button clicked. Launch snipping tool placeholder.")
        # Optionally update the image with a new placeholder to simulate a capture:
        new_pixmap = QPixmap(400, 300)
        new_pixmap.fill(QColor('lightblue'))  # Simulated new capture
        self.image_label.setPixmap(new_pixmap)

    def open_keypress_script(self):
        self.label.setText("Call to Keypress script placeholder")
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Automation Software GUI")
        self.setGeometry(100, 100, 800, 600)

        # Tab Widget
        self.tabs = QTabWidget()
        self.tabs.currentChanged.connect(self.adjust_window_size)
        self.setCentralWidget(self.tabs)

        # Add Tutorial tab
        tutorial_tab = TutorialTab(self)
        self.tabs.addTab(tutorial_tab, "Introduction")

        # Add other tabs
        self.tab1 = Tab1()
        self.tab2 = Tab2()
        self.tabs.addTab(self.tab1, "Button Press")
        self.tabs.addTab(self.tab2, "Miracle Cube")

        # Disable other tabs initially
        self.disable_tabs()

    def enable_tabs(self):
        print("Enabling tabs...")  # Debugging statement
        self.tabs.setTabEnabled(1, True)
        self.tabs.setTabEnabled(2, True)

    def disable_tabs(self):
        print("Disabling tabs...")  # Debugging statement
        self.tabs.setTabEnabled(1, False)
        self.tabs.setTabEnabled(2, False)
    def adjust_window_size(self, index):
        if index == 1:  # Tab1 selected
            self.setFixedWidth(300)
            self.setFixedHeight(300)
        elif index ==0: # Tutorial Tab selected
            self.setFixedWidth(800)
            self.setFixedHeight(600)
        elif index == 2:  # Tab2 selected
            self.setFixedWidth(800)
            self.setFixedHeight(800)
        else:
            self.setFixedWidth(800)
            self.setFixedHeight(800)   

# Run the application
if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
