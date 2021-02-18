#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
from makecell import MakeCell
import plotting_function

dt = 1/600 #hr
v = 50  #km all'ora
c = -30  #km all'ora
road_lenght = 1.25 #km
p_max  = 160   #veicoli per kilometro (densità a massima capacità)
I = 3 #num of lanes

p_init = (0.5*p_max)*I

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
data = np.array([cells[k].density for k in range(1,n_cells+1)])

for i in range(iteration):
    
    for k in range(1,n_cells+1):
        cells[k].update_capacity()
        cells[k].flow_equilibrium()
        cells[k].update_supply()
        cells[k].update_demand()
        
    for k in range(1,n_cells+1):
        Qup = min(cells[k].supply,cells[k-1].demand)
        Qdown = min(cells[k+1].supply,cells[k].demand)
        
        cells[k].density = cells[k].density +(Qup - Qdown)*dt/cell_lenght
    
    data = np.vstack((data,np.array([cells[k].density for k in range(1,n_cells+1)])))

#%%

#plotting data
    
plotting_function.plot_data_to_gif(data,[0,p_max*I])
plotting_function.plot_data_to_cmap(data)
