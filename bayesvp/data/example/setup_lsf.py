#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 23 15:01:56 2022

@author: aiswarya
"""

import numpy as np
import astropy.table as tab 
import os

filepath = ['/home/aiswarya/bvprun/aa_LSFTable_G130M_1291_LP1_cn.dat', 
            '/home/aiswarya/bvprun/aa_LSFTable_G160M_1623_LP1_cn.dat']
lsfpath = '/home/aiswarya/bvprun/'
path = '/database/'

dirs = [d for d in os.listdir('/home/aiswarya/bvprun') if os.path.isdir(os.path.join(lsfpath,d))]
#print(len(dirs))
'''

for fil in filepath:
    lsf = np.asarray(tab.Table.read(fil,format='ascii'))
    print(f'{lsf[1:][0]}')
    lsf_files = np.append(lsf_files,np.array(lsf[0]))
    for d in dirs:
        lp = lsfpath+d+'/database/'
        if not os.path.isdir(lp):
            os.makedirs(lp)
        for i in range(len(lsf[0])):
            ln = lsf[1:][i]
            #print(len(ln))
            ln = np.array([f for f in ln])
            print(ln[0])
            np.savetxt(lp+f'{lsf[0][i]:.0f}', ln)
'''
lsf_files = np.array([])
f = open(f'{lsfpath}lsf','w+')
for fil in filepath:

    lsf = tab.Table.read(fil,format='ascii')
    #print(f'{lsf[1:][0]}')
    lsf_file = list(lsf[0])
    
    f.write(f'{lsf_file}\n')

