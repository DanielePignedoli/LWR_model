#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from lwr_library import  MakeRoad 

#ROAD 1
road1 = MakeRoad(free_v = 50, mean_time_gap = 1.4, road_length = 1 , density_max = 120,  num_lanes = 1)
road1.homogeneous(0.6,1)

#ROAD 2
road2 = MakeRoad(free_v = 50, mean_time_gap = 1.4, road_length = 1 , density_max = 120,  num_lanes = 1)
road2.homogeneous(0.6,1)

#ROAD 3
road3 = MakeRoad(free_v = 50, mean_time_gap = 1.4, road_length = 1 , density_max = 120,  num_lanes = 1)
road3.homogeneous(0,2)

#%%            
            
for i in range(road1.iteration):
    road1.cell[-1].supply = road3.cell[1].supply*0.8
    road2.cell[-1].supply = road3.cell[1].supply*0.2
    road3.cell[0].demand = road1.cell[-2].demand + road2.cell[-2].demand
    
    road3.cell[9].bn_reduction = 0.4
    
    road1.data.append(road1.update_density())
    road2.data.append(road2.update_density())
    road3.data.append(road3.update_density())
    



#%%
import matplotlib.pylab as plt


fig = plt.figure()
cmap = plt.get_cmap('PuBu')
ax = plt.subplot2grid((2,4),(0,1), colspan=2)
im = ax.pcolormesh(road2.data, vmin = 0 , vmax = 120, cmap =cmap)
#fig.colorbar(im)
#ax.set_xlabel('position (km)', fontsize = 12)
xticks = [round(i*road1.cell_length,2) for i in range(0,road1.n_cells,2)]
plt.xticks(range(0,road1.n_cells, 2),xticks)
yticks = [round(i*road1.dt*60,1) for i in range(0,road1.iteration,10)]
plt.yticks(range(0,road1.iteration,10),yticks)
ax.set_ylabel('time (min)', fontsize = 12)

ax1 = plt.subplot2grid((2,4),(1,0), colspan=2)
ax1.pcolormesh(road1.data, vmin=0, vmax=120,cmap=cmap)
ax1.set_xlabel('position (km)', fontsize = 12)
xticks = [round(i*road1.cell_length,2) for i in range(0,road1.n_cells,2)]
plt.xticks(range(0,road1.n_cells, 2),xticks)
yticks = [round(i*road1.dt*60,1) for i in range(0,road1.iteration,10)]
plt.yticks(range(0,road1.iteration,10),yticks)
ax1.set_ylabel('time (min)', fontsize = 12)

ax2 = plt.subplot2grid((2,4),(1,2), colspan=2)
ax2.pcolormesh(road3.data, cmap = cmap,vmin=0, vmax=120)
#ax.set_xlabel('position (km)', fontsize = 12)
xticks = [round(i*road1.cell_length+1,2) for i in range(0,road1.n_cells,2)]
plt.xticks(range(0,road1.n_cells, 2),xticks)
yticks = [round(i*road1.dt*60,1) for i in range(0,road1.iteration,10)]
plt.yticks(range(0,road1.iteration,10),yticks)
#ax.set_ylabel('time (min)', fontsize = 12)


fig.subplots_adjust(right=0.8)
cbar_ax = fig.add_axes([0.85, 0.6, 0.03, 0.35])
fig.colorbar(im, cax=cbar_ax)



fig.tight_layout()
#if save:
fig.savefig('mering_diff_road.png')
fig.show()

