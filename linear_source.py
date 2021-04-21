#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from lwr_library import MakeRoad

road = MakeRoad(free_v = 110, mean_time_gap = 1.4, road_lenght = 2 , density_max = 120,  num_lanes = 3)
road.homogeneous(0,10)

def linear(t):
    return t*road.max_flow*road.num_lanes/road.simulation_time

for i in range(road.iteration):
    road.cell[0].demand = linear(i*2*road.dt)
    road.data.append(road.update_density())

road.plot_data()