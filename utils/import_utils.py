# -*- coding: utf-8 -*-
#!/usr/bin/env python

"""
	Created by: Hunter Young

	Description: The following contains functions that are designed specifically
for facilitating in the importing of data into iterable data types for usage later.

"""

import os
import re #for split
import pandas as pd

# ========================================================
#					Importing using Pandas
# ========================================================
def read_datalog(path, header_names=None, skip_n=1, delimiter=",", has_header=True, verbose=False, show=False):
	read_data = []

	# Extract header names before using panda for 'header-name' agnostic file reading
	if(header_names == None):
		# Before extracting header values check if the file has headers present
		if(has_header):
			# Before opening the file to read make sure the path points to a valid file
			if os.path.isfile(path):
				# Open file for reading
				with open(str(path),'r') as rf:
					# Read every line in file and parse for essential elements
					header_str = rf.readline().splitlines()
					header_extract = header_str[0].split(delimiter)
				# Remove extra stuff for the core header information
				header_names = [re.sub("\([^a-zA-Z]+\)", "", col) for col in header_extract]
			else:
				print("\n[WARNING] \'%s\' does not point to a system recognized file." % path)
		else:
			if(verbose): print("\n[WARNING] Datalog does not have any headers present.")
	else:
		print("\n User-specified header names being used.")

	# Use pandas to read in file data into an iterable data type
	try:
		# Before opening the file to read make sure the path points to a valid file
		if os.path.isfile(path):
			if(has_header):
				read_data = pd.read_csv(path,sep=delimiter,skiprows=skip_n,names=header_names)
			else:
				read_data = pd.read_csv(path,sep=delimiter,skiprows=skip_n,header=None)
		else:
			print("\n[WARNING] \'%s\' does not point to a system recognized file." % path)
	except:
		print("[ERROR] Datalog either could not be found (or potentially empty file), or declared header names are invalid. (Datalog located at -- %s)" % (path) )

	if(show):
		print("Extracted Datalog:\r\n")
		print(read_data)

	return read_data


def read_perception_lidar_log(path, verbose=False, show=False):
	read_data = []
	config_data = {}

	if os.path.isfile(path):
		# Extract Configuration parameters used to generate resulting percption_lidar_log values
		with open(str(path),'r') as rf:
			# Read first line in file (which corresponds to configuration parameters used)
			config_str = rf.readline().splitlines()
			# Split line using custom delimiter to separate individual elements
			config_extract = config_str[0].split(',')
			# Cycle through list of extracted elements looking for pairs (by 2)
			config_data = {config_extract[i]:config_extract[i+1] for i in range(0,len(config_extract)-1, 2)}

		# Use pandas to read in the rest of the file data into an iterable data type
		try:
			read_data = pd.read_table(path,sep=',', header=1)
		except:
			print("[ERROR] Datalog could not be read. Potentially empty file).\n\t(Datalog located at -- %s)" % (path) )
	else:
		print("\n[WARNING] \'%s\' does not point to a system recognized file." % path)

	if(show):
		print("Extracted Datalog:\r\n")
		print(read_data)

	return read_data, config_data

# ========================================================
#	TODO			Importing using numpy
# ========================================================
def np_read_datalog():
	return None


# ========================================================
if __name__ == '__main__':
	import time # Used for delaying function calls for better test displaying

	# Get the absolute path of this script regardless of where this script is called from
	myPath = os.path.abspath(__file__)
	myFolder = os.path.dirname(myPath)
	myParentDir = os.path.dirname(myFolder)
	# Change to repo root directory for easier calling of various paths
	os.chdir(myParentDir)

	""" Test importing different datalog types from the 'test_data' directory """

	# System data
	print("\nTesting importing a \'system_log\'...")
	logData = read_datalog("test_data/datalogs/datalog/system_log")
	sz = logData.shape
	print("\n\t [YAY!!] Successfully imported recorded system data [%d X %d]!" % (sz[0], sz[1]) )

	time.sleep(1)

	# Camera
	print("\nTesting importing \'camera_test.txt\'...")
	logData = read_datalog("test_data/datalogs/camera/camera_test.txt")
	sz = logData.shape
	print("\n\t [YAY!!] Successfully imported recorded camera log [%d X %d]!" % (sz[0], sz[1]) )

	time.sleep(1)

	# Raw Lidar Data
	print("\nTesting importing raw Lidar data \'lidar/lidar_log\'...")
	logData = read_datalog("test_data/datalogs/lidar/lidar_log", has_header = False, skip_n = 0)
	sz = logData.shape
	print("\n\t [YAY!!] Successfully imported raw Lidar data [%d X %d]!" % (sz[0], sz[1]) )

	time.sleep(1)

	# Perception Lidar Data
	print("\nTesting importing Perception Lidar data \'lidar/perception_lidar_log\'...")
	logData, configData = read_perception_lidar_log("test_data/datalogs/lidar/perception_lidar_log")
	sz = logData.shape
	print("\n\t [YAY!!] Successfully imported Perception Lidar data [%d X %d]!" % (sz[0], sz[1]) )
