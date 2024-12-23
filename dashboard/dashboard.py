from PySide6.QtWidgets import (QApplication, QMainWindow, QTabWidget, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QPushButton, QCheckBox, QTextEdit)
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
        layout = QVBoxLayout()
        self.label = QLabel("Auto: Button Press")
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        self.external_btn = QPushButton("Open CV Script")
        self.external_btn.clicked.connect(self.open_cv_script)
        layout.addWidget(self.external_btn)

        self.setLayout(layout)

    def open_cv_script(self):
        self.label.setText("Call to CV script placeholder")

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

# Run the application
if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
