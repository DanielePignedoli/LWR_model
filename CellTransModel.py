#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 13:21:02 2020

@author: daniele
"""

import numpy as np
import pandas as pd
import matplotlib.pylab as plt

dt = 1/600 #hr
v = 50  #km all'ora
c = -30  #km all'ora
road_lenght = 1.25 #km
q_max = 3000   #veicoli all'ora per corsia
p_max  = 160   #veicoli per kilometro (densità a massima capacità)
I = 1   #numero di corsie
#C = q_max*I

p_init = q_max*0.8/v

iteration = 60

cell_lenght = v * dt
n_cells = round(road_lenght / cell_lenght)

#%%%

class MakeCell:
    
    p_max = 160
    
    def __init__(self, v, c, q_max, p, S, D, Qup, Qdown, Qtot):
        self.v = v
        self.c = c
        self.q_max = q_max
        self.p = p
        self.S = S
        self.D = D
        self.Qup = Qup
        self.Qdown = Qdown
        self.Qtot = Qtot
        self.q_eq()
    
    def supply(self):
        if self.p >= self.q_max/self.v:
            self.S = self.Qtot
        else:
            self.S = self.q_max
    
    def demand(self):
        if self.p <= self.q_max/self.v:
            self.D = self.Qtot
        else:
            self.D = self.q_max
        
    
    def q_eq(self):
        if self.p<0:
            self.Qtot = 0
        elif self.p <= self.q_max/self.v:
            self.Qtot = self.v*self.p
        elif self.p > p_max:
            self.Qtot = 0
        else:
            self.Qtot = self.q_max*(1-self.c/self.v) + self.c*self.p
#%%   
S_source = q_max*0.8
S_sink = q_max
D_source = q_max*0.8
D_sink = q_max
cells = [MakeCell(v, c, q_max, p_init, S_source, D_source, None,None, None)]
for i in range(n_cells):
    cells.append(MakeCell(v,c,q_max,p_init,None,None,None,None,None))
cells.append(MakeCell(v,c,q_max,p_init,S_sink,D_sink,None,None,None))

#%%
data = np.array([cells[k].p for k in range(1,n_cells+1)]).round(0)
for i in range(iteration):
    
    #RALLENTAMENTO
#    if i in range(10,20):
#        cells[7].q_max = 1600
#        cells[7].v = 35
#        cells[7].c = (1/cells[10].v - p_max/cells[10].q_max)**(-1)
#    else:
#        cells[7].q_max = 3000
#        cells[7].v = 50
#        cells[7].c = -30 
    
    #SEMAFORO DIVENTA ROSSO
    if i in range(10,30):
        cells[7].q_max = 0
    else: 
        cells[7].q_max = 3000
    
    for k in range(1,n_cells+1):
        cells[k].supply()
        cells[k].demand()
    for k in range(1,n_cells+1):
        cells[k].Qup = min(cells[k].S,cells[k-1].D)
        cells[k].Qdown = min(cells[k+1].S,cells[k].D)
        
        cells[k].p = cells[k].p +(cells[k].Qup - cells[k].Qdown)*dt/cell_lenght
        cells[k].q_eq() 
    
    data = np.vstack((np.array([cells[k].p for k in range(1,n_cells+1)]).round(0),data))

#%%
    
df = pd.DataFrame(data)
#df.iloc[:,1:13]
fig, ax = plt.subplots()
cmap = plt.get_cmap('autumn')
im = ax.pcolormesh(data, cmap = cmap)
#im = ax.contourf(data, cmap = cmap)
fig.colorbar(im)
ax.set_title('BottleNeck at cell 8')
ax.set_xlabel('cells')
ax.set_ylabel('time_step')
fig.tight_layout()

plt.show()