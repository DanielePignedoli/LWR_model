#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#simulation of a traffic light in the second half of tthe road

import numpy as np
from makecell import MakeCell
import plotting_function

dt = 1/600 #hr
v = 50  #km all'ora
c = -30  #km all'ora
road_lenght = 1.25 #km
p_max  = 160   #veicoli per kilometro (densità a massima capacità)
I = 1 #num of lanes

p_init = 0.8*p_max

iteration = 60

cell_lenght = v * dt
n_cells = round(road_lenght / cell_lenght)

#source cell
source_demand = p_init*v*I
cells = [MakeCell(p_max,v,c, p_init, num_lanes = I, demand = source_demand )]

#road cells
for i in range(n_cells):
    cells.append(MakeCell(p_max,v,c,p_init, num_lanes = I))

#sink_cell
cells.append(MakeCell(p_max,v,c, p_init, num_lanes = I, supply = p_max*v*I))

#%%

#I want to put a red signal two times, followed by a longer green signal
# 1 min red signal == 15 iteration
# 2 min green == 15 iteration

#I put the traffic light at boundary from cell 8 to 9
# so when it's red, the supply of 9 become zero, it cannot accomodate traffic flow for ten iteration

data = np.array([cells[k].density for k in range(1,n_cells+1)])

for i in range(iteration):
    if i < 15:
        red = True
    elif i > 29 and i < 45:
        red = True
    else:
        red = False
    
    for k in range(1,n_cells+1):
        cells[k].update_capacity()
        cells[k].flow_equilibrium()
        cells[k].update_supply()
        cells[k].update_demand()
    
    if red:
        cells[9].supply = 0      
    
    for k in range(1,n_cells+1):
        Qup = min(cells[k].supply,cells[k-1].demand)
        Qdown = min(cells[k+1].supply,cells[k].demand)
        
        cells[k].density = cells[k].density +(Qup - Qdown)*dt/cell_lenght
    
    data = np.vstack((data,np.array([cells[k].density for k in range(1,n_cells+1)])))

#%%

#plotting data
    
plotting_function.plot_data_to_gif(data,[0,p_max])
plotting_function.plot_data_to_cmap(data)