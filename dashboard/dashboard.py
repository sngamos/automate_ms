from PySide6.QtWidgets import (QApplication, QMainWindow, QTabWidget, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QPushButton, QCheckBox, QTextEdit, QSpinBox, QLineEdit)
from PySide6.QtCore import Qt
from PySide6.QtGui import QDesktopServices
from PySide6.QtCore import QUrl

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
            
            """
        )
        layout.addWidget(self.text_box)

        # Add button to open YouTube video
        self.video_button = QPushButton("Click here to watch video tutorial")
        self.video_button.clicked.connect(self.open_video_tutorial)
        layout.addWidget(self.video_button, alignment=Qt.AlignCenter)

        # Checkbox for tutorial acknowledgment
        self.check_box = QCheckBox("I have read the tutorial")
        self.check_box.stateChanged.connect(self.enable_tabs)
        layout.addWidget(self.check_box, alignment=Qt.AlignCenter)

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
        self.character_input.setPlaceholderText("J")
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
        self.delay_spinbox.setValue(10)  # Default value
        self.delay_spinbox.setSuffix(" ms")
        self.delay_spinbox.setFixedWidth(80)  # Align closely with label
        delay_layout.addWidget(self.delay_spinbox)

        layout.addLayout(delay_layout)

        # Checkbox for "Hold Down Button"
        self.hold_down_checkbox = QCheckBox("Hold Down Button")
        self.hold_down_checkbox.stateChanged.connect(self.toggle_hold_down)
        layout.addWidget(self.hold_down_checkbox)

        # Button to start auto button press
        self.external_btn = QPushButton("Start Auto Button Press")
        self.external_btn.clicked.connect(self.open_cv_script)
        layout.addWidget(self.external_btn)

        # Button for NPC Interact
        self.npc_interact_btn = QPushButton("NPC Interact")
        self.npc_interact_btn.clicked.connect(self.npc_interact)
        layout.addWidget(self.npc_interact_btn)

        # Set the layout for the widget
        self.setLayout(layout)

        # Set fixed width for the window when Tab1 is selected
        self.setFixedWidth(300)

    def open_cv_script(self):
        # Placeholder function for the CV script
        if self.hold_down_checkbox.isChecked():
            self.label.setText("CV script called: Hold Down Enabled")
        else:
            delay = self.delay_spinbox.value()
            character = self.character_input.text() or "None"
            self.label.setText(f"CV script called: Delay {delay} ms, Character: {character}")

    def toggle_hold_down(self):
        # Placeholder function for checkbox state changes
        if self.hold_down_checkbox.isChecked():
            self.label.setText("Hold Down Button Enabled")
            self.delay_spinbox.setEnabled(False)
        else:
            self.label.setText("Hold Down Button Disabled")
            self.delay_spinbox.setEnabled(True)

    def npc_interact(self):
        # Placeholder function for NPC interact button
        self.label.setText("NPC Interact Button Pressed")

class Tab2(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.label = QLabel("Auto: Miracle Cube")
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        self.external_btn = QPushButton("Open Keypress Script")
        self.external_btn.clicked.connect(self.open_keypress_script)
        layout.addWidget(self.external_btn)

        self.setLayout(layout)

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
        else:
            self.setFixedWidth(800)  # Default width    

# Run the application
if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
