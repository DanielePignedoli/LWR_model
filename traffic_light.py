#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from lwr_library import MakeRoad, plot_data



road = MakeRoad(free_v = 50, cong_v = -30, road_lenght = 2, 
                density_max = 160,  num_lanes = 2)
road.homogeneous(0.6,1)

data = []

for i in range(road.iteration):
    if i==20:
        road.cell[11].bn_reduction = 1
    elif i ==40:
        road.cell[11].bn_reduction = 0
        
    data.append(road.update_density())
    
plot_data(data) 

