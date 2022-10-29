import math
import statistics
from datetime import timedelta
from decimal import Decimal, ROUND_HALF_DOWN

import matplotlib.pyplot as plt
import numpy as np


class BoxplotMulti:
    def __init__(self, all_laptimes):
        self.ax = None
        self.fig = None
        self.all_laptimes = all_laptimes
        self.racemetadata = None
        self.px_width = 800
        self.px_height = 600
        self.numberOfDrivers = len(all_laptimes)

        # define color scheme
        self.ax_color = "#2F3136"
        self.ax_gridlines_color = "#3F434A"
        self.ax_spines_color = "#3F434A"
        self.ax_tick_color = "#C8CBD0"
        self.fig_color = "#36393F"
        self.draw()


    def draw(self):

        race_completed_raw = self.extractLaptimes(self.all_laptimes, True)
        race_completed_clean_1 = self.scanForInvalidTypes(race_completed_raw, -1)
        race_completed_clean_2 = self.scanForInvalidTypes(race_completed_clean_1, None)

        race_not_completed_raw = self.extractLaptimes(self.all_laptimes, False)
        race_not_completed_clean_1 = self.scanForInvalidTypes(race_not_completed_raw, -1)
        race_not_completed_clean_2 = self.scanForInvalidTypes(race_not_completed_clean_1, None)

        drivers_raw = self.extractDrivers(self.all_laptimes)

        # self.ax.set_ylabel("time in minutes", color="white")
        # self.ax.set_title("Race report", pad="20.0", color="white")

        xmin = 0  # 0
        xmax = self.numberOfDrivers+1

        maxmin = self.calculateYMaxMin(race_completed_clean_2, 0.5)
        ymax = maxmin[1]
        ymin = maxmin[0]

        intervall = 0.5

        self.fig, self.ax = plt.subplots(nrows=1, ncols=1, figsize=(self.px_width / 100, self.px_height / 100))

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

        self.ax.boxplot(race_completed_clean_2,
                        patch_artist=True,
                        boxprops=dict(facecolor="#0084F2", color="#000000"),
                        flierprops=dict(markeredgecolor='#000000'),
                        medianprops=dict(color="#000000"),
                        whiskerprops=dict(color="#000000"),
                        capprops=dict(color="#000000"),
                        zorder=2,
                        widths=0.6
                        )

        self.ax.boxplot(race_not_completed_clean_2,
                        patch_artist=True,
                        boxprops=dict(facecolor="#6F6F6F", color="#000000"),
                        flierprops=dict(markeredgecolor='#000000'),
                        medianprops=dict(color="#000000"),
                        whiskerprops=dict(color="#000000"),
                        capprops=dict(color="#000000"),
                        zorder=2,
                        widths=0.6
                        )

        # formatting
        number_of_seconds_shown = np.arange(ymin, ymax + intervall, intervall)
        yticks = self.calculateMinutesYAxis(number_of_seconds_shown)
        self.ax.set_yticks(number_of_seconds_shown)
        self.ax.set_yticklabels(yticks)
        self.ax.set_xticks(np.arange(1, len(self.all_laptimes)+1))
        self.ax.set_xticklabels(drivers_raw, rotation=45, rotation_mode="anchor", ha="right")

        plt.tight_layout()

        plt.show()

    def calculateYMaxMin(self, lapdata_clean, roundBase):

        result = []
        tempMax = []
        tempMin = []

        for laps in lapdata_clean:

            if not laps:
                continue

            Q1, Q3 = np.percentile(laps, [25, 75])
            IQR = Q3 - Q1

            loval = Q1 - 1.5 * IQR
            hival = Q3 + 1.5 * IQR

            #find closest real laptime value compared to hival/loval
            candidates_for_top_border = max([item for item in laps if item < hival])
            tempMax.append(candidates_for_top_border)
            tempMin.append(min(laps, key=lambda x: abs(x - loval)))

        maxVal = max(tempMax)   # top border
        minVal = min(tempMin)   # bottom border

        # round min to nearest base (= roundBase; 0.5)
        minVal_test = roundBase * round(minVal / roundBase)

        #if minVal has been rounded up, round down 0.5
        if minVal_test > minVal:
            minval_final = minVal_test-0.5
            result.append(minval_final)
        else:
            result.append(minVal_test)
        result.append(roundBase * round(maxVal / roundBase))

        return result

    def extractDrivers(self, all_laptimes):

        drivers = []
        for lapdata in all_laptimes:
            drivers.append(lapdata["driver"])
        return drivers

    def extractLaptimes(self, all_laptimes, raceCompleted):

        numberOfLapsInRace = all_laptimes[0]["laps_completed"]
        numberOfDrivers = len(all_laptimes)

        if raceCompleted:
            laps = []
            for lapdata in all_laptimes:
                if lapdata["laps_completed"] == numberOfLapsInRace:
                    laps.append(lapdata["laps"])
                else:
                    continue
            return laps

        else:
            laps = []
            for lapdata in all_laptimes:
                if lapdata["laps_completed"] < numberOfLapsInRace:
                    laps.append(lapdata["laps"])
                else:
                    continue

            indicesToFillUp = numberOfDrivers - len(laps)
            for i in range(indicesToFillUp):
                laps.insert(0, "")
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
