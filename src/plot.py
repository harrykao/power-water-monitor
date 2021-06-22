import datetime
import os
import typing

import dateutil.tz
import matplotlib.axes
import matplotlib.dates
import matplotlib.pyplot

tz = dateutil.tz.gettz(os.environ["TIMEZONE"])


def plot(rainforest_data: typing.List[typing.Tuple[int, float]]):

    fig, ax = matplotlib.pyplot.subplots()

    _plot_rainforest(rainforest_data, ax)

    fig.savefig("/work/test.png")
    matplotlib.pyplot.show()


def _plot_rainforest(
    data: typing.List[typing.Tuple[int, float]], ax: matplotlib.axes.Axes
):

    now = datetime.datetime.now(tz=tz)
    end_datetime = datetime.datetime.combine(now.date(), datetime.time.min, tzinfo=tz)
    start_datetime = end_datetime - datetime.timedelta(days=1)
    epoch_start_days = datetime.date(1970, 1, 1).toordinal()

    x_datetimes = [datetime.datetime.fromtimestamp(p[0]) for p in data]
    x_days = []
    for dt in x_datetimes:
        int_part = dt.date().toordinal() - epoch_start_days
        day_start_s = datetime.datetime.combine(
            dt.date(), datetime.time.min, tzinfo=tz
        ).timestamp()
        frac_part = (dt.timestamp() - day_start_s) / (24 * 60 * 60)
        x_days.append(int_part + frac_part)

    ax.plot(x_days, [p[1] for p in data])

    # set up x axes
    ax.set(xlabel="time", ylabel="KW", title="Net Energy Use")
    ax.xaxis.set_major_locator(matplotlib.dates.HourLocator(interval=2))
    ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter("%H"))
    ax.set_xlim(
        left=start_datetime.date().toordinal() - datetime.date(1970, 1, 1).toordinal(),
        right=end_datetime.date().toordinal() - datetime.date(1970, 1, 1).toordinal(),
    )

    # add black line at 0
    ax.axline((0, 0), slope=0, color="black", linewidth=1)

    ax.grid(True, color="lightgrey")
