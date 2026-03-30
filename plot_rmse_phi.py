#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Equilibrium cross-shore model ShoreFor with optimization by Dakota.

Main script

Author: Alban Gilletta
"""

import sys
import os
import numpy as np
import matplotlib.pyplot as plt
from netCDF4 import Dataset
import matplotlib as mpl
import datetime
from datetime import datetime
from matplotlib import ticker
from scipy.stats import pearsonr

sys.path.append('./libs')
from dates_functions import _from_ordinal, datenum
from tools import match, find_nearest, find_nearest_above, find_nearest_below, rmse, nmse, bss	

###############################################################################

### PLOT FIGURE ###

mpl.rcParams.update({"font.size": 12})
mpl.rcParams["lines.linewidth"] = 2
mpl.rcParams["lines.markersize"] = 5
mpl.rcParams["lines.markeredgewidth"] = 1

#
# Figure size
#

figwidth = 12
figheight = 8

figPath = 'figures/'
if os.path.isdir(figPath) == False:
    os.system('mkdir figures')

phi_ranges = (
		[x for x in range(5, 100, 5)]
		+[x for x in range(100, 500, 20)]
		+ [x for x in range(500, 1000+50, 50)]
		)
phi_min = 100
phi_max = 200
phi_ranges = phi_ranges[np.where(phi_ranges == find_nearest_above(phi_ranges,phi_min))[0][0]:np.where(phi_ranges == find_nearest_below(phi_ranges,phi_max))[0][0]+1]

fignum1 = plt.figure(num=1,figsize=(figwidth,figheight),dpi=100)
ax11 = fignum1.add_subplot(111)
#plt.ylim(0,10) 
plt.tick_params(axis='x', which='both')
plt.ylabel(r"RMSE (m)",fontsize = '16')
plt.xlabel(r"$\phi$ (day)",fontsize = '16')
plt.tick_params(axis='y', labelsize=16)
plt.grid()

data_final = np.genfromtxt('dakota_tab_resultsrun25_duck.dat')
b = data_final[:, 0]
c = data_final[:, 1]
phi = data_final[:, 2]
rmse = data_final[:, 3]

rmse_phi = []
b_phi = []
c_phi = []
for ph in phi_ranges:
	ind = np.where(phi == ph)[0]
	idx = np.argmin(rmse[ind])
	rmse_phi.append(rmse[ind][idx])
	b_phi.append(b[ind][idx])
	c_phi.append(c[ind][idx])

ax11.plot(phi_ranges,rmse_phi)

fignum1.savefig(figPath + 'run25_rmse_phi'+".png", dpi=100, format="png")
