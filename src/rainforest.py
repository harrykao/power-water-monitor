import datetime
import json
import os
import typing

import dateutil.tz
import requests

RAINFOREST_API_URL = "https://api.rainforestcloud.com/rest"


def _authenticate() -> str:

    response = requests.post(
        f"{RAINFOREST_API_URL}/auth/accesskey",
        json.dumps(
            {
                "login": os.environ["RAINFOREST_USERNAME"],
                "password": os.environ["RAINFOREST_PASSWORD"],
            }
        ),
    )

    return response.json()["key"]


def _calc_start_end_times() -> typing.Tuple[int, int]:

    tz = dateutil.tz.gettz(os.environ["TIMEZONE"])

    now = datetime.datetime.now(tz=tz)
    today = datetime.datetime.combine(now.date(), datetime.time.min, tzinfo=tz)

    start_ms = int((today - datetime.timedelta(days=1)).timestamp()) * 1000
    end_ms = int(today.timestamp()) * 1000

    return start_ms, end_ms


def _fetch_data(
    start_ms: int, end_ms: int, token: str
) -> typing.List[typing.Tuple[int, float]]:

    response = requests.get(
        f"{RAINFOREST_API_URL}/data/metering/demand/{os.environ['RAINFOREST_DEVICE_GUID']}",
        params={"start": start_ms, "end": end_ms, "frequencyInSec": 60},
        headers={"Authorization": f"Bearer {token}"},
    )

    entries = response.json()[0]["entries"]
    return [
        (int(key_str) // 1000, entries[key_str]) for key_str in sorted(entries.keys())
    ]


def get_data() -> typing.List[typing.Tuple[int, float]]:
    token = _authenticate()
    start_ms, end_ms = _calc_start_end_times()
    return _fetch_data(start_ms, end_ms, token)
