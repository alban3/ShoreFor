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

sys.path.append('./libs')
from dates_functions import _from_ordinal, datenum
from tools import match, find_nearest, rmse, bss

###############################################################################

path = 'results/'
caseList = ['shorefor_duck_shoreline_b0.0037_c0.00632_phi231.nc']

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

figPath = '/figures/'
if os.path.isdir(figPath) == False:
    os.system('mkdir figures')

fignum1 = plt.figure(num=1,figsize=(figwidth,figheight),dpi=100)
ax11 = fignum1.add_subplot(211)
plt.ylim(0,30) 
plt.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
plt.ylabel(r"$\Omega$",fontsize = '16')
plt.tick_params(axis='y', labelsize=16)
plt.gca().xaxis.set_major_locator(mpl.dates.MonthLocator(interval = 6))
plt.grid()

ax12 = fignum1.add_subplot(212)
plt.ylim(75,155) 
plt.xlabel(r"Date",fontsize = '16')
plt.ylabel(r"$S(t)$  (m)",fontsize = '16')
plt.tick_params(axis='y', labelsize=16)
plt.grid()

plt.gca().xaxis.set_major_formatter(mpl.dates.DateFormatter('%Y/%m'))
plt.gca().xaxis.set_major_locator(mpl.dates.MonthLocator(interval = 6))
plt.xticks(rotation = 45, fontsize = 8)

for case in caseList:
	caseFile = Dataset(os.path.join(path, case))
	time_num = caseFile.variables['date_num'][:]
	omega_obs = caseFile.variables['omega_obs'][:]
	omega_eq = caseFile.variables['omega_equilibrium'][:]
	s_obs = caseFile.variables['s_obs'][:]
	s_calib = caseFile.variables['s_calib'][:]
	s_predic = caseFile.variables['s_predic'][:]
	caseFile.close()
	
	date = [_from_ordinal(t) for t in time_num]
	
	ax11.plot(date, omega_obs, color = 'k', label = r'$\Omega$')
	ax11.plot(date, omega_eq, color = 'r', ls = '--', label = r'$\Omega_{eq}$')

	ax12.scatter(date, s_obs, s = 20, color = 'k', marker = 's', label = 'Survey')
	ax12.plot(date, s_calib, color = 'g', label = 'Sim. calibration')
	ax12.plot(date, s_predic, color = 'b', label = 'Sim. prediction')

ax11.set_xlim(_from_ordinal(time_num[0]),_from_ordinal(time_num[-1]))
ax12.set_xlim(_from_ordinal(time_num[0]),_from_ordinal(time_num[-1]))

ax12.legend(loc='best')
ax11.legend(loc='best')

#plt.show()
fignum1.savefig(figPath + 'Splinter_south'+".png", dpi=100, format="png")
