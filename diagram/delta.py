from datetime import timedelta
import matplotlib.pyplot as plt
import numpy as np


class Delta:
    def __init__(self, inputLaps):
        self.ax_color = "#2F3136"
        self.fig_color = "#36393F"
        self.ax_gridlines_color = "#3F434A"
        self.ax_spines_color = "#3F434A"
        self.ax_tick_color = "#C8CBD0"

        # define color scheme
        fig, ax = plt.subplots(nrows=1, ncols=1)

        number_of_seconds_shown = range(64, 75)
        yticks = []

        for sec in number_of_seconds_shown:
            td_raw = timedelta(seconds=sec, hours=0)
            td_hours_removed = str(td_raw).split(":", 1)[1]
            yticks.append(td_hours_removed)

        # formatting
        ax.set_xticks([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14])
        ax.set_yticks(number_of_seconds_shown)
        ax.set_yticklabels(yticks)
        ax.set_xlabel("laps", color="white")
        ax.set_ylabel("time in minutes", color="white")
        ax.set_title("Race report", pad="20.0", color="white")


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

        xpoints = np.array([0, 16])
        ypoints_a = np.array(
            [70.8178, 64.2165, 64.1975, 64.4825, 64.225, 64.5757, 65.8175, 64.6673, 67.7413, 64.7549, 64.546, 65.0116,
             64.8932, 64.822, 65.0979])
        ypoints_b = np.array(
            [74.5294, 65.5478, 64.5615, 64.6712, 64.7194, 64.3988, 64.4796, 64.8501, 65.1459, None, 64.9455, 64.639,
             65.1955, 65.2884, 65.2347])
        ypoints_c = np.array(
            [73.8533, 64.4823, 64.6845, 64.5062, 64.7771, 64.7919, 64.865, 64.7773, 65.0691, 64.672, 64.8025, 65.0183,
             64.7722, 65.2883, 65.186])

        ax.plot(ypoints_a)
        ax.plot(ypoints_b)
        ax.plot(ypoints_c)

        ax.legend(["test1", "test2", "test3"])

        plt.show()
