#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 25 17:13:22 2022

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
config_files = glob.glob(f'{path}*/config*.dat',recursive=True)
config_files1 = glob.glob(f'{path}*/config*1.dat',recursive=True)
config_files2 = glob.glob(f'{path}*/config*2.dat',recursive=True)
config_files3 = glob.glob(f'{path}*/config*3.dat',recursive=True)
new_config = []
for config in config_files:
    if config in config_files1 or config in config_files2 or config in config_files3: continue
    else:
        new_config.append(config)
        
config_files = new_config
n = len(config_files)

a = 27
n-=a
print(n)
for config in config_files[a:]:
    #if 'OVI' in config:
     #   continue
    
    start = time.time()
    print(f'Running MCMC for {config}\n')
    config_params = dp(config)
    print(config_params.nsteps)
    chain_fname = config_params.chain_fname
    #try:
    setup.bvp_mcmc(config,chain_fname)
    #except: continue
    print(f'Runtime: {time.time()-start}\n')
    n-=1
    print(f'{n} files to go...')
  
config_paths = glob.glob(f'{path}*/bvp_output')
for path in config_paths:
    
    for i in range(1,3):
        config_files = glob.glob(f'{path}/config*{i}.dat',recursive=True)
        #new = config.split(sep='.')
        #config_ = new[0]+f'{i}.'+new[1]
        for config in config_files:
            
            config_params = dp(config)
            output = pm.ProcessModel(config_params)
            output.corner_plot()
            output.write_model_summary()
            output.write_model_spectrum()
  
import os
os.system("""spd-say 'yo Aiswarya, lets party'""")

