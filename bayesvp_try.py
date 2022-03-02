#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 15 18:36:44 2021

@author: aiswarya
"""

#import sys
#sys.path.append('/home/aiswarya/bayesvp')
from bayesvp.scripts import bvp_write_config as wc
from bayesvp.scripts import bvp_process_model as pm
from bayesvp.scripts import bvpfit as fit
from bayesvp import config as conf
from bayesvp import utilities as util 
from bayesvp import mcmc_setup as setup
from bayesvp.config import DefineParams as dp
import matplotlib.pyplot as plt
import glob
#import WriteConfig

spec_path = '/home/aiswarya/bvprun/sim1'
"""
config = wc.WriteBayesVPConfig()
config.print_to_file(interactive_write=(True))
"""
config_fname = spec_path+'/config_OVI.dat'
#run fitting
setup.bvp_mcmc(config_fname)

redshift = 0.34758
dv = 300
#plot fitting

compfiles = glob.glob(spec_path+'/config_OVI*.dat',recursive=True)
print(compfiles)
for file in compfiles:
    try:
        config_fname = file
        config_params = dp(config_fname)
        #print('line32')
        output = pm.ProcessModel(config_params)
        
        output.plot_model_comparison(redshift, dv)
        output.corner_plot()
        output.write_model_summary()
        output.write_model_spectrum()
        output.plot_gr_indicator()
        
        
    except:
        continue


import os

os.system("""spd-say 'yo Aiswarya, lets party'""")