import statistics
from datetime import timedelta
import matplotlib.pyplot as plt
import numpy as np


class BoxplotMulti:
    def __init__(self, all_laptimes):
        self.all_laptimes = all_laptimes
        self.racemetadata = None

        # define color scheme
        self.ax_color = "#2F3136"
        self.ax_gridlines_color = "#3F434A"
        self.ax_spines_color = "#3F434A"
        self.ax_tick_color = "#C8CBD0"
        self.fig_color = "#36393F"
        self.draw()

    fig, ax = plt.subplots(nrows=1, ncols=1)

    def draw(self):

        xmin = 0    # 0
        xmax = 13   # number of drivers

        ymax = 67.5   # 75percentile of worst? 75percentile of worst+number?
        ymin = 64   # best overall lap
        intervall = 0.5

        number_of_seconds_shown = np.arange(ymin, ymax+intervall, intervall)
        test = list(number_of_seconds_shown)

        del test[::2]

        yticks = self.calculateMinutesYAxis(number_of_seconds_shown)

        laps_raw = self.extractLaptimes(self.all_laptimes)
        laps_clean1 = self.scanForInvalidTypes(laps_raw, -1)
        laps_clean2 = self.scanForInvalidTypes(laps_clean1, None)

        median_per_lap = []
        mean_per_lap = []
        for laps in laps_clean2:
            if not not laps:
                median_per_lap.append(statistics.median(laps))
                mean_per_lap.append(statistics.mean(laps))
        print("median " + (str(statistics.median(median_per_lap))))
        print("mean " + str(statistics.mean(mean_per_lap)))





        # formatting
        self.ax.set_yticks(number_of_seconds_shown)
        self.ax.set_yticklabels(yticks)
        # self.ax.set_ylabel("time in minutes", color="white")
        # self.ax.set_title("Race report", pad="20.0", color="white")

        # set colors
        self.ax.set_facecolor(self.ax_color)
        self.ax.grid(color=self.ax_gridlines_color, axis="y", zorder=0)
        self.ax.spines["left"].set_color(self.ax_spines_color)
        self.ax.spines["bottom"].set_color(self.ax_spines_color)
        self.ax.spines["right"].set_color(self.ax_spines_color)
        self.ax.spines["top"].set_color(self.ax_spines_color)
        self.ax.tick_params(axis="x", colors=self.ax_tick_color)
        self.ax.tick_params(axis="y", colors=self.ax_tick_color)
        self.fig.set_facecolor(self.fig_color)
        self.ax.set(xlim=(xmin, xmax), ylim=(ymin, ymax))

        self.ax.boxplot(laps_clean2,
                        patch_artist=True,
                        boxprops=dict(facecolor="#0084F2", color="#000000"),
                        flierprops=dict(markeredgecolor='#000000'),
                        medianprops=dict(color="#000000"),
                        whiskerprops=dict(color="#000000"),
                        capprops=dict(color="#000000"),
                        zorder=2,
                        widths=0.6)

        plt.show()

    def extractLaptimes(self, all_laptimes):

        laps = []
        for lapdata in all_laptimes:
            laps.append(lapdata["laps"])
        return laps

    def scanForInvalidTypes(self, all_laptimes, val):

        cleanLaps = []
        for laps in all_laptimes:
            cleanLaps.append([value for value in laps if value != val])
        return cleanLaps

    def calculateMinutesYAxis(self, number_of_seconds_shown):

        yticks = []
        for sec in number_of_seconds_shown:
            sec_rounded = round(sec, 2)
            td_raw = str(timedelta(seconds=sec_rounded))

            if "." not in td_raw:
                td_raw = td_raw + ".000000"

            td_minutes = td_raw.split(":", 1)[1]
            td_minutes_cutMilliseconds = td_minutes[:-3]
            yticks.append(td_minutes_cutMilliseconds)

        return yticks
