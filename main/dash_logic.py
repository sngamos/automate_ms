import sys
import threading
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QUrl, QObject, pyqtSignal
from PyQt5.QtGui import QDesktopServices, QRegExpValidator  # In PyQt5, QDesktopServices is in QtGui
import macros.kb_mash as kb_mash
from macros.utils.kbListener import KeyboardListener
from pynput.keyboard import Listener, Key

# Create a global KeyboardListener instance and start the listener
global_keyboard_listener = KeyboardListener()
global_listener = Listener(on_press=global_keyboard_listener.on_press)
global_listener.start()

# Import the generated UI (make sure this file is in your PYTHONPATH)
from dash_layout import Ui_Form  # Adjust the module name if needed


class Dashboard(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(Dashboard, self).__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        
        # --- Initially disable the AutoInteract tab (index 1,2) until the user reads the tutorial ---
        self.ui.tabWidget.setTabEnabled(1, False)
        self.ui.tabWidget.setTabEnabled(2, False)
        
        
        # --- Connect Introduction (LandingPage) tab signals ---
        self.ui.VideoTutorial.clicked.connect(self.open_video_tutorial)
        self.ui.ReadTutorialCheckbox.stateChanged.connect(self.tutorial_checked)
        
        # --- Connect the AutoInteract tab signal ---
        self.ui.AutoInteractStartButton.clicked.connect(self.start_auto_interact)

        # Connect the Start Auto Cuber button to the auto cuber method.
        self.ui.StartCuberButton.clicked.connect(self.start_auto_cuber)

        
    def open_video_tutorial(self):
        # Open the video URL (for example, a YouTube tutorial)
        QDesktopServices.openUrl(QUrl("https://www.youtube.com/watch?v=dQw4w9WgXcQ"))
        
    def tutorial_checked(self, state):
        # Enable or disable the AutoInteract tab based on the checkbox state
        if state == QtCore.Qt.Checked:
            self.ui.tabWidget.setTabEnabled(1, True)
            self.ui.tabWidget.setTabEnabled(2, True)
        else:
            self.ui.tabWidget.setTabEnabled(1, False)
            self.ui.tabWidget.setTabEnabled(2, False)
    
    #=== AUTO INTERACT TAB ===

    def start_auto_interact(self):
        """
        Mimics the original auto interact function:
        Reads the button text and delay, updates the status label,
        resets the keyboard listener, and starts the macro in a background thread.
        """
        # Retrieve the interact/harvest button value from the textEdit (strip extra spaces)
        interact_text = self.ui.InteractButtonValue.text().strip()
        if not interact_text:
            interact_text = "j"  # default value if empty
        #check if the interact button value is valid
        if interact_text == "q" or interact_text == "esc":
            self.ui.AutoInteractTextbox.setText("Invalid interact button value\nPlease choose another key")
            return
        elif len(interact_text) > 1:
            self.ui.AutoInteractTextbox.setText("Invalid interact button value\nPlease choose a single key")
            return
        elif interact_text.isalnum == False:
            self.ui.AutoInteractTextbox.setText("Invalid interact button value\nPlease choose an alphanumeric key")
            return

        # Get the delay from the spinBox (convert milliseconds to seconds)
        button_delay = self.ui.ButtonPressDelaySpinbox.value() / 1000.0
        
        # Update the status label (label_4) to indicate that the macro has started
        self.ui.AutoInteractTextbox.setText(f"Auto Interact/Harvest macro started...\nPressing <{interact_text}> key now\nPress 'q' or 'esc' key to stop")
        
        # Reset the global keyboard listener stop state
        global_keyboard_listener.unchecked_stop_key()
        
        self.worker = MacroWorker(global_keyboard_listener, interact_text, button_delay)
        self.worker_thread = QtCore.QThread()
        self.worker.moveToThread(self.worker_thread)
        self.worker_thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.on_macro_finished)
        self.worker.finished.connect(self.worker_thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.worker_thread.finished.connect(self.worker_thread.deleteLater)
        self.worker_thread.start()
    
    def on_macro_finished(self, message):
        self.ui.AutoInteractTextbox.setText(message)


    def updateValidator(self):
        if self.ui.InteractButtonSpecialValueCheckbox.isChecked():
            # If the checkbox is checked, allow all characters:
            self.ui.InteractButtonValue.setMaxLength(7)
        else:
            # If unchecked, restrict to alphanumeric characters only.
            # The regex "[A-Za-z0-9]" allows exactly one letter or digit.
            if self.ui.InteractButtonValue.text():
                new_letter = self.ui.InteractButtonValue.text()[0]
                self.ui.InteractButtonValue.setMaxLength(1)
                self.ui.InteractButtonValue.setText(new_letter)
    
    #=== END AUTO INTERACT TAB ===

    ### === AUTO CUBER TAB ===
    def start_auto_cuber(self):
        """
        This method starts the auto cuber macro.
        It reads parameters from the AutoCuber tab, updates the status,
        resets the keyboard listener, and starts the macro in a background thread.
        """
        # Read parameters from the AutoCuber tab widgets.
        equipment_type = self.ui.EqmTypeSelectionbox.currentText()
        equipment_level = self.ui.EqmLevelSelectionBox.currentText()
        desired_tier = self.ui.DesiredTierSelectionBox.currentText()
        roll_for_tier = self.ui.RollForTierUpCheckbox.isChecked()
        
        # Debug: Print parameters to console.
        print("Starting Auto Cuber with parameters:")
        print("  Equipment Type:", equipment_type)
        print("  Equipment Level:", equipment_level)
        print("  Desired Tier:", desired_tier)
        print("  Roll for Tier Up:", roll_for_tier)
        
        # Update the AutoCuber status label.
        self.ui.CuberStatusLabel.setText("Auto Cuber macro started...\nPress 'q' to stop")
        
        # Reset the keyboard listener stop state.
        global_keyboard_listener.unchecked_stop_key()
        
        def run_auto_cuber():
            # Call the auto cuber macro function.
            # (Assuming kb_mash.auto_cuber exists and takes these parameters.)
            exit_code = kb_mash.auto_cuber(global_keyboard_listener,
                                           equipment_type,
                                           equipment_level,
                                           desired_tier,
                                           roll_for_tier)
            if exit_code == 2:
                print("User Interrupted: Auto Cuber Button Released")
            elif exit_code == 1:
                print("User Interrupted: Auto Cuber Button Loop Exited")
            else:
                print("Auto Cuber Button Loop Exited")
        
        threading.Thread(target=run_auto_cuber, daemon=True).start()
    ### === END ADDED FOR AUTO CUBER TAB ===


class MacroWorker(QObject):
    finished = pyqtSignal(str)  # Signal to indicate macro finished, passing the exit message

    def __init__(self, global_keyboard_listener, interact_text, delay):
        super().__init__()
        self.listener = global_keyboard_listener
        self.interact_text = interact_text
        self.delay = delay

    def run(self):
        exit_code = kb_mash.npc_interact(self.listener, self.interact_text, self.delay)
        if exit_code == 2:
            result = "User Interrupted: Auto Interact Button Released"
        elif exit_code == 1:
            result = "User Interrupted: Auto Interact Button Loop Exited"
        else:
            result = "Auto Interact Button Loop Exited"
        self.finished.emit(result)



def main():
    app = QtWidgets.QApplication(sys.argv)
    dashboard = Dashboard()
    dashboard.setWindowTitle("Automation Software GUI")
    dashboard.resize(680, 880)  # Match your UI size from the .ui file
    dashboard.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
