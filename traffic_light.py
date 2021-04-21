#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from lwr_library import MakeRoad



road = MakeRoad(free_v = 50, mean_time_gap = 1.2, road_length = 1.4, 
                density_max = 120)
road.homogeneous(0.7,1)


for i in range(road.iteration):
    #road.data.append(road.update_density())
    if i in [15,50,70]:
        road.cell[11].bn_reduction = 1
    elif i in [25,60,80]:
        road.cell[11].bn_reduction = 0
    road.data.append(road.update_density())
    
road.plot_data() 

