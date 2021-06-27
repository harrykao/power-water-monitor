#!/usr/bin/env python3

import datetime
import os

import dateutil.tz
from slack_sdk import WebClient

import flume
import plot
import rainforest

FILENAME = "/graph.png"

flume_data = flume.get_data()
rainforest_data = rainforest.get_data()

plot.plot(flume_data.timeseries, rainforest_data.timeseries, FILENAME)

tz = dateutil.tz.gettz(os.environ["TIMEZONE"])
yesterday = datetime.datetime.now(tz=tz) - datetime.timedelta(days=1)

comment_lines = [
    yesterday.strftime("%A, %B %-d"),
    f"*Water:* {int(flume_data.summary)} gallons",
    f"*Power:* {rainforest_data.summary:.2f} KWh",
]

client = WebClient(token=os.environ["SLACK_TOKEN"])
client.files_upload(
    channels=os.environ["SLACK_CHANNEL"],
    file=FILENAME,
    initial_comment="\n".join(comment_lines),
)
