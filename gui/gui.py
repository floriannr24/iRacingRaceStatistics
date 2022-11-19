import tkinter as tk
from tkinter import ttk

from data.recent_races import RecentRaces
from helpers.diagram import Diagram, Configurator
from sessionbuilder.session_builder import SessionBuilder


class GUI(tk.Frame):
    def __init__(self, root, *args, **kwargs):
        tk.Frame.__init__(self, root, *args, **kwargs)

        # init session
        my_sessionBuilder = SessionBuilder()
        my_sessionBuilder.authenticate()
        self.session = my_sessionBuilder.session

        # init frames
        self.top = Top(self)
        self.tab_bpm = Tab_BPM(self)
        #self.tab_delta = Tab_DELTA(self)
        self.top.pack(side="top", fill="x")
        self.tab_bpm.pack(side="bottom", fill="x")


class Top(tk.Frame):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.radio = tk.IntVar()
        self.var1 = tk.IntVar()
        self.entry1_index = tk.IntVar()
        self.listOfWidgets = None
        self.session = self.parent.session

        # Top frame
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=5)

        top_label = ttk.Label(self, text="Choose race session", font=("Arial", "14"))
        top_label.grid(column=0, row=0, padx=10, pady=10, sticky="w", columnspan=2)

        r1 = ttk.Radiobutton(self, text="Race session:", variable=self.radio, value=0)
        r1.grid(column=0, row=1, sticky="w", padx=10, pady=3)

        columnsTree = ("time", "series", "track", "start_pos", "finish_pos", "winner", "sof", "subsession_id")
        self.tree = ttk.Treeview(self, columns=columnsTree, show="headings", height=5, selectmode="browse")

        self.tree.heading("time", text="Time (GMT)")
        self.tree.heading("series", text="Series")
        self.tree.heading("track", text="Track")
        self.tree.heading("start_pos", text="Start")
        self.tree.heading("finish_pos", text="Finish")
        self.tree.heading("winner", text="Winner")
        self.tree.heading("sof", text="SOF")
        self.tree.heading("subsession_id", text="Subsession ID")
        self.tree.grid(column=1, row=1, sticky="we")

        self.tree.column("time", width=140)
        self.tree.column("start_pos", width=50)
        self.tree.column("finish_pos", width=50)
        self.tree.column("winner", width=110)
        self.tree.column("sof", width=70)
        self.tree.column("subsession_id", width=90)

        self.fillTree(True)

        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(column=2, row=1, sticky="ns")

        r2 = ttk.Radiobutton(self, text="Subsession ID:", variable=self.radio, value=1)
        r2.grid(column=0, row=2, sticky="w", padx=10, pady=3)

        self.entry2 = ttk.Entry(self)
        self.entry2.grid(column=1, row=2, sticky="w", padx=(0, 10), pady=3)

        self.refresh_button = tk.Button(self, text="Refresh table", command=self.refresh_table)
        self.refresh_button.grid(column=1, row=2, sticky="e", pady=3)

    def fillTree(self, fetchFromCache):
        tree_data = RecentRaces(self.session).get_RecentRaces_Data(fetchFromCache)

        tree_values = []

        for x in tree_data:
            tree_values.append(
                (f"{x['session_start_time']}", f"{x['series_name']}", f"{x['track_name']}", f"{x['start_position']}",
                 f"{x['finish_position']}", f"{x['winner_name']}", f"{x['SOF']}", f"{x['subsession_id']}")
            )

        for data in tree_values:
            self.tree.insert("", tk.END, values=data)

        return tree_values

    def refresh_table(self):
        self.fillTree(False)


class Tab_BPM(tk.Frame):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.optional = tk.IntVar()
        self.setYMinMax_val = tk.IntVar()
        self.setYInterval_val = tk.IntVar()
        self.DISQDISC_val = tk.IntVar()
        self.dots_val = tk.IntVar()
        self.mean_val = tk.IntVar()
        self.median_line_val = tk.IntVar()


        bottom_label = ttk.Label(self, text="Choose type of diagram", font=("Arial", "14"))
        bottom_label.pack(anchor="w", padx=10, pady=(25, 8))

        style = ttk.Style(self)
        style.configure('lefttab.TNotebook', tabposition="ws")

        frame_notebook = ttk.Notebook(self, style='lefttab.TNotebook', padding=10)

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

        # self.tab1.columnconfigure(0, weight=1)
        # self.tab1.columnconfigure(1, weight=3)
        # self.tab1.columnconfigure(2, weight=1)
        # self.tab1.columnconfigure(3, weight=1)

        tab1_title = ttk.Label(self.tab1, text="Boxplot (multiple players)", font=("Arial", "11"))
        tab1_title.grid(column=0, row=0, padx=3, pady=5)

        self.start_button_bpm = tk.Button(self.tab1, text="Start", command=self.start_bpm, width=20, height=2)
        self.start_button_bpm.grid(column=0, row=0, sticky="s", padx=20, pady=10, rowspan=6)

        self.optional_cb = ttk.Checkbutton(self.tab1, text="Options:", variable=self.optional,
                                           command=self.activate_Options)
        self.optional_cb.grid(column=2, row=0)

        sep1 = ttk.Separator(self.tab1, orient="vertical")
        sep1.grid(column=1, row=0, rowspan=7, sticky="ns", padx=(0, 20))

        self.setYMinMax_cb = ttk.Checkbutton(self.tab1, text="Set y-axis:", variable=self.setYMinMax_val,
                                             command=self.activate_yminymax)
        self.setYMinMax_cb.grid(column=2, row=1, sticky="w")
        self.ymin_entry = ttk.Entry(self.tab1, width=8)
        self.ymin_entry.grid(column=3, row=1, sticky="w")
        self.ymin_entry.config(state="disabled")
        self.ymax_entry = ttk.Entry(self.tab1, width=8)
        self.ymax_entry.grid(column=4, row=1, columnspan=2, padx=5)
        self.ymax_entry.config(state="disabled")

        self.setYAxisInterval_cb = ttk.Checkbutton(self.tab1, text="Set y-axis interval:",
                                                   variable=self.setYInterval_val, command=self.activate_interval)
        self.setYAxisInterval_cb.grid(column=2, row=2, sticky="w")
        self.yAxisInterval_combo = ttk.Combobox(self.tab1, width=5)
        self.yAxisInterval_combo.grid(column=3, row=2, sticky="w")
        self.yAxisInterval_combo["state"] = "disabled"
        self.yAxisInterval_combo["values"] = ("2.0", "1.0", "0.5", "0.25")
        self.yAxisInterval_combo.current(2)

        self.showDISCDISQ_cb = ttk.Checkbutton(self.tab1, text="Show disconnected / disqualified drivers",
                                               variable=self.DISQDISC_val)
        self.showDISCDISQ_cb.grid(column=2, row=3, sticky="w")

        self.showDots_cb = ttk.Checkbutton(self.tab1, text="Show individual laptimes", variable=self.dots_val)
        self.showDots_cb.grid(column=2, row=4, sticky="w")

        self.showMean_cb = ttk.Checkbutton(self.tab1, text="Show median line for user", variable=self.median_line_val)
        self.showMean_cb.grid(column=2, row=5, sticky="w")

        self.showMean_cb = ttk.Checkbutton(self.tab1, text="Show mean", variable=self.mean_val)
        self.showMean_cb.grid(column=2, row=6, sticky="w")

        sep2 = ttk.Separator(self.tab1, orient="vertical")
        sep2.grid(column=6, row=0, rowspan=7, sticky="ns")

        tab1_description = ttk.Label(self.tab1,
                                     text="Creates a diagram with multiple boxplots. Every driver who took part in \n"
                                          "the race session is displayed as a boxplot. In multiclass races, only one \n"
                                          "carclass (and its drivers) is displayed. The carclass is determined by what \n"
                                          "carclass you were part of in the race."
                                     , font=("Arial", "10"))
        tab1_description.grid(column=7, row=0, rowspan=6, padx=5, pady=5)


    def activate_Options(self):

        listOfWidgets = [x for x in self.tab1.winfo_children() if x["text"] != "Options:" if x["text"] != "Start"]

        for child in listOfWidgets:
            if str(child["state"]) == "disabled":
                child["state"] = "enabled"
            else:
                child["state"] = "disabled"

    def activate_yminymax(self):
        if self.setYMinMax_val.get() == 1:
            self.ymin_entry["state"] = "enabled"
            self.ymax_entry["state"] = "enabled"
        else:
            self.ymin_entry["state"] = "disabled"
            self.ymax_entry["state"] = "disabled"

    def activate_interval(self):
        if self.setYInterval_val.get() == 1:
            self.yAxisInterval_combo["state"] = "readonly"
        else:
            self.yAxisInterval_combo["state"] = "disabled"

    def start_bpm(self):
        config = self.packConfig()

        if self.parent.top.radio.get() == 0:

            try:
                treeItem_Selected = self.parent.tree.item(self.parent.tree.focus())
                treeItem_SubsessionID = treeItem_Selected["values"][7]
                Diagram([treeItem_SubsessionID], self.parent.session, config)
            except IndexError:
                print("No value selected")

        if self.parent.top.radio.get() == 1:
            if not self.parent.top.entry2.get():
                print("No value entered")
            else:
                Diagram([self.parent.entry2.get()], self.parent.session, config)

    def packConfig(self):

        return Configurator("bpm",
                            "Florian Niedermeier2",
                            setYAxis=self.setYMinMax_val.get(),
                            minVal=float(self.ymin_entry.get() or 0),
                            maxVal=float(self.ymax_entry.get() or 0),
                            setYAxisInterval=self.setYInterval_val.get(),
                            interval=float(self.yAxisInterval_combo.get()),
                            showDISC=self.DISQDISC_val.get(),
                            showLaptimes=self.dots_val.get(),
                            showMedianLine=self.median_line_val.get(),
                            showMean=self.mean_val.get(),
                            px_width=800,
                            px_height=600
                            )


class Tab_DELTA(tk.Frame):
    def __init__(self, parent):
        super().__init__()


root = tk.Tk()
GUI(root).pack(side="top", fill="both", expand=True)
root.mainloop()
