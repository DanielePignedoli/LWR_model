#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 13:21:02 2020

@author: daniele
"""

import numpy as np
import pandas as pd
import matplotlib.pylab as plt
from MakeCell import MakeCell
#%%
#Setting model parameters

dt = 1/600 #hr
v = 50  #km all'ora
c = -30  #km all'ora
road_lenght = 1.25 #km
p_max  = 160   #veicoli per kilometro (densità a massima capacità)
I = 1 #num of lanes

p_init = 0.7*p_max

iteration = 60

cell_lenght = v * dt
n_cells = round(road_lenght / cell_lenght)

#%%   

#making cells

#source cell
source_demand = p_init*v*I
cells = [MakeCell(p_max,v,c, p_init, num_lanes = I, demand = source_demand )]

#road cells
for i in range(n_cells):
    cells.append(MakeCell(p_max,v,c,p_init, num_lanes = I))

#sink_cell
cells.append(MakeCell(p_max,v,c, p_init, num_lanes = I, supply = 100000))

#%%
#homogeneous road without bottlenecks 

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
    
df = pd.DataFrame(data)
#df.iloc[:,1:13]
fig, ax = plt.subplots()
cmap = plt.get_cmap('autumn')
im = ax.pcolormesh(data, cmap = cmap)
#im = ax.contourf(data, cmap = cmap)
fig.colorbar(im)
#ax.set_title('BottleNeck at cell 8')
ax.set_xlabel('cells')
ax.set_ylabel('time_step')
fig.tight_layout()

plt.show()