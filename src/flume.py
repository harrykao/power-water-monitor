import datetime
import json
import os
import typing

import dateutil.tz
import requests

FLUME_API_URL = "https://api.flumewater.com"
TIME_FORMAT = "%Y-%m-%d %H:%M:%S"
RESOLUTION_MINUTES = 10

tz = dateutil.tz.gettz(os.environ["TIMEZONE"])


def _authenticate() -> str:

    response = requests.post(
        f"{FLUME_API_URL}/oauth/token",
        {
            "client_id": os.environ["FLUME_CLIENT_ID"],
            "client_secret": os.environ["FLUME_CLIENT_SECRET"],
            "username": os.environ["FLUME_USERNAME"],
            "password": os.environ["FLUME_PASSWORD"],
            "grant_type": "password",
        },
    )

    return response.json()["data"][0]["access_token"]


IntervalType = typing.Tuple[str, str]


# need two intervals because each minute-resolution query is limited
# to 1200 points
def _calc_query_intervals() -> typing.Tuple[IntervalType, IntervalType]:

    now = datetime.datetime.now(tz=tz)
    end_datetime = datetime.datetime.combine(now.date(), datetime.time.min)
    start_datetime = end_datetime - datetime.timedelta(days=1)
    mid_datetime = datetime.datetime.combine(start_datetime, datetime.time(12))

    return (
        (
            start_datetime.strftime(TIME_FORMAT),
            mid_datetime.strftime(TIME_FORMAT),
        ),
        (
            mid_datetime.strftime(TIME_FORMAT),
            end_datetime.strftime(TIME_FORMAT),
        ),
    )


def _fetch_data(
    interval_1: IntervalType, interval_2: IntervalType, token: str
) -> typing.List[typing.Tuple[int, float]]:

    response = requests.post(
        f"{FLUME_API_URL}/users/{os.environ['FLUME_USER_ID']}/devices/{os.environ['FLUME_DEVICE_ID']}/query",
        json.dumps(
            {
                "queries": [
                    {
                        "request_id": "1",
                        "bucket": "MIN",
                        "since_datetime": interval_1[0],
                        "until_datetime": interval_1[1],
                        "units": "GALLONS",
                        "group_multiplier": RESOLUTION_MINUTES,
                    },
                    {
                        "request_id": "2",
                        "bucket": "MIN",
                        "since_datetime": interval_2[0],
                        "until_datetime": interval_2[1],
                        "units": "GALLONS",
                        "group_multiplier": RESOLUTION_MINUTES,
                    },
                ]
            }
        ),
        headers={
            "content-type": "application/json",
            "authorization": f"Bearer {token}",
        },
    )

    data = []
    for point in response.json()["data"][0]["1"] + response.json()["data"][0]["2"]:
        data.append(
            (
                int(
                    datetime.datetime.strptime(point["datetime"], TIME_FORMAT)
                    .replace(tzinfo=tz)
                    .timestamp()
                ),
                point["value"],
            )
        )

    return data


def get_data() -> typing.List[typing.Tuple[int, float]]:
    token = _authenticate()
    interval_1, interval_2 = _calc_query_intervals()
    return _fetch_data(interval_1, interval_2, token)
