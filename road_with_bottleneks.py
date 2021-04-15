#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from lwr_library import MakeRoad, plot_data


road = MakeRoad(free_v = 50, cong_v = -30, road_lenght = 2 , density_max = 160,  num_lanes = 2)
road.homogeneous(0.6,2)

for c in road.cell[9:12]:
    c.bn_reduction = 0.5
for c in road.cell[18:21]:
    c.bn_reduction = 0.8


data = [road.update_density()  for i in range(road.iteration)]

plot_data(data)
    

