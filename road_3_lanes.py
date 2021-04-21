#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from lwr_library import MakeRoad 

road = MakeRoad(free_v = 110, mean_time_gap = 1.4, 
                road_length = 2 , density_max = 160,  num_lanes = 3, dt=1/1200)
road.homogeneous(0.8,1)

def lane_reduction(road, start, length = 0.5):
    c_i = round(start * road.n_cells)
    c_f = round((start + length/road.road_length)*road.n_cells)
    i=0
    di = 1/(c_f-c_i)
    for c in road.cell[c_i:c_f+1]:
        c.num_lanes = road.num_lanes - i
        i+=di
    for c in road.cell[c_f+1:]:
        c.num_lanes = road.num_lanes - 1

lane_reduction(road, 0.5, length=0.7)
for i in range(road.iteration):
    road.data.append(road.update_density())


road.plot_data()
    
