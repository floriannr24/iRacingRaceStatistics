import statistics
from datetime import timedelta
import matplotlib.pyplot as plt
import numpy as np

from diagrams.base import Base

# todo: iRating next to names?

class BoxplotMulti(Base):
    def __init__(self, input, config):
        # init
        self.race_completed_laps = input[0]
        self.race_not_completed_laps = input[1]
        self.drivers_raw = input[2]
        self.number_Of_Drivers = len(input[2])
        self.ymin, self.ymax, self.interval, self.showMean, self.showMedianLine = self.unpackConfig(config.options)

        # draw
        super().__init__(input, config.options.get("px_width"), config.options.get("px_height"))
        self.draw(config.name, config.options)

    def draw(self, name, options):

        xmin = 0
        xmax = self.number_Of_Drivers + 1

        self.ax.boxplot(self.race_completed_laps,
                        patch_artist=True,
                        boxprops=dict(facecolor="#0084F2", color="#000000"),
                        flierprops=dict(markeredgecolor='#000000'),
                        medianprops=dict(color="#000000", linewidth=2),
                        whiskerprops=dict(color="#000000"),
                        capprops=dict(color="#000000"),
                        zorder=2,
                        widths=0.7,
                        showmeans=self.showMean,
                        meanprops=dict(marker="o", markerfacecolor="red", fillstyle="full", markeredgecolor="None")
                        )

        if options.get("showLaptimes") == 1:
            self.draw_laptimes()

        if options.get("showDISC") == 1:
            self.draw_DISCDISQ()

        if self.showMedianLine:
            self.draw_medianLine()

        # formatting
        number_of_seconds_shown = np.arange(self.ymin, self.ymax + self.interval, self.interval)

        self.ax.set(xlim=(xmin, xmax), ylim=(self.ymin, self.ymax))
        self.ax.set_yticks(number_of_seconds_shown)
        self.ax.set_yticklabels(self.calculateMinutesYAxis(number_of_seconds_shown))

        if options.get("showDISC") == 0:
            self.ax.set_xticks(np.arange(1, self.number_Of_Drivers + 1))
            self.ax.set_xticklabels(self.drivers_raw, rotation=45, rotation_mode="anchor", ha="right")
        else:
            self.ax.set_xticks(np.arange(1, self.number_Of_Drivers + 1))
            self.ax.set_xticklabels(self.drivers_raw, rotation=45, rotation_mode="anchor", ha="right")

        try:
            index = self.drivers_raw.index(name)
            self.ax.get_xticklabels()[index].set_fontweight("bold")
        except ValueError:
            pass

        plt.tight_layout()
        plt.show()

    def draw_laptimes(self):
        scatter = []
        for i, lapdata in enumerate(self.race_completed_laps):
            x = np.random.normal(i + 1, 0.06, len(lapdata))
            scatter.append(x)
        for i, data in enumerate(self.race_completed_laps):
            self.ax.scatter(scatter[i], self.race_completed_laps[i],
                            zorder=4,
                            alpha=0.5,
                            c="yellow",
                            s=8
                            )

    def draw_DISCDISQ(self):
            self.ax.boxplot(self.race_not_completed_laps,
                            patch_artist=True,
                            boxprops=dict(facecolor="#6F6F6F", color="#000000"),
                            flierprops=dict(markeredgecolor='#000000'),
                            medianprops=dict(color="#000000", linewidth=2),
                            whiskerprops=dict(color="#000000"),
                            capprops=dict(color="#000000"),
                            zorder=2,
                            widths=0.7
                            )

    def draw_medianLine(self):

        x1 = None
        y1 = None

        try:
            index = self.drivers_raw.index("Florian Niedermeier2")
            user_boxplot_data = self.race_completed_laps[index]
            user_median = statistics.median(user_boxplot_data)
            y1 = [user_median, user_median]
            x1 = [0, 100]

        except ValueError:
            pass

        plt.plot(x1, y1, zorder=3, linestyle="dashed", color="#C2C5CA")


    def calculateYMaxMin(self, lapdata, roundBase):

        result = []
        tempMax = []
        tempMin = []

        for laps in lapdata:

            if not laps:
                continue

            Q1, Q3 = np.percentile(laps, [25, 75])
            IQR = Q3 - Q1

            loval = Q1 - 1.5 * IQR
            hival = Q3 + 1.5 * IQR

            # find closest real laptime value compared to hival/loval
            candidates_for_top_border = max([item for item in laps if item < hival])
            tempMax.append(candidates_for_top_border)
            tempMin.append(min(laps, key=lambda x: abs(x - loval)))

        maxVal = max(tempMax)  # top border
        minVal = min(tempMin)  # bottom border

        # round min to the nearest base (= roundBase; 0.5)
        minVal_test = roundBase * round(minVal / roundBase)

        # if minVal has been rounded up, round down 0.5
        if minVal_test > minVal:
            minval_final = minVal_test - 0.5
            result.append(minval_final)
        else:
            result.append(minVal_test)
        result.append(roundBase * round(maxVal / roundBase))
        return result

    def calculateMinutesYAxis(self, number_of_seconds_shown):

        yticks = []
        for sec in number_of_seconds_shown:
            sec_rounded = round(sec, 2)
            td_raw = str(timedelta(seconds=sec_rounded))

            if "." not in td_raw:
                td_raw = td_raw + ".000000"

            td_minutes = td_raw.split(":", 1)[1]
            yticks.append(td_minutes[:-3])

        return yticks

    def unpackConfig(self, options):

        if options.get("setYAxis") == 1:
            ymin = options.get("minVal")
            ymax = options.get("maxVal")
        else:
            maxmin = self.calculateYMaxMin(self.race_completed_laps, 0.5)
            ymax = maxmin[1]
            ymin = maxmin[0]

        if options.get("setYAxisInterval") == 1:
            interval = options.get("interval")
        else:
            interval = 0.5

        if options.get("showDISC") == 0:
            number_Of_Drivers_Not_Completed = len([data for data in self.race_not_completed_laps if not not data])
            self.number_Of_Drivers = self.number_Of_Drivers - number_Of_Drivers_Not_Completed
            self.drivers_raw = self.drivers_raw[:-number_Of_Drivers_Not_Completed or None]

        if options.get("showMedianLine") == 1:
            showMedianLine = True
        else:
            showMedianLine = False

        if options.get("showMean") == 1:
            showMean = True
        else:
            showMean = False

        return ymin, ymax, interval, showMean, showMedianLine


