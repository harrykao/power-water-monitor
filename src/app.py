#!/usr/bin/env python3

import flume
import plot
import rainforest

plot.plot(flume.get_data(), rainforest.get_data())
