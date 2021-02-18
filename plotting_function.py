#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import imageio
import os
import matplotlib.pylab as plt
import __main__

#makink new directory with main file name
directory = os.path.basename(__main__.__file__)[:-3] + '_plots1'

while True:
    
    try:
        os.makedirs(directory)
        break
    except FileExistsError:
        directory = directory[:-1]+str(int(directory[-1])+1)
        
#little trick to avoid error with directory with sam name. but after 19 it could generate 110 i think
    
os.makedirs(directory +'/plots')

def plot_data_to_gif(data, ylim : list):
    images = []
    
    for i in range(len(data)):
        plt.plot(data[i])
        plt.ylim(ylim)
        plt.savefig(directory+'/plots/plot%d.jpg'%i)
        plt.close()
        images.append(imageio.imread(directory+'/plots/plot%d.jpg'%i))
    
    imageio.mimsave(directory+'/density.gif',images)

def plot_data_to_cmap(data):
    fig, ax = plt.subplots()
    cmap = plt.get_cmap('autumn')
    im = ax.pcolormesh(data, cmap = cmap)
    fig.colorbar(im)
    ax.set_xlabel('cells')
    ax.set_ylabel('time_step')
    fig.tight_layout()
    fig.savefig(directory+'/density_cmap.png')