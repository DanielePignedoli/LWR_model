#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from dataclasses import dataclass

@dataclass
class MakeCell:
    
    #model parameters
    
    density_max : float #max_density per lane
    free_v : float
    cong_v : float
    
    #cell variables
    
    density : float
    num_lanes : float
    flow : float = None
    
    
    supply : float = None
    demand : float = None
    
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