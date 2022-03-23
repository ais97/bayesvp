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
import matplotlib
#matplotlib.use('TkAgg')
import numpy as np
import astropy.table as tab
import glob
import time

path = '/home/aiswarya/bvprun/'

los = glob.glob(f'{path}*/bvp_output/data_products/')
#print(los)

for line in los:
    h1 = glob.glob(f'{line}ascii/spec_H_I_*1.dat')
    outpath = f'{line}plots/'
    for h in h1:
        start = h.find('I_')+2
        end = h.find('1.dat')
        redshift = f'0.{h[start:end]}'
        #print(redshift)
        n = len(glob.glob(f'{line}ascii/spec_*_{h[start:end]}1.dat'))
        fig,ax = plt.subplots(n,3,sharex=False)
        
        for i in range(3):
            all_spec = glob.glob(f'{line}ascii/spec_*_{h[start:end]}{i+1}.dat')
            all_spec.sort()
            for j in range(n):
                try:
                    spec = tab.Table.read(all_spec[j],format='ascii')
                    
                    ax[j,i].plot(spec['wave'],spec['flux'],drawstyle='steps-mid',linewidth=0.3)
                    ax[j,i].plot(spec['wave'],spec['error'],drawstyle='steps-mid',linewidth=0.3)
                    ax[j,i].plot(spec['wave'],spec['model'],drawstyle='steps-mid',linewidth=0.3)
                    
                except: continue
        
        
        
        plt.show()  
        plt.savefig(f'{outpath}{h[start:end]}_model.pdf',bbox_inches='tight')
        
        
import os
os.system("""spd-say 'yo Aiswarya, lets party'""")

  