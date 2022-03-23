#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 23 12:17:17 2022

@author: aiswarya
"""

import glob
import numpy as np
import astropy.table as tab 
import os
from scipy import stats
c = 2.99792458e5 # velocity of light km/s


zb = lambda z,dv: (1 + z) * np.sqrt((1 - dv / c) / (1 + dv / c)) - 1
zr = lambda z,dv: (1 + z) * np.sqrt((1 + dv / c) / (1 - dv / c)) - 1



def write_config_file(spec_path,atom,state,spec_fname,wave_start,wave_end,auto,
                      central_redshift,lsf_file,logN=[8,18],b=[0,150],
                      velocity_range=150,wstmsa=[200,5000,4,'bic','kombine']):
    min_logN,max_logN = logN
    min_b, max_b = b
    nwalkers, nsteps, nthreads, model_selection, mcmc_sampler = wstmsa
    z = str(central_redshift)[2:]
    config_fname =  f'{spec_path}config_{z}_{atom}{state}.dat'
    f = open( config_fname,'w')
    f.write('spec_path {}\n'.format( spec_path[:-1]))
    if  auto > 1:
        f.write('! auto {} \n'.format(auto))
    output_chain_fname = f'{atom}_{state}_{z}'
    f.write('output {}\n'.format(  output_chain_fname))
    f.write('mcmc {} {} {} {} {}\n'.format( nwalkers, nsteps, nthreads,
                                 model_selection, mcmc_sampler))
    if len(wave_start)==1:
        f.write('%% {} {} {}\n'.format( spec_fname, wave_start[0], wave_end[0]))
    else:
        wave = np.array([[wave_start],[wave_end]])
        wave = wave.T.flat
        f.write(f'%% {spec_fname} ')
        for w in wave:
            f.write(f'{w} ')
        f.write('\n')
    f.write('% {} {} 12 30 {}\n'.format( atom,  state, central_redshift))
    
    f.write('logN {} {}\n'.format( min_logN,     max_logN))
    f.write('b    {} {}\n'.format( min_b,        max_b))
    f.write('z    {} {}\n'.format( central_redshift, velocity_range))

    if lsf_file!='':
        f.write('lsf')
        for l in lsf_file:
            f.write(f' {l}')
        f.write('\n')
    #f.write('continuum {}\n'.format( cont))
    f.close()
    
    print('Written config file: {}\n'.format( config_fname))    
    return

path = '/home/aiswarya/bla/igm/*/*'
ext1 = '.fits'
ext2 = 'igm-systems.txt'
ext3 = 'linelist.txt'

endpath = '/home/aiswarya/bvprun/'


"""
fitsfiles = glob.glob(path+ext1)
#print(len(fitsfiles))

for fit in fitsfiles:
    start = fit.find('igm/')+4
    end = fit.find('/hlsp')
    name = fit[start:end]
    print(name)
    pathname = endpath+name
    fitstable = tab.Table.read(fit)
    wave = np.asarray(fitstable['WAVE'])
    flux = np.asarray(fitstable['FLUX']/fitstable['CONT'])
    err = np.asarray(fitstable['ERR']/fitstable['CONT'])
    spec = np.column_stack((wave,flux,err))
    print(spec[1000])
    if not os.path.isdir(pathname):
        os.makedirs(pathname)
    np.savetxt(pathname+f'/{name}.spec',spec,fmt='%1.6f')
"""    
"""    
linefiles = glob.glob(path+ext2)
i=0

for line in linefiles:
    start = line.find('igm/')+4
    end = line.find('/hlsp')
    name = line[start:end]
    print(name)
    pathname = endpath+name
    data = tab.Table.read(line,format='ascii')
    data['qname'] = [name]*len(data)

    lya = data[data['col4']=='Lya 1215']
    blas =  lya[lya['col10']>40]
    blas =  blas[ blas['col18']>3]
    i+=len( blas)
    
    j=1
    bla_prev = []
    for bla in blas:
        if bla in bla_prev:
            continue
        cen_z = bla['col1']
        new_data = lya[lya['col1']>zb(cen_z,300)]
        new_data = new_data[new_data['col1']<zr(cen_z,300)]
        print(new_data['col1','col18','qname'])
        fz = str(np.round(cen_z,7))
        new_data.write(pathname+f'/sys_{name}_blaz{fz[2:]}.dat',format='ascii',overwrite=True)
        
        bla_prev = new_data
        
        j+=1
    blas.write(pathname+'/lya.dat',format='ascii',overwrite=True)
    
    filelist = glob.glob(f'{pathname}/sys_{name}_blaz*.dat',recursive=True)
    for file in filelist:
        system = tab.Table.read(file,format='ascii')
        start = file.find('_blaz')+5
        end = file.find('.dat')
        zname = file[start:end]
        lines = []
        i+=1
        for sys in system:
            new_data = data[data['col1']==sys['col1']]
            try:
                lines = tab.vstack([lines,new_data])
            except:
                lines = new_data
            
        
        lines.write(f'{pathname}/sys_{name}_allz_{zname}.dat',format='ascii',overwrite=True)

""" 

filelist = glob.glob(f'{endpath}*/sys_*_allz_*.dat',)

lsf_table = np.genfromtxt('/home/aiswarya/bvprun/lsf',delimiter=',')

for file in filelist:
    all_lines = tab.Table.read(file,format='ascii')
    name = all_lines['qname'][0]
    print(name)
    spec_fname = name+'.spec'
    spec_path = endpath+name+'/'
    cen_z = stats.mode(all_lines['col1'])[0][0]
    atom = ['C','N','O','Ne','Si','S','P','Fe','Al',]
    state = ['I','II','III','IV','V','VI','VII','VIII','IX','X']
    for at in atom:
        for st in state:
            at_st = at+st
            atomstate = tab.Table()
            
            for line in all_lines:
                if at_st==line['col4'].split()[0] and line not in atomstate:
                    atomstate = tab.vstack([atomstate,line])
            met = tab.Table()
            for line in atomstate:
                if len(met)==0 or line['col4'] not in met['col4']:
                    met = tab.vstack([met,line])
               

            wave_start,wave_end=[],[]
            for m in met:
                s0 = m['col3']-1
                wave_start.append(s0)
                s1 = m['col3']+1
                wave_end.append(s1)
            
            wave_start = np.array(wave_start)
            wave_end = np.array(wave_end)
            wave_start.sort()
            wave_end.sort()
            
            
            """
            ind = []
            for i in range(len(wave_start)):
                if i>0 and wave_end[i]>wave_start[i-1]:
                    wave_start[i] = wave_start[i-1]
                    ind.append(i-1)
                if wave_start[i]<1135:
                    wave_start[i] = 1135
                elif wave_end[i]>1795:
                    wave_end = 1795
            wave_start = np.delete(wave_start,ind)
            wave_end = np.delete(wave_end,ind)
            #print(wave_start,wave_end,name,'\n')
            wave_start.sort()
            wave_end.sort()
            print(np.column_stack((wave_start,wave_end)))
            """
            lsf = []
            for i in range(len(wave_start)):
                lsf_coarse = np.mean([wave_start[i],wave_end[i]])
                lsf_diff = np.abs(lsf_coarse-lsf_table)
                lsf.append(f'{lsf_table[np.argmin(lsf_diff)]:.0f}')
            if len(wave_start)>0:
                print(np.column_stack((wave_start,wave_end)))
                print(lsf)
            if len(lsf)>0:
                write_config_file(spec_path,atom=at,state=st,spec_fname=spec_fname,
                             wave_start=wave_start,wave_end=wave_end,auto=3,
                             central_redshift=cen_z,lsf_file=lsf)  
                    
                    
           # print(atomstate)
    auto=1
    ly = tab.Table()
    for line in all_lines:
                   
         if 'Ly' in line['col4']:
             
            if len(ly)==0:
                 ly = tab.vstack([ly,line])

            elif line['col4'] not in ly['col4']:
                 ly = tab.vstack([ly,line])
            else:
                continue
        
    atom,state='H','I'
    wave_start = []
    wave_end = []
    for l in ly:
        s0 = l['col3']-2
        wave_start.append(s0)
        s1 = l['col3']+2
        wave_end.append(s1)

    wave_start = np.array(wave_start)
    wave_end = np.array(wave_end)
    ind = []
    wave_start.sort()
    wave_end.sort()
    
    for i in range(len(wave_start)):
        try:
            if wave_end[i-1]>wave_start[i] and i!=0:
                wave_start[i] = wave_start[i-1]
                
                ind.append(i-1)
            
            if wave_start[i]<1135:
                wave_start[i] = 1135
            elif wave_end[i]>1795:
                wave_end = 1795 
        except: continue
    
    wave_start = np.delete(wave_start,ind)
    wave_end = np.delete(wave_end,ind)
    
    
    
    lsf = []
    for i in range(len(wave_start)):
        lsf_coarse = np.mean([wave_start[i],wave_end[i]])
        lsf_diff = np.abs(lsf_coarse-lsf_table)
        lsf.append(f'{lsf_table[np.argmin(lsf_diff)]:.0f}')
    if len(wave_start)>0:
        print(np.column_stack((wave_start,wave_end)))
        print(lsf)
    if len(lsf)>0:
        write_config_file(spec_path,atom,state,spec_fname,wave_start,
                          wave_end,auto=3,central_redshift=cen_z,lsf_file=lsf)    
        
    


              

