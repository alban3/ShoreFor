#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
These functions save the results of the calibration part and the extrapolation if needed
"""

from matplotlib import dates
import numpy as np
from dates_functions import _from_ordinal, datenum
from netCDF4 import Dataset

def save_results(time_general, shoreline_calib, shoreline_future, dean_F, dean_eq, vec_ind_tot, time_survey, survey_shoreline, std, name_case, evolu, b, c, phi):
	
	from dates_functions import datenum
	from tools import match

	general_time_num = [datenum(t) for t in time_general]
	
	idx = match(time_survey, time_general)
	shoreline_obs, shoreline_std_obs = np.empty((2,len(time_general)))
	
	shoreline_obs.fill(np.nan)
	shoreline_std_obs.fill(np.nan)
	shoreline_obs[idx] = survey_shoreline
	shoreline_std_obs[idx] = std
	
	omega_inst = dean_F[vec_ind_tot]
	omega_eq = dean_eq[vec_ind_tot]
	
	try: ncfile.close()  # just to be safe, make sure dataset is not already open.
	except: pass
	ncfile = Dataset('results/'+'shorefor_'+name_case+'_'+evolu
               +'_b'+str(b)+'_c'+str(c)+'_phi'+str(phi)+'.nc', mode='w',format='NETCDF4_CLASSIC')
	print(ncfile)

	Nt = len(time_general)
	time_dim = ncfile.createDimension('time', Nt)     # cell number
	for dim in ncfile.dimensions.items():
		print(dim)

	date_num = ncfile.createVariable('date_num', np.float32, ('time'))
	date_num.long_name = 'date_num'
	s_obs = ncfile.createVariable('s_obs', np.float32, ('time',))
	s_obs.units = 'm'
	s_obs.long_name = 'shoreline observed position (m)'
	s_calib = ncfile.createVariable('s_calib', np.float32, ('time',))
	s_calib.units = 'm'
	s_calib.long_name = 'shoreline calibrated position (m)'
	s_predic = ncfile.createVariable('s_predic', np.float32, ('time',))
	s_predic.units = 'm'
	s_predic.long_name = 'shoreline predicted position (m)'
	omega_obs = ncfile.createVariable('omega_obs', np.float32, ('time',))
	omega_obs.long_name = 'Dean number'
	omega_equilibrium = ncfile.createVariable('omega_equilibrium', np.float32, ('time',))
	omega_equilibrium.long_name = 'Equilibrium Dean number'
	
	s_obs[:] = shoreline_obs
	s_calib[:] = shoreline_calib
	s_predic[:] = shoreline_future
	omega_obs[:] = omega_inst
	omega_equilibrium[:] = omega_eq
	date_num[:] = general_time_num

	# first print the Dataset object to see what we've got
	print(ncfile)
	# close the Dataset.
	ncfile.close(); print('Dataset is closed!')
