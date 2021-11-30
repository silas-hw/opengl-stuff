import tkinter as tk
from tkinter import ttk, messagebox
import json

import os 

class Menu(tk.Frame):

    def __init__(self, root):
        self.dir_path = dir_path = os.path.dirname(os.path.realpath(__file__))
        self.root = root
        self.root.geometry("170x200")
        self.root.resizable(0, 0)
        super().__init__(self.root)

        self.pady = 10
        self.entry_width = 10

        self.rotateLabel = tk.Label(self.root, text="Rotate Speed")
        self.rotateLabel.grid(row=0, column=0, pady=self.pady, sticky=tk.W)

        self.rotateEntry = ttk.Entry(self.root, width=self.entry_width)
        self.rotateEntry.grid(row=0, column=1, pady=self.pady)

        self.movementLabel = tk.Label(self.root, text="Movement Speed")
        self.movementLabel.grid(row=1, column=0, pady=self.pady, sticky=tk.W)

        self.movementEntry = ttk.Entry(self.root, width=self.entry_width)
        self.movementEntry.grid(row=1, column=1, pady=self.pady)

        self.applyButt = ttk.Button(self.root, text="Apply", width=self.entry_width, command=self.applyChanges)
        self.applyButt.grid(row=2, column=1, pady=self.pady)

    def applyChanges(self):
        try:
            movement_speed = int(self.movementEntry.get())
            rotate_speed = int(self.rotateEntry.get())
        except ValueError:
            messagebox.showerror("ERROR", "Entered values must be positive real numbers!")

        with open("config.json", "r") as f:
            current_config = json.load(f)

        current_config['movement_speed'] = movement_speed
        current_config['rotate_speed'] = rotate_speed

        with open("config.json", "w") as f:
            json.dump(current_config, f)

    def createWindow(self):
        self.root.mainloop()

    def destroyWindow(self):
        self.root.destroy()

if __name__ == '__main__':
    root = tk.Tk()
    menu = Menu(root)
    menu.createWindow()