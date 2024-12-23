import tkinter as tk
from tkinter import ttk

def create_tab(notebook, title, content):
    """Helper function to create a new tab with given title and content."""
    frame = ttk.Frame(notebook)
    notebook.add(frame, text=title)
    
    # Example content for the tab
    label = tk.Label(frame, text=content, font=("Arial", 14))
    label.pack(pady=20, padx=20)

# Create the main application window
root = tk.Tk()
root.title("Tkinter Tabbed GUI Example")
root.geometry("800x600")

# Create a Notebook widget for the tabs
notebook = ttk.Notebook(root)
notebook.pack(fill='both', expand=True)

# Add tabs to the notebook
create_tab(notebook, "Tab 1", "Welcome to Tab 1")
create_tab(notebook, "Tab 2", "Welcome to Tab 2")
create_tab(notebook, "Tab 3", "Welcome to Tab 3")

# Add a button to add a new tab dynamically
def add_new_tab():
    tab_number = len(notebook.tabs()) + 1
    create_tab(notebook, f"Tab {tab_number}", f"Welcome to Tab {tab_number}")

button_frame = ttk.Frame(root)
button_frame.pack(fill="x", pady=5)

add_tab_button = ttk.Button(button_frame, text="Add New Tab", command=add_new_tab)
add_tab_button.pack(pady=5)

# Run the application
root.mainloop()
