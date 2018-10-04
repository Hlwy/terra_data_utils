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
	for collect in collections:
		if fnmatch.fnmatch(str(collect['name']), '*real*'):
			print("Real")
			spd_gain = -1
		elif fnmatch.fnmatch(str(collect['name']), '*simrun2*'):
			print("Simulated Run 2")
			spd_gain = -1.9
		elif fnmatch.fnmatch(str(collect['name']), '*sim*'):
			print("Simulated")
			spd_gain = -1.75
			spd_gain = -1.5
		else:
			spd_gain = -1.15

		tmpOut = process_lidar_logs(collect['lidar_log'], collect['perception_lidar'], collect['system_log'])
		# print tmpOut
		lids,cents,dLs,dRs, lbls = prepare_plot_data(tmpOut)
		tmpData = [lids,cents,dLs,dRs, lbls, str(collect['name'])]
		figDs.append(tmpData)

	return figDs, len(figDs)


""" ================================
			Mulitple Plots
===================================== """
# fig, ax = plt.subplots()

gridsize = (4, 2)
fig = plt.figure(figsize=(12, 8))
ax1 = plt.subplot2grid(gridsize, (0, 0), colspan=1, rowspan=2)
ax2 = plt.subplot2grid(gridsize, (0, 1), colspan=1, rowspan=2)
ax3 = plt.subplot2grid(gridsize, (2, 0), colspan=1, rowspan=2)
ax4 = plt.subplot2grid(gridsize, (2, 1), colspan=1, rowspan=2)

dCollects,dirNames = collect_experiments()
plotData, nPlots = setup_plot_data(dCollects)

# Retrieve all collected data collection folder names for displaying each check box in graph
names = [cName for _,_,_,_,_,cName in plotData]
chkBoxFlags = tuple([False for i in range(0,nPlots)])
rax = plt.axes([0.05, 0.4, 0.1, 0.15])
check = CheckButtons(rax, tuple(names), chkBoxFlags)

print plotData[0][4]

r = lambda: random.uniform(0,1)

subFigs1 = []
subFigs2 = []
subFigs3 = []
subFigs4 = []
for i in range(0,len(plotData)):
	tmpColor = (r(),r(),r())

	tmpFig, = ax1.plot(plotData[i][0][0], plotData[i][0][1], visible=False, marker='.',linestyle='None', label=plotData[i][4][0])
	subFigs1.append(tmpFig)

	tmpFig2, = ax2.plot(plotData[i][1][0], plotData[i][1][1], visible=False, marker="4",linestyle='-', label=plotData[i][4][1])
	subFigs2.append(tmpFig2)

	tmpFig3, = ax1.plot(plotData[i][2][0], plotData[i][2][1], color=tmpColor, visible=False, marker='_', label=plotData[i][4][2])
	subFigs3.append(tmpFig3)

	tmpFig4, = ax1.plot(plotData[i][3][0], plotData[i][3][1], color=tmpColor, visible=False, marker='_', label=plotData[i][4][3])
	subFigs4.append(tmpFig4)


# fLM1, = ax.plot(plotData[0][0][0], plotData[0][0][1], visible=False, marker='.',linestyle='None', label=plotData[0][4][0])
# fLM2, = ax.plot(plotData[1][0][0], plotData[1][0][1]+0.09, visible=False, marker='.',linestyle='None', label=plotData[1][4][0])
# # fLM3, = ax.plot(plotData[2][0][0], plotData[2][0][1], visible=False, marker='.',linestyle='None', label=plotData[2][4][0])
# # fLM4, = ax.plot(plotData[3][0][0], plotData[3][0][1]+0.09, visible=False, marker='.',linestyle='None', label=plotData[3][4][0])
# lidFigs = [fLM1,fLM2,fLM3,fLM4]
# lidFigs = [fLM1,fLM2]

# ax1.legend(loc='upper left')
ax1.set_aspect('equal', 'datalim')
ax2.legend(loc='upper left')
ax2.set_aspect('equal', 'datalim')

def func(label):
	for name in names:
		if label == name:
			idx = names.index(name)
			subFigs1[idx].set_visible(not subFigs1[idx].get_visible())
			subFigs2[idx].set_visible(not subFigs2[idx].get_visible())
			subFigs3[idx].set_visible(not subFigs3[idx].get_visible())
			subFigs4[idx].set_visible(not subFigs4[idx].get_visible())

		# ax1.legend(loc='upper left')
		ax1.set_aspect('equal', 'datalim')
		ax2.legend(loc='upper left')
		ax2.set_aspect('equal', 'datalim')
		plt.draw()


check.on_clicked(func)
plt.show()
