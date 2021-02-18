#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from dataclasses import dataclass

@dataclass
class MakeCell:
    
    #model parameters
    
    density_max : float
    free_v : float
    cong_v : float
    
    #cell variables
    
    density : float
    num_lanes : float
    flow : float = None
    
    
    supply : float = None
    demand : float = None
    
    def update_capacity(self):
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
        if self.density<0:
            self.flow = 0
        elif self.density <= self.capacity/self.free_v:
            self.flow = self.free_v*self.density
        elif self.density > self.density_max:
            self.flow = 0
        else:
            self.flow = self.capacity*(1-self.cong_v/self.free_v) + self.cong_v*self.density    