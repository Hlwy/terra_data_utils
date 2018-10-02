# -*- coding: utf-8 -*-

import argparse
from utils.perception_lidar_utils import *
from utils.experiment_utils import *
from matplotlib.widgets import CheckButtons		# Using this for dynamic overlaying of multiple data collections

def collect_experiments():
	ap = argparse.ArgumentParser(description='Plots the perception lidar outputs for the entire length of collection')
	ap.add_argument("--experiment", "-e",           type=str,   default='test_data/experiments/corn', help="Name of the directory associated with the experiment user wants to plot data from.")
	# Store parsed arguments into array of variables
	args = vars(ap.parse_args())

	# Extract stored arguments array into individual variables for later usage in script
	exp_path = args["experiment"]

	# Find all recognizable collection folders
	collection_paths, nFound = find_collections(exp_path, verbose=True)
	# Get all recognizable datalogs for each recognizable collection folder
	collections = [get_collection(path) for path in collection_paths]
	# print len(collections)

	# Retrieve all collected data collection folder names for displaying each check box in graph
	dirNames = tuple([tmpDict['name'] for tmpDict in collections])
	return collections, dirNames

def setup_plot_data(collections):
	figDs = []
	for collect in collections:
		if fnmatch.fnmatch(str(collect['name']), '*real*'):
			print("Real")
			spd_gain = -1
		elif fnmatch.fnmatch(str(collect['name']), '*sim*'):
			print("Simulated")
			spd_gain = -1.75
			spd_gain = -1.6

		tmpOut = process_lidar_logs(collect['lidar_log'], collect['perception_lidar'], collect['system_log'],spd_gain)
		lids,cents,dLs,dRs, lbls = prepare_plot_data(tmpOut)

		tmpData = [lids,cents,dLs,dRs, lbls, str(collect['name'])]
		figDs.append(tmpData)

	return figDs, len(figDs)

""" ================================
			Mulitple Plots
===================================== """
fig, ax = plt.subplots()

dCollects,dirNames = collect_experiments()
plotData, nPlots = setup_plot_data(dCollects)

# Retrieve all collected data collection folder names for displaying each check box in graph
names = [cName for _,_,_,_,_,cName in plotData]
chkBoxFlags = tuple([False for i in range(0,nPlots)])
rax = plt.axes([0.05, 0.4, 0.1, 0.15])
check = CheckButtons(rax, tuple(names), chkBoxFlags)

fLM1, = ax.plot(plotData[0][0][0], plotData[0][0][1], visible=False, marker='.',linestyle='None', label=plotData[0][4][0])
fLM2, = ax.plot(plotData[1][0][0], plotData[1][0][1], visible=False, marker='.',linestyle='None', label=plotData[1][4][0])
lidFigs = [fLM1,fLM2]

ax.legend(loc='upper left')
ax.set_aspect('equal', 'datalim')

def func(label):
	for name in names:
		if label == name:
			idx = names.index(name)
			lidFigs[idx].set_visible(not lidFigs[idx].get_visible())

		plt.draw()
		ax.legend(loc='upper left')
		ax.set_aspect('equal', 'datalim')


check.on_clicked(func)
plt.show()
