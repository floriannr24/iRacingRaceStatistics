import statistics
from datetime import timedelta
import random

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
from matplotlib.colors import Normalize
from numpy import linspace

from diagram.diagram_base import DiagramBase


# ToDo: select only a handful of players for comparison


class DeltaMulti(DiagramBase):
    def __init__(self, input, px_width, px_height):
        super().__init__(input, px_width, px_height)
        self.number_of_laps = input[0]["laps_completed"] + 1
        self.draw()

    def draw(self):

        # set line color
        colorList_top3 = ["#FFD900", "#CFCEC9", "#D4822A"]
        colorList_rest = ['#1f77b4', '#2ca02c', '#A3E6A3', '#d62728', '#811818', '#8261FF', '#8c564b', '#e377c2',
                          '#919191', '#CFCF4B', '#97ED27', '#17becf']

        self.ax.set_prop_cycle("color", colorList_rest)

        # draw boxplot
        for i in range(0, 3, 1):
            self.ax.plot(self.input[i]["delta"], color=colorList_top3[i])

        for i in range(3, len(self.input), 1):
            self.ax.plot(self.input[i]["delta"])

        # formatting
        bottom_border = 5 * round(self.calculateYMin() * 1.5 / 5)
        self.ax.set(xlim=(-0.5, self.number_of_laps - 0.5), ylim=(-5, bottom_border))
        self.ax.set_xticks(np.arange(0, self.number_of_laps))
        self.ax.set_xlabel("Laps", color="white")
        self.ax.set_ylabel("Cumulative gap to leader in seconds", color="white")
        self.ax.legend(self.extractDrivers(), loc="center left", facecolor="#36393F", labelcolor="white",
                       bbox_to_anchor=(1.05, 0.5), labelspacing=0.5, edgecolor="#7D8A93")
        # ax.set_title("Race report", pad="20.0", color="white")
        self.ax.invert_yaxis()
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
