import tkinter as tk
from tkinter import ttk
from data.recent_races import RecentRaces
from helpers.diagram import Diagram, Configurator
from sessionbuilder.session_builder import SessionBuilder


class GUI:

    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("500x280")
        self.radio = tk.IntVar()
        self.var1 = tk.IntVar()
        self.entry1_index = tk.IntVar()
        self.root.title("iRacing race analyzer")

        # Top frame

        frame_top = tk.Frame(self.root)
        frame_top.pack(side="top", fill="x")

        frame_top.columnconfigure(0, weight=1)
        frame_top.columnconfigure(1, weight=5)

        top_label = ttk.Label(frame_top, text="Choose race session", font=("Arial", "14"))
        top_label.grid(column=0, row=0, padx=10, pady=10, sticky="w")

        r1 = ttk.Radiobutton(frame_top, text="Race session:", variable=self.radio, value=0, command=self.enableEntry1)
        r1.grid(column=0, row=1, sticky="w", padx=10, pady=3)

        self.entry1 = ttk.Combobox(frame_top, textvariable=self.entry1_index)
        self.entry1.grid(column=1, row=1, sticky="we", padx=(0, 10), pady=3)
        self.entry1["state"] = "readonly"
        self.entry1["values"] = self.fillEntry1()
        self.entry1.current(0)

        r2 = ttk.Radiobutton(frame_top, text="Subsession ID:", variable=self.radio, value=1, command=self.enableEntry2)
        r2.grid(column=0, row=2, sticky="w", padx=10, pady=3)

        self.entry2 = ttk.Entry(frame_top)
        self.entry2.grid(column=1, row=2, sticky="we", padx=(0, 10), pady=3)
        self.entry2.config(state="disabled")

        # Bottom frame

        frame_bottom = tk.Frame(self.root)
        frame_bottom.pack(fill="x")

        bottom_label = ttk.Label(frame_bottom, text="Choose type of diagram", font=("Arial", "14"))
        bottom_label.pack(anchor="w", padx=10, pady=(25, 8))

        style = ttk.Style(frame_bottom)
        style.configure('lefttab.TNotebook', tabposition="ws")

        frame_notebook = ttk.Notebook(frame_bottom, style='lefttab.TNotebook', padding=10)

        tab1 = ttk.Frame(frame_notebook)
        tab2 = ttk.Frame(frame_notebook)
        tab3 = ttk.Frame(frame_notebook)
        tab4 = ttk.Frame(frame_notebook)
        tab5 = ttk.Frame(frame_notebook)

        frame_notebook.add(tab1, text='bpm')
        frame_notebook.add(tab2, text='bps')
        frame_notebook.add(tab3, text='delta')
        frame_notebook.add(tab4, text='delta2avg')
        frame_notebook.add(tab5, text='delta2avgsingle')

        frame_notebook.pack(side="left", expand=1, fill="x")

        tab1.columnconfigure(0, weight=1)
        tab1.columnconfigure(1, weight=3)
        tab1.columnconfigure(2, weight=5)

        cb1 = ttk.Checkbutton(tab1, text="hgallo", onvalue=1, variable=self.var1)
        cb1.grid(column=0, row=0)

        # ttk.Label(tab1, text="Welcome to GeeksForGeeks").grid(column=0, row=0, padx=30, pady=30)
        # ttk.Label(tab2, text="Lets dive into the world of computers").grid(column=0, row=0, padx=30, pady=30)

        start_button_bpm = tk.Button(tab1, text="Start", command=self.start_bpm).grid(column=1, row=0, sticky="we")

        self.root.mainloop()

    def enableEntry1(self):
        self.entry1.config(state="enabled")
        self.entry2.config(state="disabled")

    def enableEntry2(self):
        self.entry1.config(state="disabled")
        self.entry2.config(state="enabled")

    def fillEntry1(self):
        my_sessionBuilder = SessionBuilder()
        my_sessionBuilder.authenticate()
        session = my_sessionBuilder.session

        self.entry1_data = RecentRaces(session).get_RecentRaces_Data()

        entry_values = []

        for x in self.entry1_data:
            entry_values.append(str(x["session_start_time"]) + " / " + str(x["series_name"]) + " / " + str(x["track_name"]) + " / " + str(x["winner_name"]) + " / " + str(x["SOF"]) + " / " + str(x["subsession_id"]))

        return entry_values

    def start_bpm(self):
        my_sessionBuilder = SessionBuilder()
        my_sessionBuilder.authenticate()
        session = my_sessionBuilder.session

        if self.radio.get() == 0:
            index = self.entry1.current()
            subsession_id = self.entry1_data[index]["subsession_id"]
            Diagram(subsession_id, session, Configurator(None, None, "bpm"))


        elif self.radio.get() == 1:
            Diagram(self.entry2.get(), session, Configurator(None, None, "bpm"))

GUI()



