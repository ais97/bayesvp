################################################################################
#
# bvp_write_config.py 	(c) Cameron Liang
#						University of Chicago
#     				    jwliang@oddjob.uchicago.edu
#
# Script to aid writing a config file for voigt profile fitting. 
# Use either automatic for writing a default one or interactive to make your own
################################################################################

import os
import sys
import numpy as np
from bayesvp.utilities import MyParser

class WriteBayesVPConfig:

    def __init__(self):
        self.spec_path    = 'test_path_to_spec'
        self.spec_fname   = 'OVI.spec'
        self.output_chain_fname = 'o6'
        self.atom         = 'O'
        self.state        = 'VI'
        self.auto         = 1
        self.wave_start   = 1030.0
        self.wave_end     = 1033.0

        self.nwalkers     = 100
        self.nsteps       = 200
        self.nthreads     = 4

        self.min_logN = 10.0;       self.max_logN       = 18
        self.min_b    = 0;          self.max_b          = 100
        self.central_redshift = 0.; self.velocity_range = 300

        self.model_selection = 'bic'
        self.mcmc_sampler    = 'kombine'

    def interactive_var(self):
        self.spec_path    = input('Path to spectrum:\n')
        self.spec_fname   = input('Spectrum filename: ')
        self.output_chain_fname = input('filename for output chain: ')
        self.atom         = input('atom: ')
        self.state        = input('state: ')
        self.auto         = int(input('Maximum number of components to try: '))
        self.wave_start   = float(input('Starting wavelength: '))
        self.wave_end     = float(input('Ending wavelength: '))
        
        print('\nNow enter the priors. Press Enter for default values.')
        self.min_logN = 0; self.max_logN = 24 

        try:
            self.min_logN = float(input('min logN = '))
        except ValueError:
            self.min_logN = 0

        try:
            self.max_logN = float(input('max logN = '))
        except ValueError:
            self.max_logN = 24

        try:
            self.min_b = float(input('min b = '))
        except ValueError:
            self.min_b = 0

        try:
            self.max_b = float(input('max b = '))
        except ValueError:
            self.max_b = 100

        try:
            self.central_redshift = float(input('central redshift = '))
        except ValueError:
            self.central_redshift = 0

        try:
            self.velocity_range   = float(input('velocity range [km/s] = '))
        except ValueError:
            self.velocity_range = 300

        print('\nNow enter the MCMC parameters..')
        try:
            self.nwalkers = int(input('Number of walkers: '))
        except ValueError:
            self.nwalkers = 100
        
        try:
            self.nsteps   = int(input('Number of steps:  '))
        except ValueError:
            self.nsteps = 200

        try:
            self.nthreads = int(input('Number of processes: '))
        except ValueError:
            self.nthreads = 4

        self.model_selection = input('Model selection method bic(default),aic,bf: ')
        if self.model_selection == '':
            self.model_selection = 'bic'
        
        self.mcmc_sampler = input('MCMC sampler kombine(default), emcee: ')
        if self.mcmc_sampler == '':
            self.mcmc_sampler = 'kombine'
            
        self.lsf_file = input('LSF file name:')
        
        self.cont = input('Enter polynomial order for continuum fitting:')

    def print_to_file(self,interactive_write=True):

        if interactive_write:
            self.interactive_var()

        if self.spec_path == 'test_path_to_spec':
            self.config_path = '/home/aiswarya/bayesvp/bayesvp/data/example'  ## need to change this while doing the real thing

        else:
            self.config_path = '/home/aiswarya/bayesvp/bayesvp/data/example'  ## need to change this while doing the real thing

        if not os.path.isdir(self.config_path):
            os.mkdir(self.config_path)

        self.config_fname = self.config_path + '/config_' + self.atom + self.state + '.dat'
        f = open(self.config_fname,'w')
        f.write('spec_path {}\n'.format(self.spec_path))
        if self.auto > 1:
            f.write('! auto {}\n'.format(self.auto))
        f.write('output {}\n'.format( self.output_chain_fname))
        f.write('mcmc {} {} {} {} {}\n'.format(self.nwalkers,self.nsteps,self.nthreads,
                                    self.model_selection,self.mcmc_sampler))
        f.write('%% {} {} {}\n'.format(self.spec_fname,self.wave_start,self.wave_end))
        f.write('% {} {} 15 30 {}\n'.format(self.atom, self.state,self.central_redshift))

        f.write('logN {} {}\n'.format(self.min_logN,    self.max_logN))
        f.write('b    {} {}\n'.format(self.min_b,       self.max_b))
        f.write('z    {} {}\n'.format(self.central_redshift,self.velocity_range))
        if self.lsf_file != '':
            f.write('LSF {}\n'.format(self.lsf_file))
        f.write('continuum {}\n'.format(self.cont))
        f.close()

        print('Written config file: {}\n'.format(self.config_fname))


def main():

    config_writer = WriteBayesVPConfig()

    parser = MyParser()
    parser.add_argument("-a", "--auto",help="write default config file",
                        action="store_true")
    parser.add_argument("-i", "--interactive",help="write config file based on user input",
                        action="store_true")
    
    args = parser.parse_args()

    if len(sys.argv)==1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    
    if args.auto:
        config_writer.print_to_file()

    if args.interactive:
        config_writer.print_to_file(args.interactive)

if __name__ == '__main__':
    sys.exit(main() or 0)
