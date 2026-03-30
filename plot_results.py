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
from tools import match, find_nearest, rmse, nmse, bss


def convertFloatYear2Date(yearFloat):
	year = int(yearFloat)
	remainderDays = yearFloat - year
	if year % 4 == 0:
		nday = remainderDays*366	
		if nday < 31:
			month = '01'
			day = int(nday)+1
		elif 31 <= nday < 60:
			month = '02'
			day = int(nday) - 30 
		elif 60 <= nday < 91:
			month = '03'
			day = int(nday) - 59 
		elif 91 <= nday < 121:
			month = '04'
			day = int(nday) - 90 
		elif 121 <= nday < 152:
			month = '05'
			day = int(nday) - 120
		elif 152 <= nday < 183:
			month = '06'
			day = int(nday) - 151
		elif 183 <= nday < 213:
			month = '07'
			day = int(nday) - 182
		elif 213 <= nday < 244:
			month = '08'
			day = int(nday) - 212
		elif 244 <= nday < 274:
			month = '09'
			day = int(nday) - 243
		elif 274 <= nday < 305:
			month = '10'
			day = int(nday) - 273
		elif 305 <= nday < 335:
			month = '11'
			day = int(nday) - 304
		elif 335 <= nday < 366:
			month = '12'
			day = int(nday) - 334						
	else : 
		nday = remainderDays*365
		if nday < 31:
			month = '01'
			day = int(nday)+1
		elif 31 <= nday < 59:
			month = '02'
			day = int(nday) - 30
		elif 59 <= nday < 90:
			month = '03'
			day = int(nday) - 58
		elif 90 <= nday < 120:
			month = '04'
			day = int(nday) - 89
		elif 120 <= nday < 151:
			month = '05'
			day = int(nday) - 119
		elif 151 <= nday < 182:
			month = '06'
			day = int(nday) - 150
		elif 182 <= nday < 212:
			month = '07'
			day = int(nday) - 181
		elif 212 <= nday < 243:
			month = '08'
			day = int(nday) - 211
		elif 243 <= nday < 273:
			month = '09'
			day = int(nday) - 242
		elif 273 <= nday < 304:
			month = '10'
			day = int(nday) - 272
		elif 304 <= nday < 334:
			month = '11'
			day = int(nday) - 303
		elif 334 <= nday < 365:
			month = '12'
			day = int(nday) - 333
	if day < 10:
		day = '0'+ str(day)
	else :
		day = str(day)
	return str(year) +'-' + month + '-' + day
	
	
	

###############################################################################

path = 'results/'
caseList = ['shorefor_run18_duck_shoreline_b0.00465_c0.004042_phi140.0.nc', 'shorefor_run26_duck_shoreline_b0.006029_c0.001287_phi160.0.nc', 
			'shorefor_run28_duck_shoreline_b0.006481_c0.00212_phi160.0.nc','shorefor_run29_duck_shoreline_b0.005588_c0.002548_phi160.0.nc','shorefor_run27_duck_shoreline_b0.005588_c0.002548_phi160.0.nc']
colorList = ['r', 'b', 'g', 'm', 'turquoise']
colorListOmegaEq = ['darkred', 'darkblue', 'darkgreen', 'darkmagenta', 'darkturquoise']
nameList = [r'pop size = 1000', r'pop size = 2000', r'pop size = 3000', r'pop size = 4000', r'pop size = 5000']
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

fignum1 = plt.figure(num=1,figsize=(figwidth,figheight),dpi=100)
ax11 = fignum1.add_subplot(211)
plt.ylim(0,30) 
plt.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
plt.ylabel(r"$\Omega$",fontsize = '16')
plt.tick_params(axis='y', labelsize=16)
plt.gca().xaxis.set_major_locator(mpl.dates.MonthLocator(interval = 6))
plt.grid()

ax12 = fignum1.add_subplot(212)
plt.ylim(-40,40) 
plt.xlabel(r"Date",fontsize = '16')
plt.ylabel(r"$S(t)$  (m)",fontsize = '16')
plt.tick_params(axis='y', labelsize=16)
plt.grid()

plt.gca().xaxis.set_major_formatter(mpl.dates.DateFormatter('%Y/%m'))
plt.gca().xaxis.set_major_locator(mpl.dates.MonthLocator(interval = 6))
plt.xticks(rotation = 45, fontsize = 8)

k = -1
for case in caseList:
	k += 1
	b = float(case.split('_b')[1].split('_')[0])
	c = float(case.split('_c')[1].split('_')[0])
	phi = float(case.split('_phi')[1].split('_')[0].split('.nc')[0])
	caseFile = Dataset(os.path.join(path, case))
	time_num = caseFile.variables['date_num'][:]
	omega_obs = caseFile.variables['omega_obs'][:]
	omega_eq = caseFile.variables['omega_equilibrium'][:]
	s_obs = caseFile.variables['s_obs'][:]
	s_calib = caseFile.variables['s_calib'][:]
	s_predic = caseFile.variables['s_predic'][:]
	caseFile.close()
	
	date = [_from_ordinal(t) for t in time_num]
	
	ax11.plot(date, omega_obs, color = colorList[k], label = nameList[k], lw = 1)
	ax11.plot(date, omega_eq, color = colorListOmegaEq[k], ls = '--')

	ax12.plot(date, s_calib-114.33216778397856, color = colorList[k], label = nameList[k])
	#ax12.plot(date, s_predic, color = colorList[k], label = 'Sim. prediction')
	ax12.scatter(date, s_obs-114.33216778397856, s = 20, color = colorList[k], marker = 's')
	
	print('Case = ',case)
	print('BSS = ', 1/bss(s_obs[~np.isnan(s_obs)], s_calib[~np.isnan(s_obs)], b))
	print('R = ', pearsonr(s_obs[~np.isnan(s_obs)], s_calib[~np.isnan(s_obs)])[0])
	print('RMSE = ', rmse(s_obs[~np.isnan(s_obs)], s_calib[~np.isnan(s_obs)]))
	print('NMSE = ', nmse(s_obs[~np.isnan(s_obs)]-np.mean(s_obs[~np.isnan(s_obs)]), s_calib[~np.isnan(s_obs)]-np.mean(s_obs[~np.isnan(s_obs)])))



ax11.set_xlim(_from_ordinal(time_num[0]),_from_ordinal(time_num[-1]))
ax12.set_xlim(_from_ordinal(time_num[0]),_from_ordinal(time_num[-1]))

### Add Splinter plot Digit ###

pathResultSplinterDigit = 'examples/'
timeShorelineSplinterDigit, ShorelineSplinterDigit = np.loadtxt(pathResultSplinterDigit+'shoreline_measure.csv', delimiter='\t',usecols=(0, 1),unpack=True)
timeShorelineSplinterModelDigit, ShorelineModelSplinterDigit = np.loadtxt(pathResultSplinterDigit+'shoreline_model.csv', delimiter='\t',usecols=(0, 1),unpack=True)

dateShorelineSplinterDigit = []
for i in timeShorelineSplinterDigit:
	dateShorelineSplinterDigit.append(convertFloatYear2Date(i))

dateShorelineSplinterDigit = [_from_ordinal(datenum(dateShorelineSplinterDigit[i])) for i in range(len(timeShorelineSplinterDigit))]

dateShorelineSplinterModelDigit = []
for i in timeShorelineSplinterModelDigit:
	dateShorelineSplinterModelDigit.append(convertFloatYear2Date(i))

dateShorelineSplinterModelDigit = [_from_ordinal(datenum(dateShorelineSplinterModelDigit[i])) for i in range(len(timeShorelineSplinterModelDigit))]


offset = s_obs[1] - ShorelineSplinterDigit[0]

ax12.scatter(dateShorelineSplinterDigit, ShorelineSplinterDigit, s = 15, color = 'k', marker = 'o', facecolors = 'None', label = 'Splinter measure')
ax12.plot(dateShorelineSplinterModelDigit, ShorelineModelSplinterDigit, lw = 1 , color = 'k', label = 'Splinter model')


#ax12.legend(loc='best')
ax11.legend(loc='best')

#plt.show()
fignum1.savefig(figPath + 'run_18-26-27-28-29'+".png", dpi=100, format="png")
