#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from dataclasses import dataclass, field

@dataclass
class MakeRoad:
    

    
    #road params
    free_v : float  #km all'ora
    cong_v : float  #km all'ora
    road_lenght : float  #km
    density_max : float   #veicoli per kilometro (lane average)
  
    
    #parameters to initialise
    iteration : int = field(init=False)
    cell_lenght : float = field(init=False)
    n_cells : int = field(init=False)
    
    #method parameter
    dt : float = field(default=1/600) #hr
    simulation_time : float = field(default=1/6) #hr, so 10 min
    
    def __post_init__(self):
        self.iteration = round(self.simulation_time/self.dt)
        self.cell_lenght = self.cong_v * self.dt
        self.n_cells = round(self.road_lenght/self.cell_lenght)



@dataclass
class MakeCell(MakeRoad):
    
    #model parameters
    
    #density_max : float #max_density per lane
    #free_v : float
    #cong_v : float
    
    #cell variables
    num_lanes : float  #num of lanes
    density : float = None
    #num_lanes : float
    flow : float = None
    
    
    supply : float = None
    demand : float = None
    
    max_flow : float = None
    capacity : float = None
    
    def update_capacity(self):
        #max flow per lane
        self.max_flow = self.density_max*self.free_v*self.cong_v/(self.cong_v-self.free_v)
        self.capacity = self.max_flow*self.num_lanes

    def update_supply(self):
        if self.density >= self.capacity/self.free_v:
            self.supply = self.flow
        else:
            self.supply = self.capacity
    
    def update_demand(self):
        if self.density <= self.capacity/self.free_v:
            self.demand = self.flow
        else:
            self.demand = self.capacity
        
    
    def flow_equilibrium(self):
        #return the total flow in the cell
        p_avg = self.density/self.num_lanes
        if p_avg<0:
            self.flow = 0
        elif p_avg <= self.max_flow/self.free_v:
            self.flow = self.free_v*p_avg*self.num_lanes
        elif p_avg > self.density_max:
            self.flow = 0
        else:
            self.flow = (self.max_flow*(1-self.cong_v/self.free_v) + self.cong_v*p_avg)*self.num_lanes
            
    def updates(self):
        self.update_capacity()
        self.flow_equilibrium()
        self.update_supply()
        self.update_demand()