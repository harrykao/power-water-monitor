import datetime
import os
import typing

import dateutil.tz
import matplotlib.axes
import matplotlib.dates
import matplotlib.pyplot
import matplotlib.ticker

tz = dateutil.tz.gettz(os.environ["TIMEZONE"])


def plot(rainforest_data: typing.List[typing.Tuple[int, float]]):

    fig, ax = matplotlib.pyplot.subplots(figsize=(10, 6), dpi=300)

    _plot_rainforest(rainforest_data, ax)

    fig.savefig("/work/test.png")
    matplotlib.pyplot.show()


def _plot_rainforest(
    data: typing.List[typing.Tuple[int, float]], ax: matplotlib.axes.Axes
):

    # stuff for calculating x data
    now = datetime.datetime.now(tz=tz)
    end_datetime = datetime.datetime.combine(now.date(), datetime.time.min, tzinfo=tz)
    start_datetime = end_datetime - datetime.timedelta(days=1)
    epoch_start_days = datetime.date(1970, 1, 1).toordinal()

    # stuff for calculating y data
    min_y = min([p[1] for p in data])
    max_y = max([p[1] for p in data])
    tick_values = matplotlib.ticker.MultipleLocator(2).tick_values(min_y, max_y)

    # prepare x data
    x_datetimes = [datetime.datetime.fromtimestamp(p[0]) for p in data]
    x_days = []
    for dt in x_datetimes:
        int_part = dt.date().toordinal() - epoch_start_days
        day_start_s = datetime.datetime.combine(
            dt.date(), datetime.time.min, tzinfo=tz
        ).timestamp()
        frac_part = (dt.timestamp() - day_start_s) / (24 * 60 * 60)
        x_days.append(int_part + frac_part)

    # plot data
    ax.plot(x_days, [p[1] for p in data], linewidth=0.75)

    # set up axes
    ax.set(xlabel="time", ylabel="KW", title="Net Energy Use")
    ax.xaxis.set_major_locator(matplotlib.dates.HourLocator(interval=2))
    ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter("%H"))
    ax.xaxis.set_minor_locator(matplotlib.dates.HourLocator(interval=1))
    ax.set_xlim(
        left=start_datetime.date().toordinal() - datetime.date(1970, 1, 1).toordinal(),
        right=end_datetime.date().toordinal() - datetime.date(1970, 1, 1).toordinal(),
    )
    ax.yaxis.set_major_locator(matplotlib.ticker.MultipleLocator(2))
    ax.yaxis.set_minor_locator(matplotlib.ticker.MultipleLocator(1))
    ax.set_ylim(tick_values[0], tick_values[-1])

    # set up grid, make y=0 black
    ax.grid(True, color="lightgrey")
    gridlines = ax.get_ygridlines()
    gridlines[list(tick_values).index(0) + 1].set_color("black")
