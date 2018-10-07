# -*- coding: utf-8 -*-

import argparse
from utils.experiment_utils import *
from utils.perception_lidar_utils import *
import random

def collect_experiments():
	ap = argparse.ArgumentParser(description='Plots the perception lidar outputs for the entire length of collection')
	ap.add_argument("--experiment", "-e",           type=str,   default='test_data/experiments/controlled', help="Name of the directory associated with the experiment user wants to plot data from.")
	# Store parsed arguments into array of variables
	args = vars(ap.parse_args())

	# Extract stored arguments array into individual variables for later usage in script
	exp_path = args["experiment"]

	# Find all recognizable collection folders
	collection_paths, nFound = find_collections(exp_path, verbose=True)
	# Get all recognizable datalogs for each recognizable collection folder
	if nFound == 1: collections = [get_collection(collection_paths,verbose=True)]
	else: collections = [get_collection(path,verbose=True) for path in collection_paths]
	# print len(collections)

	# Retrieve all collected data collection folder names for displaying each check box in graph
	dirNames = tuple([tmpDict['name'] for tmpDict in collections])
	return collections, dirNames


def setup_plot_data(collections):
	figDs = []
	legendName = None
	for collect in collections:
		tmpOut = process_lidar_logs(collect['lidar_log'], collect['perception_lidar'], collect['system_log'])
		lids,cents,dLs,dRs, lbls = prepare_plot_data(tmpOut, True)

		if fnmatch.fnmatch(str(collect['name']), '*sim*'):
			legendName = "Simulated Field Data"
			tmpData = [lids,cents,dLs,dRs, lbls, legendName, 'sim', str(collect['name'])]
		else:
			legendName = "Real Field Data"
			tmpData = [lids,cents,dLs,dRs, lbls, legendName, 'real', str(collect['name'])]

		figDs.append(tmpData)

	return figDs, len(figDs)


""" ================================
			Mulitple Plots
===================================== """
# fig, ax = plt.subplots()

# gridsize = (4, 2)
# fig = plt.figure(figsize=(12, 8))
# ax1 = plt.subplot2grid(gridsize, (0, 0), colspan=2, rowspan=2)
# # ax2 = plt.subplot2grid(gridsize, (0, 1), colspan=1, rowspan=2)
# ax3 = plt.subplot2grid(gridsize, (2, 0), colspan=1, rowspan=2)
# ax4 = plt.subplot2grid(gridsize, (2, 1), colspan=1, rowspan=2)

dCollects,dirNames = collect_experiments()
plotData, nPlots = setup_plot_data(dCollects)

# Retrieve all collected data collection folder names for displaying each check box in graph
subFigs1 = []
subFigs2 = []
subFigs3 = []
subFigs4 = []
plt.figure(1)
for i in range(0,len(plotData)):

	if plotData[i][6] == 'real':
		print "Real Data"
		# tmpFig, = ax1.plot(plotData[i][0][0], plotData[i][0][1], 'g.', label="Raw Lidar Measurements (Real)")
		# tmpFig3, = ax1.plot(plotData[i][2][0], plotData[i][2][1], color='lime', linestyle='-', label="Extracted L/R Distances (Real)")
		# tmpFig4, = ax1.plot(plotData[i][3][0], plotData[i][3][1], color='lime', linestyle='-')
		plt.plot(plotData[i][0][0], plotData[i][0][1], 'g.', label="Raw Lidar Measurements (Real)")
		plt.plot(plotData[i][2][0], plotData[i][2][1], color='yellow', linestyle='-', linewidth=3.0, label="Extracted L/R Distances (Real)")
		plt.plot(plotData[i][3][0], plotData[i][3][1], color='yellow', linestyle='-', linewidth=3.0)
	elif plotData[i][6] == 'sim':
		print "Simulated Data"
		# tmpFig, = ax1.plot(plotData[i][0][0], plotData[i][0][1], 'b.', label="Raw Lidar Measurements (Simulated)")
		# tmpFig3, = ax1.plot(plotData[i][2][0], plotData[i][2][1], 'c-', label="Extracted L/R Distances (Simulated)")
		# tmpFig4, = ax1.plot(plotData[i][3][0], plotData[i][3][1], 'c-')
		plt.plot(plotData[i][0][0], plotData[i][0][1], 'b.', label="Raw Lidar Measurements (Simulated)")
		plt.plot(plotData[i][2][0], plotData[i][2][1], 'm-', linewidth=3.0, label="Extracted L/R Distances (Simulated)")
		plt.plot(plotData[i][3][0], plotData[i][3][1], 'm-', linewidth=3.0)


plt.axis('equal')
plt.xlabel('Distance [m]')
plt.ylabel('Y [m]')
plt.ylim(-1,1)
plt.title('Simulated vs. Real Corn Field Data [LBIRNT]')
plt.legend()
plt.show()
