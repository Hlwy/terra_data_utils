# -*- coding: utf-8 -*-
#!/usr/bin/env python

import math
import numpy as np
import matplotlib.pyplot as plt

# Add to utils
from utils import experiment_utils as eut

def fcnProjectLidarScan(lidar_data, ang, lim_x_i, lim_x_s, lim_y_i, lim_y_s, theta):
    x_f = []
    y_f = []
    x = [0]*len(lidar_data)
    y = [0]*len(lidar_data)

	# For each distance measurement in current 2D Lidar scan
    for i in range(0, len(lidar_data)):

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
        if lidar_data[i] == -1000: lidar_data[i] = 65533 		# Max
        if lidar_data[i] == -2000: lidar_data[i] = 0	 		# Min TODO: make sure value matches

		""" NOTE: The following two lines do the following for each raw distance
		measurement (lidar[i]) received from the Lidar's frame of reference:

			- Converts measurement of lidar[i] (which is in polar coordinates)
			into cartesian coordinates [X, Y]

			- Transform converted X, Y coordinates (in the robot's frame of
			reference) such that, when plotted, will always be parallel. This
			was done by incorporating the robot's estimated heading (relative
			from within the crop row) with the angle of associated with lidar[i]
		"""
		x=(lidar_data[i]*math.cos(ang[i]*math.pi/180 + theta))/1000;
        y=(lidar_data[i]*math.sin(ang[i]*math.pi/180 + theta))/1000;

		# Only use lidar measurements that are within a specified "bounding rectangle"
        if x < lim_x_s and x> lim_x_i and y < lim_y_s and y > lim_y_i:
            x_f.append(x);
            y_f.append(y);

    return x_f, y_f



# perception_lidar_log variables
p = pTS[exp]								# perception lidar log data
pc = pTS_configs[exp]  						# perception_lidar_log config values
lts = p.lidar_ts_ms							# lidar timestamp used by the perception
ts = p.timestamp							# timestamp from perception_lidar_log
dl = p.distance_left
dr = p.distance_right
heading = p.heading

# lidar_log variables
l_ts = list(lidar[exp])						# timestamp from lidar_log file

# system_log variables
d = datalog[exp]								# system_log data
el = d.speed_calculation_from_encoder_left_m_s
er = d.speed_calculation_from_encoder_right_m_s


def get_estimated_offset_from_reference(distances_left, distances_right, pl_config):
	""" Desired offset of the navigation reference line (usually is 0 meaning the
	user wanted the robot to travel down the center of the row """
	ref_offset =  pl_config['middle_ref_m']
	# Estimate the robot's offset from its desired navigation line (e.g lane center)
	estimated_center = 0.5 * (distances_right - distances_left) - ref_offset
	return estimated_center

def get_avg_speed(encoders_left, encoders_right):
	bot_spd = (encoders_left + encoders_right) / 2
	avg_spd = np.nanmean(bot_spd)
	return avg_spd

def get_estimated_robot_position(avg_spd, times):
	t0 = times[0]				# Initial System Time [ms] of datalog
	ts = np.array(times[1:])	# System times after data collection start [ms]
	# Get the change in time [sec] since the beginning of collection
	dts = (ts - t0)*pow(10,-3)
	# Estimates how much distance the robot has travelled from its beginning location
	y_robot = avg_spd * dts # [Eq.] position = velocity * dt
	return y_robot



def process_lidar_logs(raw_lidar_times, lidar_data):
	""" NOTE:

		- l_ts	: lidar_log times
		- lts	: perception_lidar_log times
		- pc	: perception_lidar_log configuration parameters
	"""
	raw_lidar_times = 
	lidar_data =

	index0 = 1
	x_raw=[]
	y_raw=[]
	# Loop through each recorded Lidar scan data
	for pl_scan_idx in range (index0, len(estimated_center)):

		# Use the timestamp of the 'perception_lidar_log' as reference
		t_ref = lts[pl_scan_idx]
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
		scan_data = lidar_data[exp][t_sync]
		# Generate angular range of Lidar distance measurements [degrees]
		ang_rng = np.linspace(-45,225,1080, endpoint = False)
		# Project time-sync'd raw lidar scan into corrected cartesian coordinates
		xf, yf = fcnProjectLidarScan(scan_data, ang_rng, -pc['LANE_WIDTH'], ⁠\
									pc['LANE_WIDTH'], pc['lim_y_i'], \
									pc['lim_y_s'], p.heading[pl_scan_idx])

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
		xf2 = np.array(xf2) - pc['middle_ref_m']
		yf2 = np.array(yf2) + avg_speed_m_s*(ts[scan] - ts[0])*pow(10,-3)
		if len(yf2) > 0:
			aux_maxy = max(yf2)
			if aux_maxy > maxy:
				maxy = aux_maxy

		# Store cartesian coordinates for later visualization
		x_raw = np.append(x_raw,xf2)
		y_raw = np.append(y_raw,yf2)


def plot_data():
	plt.figure(1)
	plt.cla()
	#plot lateral rows
	plt.plot(y_raw-y_raw[0], x_raw,'g*', marker='.', linestyle='None')
	#plot estimated position of the robot
	plt.plot(y_robot-y_raw[0],-estimated_center[1:],'k',lw=2)
	#plot estimated left lateral distance
	plt.plot(y_robot-y_raw[0],dl[1:],'r-',lw=2)
	#plot estimated right lateral distance
	plt.plot(y_robot-y_raw[0],-dr[1:],'r-',lw=2)
	ax = plt.gca()
	ax.set_aspect('equal', 'datalim')
	plt.show()
