import datetime
import os
import typing

import dateutil.tz
import matplotlib.axes
import matplotlib.dates
import matplotlib.pyplot
import matplotlib.ticker

import flume

tz = dateutil.tz.gettz(os.environ["TIMEZONE"])


def plot(
    flume_data: typing.List[typing.Tuple[int, float]],
    rainforest_data: typing.List[typing.Tuple[int, float]],
):

    fig, [ax_top, ax_bottom] = matplotlib.pyplot.subplots(
        nrows=2, sharex=True, figsize=(10, 12), dpi=300
    )

    _plot_flume(flume_data, ax_top)
    _plot_rainforest(rainforest_data, ax_bottom)

    fig.savefig("/work/test.png")
    matplotlib.pyplot.show()


def _convert_x_data(seconds: typing.List[int]) -> typing.List[float]:

    epoch_start_days = datetime.date(1970, 1, 1).toordinal()
    x_datetimes = [datetime.datetime.fromtimestamp(s) for s in seconds]
    x_days = []

    for dt in x_datetimes:
        int_part = dt.date().toordinal() - epoch_start_days
        day_start_s = datetime.datetime.combine(
            dt.date(), datetime.time.min, tzinfo=tz
        ).timestamp()
        frac_part = (dt.timestamp() - day_start_s) / (24 * 60 * 60)
        x_days.append(int_part + frac_part)

    return x_days


def _plot_flume(data: typing.List[typing.Tuple[int, float]], ax: matplotlib.axes.Axes):

    # plot data
    x_data = _convert_x_data([p[0] for p in data])
    y_data = [p[1] / flume.RESOLUTION_MINUTES for p in data]
    ax.bar(
        x_data,
        y_data,
        width=flume.RESOLUTION_MINUTES / (24 * 60),
        align="edge",
        zorder=3,
    )

    # set up axes (rainforest function will set x locator and limits
    ax.set(ylabel="gal/min", title="Water Use")
    ax.xaxis.set_tick_params(labelbottom=True)
    tick_values = matplotlib.ticker.MultipleLocator(0.5).tick_values(
        min(y_data), max(y_data)
    )
    ax.yaxis.set_major_locator(matplotlib.ticker.MultipleLocator(0.5))
    ax.yaxis.set_minor_locator(matplotlib.ticker.MultipleLocator(0.25))
    ax.set_ylim(0, tick_values[-1])

    # set up grid
    ax.grid(True, color="lightgrey", zorder=0)


def _plot_rainforest(
    data: typing.List[typing.Tuple[int, float]], ax: matplotlib.axes.Axes
):

    # stuff for calculating x data
    now = datetime.datetime.now(tz=tz)
    end_datetime = datetime.datetime.combine(now.date(), datetime.time.min, tzinfo=tz)
    start_datetime = end_datetime - datetime.timedelta(days=1)

    # stuff for calculating y data
    min_y = min([p[1] for p in data])
    max_y = max([p[1] for p in data])
    tick_values = matplotlib.ticker.MultipleLocator(2).tick_values(min_y, max_y)

    # plot data
    ax.plot(_convert_x_data([p[0] for p in data]), [p[1] for p in data], linewidth=0.75)

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
