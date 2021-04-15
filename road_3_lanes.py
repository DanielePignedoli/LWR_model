#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from lwr_library import MakeRoad, plot_data

road = MakeRoad(free_v = 50, cong_v = -30, road_lenght = 2 , density_max = 160,  num_lanes = 3)
road.homogeneous(0.8,1)


data = []
for i in range(road.iteration):
    data.append(road.update_density())
    if i in range(20,50):
        for c in road.cell[8:10]:
            c.num_lanes = road.num_lanes - 1
    else:
        for c in road.cell[8:10]:
            c.num_lanes = road.num_lanes 
        

plot_data(data)
    
