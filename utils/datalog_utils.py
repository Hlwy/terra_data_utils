# -*- coding: utf-8 -*-
#!/usr/bin/env python

"""
	Created by: Hunter Young

	@description: The following contains functions that are designed specifically
for aiding in the interaction with data logs associated with supported data
sources that were recorded and generated using the Terrasentia robot framework.
The capabilities of the functions contained within include, but is not limited
to, the following:

	- Searching for all available datalog types (camera, lidar, etc.), and their
respective paths, contained within a specified directory

	- Support for multiple variations in the datalogs containing the same
essential information

"""

import os
import glob
import fnmatch
from import_utils import *

# ========================================================
#                 Directory & Filepath Searching
# ========================================================
def find_system_logs(search_path, patterns=None, verbose=False):
	found_paths = []
	# Filename patterns associated with an acceptable datalog
	if patterns == None:
		patterns = ['*system_log']

	if(verbose):
		print("\nSearching for system logs in data collection....")
		print("\t[INFO] searching directory ----- %s" % (str(search_path)))
		print("\t[INFO] search patterns ----- %s" % (str(patterns)))

	# Search everywhere in collection directory for acceptable patterns
	for root, dirs, files in os.walk(str(search_path)):
		for pat in patterns: 					# Try all patterns
			for file in files: 					# Try all files
				if fnmatch.fnmatch(file, pat):	# Check for a match
					tmp = os.path.join(root, file)
					found_paths.append(tmp)

	if(len(found_paths) == 0):
		tmpStr = str(search_path) + "/*datalog/datalog*.txt"
		# print tmpStr
		found_paths = glob.glob(tmpStr)
		print found_paths

	# See how many were found
	nFound = len(found_paths)
	if nFound == 0: print("!!\t[WARNING] No system datalogs found!")
	# If only one datalog found remove path element from paths list for easy usage
	if nFound == 1: found_paths = found_paths[0]

	if(verbose):
		print("\t[INFO] Found %d system datalogs:" % nFound)

		if nFound == 1: print("\t\t- %s" % found_paths)
		else:
			for log in found_paths:
				print("\t\t- %s" % log)

	return found_paths,nFound


def find_camera_logs(search_path, patterns=None,specific_target=None, verbose=False):
	print("\n\n[WARNING] find_camera_logs() ----- does not look for video files!!!")

	found_paths = []
	# Filename patterns associated with an acceptable datalog
	if patterns == None:
		patterns = ['*cam*.txt','*cam']

	if(verbose):
		print("\nSearching for available cameras recorded in data collection....")
		print("\t[INFO] searching directory ----- %s" % (str(search_path)))
		print("\t[INFO] search patterns ----- %s" % (str(patterns)))

	# Search everywhere in collection directory for acceptable patterns
	for root, dirs, files in os.walk(str(search_path)):
		for pat in patterns: 					# Try all patterns
			for file in files: 					# Try all files
				if fnmatch.fnmatch(file, pat):	# Check for a match
					tmp = os.path.join(root, file)
					found_paths.append(tmp)

	# Check for how many valid data paths found
	nFound = len(found_paths)
	nReturn = 0
	data_path = []

	# If user does define specific data to find then return all possible options
	if(nFound > 0):
		if(specific_target == None):
			if(verbose): print("\t[INFO] No specific camera log defined. Returning all camera logs found.")
			data_path = found_paths
			nReturn = nFound
		else:
			# Check if defined data target exists in found directories
			for path in found_paths:
				if(os.path.basename(path) == specific_target):
					if(verbose): print("\t[INFO] Found camera data for target \'%s\' at \'%s\'" % (specific_target, path) )
					data_path = path
					nReturn = 1
	else:
		if(specific_target == None): print("!!\t[WARNING] No camera datalogs found!")
		else: print("\t[WARNING] Could not find specified camera data [%s]" % (specific_target) )
		nReturn = 0

	if(verbose):
		print("\t[INFO] Found %d camera datalogs:" % nFound)
		if nFound == 1: print("\t\t- %s" % found_paths)
		else:
			for log in found_paths:
				print("\t\t- %s" % log)

	return data_path, nReturn, nFound


def find_lidar_logs(search_path, patterns=None, specific_target=None,verbose=False):
	print("\n\n[WARNING] find_lidar_logs() ----- does not filter out \'perception_lidar_log\' files!!!")

	found_paths = []
	# Filename patterns associated with an acceptable datalog
	if patterns == None:
		patterns = ['*datalog-lidar*measurements.txt','*lidar_log']
		# patterns = ['*lidar_log']

	if(verbose):
		print("\nSearching for available Lidars recorded in data collection....")
		print("\t[INFO] searching directory ----- %s" % (str(search_path)))
		print("\t[INFO] search patterns ----- %s" % (str(patterns)))

	# Search everywhere in collection directory for acceptable patterns
	for root, dirs, files in os.walk(str(search_path)):
		for pat in patterns: 					# Try all patterns
			for file in files: 					# Try all files
				if fnmatch.fnmatch(file, pat):	# Check for a match
					tmp = os.path.join(root, file)
					found_paths.append(tmp)

	# Check for how many valid data paths found
	nFound = len(found_paths)
	nReturn = 0
	data_path = []

	# If user does define specific data to find then return all possible options
	if(nFound > 0):
		if(specific_target == None):
			if(verbose): print("\t[INFO] No specific lidar log defined. Returning all Lidar logs found.")
			data_path = found_paths
			nReturn = nFound
		else:
			# Check if defined data target exists in found directories
			for path in found_paths:
				if(os.path.basename(path) == specific_target):
					if(verbose): print("\t[INFO] Found Lidar data for target \'%s\' at \'%s\'" % (specific_target, path) )
					data_path = path
					nReturn = 1
	else:
		if(specific_target == None): print("!!\t[WARNING] No Lidar datalogs found!")
		else: print("\t[WARNING] Could not find specified Lidar data [%s]" % (specific_target) )
		nReturn = 0

	if(verbose):
		print("\t[INFO] Found %d Lidar datalogs:" % nFound)
		for log in found_paths:
			print("\t\t- %s" % log)

	return data_path, nReturn, nFound, found_paths


def find_perception_lidar_logs(search_path, patterns=None,specific_target=None,verbose=False):
	found_paths = []
	# Filename patterns associated with an acceptable datalog
	if patterns == None:
		patterns = ['*datalog-lidar*perception.txt','*perception_lidar_log']
		# patterns = ['*perception_lidar_log']

	if(verbose):
		print("\nSearching for available Perception Lidar recorded in data collection....")
		print("\t[INFO] searching directory ----- %s" % (str(search_path)))
		print("\t[INFO] search patterns ----- %s" % (str(patterns)))

	# Search everywhere in collection directory for acceptable patterns
	for root, dirs, files in os.walk(str(search_path)):
		for pat in patterns: 					# Try all patterns
			for file in files: 					# Try all files
				if fnmatch.fnmatch(file, pat):	# Check for a match
					tmp = os.path.join(root, file)
					found_paths.append(tmp)

	# Check for how many valid data paths found
	nFound = len(found_paths)
	nReturn = 0
	data_path = []

	# If user does define specific data to find then return all possible options
	if(nFound > 0):
		if(specific_target == None):
			if(verbose): print("\t[INFO] No specific Perception Lidar log defined. Returning all Perception Lidar logs found.")
			data_path = found_paths
			nReturn = nFound
		else:
			# Check if defined data target exists in found directories
			for path in found_paths:
				if(os.path.basename(path) == specific_target):
					if(verbose): print("\t[INFO] Found Perception Lidar data for target \'%s\' at \'%s\'" % (specific_target, path) )
					data_path = path
					nReturn = 1
	else:
		if(specific_target == None): print("!!\t[WARNING] No Perception Lidar datalogs found!")
		else: print("\t[WARNING] Could not find specified Perception Lidar data [%s]" % (specific_target) )
		nReturn = 0

	if(verbose):
		print("\t[INFO] Found %d Perception Lidar datalogs:" % nFound)
		for log in found_paths:
			print("\t\t- %s" % log)

	return data_path, nReturn, nFound, found_paths


# ========================================================
#                 Type-specific Data Importing
# ========================================================
def get_system_data(path, verbose=False):
	output_data = []
	if(verbose):
		print("\nGetting available data recorded for Collection:")
		print("\t[INFO] parent directory ----- %s" % (str(path)))

	# Find all available camera log directories
	log_path, nLogs = find_system_logs(path,verbose=verbose)
	if(verbose): print("\t[INFO] Found %d system logs" % (nLogs) )

	# Exiting Conditions
	if(nLogs <= 0):
		print("\t[WARNING] No system log data could be found!")
		output_data = None
	elif(nLogs == 1):
		if(verbose): print("\t[INFO] Found system log data at \'%s\'" % (log_path) )
		output_data = read_datalog(log_path, show=verbose)
	else:
		print("!!!!! [TODO] Handle collecting multiple logs for  \'get_collection_data_system\'")
		output_data = None

	return output_data

def get_camera_log_data(path, target_camera, verbose=False):
	output_data = []
	if(verbose):
		print("\nGetting available camera data for a data collection bundle:")
		print("\t[INFO] parent directory ----- %s" % (str(path)))

	# Find all available camera log directories
	cam_path, nReturn, nFound = find_camera_logs(path,specific_target=target_camera,verbose=verbose)
	if(len(cam_path) <= 0):
		print("\t[WARNING] No camera data could be found!")
		output_data = None

	# Extract necessary data from path
	if(verbose):
		print("\t[INFO] Found camera data at \'%s\'" % (cam_path) )
	print("!!!!! [TODO] Implement output of both camera log and video file (via \'return cam_log, vid_file\') for function \'get_collection_data_camera\'")

	return output_data

def get_raw_lidar_data(path, target_lidar="lidar_log", verbose=False):
	output_data = []

	if(verbose):
		print("\nGetting available Lidar data recorded for Collection:")
		print("\t[INFO] parent directory ----- %s" % (str(path)))

	# Find all available camera log directories
	log_path, nReturned, nFound, found_paths = find_lidar_logs(path,specific_target=target_lidar, verbose=verbose)

	# Pre-Checking Conditions
	if(nReturned == 0):
		if(nFound > 0):
			if(nFound == 1):
				nLogs = 1
				log_path = found_paths[0]
			else:
				nLogs = nFound
				log_path = found_paths
			print("\t[WARNING] Specific Lidar log data could not be found.\tReturning all %d found Lidar logs." % nFound)
		else:
			nLogs = 0
	else:
		nLogs = nReturned

	# Exiting Conditions
	if(nLogs == 0):
		print("\t[ERROR] No Lidar log data could be found!")
		output_data = None
	elif(nLogs == 1):
		if(verbose): print("\n\t[INFO] Found Lidar log at \'%s\'\n" % (log_path) )
		tmp_data = read_datalog(log_path, has_header = False, skip_n = 0,show=verbose)

		""" NOTE: This portion is to handle previous datalogs that
		were setup differently
		"""
		# if df.shape[1] <= 1082:
		# 	ts = df[0]
		# 	lm = df.loc[:,1:1080].values.tolist()
		# elif df.shape[1] == 1083:
		# 	print("Used this...")
		# 	ldf = df
		# 	ts = df[2]
		# 	lm = df.loc[:,3:1083].values.tolist()
		# else:
		# 	print("Check lidar column size")
		#
		# print("\nsize ts: " + str(len(ts)) + "\tlm: " + str(len(lm)) + "/" + str(len(lm[0])))
		# lidar[os.path.basename(str(exp))] = OrderedDict(zip(ts,lm))
		""" END NOTE """
		output_data = tmp_data
	else:
		print("!!!!! [TODO] Handle collecting multiple logs for  \'get_collection_data_lidar\'")
		output_data = None

	return output_data

def get_perception_lidar_data(path, target_lidar="perception_lidar_log", verbose=False):
	output_data = []
	config_data = []

	if(verbose):
		print("\nGetting available Perception Lidar data recorded for Collection:")
		print("\t[INFO] parent directory ----- %s" % (str(path)))


	# Find all available camera log directories
	log_path, nReturned, nFound, found_paths = find_perception_lidar_logs(path,specific_target=target_lidar, verbose=verbose)

	# Pre-Checking Conditions
	if(nReturned == 0):
		if(nFound > 0):
			if(nFound == 1):
				nLogs = 1
				log_path = found_paths[0]
			else:
				nLogs = nFound
				log_path = found_paths
			print("\t[WARNING] Specific Perception Lidar log data could not be found.\tReturning all %d found Perception Lidar logs." % nFound)
		else:
			nLogs = 0
	else:
		nLogs = nReturned


	# Exiting Conditions
	if(nLogs == 0):
		print("\t[WARNING] No Perception Lidar log data could be found!")
		output_data = None
		config_data = None
	elif(nLogs == 1):
		if(verbose): print("\n\t[INFO] Found Perception Lidar log at \'%s\'\n" % (log_path) )
		output_data, config_data = read_perception_lidar_log(log_path, verbose=verbose)
	else:
		print("!!!!! [TODO] Handle collecting multiple logs for  \'get_collection_data_perception_lidar\'")
		output_data = None
		config_data = None

	return output_data, config_data

# ========================================================
#				 	  MAIN SYSTEM CALL
# ========================================================
if __name__ == '__main__':
	import time # Used for delaying function calls for better test displaying

	TEST_SEARCHING = False
	TEST_GETTING = True

	# Get the absolute path of this script regardless of where this script is called from
	myPath = os.path.abspath(__file__)
	myFolder = os.path.dirname(myPath)
	myParentDir = os.path.dirname(myFolder)
	# Change to repo root directory for easier calling of various paths
	log_dir = os.path.join(myParentDir,"test_data/datalogs")

	""" -------	TESTS FOR FINDING DIFFERENT DATA LOGS ------- """
	if(TEST_SEARCHING):
		paths, nLogs = find_system_logs(log_dir)
		print("\n[YAY!!] Successfully found %d system datalogs!" % (nLogs) )
		time.sleep(1)

		paths, nReturned, nFound = find_camera_logs(log_dir,specific_target="camera_test")
		print("\n[YAY!!] Successfully found %d camera datalogs!" % (nFound) )
		time.sleep(1)

		paths, nReturned, nFound = find_lidar_logs(log_dir)
		print("\n[YAY!!] Successfully found %d Lidar datalogs!" % (nFound) )
		time.sleep(1)

		paths, nReturned, nFound = find_perception_lidar_logs(log_dir)
		print("\n[YAY!!] Successfully found %d Perception Lidar datalogs!" % (nFound) )
		time.sleep(1)

	""" -------	TESTS FOR LOADING LOGGED DATA INTO VARIABLES ------- """
	if(TEST_GETTING):
		data = get_system_data(log_dir)
		sz = data.shape
		print("\n\t [YAY!!] Successfully retrieved system data [%d X %d]!" % (sz[0], sz[1]) )
		time.sleep(1)

		data = get_raw_lidar_data(log_dir, verbose=False)
		sz = data.shape
		print("\n\t [YAY!!] Successfully retrieved raw Lidar data [%d X %d]!" % (sz[0], sz[1]) )
		time.sleep(1)

		data, configParams = get_perception_lidar_data(log_dir, verbose=False)
		sz = data.shape
		szCfg = len(configParams)
		print("\n\t [YAY!!] Successfully retrieved Perception Lidar data [%d X %d] with %d configuration parameters!" % (sz[0], sz[1], szCfg) )
		time.sleep(1)
