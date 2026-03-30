#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This functions reads the configuration file.
If the optimization is required to be done with Dakota,
the functions runs the optimization and reads the final optimized parameters.

Author: Alexandre Paris 
"""

import sys
import os
import yaml
import subprocess
import numpy as np


def optimization(phi):
    """
    Read the configuration file and run the optimization
    of the parameters b, c and phi or read their values
    """
    with open(r'./config_shorefor.yaml') as f:
        clef = yaml.full_load(f)
    run = clef['case']['study']
    opti = clef['optimization']['dakota']
    b_min = clef['dakota_params']['b_min']
    b_max = clef['dakota_params']['b_max']
    c_min = clef['dakota_params']['c_min']
    c_max = clef['dakota_params']['c_max']
    phi_min = clef['dakota_params']['phi_min']
    # Calculate the initial parameters from previous limits
    b_init = round(((b_max - b_min)/2)+b_min, 1)
    c_init = round(((c_max - c_min)/2)+c_min, 1)
    if phi == phi_min:
        try : 
            os.remove('dakota_tab_results'+run+'.dat')
        except FileNotFoundError:
            pass
    else:
        pass
    
    with open('./dakota_pstudy.in', 'r') as file:
        get_all = file.readlines()
    
    with open('./dakota_pstudy.in', 'w') as file:
        for i, line in enumerate(get_all, 1):
            if 'initial_point' in line:
                file.writelines('    initial_point    {}        {}\
                                \n'.format(b_init, c_init))
            elif 'lower_bounds' in line:
                file.writelines('    lower_bounds    {}        {}\
                                \n'.format(b_min, c_min))
            elif 'upper_bounds' in line:
                file.writelines('    upper_bounds    {}        {}\
                                \n'.format(b_max, c_max))
            elif 'initial_state' in line:
                file.writelines('    initial_state    {}        \
                                \n'.format(phi))
            else:
                file.writelines(line)
    
    with open('parameters.txt.template', 'w') as file:
        lines = ['# b c phi \n',
                 '{} {} {} #min\n'.format(b_min, c_min, phi),
                 '{} {} {} #max\n'.format(b_max, c_max, phi),
                 '{b} {c} {phi} #start\n']
        file.writelines(lines)
    
    if opti == 1:
        with subprocess.Popen(['dakota', '-i', 'dakota_pstudy.in']) as process:
            process.wait()

        # Best RMSE and BSS
        '''with open('dakota_results.txt', 'r') as f:
            params = f.readlines()[5:8]
            bopti = float(params[0])
            copti = float(params[1])
            phiopti = float(params[2])'''
        
        data = np.genfromtxt('dakota_tabular.dat')
        data = data[1:]
        b = data[:, 2]
        c = data[:, 3]
        phi = data[:, 4]
        rmse = data[:, 5]
        
        try:
            with open('dakota_tab_results'+run+'.dat', 'x') as file:
                pass
            np.savetxt('dakota_tab_results'+run+'.dat', np.c_[b, c, phi, rmse], fmt='%.6f')
            idx = np.argmin(rmse)
            bopti = b[idx]
            copti = c[idx]
            phiopti = phi[idx]
            print('file do not exist')
        except FileExistsError:
            data_final = np.genfromtxt('dakota_tab_results'+run+'.dat')
            b_saved = np.concatenate((data_final[:, 0], b))
            c_saved = np.concatenate((data_final[:, 1], c))
            phi_saved = np.concatenate((data_final[:, 2], phi))
            rmse_saved = np.concatenate((data_final[:, 3], rmse))   
            np.savetxt('dakota_tab_results'+run+'.dat', np.c_[b_saved, c_saved, phi_saved, rmse_saved], fmt='%.6f')
            idx = np.argmin(rmse_saved)
            bopti = b_saved[idx]
            copti = c_saved[idx]
            phiopti = phi_saved[idx]
            print('file exist')
 
        
		
        print('Otimized coefficients:\n')
        print('b: ', bopti)
        print('c: ', copti)
        print('phi: ', phiopti)
    
    elif opti == 2:
        bopti = clef['optimization']['b']
        copti = clef['optimization']['c']
        phiopti = clef['optimization']['phi']
    
    else:
        print('ERROR: Optimization choice in the configuration file is not recognized')
        sys.exit()

    return bopti, copti, phiopti
