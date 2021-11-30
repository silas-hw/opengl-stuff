import tkinter as tk
from tkinter import ttk

class Menu(tk.Frame):

    def __init__(self, root):
        self.root = root
        self.root.geometry("150x200")
        self.root.resizable(0, 0)
        super().__init__(self.root)

        self.pady = 10
        self.entry_width = 10

        self.rotateLabel = tk.Label(self.root, text="Rotate Speed")
        self.rotateLabel.grid(row=0, column=0, pady=self.pady)

        self.rotateEntry = ttk.Entry(self.root, width=self.entry_width)
        self.rotateEntry.grid(row=0, column=1, pady=self.pady)

        self.movementLabel = tk.Label(self.root, text="Movement Speed")
        self.movementLabel.grid(row=1, column=0, pady=self.pady)

        self.movementEntry = ttk.Entry(self.root, width=self.entry_width)
        self.movementEntry.grid(row=1, column=1, pady=self.pady)

    def createWindow(self):
        self.root.mainloop()

    def destroyWindow(self):
        self.root.destroy()

if __name__ == '__main__':
    root = tk.Tk()
    menu = Menu(root)
    menu.createWindow()