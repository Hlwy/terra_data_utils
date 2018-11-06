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
		# lids,cents,dLs,dRs, lbls = prepare_plot_data(tmpOut, True)
		# lids,cents,dLs,dRs, lbls = prepare_plot_data(tmpOut, None)

		if fnmatch.fnmatch(str(collect['name']), '*sim*'):
			legendName = "Simulated Field Data"

			# lids,cents,dLs,dRs, lbls = prepare_plot_data(tmpOut, None)
			lids,cents,dLs,dRs, lbls = prepare_plot_data(tmpOut, [3.5])

			tmpData = [lids,cents,dLs,dRs, lbls, legendName, 'sim', str(collect['name'])]
		else:
			legendName = "Real Field Data"

			# lids,cents,dLs,dRs, lbls = prepare_plot_data(tmpOut, None)
			# lids,cents,dLs,dRs, lbls = prepare_plot_data(tmpOut, [40.4, 44.5]) # Sorghum Run 1
			# lids,cents,dLs,dRs, lbls = prepare_plot_data(tmpOut, [30.26, 34.5]) # Sorghum Run 2
			# lids,cents,dLs,dRs, lbls = prepare_plot_data(tmpOut, [4.5]) # Sorghum Run 3
			# lids,cents,dLs,dRs, lbls = prepare_plot_data(tmpOut, [5.3])
			lids,cents,dLs,dRs, lbls = prepare_plot_data(tmpOut, [3.4])

			tmpData = [lids,cents,dLs,dRs, lbls, legendName, 'real', str(collect['name'])]

		figDs.append(tmpData)

	return figDs, len(figDs)


""" ================================
			Mulitple Plots
===================================== """

dCollects,dirNames = collect_experiments()
plotData, nPlots = setup_plot_data(dCollects)

# Retrieve all collected data collection folder names for displaying each check box in graph
plt.figure(1)
for i in range(0,len(plotData)):

	if plotData[i][6] == 'real':
		print "Real Data"
		plt.plot(plotData[i][0][0], plotData[i][0][1], color='darkgreen', linestyle='None', marker='.', zorder=0, label="Raw Lidar Measurements (Real)")
		plt.plot(plotData[i][2][0], plotData[i][2][1], color='yellow', linestyle='-', linewidth=3.0, zorder=2, label="Extracted L/R Distances (Real)")
		plt.plot(plotData[i][3][0], plotData[i][3][1], color='yellow', linestyle='-', linewidth=3.0, zorder=2)
	elif plotData[i][6] == 'sim':
		print "Simulated Data"
		plt.plot(plotData[i][0][0], plotData[i][0][1], color='b', linestyle='None', marker='.', zorder=1, label="Raw Lidar Measurements (Simulated)")
		plt.plot(plotData[i][2][0], plotData[i][2][1], color='m', linestyle='-', linewidth=3.0, zorder=3, label="Extracted L/R Distances (Simulated)")
		plt.plot(plotData[i][3][0], plotData[i][3][1], color='m', linestyle='-', linewidth=3.0, zorder=3)


plt.axis('equal')
plt.xlabel('Distance [m]')
plt.ylabel('Y [m]')
plt.ylim(-1,1)
plt.title('Simulated vs. Real Controlled Field Data [LBIRNT]')
plt.legend()
plt.show()
