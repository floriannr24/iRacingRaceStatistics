from gui.gui import GUI
import tkinter as tk

root = tk.Tk()
GUI(root).pack(side="top", fill="both", expand=True)
root.mainloop()