#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  1 20:57:55 2022

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

path = '/home/aiswarya/bvprun/'

config_paths = glob.glob(f'{path}*/bvp_output')
for path in config_paths:
    
    for i in range(1,3):
        config_files = glob.glob(f'{path}/config*{i}.dat',recursive=True)
        #new = config.split(sep='.')
        #config_ = nepath = '/home/aiswarya/bvprun/'w[0]+f'{i}.'+new[1]
        for config in config_files:
            
            config_params = dp(config)
            output = pm.ProcessModel(config_params)
            output.corner_plot()
            output.write_model_summary()
            output.write_model_spectrum()
            

import os
os.system("""spd-say 'yo Aiswarya, lets party'""")

  