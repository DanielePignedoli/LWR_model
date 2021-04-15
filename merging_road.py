#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from lwr_library import  MakeRoad, plot_data

#ROAD 1
road1 = MakeRoad(free_v = 50, cong_v = -30, road_lenght = 1 , density_max = 160,  num_lanes = 3)
road1.homogeneous(0.6,1)

#ROAD 2
road2 = MakeRoad(free_v = 50, cong_v = -30, road_lenght = 1 , density_max = 160,  num_lanes = 1)
road2.homogeneous(0.6,1)

#ROAD 3
road3 = MakeRoad(free_v = 50, cong_v = -30, road_lenght = 1 , density_max = 160,  num_lanes = 3)
road3.homogeneous(0,2)

#%%            
            

data1 = []
data2 = []
data3 = []


for i in range(road1.iteration):
    road1.cell[-1].supply = road3.cell[1].supply*0.9
    road2.cell[-1].supply = road3.cell[1].supply*0.1
    road3.cell[0].demand = road1.cell[-2].demand + road2.cell[-2].demand
    
    data1.append(road1.update_density())
    data2.append(road2.update_density())
    data3.append(road3.update_density())

plot_data(data1)
plot_data(data2)
plot_data(data3)