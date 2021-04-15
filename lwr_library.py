#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from dataclasses import dataclass, field
import numpy as np

@dataclass
class MakeRoad():
    

    
    #road params
    free_v : float  #km all'ora
    cong_v : float  #km all'ora
    road_lenght : float  #km
    density_max : float   #veicoli per kilometro (lane average)
    num_lanes : float = 1 #num of lanes
  
    
    #parameters to initialise
    iteration : int = None
    cell_lenght : float = None
    n_cells : int = None
    max_flow : float = None         #max flow per lane
    p_c : float = None        #crtical density
    
    #method parameter
    dt : float = field(default=1/600) #hr
    simulation_time : float = field(default=1/6) #hr, so 10 min
    
    def __post_init__(self):
        self.iteration = round(self.simulation_time/self.dt)
        self.cell_lenght = self.free_v * self.dt
        self.n_cells = round(self.road_lenght/self.cell_lenght)
        self.max_flow = self.density_max*self.free_v*self.cong_v/(self.cong_v-self.free_v)
        self.p_c = self.max_flow/self.free_v
        
    def homogeneous(self, source=0, sink=0):
        
        self.cell = []
        if source:
            self.cell.append(MakeCell(self, source = source))
        for i in range(self.n_cells):
            self.cell.append(MakeCell(self))
        if sink:
            self.cell.append(MakeCell(self, sink=sink))
    
    def method(self):
        self.data = np.array([c.density for c in self.cell[1:-1]])
        
        for i in range(self.iteration):
            self.data = np.vstack((self.data,np.array([c.density for c in self.cell[1:-1]])))
            
            for c in self.cell[1:-1]:
                c.updates()
            
            demands = [c.demand for c in self.cell[:-1]]
            supplies = [c.supply for c in self.cell[1:]]
            
            flows = np.minimum(demands, supplies)
            for num, c in enumerate(self.cell[1:-1]):
                c.density = c.density +(flows[num] - flows[num+1])*self.dt/self.cell_lenght

            
        


@dataclass
class MakeCell():
    
    #road
    road : MakeRoad
    
    #cell variables
    density : float = field(default=0)
    flow : float = None
    
    
    supply : float = field(init=False)
    demand : float = field(init=False)
    
    #max_flow : float = None
    capacity : float = field(init=False)
    
    #source&sink
    source : float = field(default = 0)  # fraction of capacity
    sink : float = field(default = 0)  # fraction of capacity
    
    def __post_init__(self):
        if self.source:
            self.make_source()
        if self.sink:
            self.make_sink()
        
    def update_capacity(self):
        self.capacity = self.road.max_flow*self.road.num_lanes

    def update_supply(self):
        if self.p_avg >= self.road.p_c:
            self.supply = self.flow
        else:
            self.supply = self.capacity
    
    def update_demand(self):
        if self.p_avg <= self.road.p_c:
            self.demand = self.flow
        else:
            self.demand = self.capacity
        
    
    def flow_equilibrium(self):
        #p_avg is the lane averaged density
        self.p_avg = self.density/self.road.num_lanes
        #return the total flow in the cell 
        if self.p_avg<0:
            self.flow = 0
        elif self.p_avg <= self.road.p_c:
            self.flow = self.road.free_v*self.p_avg*self.road.num_lanes
        elif self.p_avg > self.road.density_max:
            self.flow = 0
        else:
            self.flow = (self.road.max_flow*(1-self.road.cong_v/self.road.free_v) + self.road.cong_v*self.p_avg)*self.road.num_lanes
            
    def updates(self):
        
        self.update_capacity()
        self.flow_equilibrium()
        self.update_supply()
        self.update_demand()
        
    def make_source(self):
        self.update_capacity()
        self.demand = self.source * self.capacity
        
    def make_sink(self):
        self.update_capacity()
        self.supply = self.capacity * self.sink
        

