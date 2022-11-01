from datetime import timedelta
import matplotlib.pyplot as plt
import numpy as np


class Delta():
    def __init__(self, input):
        self.ax_color = "#2F3136"
        self.fig_color = "#36393F"
        self.ax_gridlines_color = "#3F434A"
        self.ax_spines_color = "#3F434A"
        self.ax_tick_color = "#C8CBD0"
        self.input = input
        self.px_width = 800
        self.px_height = 600
        self.number_of_laps = np.arange(0, input[0]["laps_completed"])

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

        #ax.legend(["test1", "test2", "test3"])

        # formatting
        ax.set(ylim=(-1, 20))
        ax.set_yticks(np.arange(0, 30, 2))
        ax.set_xticks(self.number_of_laps)
        #ax.set_yticks(number_of_seconds_shown)
        #ax.set_yticklabels(yticks)
        #ax.set_xlabel("laps", color="white")
        #ax.set_ylabel("time in minutes", color="white")
        #ax.set_title("Race report", pad="20.0", color="white")
        ax.invert_yaxis()

        plt.tight_layout()

        plt.show()


