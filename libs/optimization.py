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
import objective_functions

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
            os.remove('scipy_tab_results'+run+'.dat')
        except FileNotFoundError:
            pass
    else:
        pass
        
    if opti == 1:
        with subprocess.Popen(['python', 'objective_function.py']) as process:
            process.wait()

        # Best RMSE and BSS
        '''with open('dakota_results.txt', 'r') as f:
            params = f.readlines()[5:8]
            bopti = float(params[0])
            copti = float(params[1])
            phiopti = float(params[2])'''
        
        data = np.genfromtxt('scipy_tabular.dat')
        data = data[1:]
        b = data[:, 2]
        cp = data[:, 3]
        cm = data[:, 4]
        phi = data[:, 5]
        rmse = data[:, 6]
        
        try:
            with open('scipy_tab_results'+run+'.dat', 'x') as file:
                pass
            np.savetxt('scipy_tab_results'+run+'.dat', np.c_[b, cp, cm, phi, rmse], fmt='%.6f')
            idx = np.argmin(rmse)
            bopti = b[idx]
            cpopti = cp[idx]
            cmopti = cm[idx]
            phiopti = phi[idx]
            print('file do not exist')
        except FileExistsError:
            data_final = np.genfromtxt('scipy_tab_results'+run+'.dat')
            b_saved = np.concatenate((data_final[:, 0], b))
            cp_saved = np.concatenate((data_final[:, 1], cp))
            cm_saved = np.concatenate((data_final[:, 2], cm))
            phi_saved = np.concatenate((data_final[:, 3], phi))
            rmse_saved = np.concatenate((data_final[:, 4], rmse))   
            np.savetxt('scipy_tab_results'+run+'.dat', np.c_[b_saved, cp_saved, cm_saved, phi_saved, rmse_saved], fmt='%.6f')
            idx = np.argmin(rmse_saved)
            bopti = b_saved[idx]
            cpopti = cp_saved[idx]
            cmopti = cm_saved[idx]
            phiopti = phi_saved[idx]
            print('file exist')
 
        
		
        print('Otimized coefficients:\n')
        print('b: ', bopti)
        print('cp: ', cpopti)
        print('cm: ', cmopti)
        print('phi: ', phiopti)
    
    elif opti == 2:
        bopti = clef['optimization']['b']
        cpopti = clef['optimization']['cp']
        cmopti = clef['optimization']['cm']
        phiopti = clef['optimization']['phi']
    
    else:
        print('ERROR: Optimization choice in the configuration file is not recognized')
        sys.exit()

    return bopti, cpopti, cmopti, phiopti
