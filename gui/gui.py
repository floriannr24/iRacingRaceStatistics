import tkinter as tk
from tkinter import ttk
from data.recent_races import RecentRaces
from helpers.diagram import Diagram, Configurator, ConfiguratorTest
from sessionbuilder.session_builder import SessionBuilder


class GUI:

    def __init__(self):
        self.root = tk.Tk()
        self.radio = tk.IntVar()
        self.var1 = tk.IntVar()
        self.entry1_index = tk.IntVar()
        self.root.title("iRacing race analyzer")
        self.listOfWidgets = None

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
            entry_values.append(
                f"{x['session_start_time']} / {x['series_name']} / {x['track_name']} / {x['winner_name']} / {x['SOF']} / {x['subsession_id']}")

        return entry_values


class TabONE(GUI):
    def __init__(self):
        super().__init__()
        self.optional = tk.IntVar()
        self.setYMinMax_val = tk.IntVar()
        self.setYInterval_val = tk.IntVar()
        self.DISQDISC_val = tk.IntVar(value=1)
        self.dots_val = tk.IntVar()
        self.mean_val = tk.IntVar()

        frame_bottom = tk.Frame(self.root)
        frame_bottom.pack(fill="x")

        bottom_label = ttk.Label(frame_bottom, text="Choose type of diagram", font=("Arial", "14"))
        bottom_label.pack(anchor="w", padx=10, pady=(25, 8))

        style = ttk.Style(frame_bottom)
        style.configure('lefttab.TNotebook', tabposition="ws")

        frame_notebook = ttk.Notebook(frame_bottom, style='lefttab.TNotebook', padding=10)

        self.tab1 = ttk.Frame(frame_notebook)
        tab2 = ttk.Frame(frame_notebook)
        tab3 = ttk.Frame(frame_notebook)
        tab4 = ttk.Frame(frame_notebook)
        tab5 = ttk.Frame(frame_notebook)

        frame_notebook.add(self.tab1, text='bpm')
        frame_notebook.add(tab2, text='bps')
        frame_notebook.add(tab3, text='delta')
        frame_notebook.add(tab4, text='delta2avg')
        frame_notebook.add(tab5, text='delta2avgsingle')

        frame_notebook.pack(side="left", expand=1, fill="x")

        self.tab1.columnconfigure(0, weight=1)
        self.tab1.columnconfigure(1, weight=3)
        self.tab1.columnconfigure(2, weight=1)
        self.tab1.columnconfigure(3, weight=1)

        self.optional_cb = ttk.Checkbutton(self.tab1, text="Options:", variable=self.optional,
                                           command=self.activateOptions)
        self.optional_cb.grid(column=1, row=0)

        self.setYAxis_cb = ttk.Checkbutton(self.tab1, text="Set y-axis:", variable=self.setYMinMax_val)
        self.setYAxis_cb.grid(column=1, row=1, sticky="w")
        self.ymin_entry = ttk.Entry(self.tab1)
        self.ymin_entry.grid(column=2, row=1)
        self.ymax_entry = ttk.Entry(self.tab1)
        self.ymax_entry.grid(column=3, row=1)

        self.setYAxisInterval_cb = ttk.Checkbutton(self.tab1, text="Set y-axis interval:",
                                                   variable=self.setYInterval_val)
        self.setYAxisInterval_cb.grid(column=1, row=2, sticky="w")
        self.yAxisInterval_combo = ttk.Combobox(self.tab1)
        self.yAxisInterval_combo.grid(column=2, row=2)
        self.yAxisInterval_combo["state"] = "readonly"
        self.yAxisInterval_combo["values"] = ("2.0", "1.0", "0.5", "0.25")
        self.yAxisInterval_combo.current(2)

        self.showDISCDISQ_cb = ttk.Checkbutton(self.tab1, text="Show DISC / DISQ drivers", variable=self.DISQDISC_val)
        self.showDISCDISQ_cb.grid(column=1, row=3, sticky="w")
        self.showDots_cb = ttk.Checkbutton(self.tab1, text="Show individual laptimes", variable=self.dots_val)
        self.showDots_cb.grid(column=1, row=4, sticky="w")
        self.showMean_cb = ttk.Checkbutton(self.tab1, text="Show mean", variable=self.mean_val).grid(column=1, row=5,
                                                                                                     sticky="w")

        self.start_button_bpm = tk.Button(self.tab1, text="Start", command=self.start_bpm).grid(column=0, row=0,
                                                                                                sticky="we")

        self.root.mainloop()

    def activateOptions(self):

        listOfWidgets = [x for x in self.tab1.winfo_children() if x["text"] != "Options:" if x["text"] != "Start"]

        for child in listOfWidgets:
            if str(child["state"]) == "disabled":
                child["state"] = "enabled"
            else:
                child["state"] = "disabled"

    def start_bpm(self):
        my_sessionBuilder = SessionBuilder()
        my_sessionBuilder.authenticate()
        session = my_sessionBuilder.session

        config = self.packConfig()

        for key, value in config.options.items():
            print(f" Key: {key} / Value: {value} ")

        if self.radio.get() == 0:
            index = self.entry1.current()
            subsession_id = self.entry1_data[index]["subsession_id"]
            Diagram(subsession_id, session, Configurator("bpm"))


        elif self.radio.get() == 1:
            Diagram(self.entry2.get(), session, Configurator("bpm"))

    def packConfig(self):
        return Configurator("bpm",
                            setYAxis=self.setYMinMax_val.get(),
                            minVal=self.ymin_entry.get(),
                            maxVal=self.ymax_entry.get(),
                            showDISC=self.DISQDISC_val.get(),
                            showLaptimes=self.dots_val.get(),
                            showMean=self.mean_val.get()
                            )


TabONE()
