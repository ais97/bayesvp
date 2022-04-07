#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  2 19:36:58 2022

@author: aiswarya
"""

from bayesvp.scripts import bvp_write_config as wc
from bayesvp.scripts import bvp_process_model as pm
from bayesvp.scripts import bvpfit as fit
from bayesvp import config as conf
from bayesvp import utilities as util 
from bayesvp import mcmc_setup as setup
from bayesvp.config import DefineParams as dp
import matplotlib.pyplot as plt
import glob
import time
import numpy as np

path = '/home/aiswarya/bvprun/'

config_paths = glob.glob(f'{path}*/')
config_paths.sort()
#print(config_files[:12])

for cp in config_paths:
    
    for i in range(1,4):
        config_files = glob.glob(f'{cp}/config*{i}.dat',recursive=True)
        config_files.sort()
        #new = config.split(sep='.')
        #config_ = new[0]+f'{i}.'+new[1]
        
        for config in config_files:
            try:  
                
                config_params = dp(config)
                output = pm.ProcessModel(config_params)
                
                output.corner_plot()
                output.write_model_summary()
                output.write_model_spectrum()
                plt.close()
                
            except: continue
        
"""
a = 203-np.asarray([91,90,81,80,78])
for i in a:
    print(config_files[i])        
"""      
import os
os.system("""spd-say 'yo Aiswarya, lets party'""")