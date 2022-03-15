#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 23 15:01:56 2022

@author: aiswarya
"""

import numpy as np
import astropy.table as tab 
import os
import glob

filepath = ['/home/aiswarya/bvprun/aa_LSFTable_G130M_1291_LP1_cn.dat', 
            '/home/aiswarya/bvprun/aa_LSFTable_G160M_1623_LP1_cn.dat']
lsfpath = '/home/aiswarya/bvprun/'
path = '/database/'

dirs = glob.glob(f'{lsfpath}*/database/')
print(len(dirs))
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

lsf_files = np.array([])
f = open(f'{lsfpath}lsf','w+')
for fil in filepath:

    lsf = tab.Table.read(fil,format='ascii')
    #print(f'{lsf[1:][0]}')
    lsf_file = list(lsf[0])
    
    f.write(f'{lsf_file}\n')
'''
lsf_list = np.array([])
names = np.array([])
for file in filepath:
    lsf = np.genfromtxt(file)
    print(file)
    #print(np.shape(lsf))
    for i in range(len(lsf[0,:])):
        new_lsf = np.reshape(lsf[:,i],(322,))
        if len(lsf_list)==0:
            lsf_list = new_lsf[1:]
        else:
            lsf_list = np.column_stack((lsf_list,new_lsf[1:]))
        names = np.append(names,str(f'{new_lsf[0]:.0f}'))

print(np.shape(lsf_list))
lsf_list = lsf_list.T
print(lsf_list)
#print(len(lsf))
#print(names)

for diri in dirs:
    for i in range(len(lsf_list)):
        lsf = lsf_list[i]
        print(len(lsf))
        name = names[i]
        print(f'saving {name}')
        np.savetxt(diri+name,lsf)
        
        