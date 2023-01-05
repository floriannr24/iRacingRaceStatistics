import tkinter as tk
import datetime
import configparser
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from data.recent_races import RecentRaces
from helpers.diagram import Diagram, Configurator
from sessionbuilder.session_builder import SessionBuilder
import pytz
from iso3166 import countries


class GUI(tk.Frame):
    def __init__(self, root, *args, **kwargs):
        tk.Frame.__init__(self, root, *args, **kwargs)
        self.root = root
        self.window_width = None

        # init timeinfo
        self.timeinfo = Timeinfo()
        self.timezone = self.loadTimzeone()

        # init session
        my_sessionBuilder = SessionBuilder()
        my_sessionBuilder.authenticate()
        self.session = my_sessionBuilder.session

        # init menubar
        self.menubar = Menubar(self)

        # init frames
        self.top = Top(self)
        self.top.pack()

        self.bottom = Bottom(self)
        self.bottom.pack()

        self.canvas = Canvas(self)
        self.canvas.pack(side="bottom")

        self.root.update_idletasks()
        self.window_width = self.root.winfo_width()

    def loadTimzeone(self):
        try:
            return SettingsFile().loadSettingsFile()["general"]["timezone"]
        except KeyError:
            return None


class Timeinfo:
    def __init__(self):
        self.getCountryData()

    def getCountryData(self):

        tzList = []
        for c in countries:
            dict = {}
            dict["country"] = c[0]
            dict["country_code"] = c[1]
            try:
                tzint_lbl = []
                tzint_val = []
                for tz in pytz.country_timezones[c[1]]:
                    tzint_val.append(tz)
                    dict["timezones_values"] = tzint_val
                    td = self.calcTimeDifference(tz)
                    tzint_lbl.append(f"(UTC {td}) {tz}")
                dict["timezones_label"] = tzint_lbl
            except KeyError:
                continue
            tzList.append(dict)
        return tzList

    def calcTimeDifference(self, tz):
        tz1 = pytz.timezone("UTC")
        tz2 = pytz.timezone(tz)
        time1 = tz1.localize(datetime.datetime.now())
        time2 = tz2.localize(datetime.datetime.now())
        duration = (time1 - time2).total_seconds()
        td = divmod(duration, 3600)[0]

        if td >= 0:
            td = "+" + str(td) + "0"
        else:
            td = str(td) + "0"
        if len(td) < 6:
            td = td[0:1] + "0" + td[1:]
        td = td.replace(".", ":")

        return td

    def convertToTimezone(self, string, timezone):
        if not timezone:
            timezone = "UTC"

        time = datetime.datetime.strptime(string, '%Y-%m-%dT%H:%M:%SZ')
        utc = time.replace(tzinfo=pytz.UTC)
        dt_tz = utc.astimezone(pytz.timezone(timezone))
        return dt_tz.strftime('%Y-%m-%d  %H:%M:%S')


class SettingsFile:
    def __init__(self):
        self.settings = configparser.ConfigParser()

    def saveSettingsFile(self, **options):

        if not "general" in self.settings:
            self.settings.add_section("general")

        for opt, value in options.items():
            self.settings['general'][opt] = value

        with open("settings.ini", "w") as file:
            self.settings.write(file)

    def loadSettingsFile(self):
        self.settings.read("settings.ini")
        return self.settings


class Menubar:
    def __init__(self, parent):
        self.parent = parent
        self.parent.root.option_add('*tearOff', False)
        self.window_settings = None

        menubar = tk.Menu(self.parent.root)
        self.parent.root.config(menu=menubar)

        menubar.add_command(
            label="Settings",
            command=self.openSettings_window
        )

    def openSettings_window(self):
        self.window_settings = Settings(self.parent)
        self.window_settings.geometry("300x300")
        self.window_settings.propagate(False)


class Settings(tk.Toplevel):
    def __init__(self, root):
        super().__init__(root)
        self.countryData = None
        self.root = root
        self.location = None
        self.initProcess = True
        self.tz_list = None
        self.settingsFile = SettingsFile()

        location_label = tk.Label(self, text="Location:")
        location_label.grid(column=0, row=0)

        self.location_combo = ttk.Combobox(self, state="readonly", width=30)
        self.location_combo.config(validate="focus", validatecommand=self.insertTimezones)
        self.location_combo.grid(column=1, row=0)
        self.location_combo["values"] = self.insertCountries()
        self.location_combo.current(self.loadLocation())

        timezone_label = tk.Label(self, text="Timezone:")
        timezone_label.grid(column=0, row=1)

        self.timezone_combo = ttk.Combobox(self, state="readonly", width=30)
        self.timezone_combo.grid(column=1, row=1)
        self.timezone_combo["state"] = "readonly"

        self.insertTimezones()

        self.save_button = ttk.Button(self, text="Save", command=self.saveSettings)
        self.save_button.grid(column=0, row=3)

        self.loadTz()

    def insertCountries(self):
        self.countryData = self.root.timeinfo.getCountryData()
        return [f"{c['country']}" for c in self.countryData]

    def insertTimezones(self):
        for cd in self.countryData:
            if cd["country"] == self.location_combo.get():
                self.tz_list = cd
                self.timezone_combo["values"] = cd["timezones_label"]
                self.timezone_combo.current(0)
        return True

    def saveSettings(self):

        # clean timezone value
        tz = self.timezone_combo.get()
        tz = tz[tz.index(")")+2:len(tz)]

        self.settingsFile.saveSettingsFile(
            location=self.location_combo.get(),
            timezone=tz
            )
        self.root.timezone = tz
        self.destroy()

    def loadLocation(self):
        try:
            loc = self.settingsFile.loadSettingsFile()["general"]["location"]
            return self.insertCountries().index(loc)
        except KeyError:
            return 0

    def loadTz(self):
        try:
            tz = self.settingsFile.loadSettingsFile()["general"]["timezone"]
            x = self.tz_list["timezones_values"].index(tz)
            self.timezone_combo.current(x)
        except KeyError:
            return 0


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

        top_label = ttk.Label(self, text="Choose race session", font=("Arial", "14"))
        top_label.grid(column=0, row=0, padx=10, pady=10, sticky="w", columnspan=2)

        r1 = ttk.Radiobutton(self, text="Race session:", variable=self.radio, value=0)
        r1.grid(column=0, row=1, sticky="w", padx=10, pady=3)

        columnsTree = ("time", "series", "track", "start_pos", "finish_pos", "winner", "sof", "subsession_id")
        self.tree = ttk.Treeview(self, columns=columnsTree, show="headings", height=5, selectmode="browse")

        self.tree.heading("time", text="Time")
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

        for data in tree_data:
            data['session_start_time'] = self.parent.timeinfo.convertToTimezone(data['session_start_time'], self.parent.timezone)

        tree_values = [
            (f"{x['session_start_time']}", f"{x['series_name']}", f"{x['track_name']}", f"{x['start_position']}",
             f"{x['finish_position']}", f"{x['winner_name']}", f"{x['SOF']}", f"{x['subsession_id']}")
            for x in tree_data]

        for data in tree_values:
            self.tree.insert("", tk.END, values=data)

        return tree_values

    def refresh_table(self):
        for data in self.tree.get_children():
            self.tree.delete(data)
        self.fillTree(False)


class Canvas(tk.Frame):
    def __init__(self, parent):
        super().__init__(height=500)
        self.parent = parent
        self.canvas = None

    def addToCanvas(self, fig):
        if self.canvas:
            self.canvas.get_tk_widget().pack_forget()

        if fig:
            self.canvas = FigureCanvasTkAgg(fig, master=self)
            self.canvas.get_tk_widget().pack()


class Bottom(tk.Frame):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        bottom_label = ttk.Label(self, text="Choose type of diagram", font=("Arial", "14"))
        bottom_label.pack(anchor="w", padx=10, pady=(25, 8))

        style = ttk.Style(self)
        style.configure('lefttab.TNotebook', tabposition="wn")

        self.notebook = Notebook(self, style="lefttab.TNotebook", padding=10)


class Notebook(ttk.Notebook):
    def __init__(self, parent, style, padding):
        super().__init__(parent, style=style, padding=padding)
        self.parent = parent

        self.tab1 = Tab_BPM(self)
        self.tab2 = Tab_DELTA(self)

        self.add(self.tab1, text='bpm')
        self.add(self.tab2, text="delta")
        self.pack(side="left", expand=1, fill="x")


class Tab_BPM(tk.Frame):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.top = parent.parent.parent.top
        self.session = parent.parent.parent.session
        self.optional = tk.IntVar()
        self.setYMinMax_val = tk.IntVar()
        self.setYInterval_val = tk.IntVar()
        self.DISQDISC_val = tk.IntVar()
        self.dots_val = tk.IntVar()
        self.mean_val = tk.IntVar()
        self.median_line_val = tk.IntVar()

        tab1_title = tk.Label(self, text="Boxplot (multiple players)", font=("Arial", "11"))
        tab1_title.grid(column=0, row=0, padx=3, pady=5)

        self.start_button_bpm = tk.Button(self, text="Start", command=self.start_bpm, width=20, height=2)
        self.start_button_bpm.grid(column=0, row=0, sticky="s", padx=20, pady=10, rowspan=6)

        self.optional_cb = ttk.Checkbutton(self, text="Options:", variable=self.optional, command=self.activate_Options)
        self.optional_cb.grid(column=2, row=0)

        sep1 = ttk.Separator(self, orient="vertical")
        sep1.grid(column=1, row=0, rowspan=7, sticky="ns", padx=(0, 20))

        self.setYMinMax_cb = ttk.Checkbutton(self, text="Set y-axis:", variable=self.setYMinMax_val,
                                             command=self.activate_yminymax)
        self.setYMinMax_cb.grid(column=2, row=1, sticky="w")
        self.ymin_entry = ttk.Entry(self, width=8)
        self.ymin_entry.grid(column=3, row=1, sticky="w")
        self.ymin_entry.config(state="disabled")
        self.ymax_entry = ttk.Entry(self, width=8)
        self.ymax_entry.grid(column=4, row=1, columnspan=2, padx=5)
        self.ymax_entry.config(state="disabled")

        self.setYAxisInterval_cb = ttk.Checkbutton(self, text="Set y-axis interval:",
                                                   variable=self.setYInterval_val, command=self.activate_interval)
        self.setYAxisInterval_cb.grid(column=2, row=2, sticky="w")
        self.yAxisInterval_combo = ttk.Combobox(self, width=5)
        self.yAxisInterval_combo.grid(column=3, row=2, sticky="w")
        self.yAxisInterval_combo["state"] = "disabled"
        self.yAxisInterval_combo["values"] = ("2.0", "1.0", "0.5", "0.25")
        self.yAxisInterval_combo.current(2)

        self.showDISCDISQ_cb = ttk.Checkbutton(self, text="Show disconnected / disqualified drivers",
                                               variable=self.DISQDISC_val)
        self.showDISCDISQ_cb.grid(column=2, row=3, sticky="w")

        self.showDots_cb = ttk.Checkbutton(self, text="Show individual laptimes", variable=self.dots_val)
        self.showDots_cb.grid(column=2, row=4, sticky="w")

        self.showMean_cb = ttk.Checkbutton(self, text="Show median line for user", variable=self.median_line_val)
        self.showMean_cb.grid(column=2, row=5, sticky="w")

        self.showMean_cb = ttk.Checkbutton(self, text="Show mean", variable=self.mean_val)
        self.showMean_cb.grid(column=2, row=6, sticky="w")

        sep2 = ttk.Separator(self, orient="vertical")
        sep2.grid(column=6, row=0, rowspan=7, sticky="ns")

        tab1_description = ttk.Label(self,
                                     text="Creates a diagram with multiple boxplots. Every driver who took part in \n"
                                          "the race session is displayed as a boxplot. In multiclass races, only one \n"
                                          "carclass (and its drivers) is displayed. The carclass is determined by what \n"
                                          "carclass you were part of in the race."
                                     , font=("Arial", "10"))
        tab1_description.grid(column=7, row=0, rowspan=6, padx=5, pady=5)

    def activate_Options(self):

        listOfWidgets = [x for x in self.winfo_children() if x["text"] != "Options:" if x["text"] != "Start"]

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
        config = self.packConfig_bpm()

        if self.top.radio.get() == 0:

            try:
                treeItem_Selected = self.top.tree.item(self.top.tree.focus())
                treeItem_SubsessionID = treeItem_Selected["values"][7]
                diagram = Diagram([treeItem_SubsessionID], self.session, config)
                self.top.parent.canvas.addToCanvas(diagram.data.fig)

            except IndexError:
                print("No value selected")

        if self.top.radio.get() == 1:
            if not self.parent.top.entry2.get():
                print("No value entered")
            else:
                Diagram([self.top.entry2.get()], self.session, config)

    def packConfig_bpm(self):

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
                            px_width=self.top.parent.window_width,
                            px_height=500
                            )


class Tab_DELTA(tk.Frame):
    def __init__(self, parent):
        super().__init__()


root = tk.Tk()
GUI(root).pack(side="top", fill="both", expand=True)
root.mainloop()
