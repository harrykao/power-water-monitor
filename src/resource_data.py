import typing


class ResourceData(typing.NamedTuple):
    summary: float
    timeseries: typing.List[typing.Tuple[int, float]]
