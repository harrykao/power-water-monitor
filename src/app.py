#!/usr/bin/env python3

import flume
import plot
import rainforest

flume_data = flume.get_data()
rainforest_data = rainforest.get_data()

plot.plot(flume_data.timeseries, rainforest_data.timeseries)
