from datetime import timedelta, datetime

import matplotlib.pyplot as plt
import numpy as np


class BoxplotSingle:
    def __init__(self, y_values):
        self.y_values = y_values

    fig, ax = plt.subplots(nrows=1, ncols=1)

    y_values = np.array(
        [64.2165, 64.1975, 64.4825, 64.225, 64.5757, 65.8175, 64.6673, 64.7549, 64.546, 65.0116, 64.8932, 64.822])

    # define color scheme
    ax_color = "#2F3136"
    ax_gridlines_color = "#3F434A"
    ax_spines_color = "#3F434A"
    ax_tick_color = "#C8CBD0"
    fig_color = "#36393F"

    number_of_seconds_shown = np.arange(64, 72, 0.2)
    yticks = []

    for sec in number_of_seconds_shown:
        sec_rounded = round(sec, 2)
        td_raw = str(timedelta(seconds=sec_rounded))

        if "." not in td_raw:
            td_raw = td_raw + ".000000"

        td_minutes = td_raw.split(":", 1)[1]
        td_minutes_cutMilliseconds = td_minutes[:-3]
        yticks.append(td_minutes_cutMilliseconds)

    # formatting
    ax.set_yticks(number_of_seconds_shown)
    ax.set_yticklabels(yticks)
    ax.set_ylabel("time in minutes", color="white")
    ax.set_title("Race report", pad="20.0", color="white")

    # set colors
    ax.set_facecolor(ax_color)
    ax.grid(color=ax_gridlines_color, axis="y", zorder=0)
    ax.spines["left"].set_color(ax_spines_color)
    ax.spines["bottom"].set_color(ax_spines_color)
    ax.spines["right"].set_color(ax_spines_color)
    ax.spines["top"].set_color(ax_spines_color)
    ax.tick_params(axis="x", colors=ax_tick_color)
    ax.tick_params(axis="y", colors=ax_tick_color)

    fig.set_facecolor(fig_color)

    xpoints = np.random.normal(loc=1.0, scale=0.005, size=len(y_values))

    ax.scatter(xpoints, y_values, c="#6BBCFF", edgecolors="#0059A2", zorder=4, s=80, alpha=0.7)

    ax.boxplot(y_values,
               patch_artist=True,
               boxprops=dict(facecolor="#0084F2", color="#000000"),
               flierprops=dict(markeredgecolor='#000000'),
               medianprops=dict(color="#000000"),
               whiskerprops=dict(color="#000000"),
               capprops=dict(color="#000000"),
               zorder=2)

    # ax.legend(["test1"])

    plt.show()
