import tkinter as tk
from tkinter import ttk

from helpers.configurator import Configurator
from helpers.diagram import Diagram
from sessionbuilder.session_builder import SessionBuilder


class GUI:

    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("500x300")
        self.var = tk.IntVar()
        self.root.title("iRacing race analyzer")

        # Top frame

        frame_top = tk.Frame(self.root)
        frame_top.pack(side="top", fill="x")

        frame_notebook = tk.Frame(self.root)
        frame_notebook.pack(side="bottom")

        frame_top.columnconfigure(0, weight=1)
        frame_top.columnconfigure(1, weight=5)

        top_label = ttk.Label(frame_top, text="Choose race session", font=("Arial", "14"))
        top_label.grid(column=0, row=0, padx=10, pady=10, sticky="w")

        r1 = ttk.Radiobutton(frame_top, text="Race session:", variable=self.var, value=0, command=self.optIdent)
        r1.grid(column=0, row=1, sticky="w", padx=10, pady=3)

        self.entry1 = ttk.Combobox(frame_top)
        self.entry1.grid(column=1, row=1, sticky="we", padx=(0, 10), pady=3)

        r2 = ttk.Radiobutton(frame_top, text="Subsession ID:", variable=self.var, value=1, command=self.optIdent)
        r2.grid(column=0, row=2, sticky="w", padx=10, pady=3)

        self.entry2 = ttk.Entry(frame_top)
        self.entry2.grid(column=1, row=2, sticky="we", padx=(0, 10), pady=3)

        # Bottom frame

        frame_bottom = tk.Frame(self.root, background="green")
        frame_bottom.pack(side="bottom", fill="x")

        bottom_label = ttk.Label(frame_bottom, text="Choose type of diagram", font=("Arial", "14"))
        bottom_label.pack(anchor="w", padx=10, pady=(0, 8))

        frame_notebook = ttk.Notebook(frame_bottom, padding=10)

        tab1 = ttk.Frame(frame_notebook)
        tab2 = ttk.Frame(frame_notebook)

        frame_notebook.add(tab1, text='Tab 1')
        frame_notebook.add(tab2, text='Tab 2')
        frame_notebook.pack(side="left", padx=10, expand=1, fill="x")

        ttk.Label(tab1, text="Welcome to GeeksForGeeks").grid(column=0, row=0, padx=30, pady=30)
        ttk.Label(tab2, text="Lets dive into the world of computers").grid(column=0, row=0, padx=30, pady=30)

        start_button = tk.Button(frame_bottom, text="Start", width=15, height=7, command=self.start)
        start_button.pack(side="right")

        self.root.mainloop()

    def optIdent(self):
        return self.var.get()

    def start(self):

        my_sessionBuilder = SessionBuilder()
        my_sessionBuilder.authenticate()
        session = my_sessionBuilder.session

        if self.optIdent() == 0:
            print("not yet implemented")

        elif self.optIdent() == 1:
            Diagram(self.entry2.get(), session, Configurator(None, None, "delta"))


GUI()
