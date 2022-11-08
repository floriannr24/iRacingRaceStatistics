from datetime import timedelta
import matplotlib.pyplot as plt
import numpy as np

from diagram.diagram_base import DiagramBase


# todo: mark own player name as fat
# todo: iRating next to names?

class BoxplotMulti(DiagramBase):
    def __init__(self, input, px_width, px_height):
        super().__init__(input, px_width, px_height)
        self.race_completed_laps = input[0]
        self.race_not_completed_laps = input[1]
        self.drivers_raw = input[2]
        self.number_Of_Drivers = len(input[2])
        self.draw()

    def draw(self):

        # self.ax.set_ylabel("time in minutes", color="white")
        # self.ax.set_title("Race report", pad="20.0", color="white")

        xmin = 0
        xmax = self.number_Of_Drivers + 1

        maxmin = self.calculateYMaxMin(self.race_completed_laps, 0.5)
        ymax = maxmin[1]
        ymin = maxmin[0]

        intervall = 0.5

        self.ax.boxplot(self.race_completed_laps,
                        patch_artist=True,
                        boxprops=dict(facecolor="#0084F2", color="#000000"),
                        flierprops=dict(markeredgecolor='#000000'),
                        medianprops=dict(color="#000000"),
                        whiskerprops=dict(color="#000000"),
                        capprops=dict(color="#000000"),
                        zorder=2,
                        widths=0.6
                        )

        self.ax.boxplot(self.race_not_completed_laps,
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

        self.ax.set(xlim=(xmin, xmax), ylim=(ymin, ymax))
        self.ax.set_yticks(number_of_seconds_shown)
        self.ax.set_yticklabels(self.calculateMinutesYAxis(number_of_seconds_shown))
        self.ax.set_xticks(np.arange(1, self.number_Of_Drivers + 1))
        self.ax.set_xticklabels(self.drivers_raw, rotation=45, rotation_mode="anchor", ha="right")

        plt.tight_layout()
        plt.show()

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
            td_minutes_cutMilliseconds = td_minutes[:-3]
            yticks.append(td_minutes_cutMilliseconds)

        return yticks
