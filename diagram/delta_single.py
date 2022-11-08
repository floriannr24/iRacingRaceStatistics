import statistics
import matplotlib.pyplot as plt
import numpy as np


# ToDo: delta to median-time of a single user

class DeltaSingle:
    def __init__(self, input):
        self.ax_color = "#2F3136"
        self.fig_color = "#36393F"
        self.ax_gridlines_color = "#3F434A"
        self.ax_spines_color = "#3F434A"
        self.ax_tick_color = "#C8CBD0"
        self.input = input
        self.px_width = 950
        self.px_height = 600
        self.number_of_laps = input[0]["laps_completed"] + 1
        self.draw()

    def draw(self):

        # define color scheme
        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(self.px_width / 100, self.px_height / 100))

        # set colors
        ax.set_facecolor(self.ax_color)
        ax.grid(color=self.ax_gridlines_color)
        ax.spines["left"].set_color(self.ax_spines_color)
        ax.spines["bottom"].set_color(self.ax_spines_color)
        ax.spines["right"].set_color(self.ax_spines_color)
        ax.spines["top"].set_color(self.ax_spines_color)
        ax.tick_params(axis="x", colors=self.ax_tick_color)
        ax.tick_params(axis="y", colors=self.ax_tick_color)
        fig.set_facecolor(self.fig_color)
        self.colorList_top3 = ["#FFD900", "#CFCEC9", "#D4822A"]
        self.colorList_rest = ['#1f77b4', '#2ca02c', '#A3E6A3', '#d62728', '#811818', '#8261FF', '#8c564b', '#e377c2',
                               '#919191', '#CFCF4B', '#97ED27', '#17becf']
        ax.set_prop_cycle("color", self.colorList_rest)

        for i in range(0, 3, 1):
            ax.plot(self.input[i]["delta"], color=self.colorList_top3[i])

        for i in range(3, len(self.input), 1):
            ax.plot(self.input[i]["delta"])

        bottom_border = 5 * round(self.calculateYMin() * 1.5 / 5)

        # formatting
        ax.set(xlim=(-0.5, self.number_of_laps - 0.5), ylim=(-5, bottom_border))
        ax.set_xticks(np.arange(0, self.number_of_laps))
        # ax.set_xticklabels(np.arange(1, self.number_of_laps+1, 1))
        ax.set_xlabel("Laps", color="white")
        ax.set_ylabel("Cumulative gap to leader in seconds", color="white")
        # ax.set_title("Race report", pad="20.0", color="white")
        ax.legend(self.extractDrivers(), loc="center left", facecolor="#36393F", labelcolor="white",
                  bbox_to_anchor=(1.05, 0.5), labelspacing=0.5, edgecolor="#7D8A93")
        ax.invert_yaxis()
        plt.tick_params(labelright=True)

        plt.tight_layout()

        plt.show()

    def calculateYMin(self):
        deltaAtEnd = []

        for lapdata in self.input:
            indexLastLap = len(lapdata["delta"]) - 1
            deltaAtEnd.append(lapdata["delta"][indexLastLap])
        return statistics.median(deltaAtEnd)

    def extractDrivers(self):
        return [lapdata["driver"] for lapdata in self.input]
