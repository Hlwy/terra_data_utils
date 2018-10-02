# -*- coding: utf-8 -*-
#!/usr/bin/env python

import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import CheckButtons		# Using this for dynamic overlaying of multiple data collections


# Add to utils
# from utils import experiment_utils as eut
from collection_utils import *

def fcnProjectLidarScan(lidar_scan, ang, lim_x_i, lim_x_s, lim_y_i, lim_y_s, theta):
	x_f = []
	y_f = []
	x = [0]*len(lidar_scan)
	y = [0]*len(lidar_scan)

	# For each distance measurement in current 2D Lidar scan
	for i in range(0, len(lidar_scan)):

		""" NOTE: 'terrasentia-gazebo' simulated Lidar measurements, which are
		serialized and broadcasted over UDP ('terrasentia_bridge' package), are
		pre-processed converting any distance measurement [di] () into a negative
		number according to the following

			if di >= max_lidar_sensing_range, then di = -1, or -1000 if serialized
			if di <= min_lidar_sensing_range, then di = -2, or -2000 if serialized

		This method was developed such that end users don't need to know what
		the physical sensing limits are of the Lidar being used regardless of
		what actual Lidar is being is in the simulation to generate the recorded
		readings.
		"""
		# Convert max/min simulated lidar measurments to respective values
		if lidar_scan[i] == -1000: lidar_scan[i] = 65533 		# Max
		if lidar_scan[i] == -2000: lidar_scan[i] = 0	 		# Min TODO: make sure value matches

		""" NOTE: The following two lines do the following for each raw distance
		measurement (lidar[i]) received from the Lidar's frame of reference:

			- Converts measurement of lidar[i] (which is in polar coordinates)
			into cartesian coordinates [X, Y]

			- Transform converted X, Y coordinates (in the robot's frame of
			reference) such that, when plotted, will always be parallel. This
			was done by incorporating the robot's estimated heading (relative
			from within the crop row) with the angle of associated with lidar[i]
		"""
		x=(lidar_scan[i]*math.cos(ang[i]*math.pi/180 + theta))/1000;
		y=(lidar_scan[i]*math.sin(ang[i]*math.pi/180 + theta))/1000;

		# Only use lidar measurements that are within a specified "bounding rectangle"
		if x < lim_x_s and x> lim_x_i and y < lim_y_s and y > lim_y_i:
			x_f.append(x);
			y_f.append(y);

	return x_f, y_f


def get_estimated_offset_from_reference(distances_left, distances_right, ref_offset):
	""" Desired offset of the navigation reference line (usually is 0 meaning the
	user wanted the robot to travel down the center of the row """
	# Estimate the robot's offset from its desired navigation line (e.g lane center)
	estimated_center = 0.5 * (distances_right - distances_left) - ref_offset
	return estimated_center

def get_avg_speed(encoders_left, encoders_right,gain=-1.75):
	bot_spd = (encoders_left + encoders_right) / 2
	avg_spd = np.nanmean(bot_spd)
	return avg_spd*pow(10,gain) # Simulation
	# return avg_spd*pow(10,-1.15) # Real

def get_estimated_robot_position(avg_spd, times):
	t0 = times[0]				# Initial System Time [ms] of datalog
	ts = np.array(times[1:])	# System times after data collection start [ms]
	# Get the change in time [sec] since the beginning of collection
	dts = (ts - t0)*pow(10,-3)
	# Estimates how much distance the robot has travelled from its beginning location
	y_robot = avg_spd * dts # [Eq.] position = velocity * dt
	return y_robot


def process_lidar_logs(raw_lidar_data, perception_lidar_data, system_data,avg_speed_multiplier=-1.75):
	""" NOTE:

		- l_ts	: lidar_log times
		- lts	: perception_lidar_log times
		- pc	: perception_lidar_log configuration parameters
	"""
	# System log data
	sysLog = system_data
	encsL = sysLog['speed calculation from encoder left (m/s)']
	encsR = sysLog['speed calculation from encoder right (m/s)']

	# Raw Lidar data
	lidarLog = raw_lidar_data
	raw_lidar_times = list(lidarLog[0][:])

	# print raw_lidar_times
	# print lidarLog.iloc[2,1:].values

	# Perception Lidar data
	if isinstance(perception_lidar_data, dict):
		plLog = perception_lidar_data['data']
		plConfig = perception_lidar_data['config']
	elif isinstance(perception_lidar_data, list):
		plLog = perception_lidar_data[0]
		plConfig = perception_lidar_data[1]


	plTimes = plLog['timestamp']
	plLidTimes = plLog['lidar_ts_ms']

	distsL = plLog['distance_left']
	distsR = plLog['distance_right']
	headings = plLog['heading']

	ref_offset =  float(plConfig['middle_ref_m'])
	LW = float(plConfig['LANE_WIDTH'])
	limYs = float(plConfig['lim_y_s'])
	limYi = float(plConfig['lim_y_i'])

	# Calculate Intermediate Values
	estimatedCenters = get_estimated_offset_from_reference(distsL, distsR, ref_offset)
	avg_spd = get_avg_speed(encsL, encsR,avg_speed_multiplier)
	y_bot = get_estimated_robot_position(avg_spd, plTimes)
	print("\n\tProcessing Perception Lidar Data --- Calculated Average Speed ---- %f" % (avg_spd) )
	# Loop through perception lidar data
	index0 = 1
	x_raw=[]
	y_raw=[]
	# Loop through each recorded Lidar scan data
	for pl_scan_idx in range (index0, len(estimatedCenters)):

		# Use the timestamp of the 'perception_lidar_log' as reference
		t_ref = plLidTimes[pl_scan_idx]

		in_sync = False
		i = 0
		# Ensure time of raw lidar data used syncs up with 'perception_lidar_log' information
		while i < len(raw_lidar_times) - 1 and not in_sync:
			# Exit if current raw scan time is after current reference time
			if t_ref < raw_lidar_times[i]:
				scan_idx = i
				in_sync = True
			elif t_ref >= raw_lidar_times[i] and t_ref < raw_lidar_times[i+1]:
				scan_idx = i
				in_sync = True
			# Index end conditions: Exit if we are about to run out of indices
			elif i == len(raw_lidar_times) - 2:
				scan_idx = len(raw_lidar_times) - 2
				in_sync = True

			# Go to next time step if we aren't in sync
			i +=1
		# Extract stored and synchronized timestamp value
		t_sync = raw_lidar_times[scan_idx]
		# Get lidar distance measurements from time-synchronized scan
		# print scan_idx
		scan_data = lidarLog.iloc[scan_idx,1:].values
		# print scan_data
		# Generate angular range of Lidar distance measurements [degrees]
		ang_rng = np.linspace(-45,225,1080, endpoint = False)
		# Project time-sync'd raw lidar scan into corrected cartesian coordinates
		xf, yf = fcnProjectLidarScan(scan_data, ang_rng, -LW, LW, limYi, limYs, float(headings[pl_scan_idx]))

		# Check Sizes
		# print len(scan_data)

		# TODO: Figure out logic
		E = 0.1
		E0 = 0.06
		maxy = 0
		xf1 = []
		yf1 = []
		for i in range (0, len(yf)):
			if abs(yf[i]) < E:
				yf1.append(yf[i])
				xf1.append(xf[i])

		# TODO: Figure out logic
		xf2 = []
		yf2 = []
		for i in range (0, len(xf1)):
			if abs(xf1[i]) > E0:
				yf2.append(yf1[i])
				xf2.append(xf1[i])

		# TODO: Figure out logic
		xf2 = np.array(xf2) - ref_offset
		yf2 = np.array(yf2) + avg_spd*(plTimes[pl_scan_idx] - plTimes[0])*pow(10,-3)
		if len(yf2) > 0:
			aux_maxy = max(yf2)
			if aux_maxy > maxy:
				maxy = aux_maxy

		# Store cartesian coordinates for later visualization
		x_raw = np.append(x_raw,xf2)
		y_raw = np.append(y_raw,yf2)

	# Return essential data
	return x_raw, y_raw, y_bot, estimatedCenters, distsL,distsR


def prepare_plot_data(processed_perception_data):
	# Initialize empty list dedicated to storing each plots pair of data
	plot_data_pairs = []
	# Initialize the generic labels to be used for the legend
	labels = ['lidar readings', 'estimated bot position', 'estimated distance (Left)', 'estimated distance (Right)']
	# Extract combined processed data
	# NOTE: should be in form of [x_raw, y_raw, y_bot, estimatedCenters, distsL,distsR]
	raw_xs, raw_ys, bot_ys, centers, distsL, distsR = processed_perception_data

	# ------------ raw lidar readings ----------------
	lidar_plot = [raw_ys-raw_ys[0], raw_xs]
	# ------------ estimated robot center ----------------
	estCents = [bot_ys-raw_ys[0], (-1)*centers[1:]]
	# ------------ lateral distance left ----------------
	dLs = [bot_ys-raw_ys[0], distsL[1:]]
	# ------------ lateral distance right ----------------
	dRs = [bot_ys-raw_ys[0], (-1)*distsR[1:]]

	return lidar_plot,estCents,dLs,dRs, labels


	# plt.figure(1)
	# plt.cla()
	# #plot lateral rows
	# plt.plot(y_raw-y_raw[0], x_raw,'g*', marker='.', linestyle='None')
	# #plot estimated position of the robot
	# plt.plot(y_robot-y_raw[0],-estimated_center[1:],'k',lw=2)
	# #plot estimated left lateral distance
	# plt.plot(y_robot-y_raw[0],dl[1:],'r-',lw=2)
	# #plot estimated right lateral distance
	# plt.plot(y_robot-y_raw[0],-dr[1:],'r-',lw=2)
	# ax = plt.gca()
	# ax.set_aspect('equal', 'datalim')
	# plt.show()

# ========================================================
#				 	  MAIN SYSTEM CALL
# ========================================================
if __name__ == '__main__':

	# DEBUG FLAGS
	DEBUG_METH = 1

	dLs = []	# System Datalogs
	lLs = []	# Raw Lidar Datalogs
	plLs = []	# Perception Lidar Datalogs

	# Get the absolute path of this script regardless of where this script is called from
	myPath = os.path.abspath(__file__)
	myFolder = os.path.dirname(myPath)
	myParentDir = os.path.dirname(myFolder)
	# Change to repo root directory for easier calling of various paths
	experiment_dir = os.path.join(myParentDir,"test_data/experiments")
	collection_paths, nFound = find_collections(experiment_dir)

	""" ============================
		Simple Example: Single Plot
	================================ """
	if DEBUG_METH is 0:
		for path in collection_paths:
			sysData = get_system_data(path)
			lData = get_raw_lidar_data(path)
			plData, plConfigs = get_perception_lidar_data(path)

			dLs.append(sysData)
			lLs.append(lData)
			plLs.append([plData, plConfigs])

		xs, ys, bot_ys, centers, distsL,distsR = process_lidar_logs(lLs[1], plLs[1], dLs[1])

		plt.figure(1)
		#plot lateral rows
		plt.plot(ys-ys[0], xs,'g*', marker='.', linestyle='None')
		#plot estimated position of the robot
		plt.plot(bot_ys-ys[0],-centers[1:],'k',lw=2)
		#plot estimated left lateral distance
		plt.plot(bot_ys-ys[0],distsL[1:],'r-',lw=2)
		#plot estimated right lateral distance
		plt.plot(bot_ys-ys[0],-distsR[1:],'r-',lw=2)
		ax = plt.gca()
		ax.set_aspect('equal', 'datalim')
		plt.show()

	""" ================================
		Complex Example: Mulitple Plots
	===================================== """
	if DEBUG_METH is 1:
		meta_plot_data = []
		figs = []

		# Get all recognizable datalogs for each recognizable collection folder
		cDicts = [get_collection(path) for path in collection_paths]
		# Retrieve all collected data collection folder names for displaying each check box in graph
		dirNames = [tmpDict['name'] for tmpDict in cDicts]
		chkBoxFlags = tuple([False for i in range(0,len(dirNames))])

		for cDict in cDicts:
			tmpOut = process_lidar_logs(cDict['lidar_log'], cDict['perception_lidar'], cDict['system_log'])
			tmpPlotData, tmpLabels = prepare_plot_data(tmpOut)
			# Add collection name as prefix for all associated plot labels
			labels = [str(cDict['name']) + "-" + lbl for lbl in tmpLabels]

			meta_plot_data.append([tmpPlotData,labels])

		# Initialize Figure
		fig, ax = plt.subplots()
		plt.subplots_adjust(left=0.2)

		# Loop through all plots
		for figData, figLbl in meta_plot_data:
			figLsts = []
			# print figLbl
			# print
			for i in range(0,len(figLbl)):
				tmpFig1, = ax.plot(figData[i][0], figData[i][1], visible=False, marker='.',linestyle='None', label=figLbl[i][0])
				tmpFig2, = ax.plot(figData[i][0], figData[i][1], visible=False, marker="4",linestyle='-', label=figLbl[i][1])
				tmpFig3, = ax.plot(figData[i][0], figData[i][1], visible=False, marker='_',linestyle='--', label=figLbl[i][2])
				tmpFig4, = ax.plot(figData[i][0], figData[i][1], visible=False, marker='_',linestyle='--', label=figLbl[i][3])
				figLsts.append([tmpFig1,tmpFig2,tmpFig3,tmpFig4])

		rax = plt.axes([0.05, 0.4, 0.1, 0.15])
		check = CheckButtons(rax, tuple(dirNames), chkBoxFlags)


		# print meta_plot_data.shape
		def func(label):
			for i in range(0,len(dirNames)):
				if label == dirNames[i]:
					for subFigs in figLsts[i]:
						# print len(subFigs)
						subFigs.set_visible(not subFigs.get_visible())
					plt.draw()
			# [value if condition else value for value in variable if label == ]
			#
			# if label == '2 Hz':
			# 	l0.set_visible(not l0.get_visible())
			# elif label == '4 Hz':
			# 	l1.set_visible(not l1.get_visible())
			# elif label == '6 Hz':
			# 	l2.set_visible(not l2.get_visible())

		check.on_clicked(func)

		plt.show()
