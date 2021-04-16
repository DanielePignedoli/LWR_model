#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from lwr_library import MakeRoad 

road = MakeRoad(free_v = 80, mean_time_gap = 1.4, 
                road_lenght = 2 , density_max = 160,  num_lanes = 3)
road.homogeneous(0.8,1)

for i in range(road.iteration):
    road.data.append(road.update_density())
    if i in range(20,50):
        for c in road.cell[8:10]:
            c.num_lanes = road.num_lanes - 1
    else:
        for c in road.cell[8:10]:
            c.num_lanes = road.num_lanes 
        

road.plot_data()
    
