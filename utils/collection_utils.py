# -*- coding: utf-8 -*-
#!/usr/bin/env python

"""
	Created by: Hunter Young

	@description: The following contains functions that are designed specifically
for aiding in the interaction with data collections created automatically from the
Terrasentia robot framework. The capabilities of the functions contained within
include, but is not limited to, the following:

	- Retrieving any meta-data associated with the collection (i.e type of
crops, name of field, etc.)

	- View/Retrieve/Package available sources of information contained in
associated data collections for easier bundling, handling, and usage for later

	- Keeping track of the paths associated with various data collections

"""

import os
import glob
from datalog_utils import *
from manifest_utils import *

# ========================================================
#                 Collections Meta-Data Utilites
# ========================================================
def get_collection_name(collection_dir, verbose=False):
	if(verbose):
		print("\nGetting Data Collection Name:")
		print("\t[INFO] parent directory ----- %s" % (collection_dir))

	tmp_file = os.path.join(str(collection_dir),'name.txt')
	# Check if specified file is valid
	if os.path.isfile(tmp_file):
		# Open file for reading
		with open(str(tmp_file),'r') as rf:
			collection_name = rf.readline()

		if(verbose): print("\tstored data collection name ----- %s" % (collection_name))
		return collection_name

def get_collection_info(collection_dir, delimiter=" ", verbose=False):
	if(verbose):
		print("\nGetting Data Collection Info:")
		print("\t[INFO] parent directory ----- %s" % (collection_dir))

	tmp_file = os.path.join(str(collection_dir),'info.txt')
	# Check if specified file is valid
	if os.path.isfile(tmp_file):
		# Open file for reading
		with open(str(tmp_file),'r') as rf:
			# Read every line in file and parse for essential elements
			lines = rf.read().splitlines()
			extracted_data = [line.split(delimiter) for line in lines]

		# Store extracted data into single dictionary for output
		if(verbose):
			print("\tParsed file entries: \'[Id]:Value\'")
			for i, j in extracted_data:
				print("\t\t%s:%s" % (i,j))

def show_collection_contents(collection_dir, verbose=False):
	if(verbose):
		print("\nShowing available objects of recorded Data Collection:")
		print("\t[INFO] parent directory ----- %s" % (str(collection_dir)))

	# Loop through collection's sub-directories
	for sub in collection_dir.iterdir():
		# Do something depending on whether the current object is a directory or file
		if(os.path.isfile(str(sub)) ):
			dbg_type = "file"
		elif(os.path.isdir(str(sub)) ):
			dbg_type = "subdirectory"
		else:
			dbg_type = "unknown"

		if(verbose):
			dbg_base = os.path.basename(str(sub))
			print("\t%s ----- %s" % (dbg_type, dbg_base) )


""" TODO:
	This function should extract potentially useful information from the
collection.field file that should be within a collection folder
"""
def get_collection_field_info(collection_dir, delimiter=" ", verbose=False):
	return None


def find_collections(search_dir, collection_patterns=None,datalog_patterns=None, verbose=False):
	""" Description:
	This function should find all collection folders within specified directory by
	looking for either a 'collection.field' or a 'collection.mp' files
	"""
	found_collections = []

	# Look for default files that should be present in a data collection folder
	if collection_patterns == None:
		collection_patterns = ['*collection.field', '*collection.mp']

	""" NOTE: Search for system log files as a failsafe, or for cases where
	patterns specific to 'collection's aren't found.

		- ASSUMES that a 'collection' folder should at minimum have a system
		datalog
	"""
	if datalog_patterns == None:
		datalog_patterns = ['*datalog*.txt', '*system_log']

	if(verbose):
		print("\nSearching for collection directories in specified directory....")
		print("\t[INFO] searching directory ----- %s" % (str(search_dir)))
		print("\t[INFO] collection search pattern(s) ----- %s" % (str(collection_patterns)))
		print("\t[INFO] datalog search pattern(s) ----- %s" % (str(datalog_patterns)))

	# Search everywhere in directory for acceptable patterns
	foundTmps = []
	for root, dirs, files in os.walk(str(search_dir)):
		# TODO Doesnt work: If data collection already found skip ahead (ensure to reduce computation by avoiding duplicate operations)
		if any(fnmatch.fnmatch(str(root), os.path.basename(path)) for path in foundTmps):
			if(verbose): print("[INFO] ----- Root already archived skipping ahead....")
			continue

		# First check if any files match to recorded system data
		for file in files:
			if any(fnmatch.fnmatch(file, pat) for pat in collection_patterns):
				has_collection = True
				if root not in foundTmps:
					if(verbose): print("\t\tFound a new collection pattern!")
					foundTmps.append(root)
			elif any(fnmatch.fnmatch(file, pat) for pat in datalog_patterns):
				has_datalog = True
				if os.path.dirname(root) not in foundTmps:
					if(verbose): print("\t\tNo collection patterns found ..... but found an new datalog!")
					foundTmps.append(os.path.dirname(root))

	# TODO: Ensure that any duplicates are removed
	found_collections = foundTmps	# For now using tmps

	# See how many were found
	nFound = len(found_collections)
	if nFound == 0: print("!!\t[WARNING] No data collection folders found using any search patterns \'%s\'!" % (collection_patterns+datalog_patterns) )
	# If only one data collection found remove path element from list for easy usage
	if nFound == 1: found_collections = found_collections[0]

	if(verbose):
		print("\t[INFO] Found %d data collection folders:" % nFound)

		if nFound == 1: print("\t\t- %s" % found_collections)
		else:
			for log in found_collections:
				print("\t\t- %s" % log)

	return found_collections,nFound

""" TODO:
	Retrieves all the information available for any given collection into a
	dictionary
"""
def get_collection(collection_path, verbose=False):
	cDict = {}		# Entire Collection dictionary for storing everything
	plDict = {}		# Dictionary for storing perception lidar data and config

	cName = os.path.basename(collection_path)
	cDict['name'] = cName
	cDict['path'] = collection_path

	if(verbose):
		print("\nGetting all data available for specified collection.... %s", cName)
		print("\t[INFO] full collection path ----- %s" % (str(collection_path)))

	# ------------ Get System log data ----------------
	tmpData = get_system_data(collection_path)
	# Store data if one exists otherwise throw warning
	if tmpData is None:
		print("\t[WARNING] Could not find system log data!")
	else:
		cDict['system_log'] = tmpData

	# ------------ Get Raw Lidar log data ----------------
	tmpData = get_raw_lidar_data(collection_path)
	# Store data if one exists otherwise throw warning
	if tmpData is None:
		print("\t[WARNING] Could not find raw lidar log data!")
	else:
		cDict['lidar_log'] = tmpData

	# ------------ Get Perception Lidar log data ----------------
	tmpData, tmpConfig = get_perception_lidar_data(collection_path)
	# Store data if one exists otherwise throw warning
	if tmpData is None:
		print("\t[WARNING] Could not find perception lidar log data!")
	else:
		plDict['data'] = tmpData
	# Store configuration if one exists otherwise throw warning
	if tmpConfig is None:
		print("\t[WARNING] Could not find perception lidar log configuration!")
	else:
		plDict['config'] = tmpConfig

	cDict['perception_lidar'] = plDict

	# ------------ TODO: Get Camera log data ----------------
	camDict = {
		'id':"front",
		'log':[],
		'video':"/path/to/location/of/recorded/video1.mp4"
	}
	cDict['camera_front'] = camDict

	# ------------ ----------------
	if(verbose): print cDict['perception_lidar']['config']

	return cDict

# ========================================================
#				 	  MAIN SYSTEM CALL
# ========================================================
if __name__ == '__main__':
	import time # Used for delaying function calls for better test displaying

	TEST_SEARCHING = True
	TEST_MISC = False

	# Get the absolute path of this script regardless of where this script is called from
	myPath = os.path.abspath(__file__)
	myFolder = os.path.dirname(myPath)
	myParentDir = os.path.dirname(myFolder)
	# Change to repo root directory for easier calling of various paths
	# collection_dir = os.path.join(myParentDir,"test_data/collections") # Original
	collection_dir = os.path.join(myParentDir,"test_data/experiments/corn/controlled")

	""" -------	SEARCHING OF COLLECTIONS ------- """
	if TEST_SEARCHING:
		# Search for all available data collection folders within test directory
		collection_paths, nFound = find_collections(collection_dir, verbose=True)
		print("\n\t[YAY!!] Successfully retrieved %d data collections!" % (nFound) )
		time.sleep(1)

		get_collection(collection_paths[0])

	""" -------	MISCELLANEOUS TESTS ------- """
	if TEST_MISC:
		# Get sample collection's available data
		show_collection_contents(tmp_collection, True)

		exp_manifest = collections.OrderedDict()
		test_data_manifest_id = os.path.basename(tmp_collection)
		dC_name = get_collection_name(tmp_collection)
		get_collection_info(tmp_collection)
		add_manifest_entry(exp_manifest, test_data_manifest_id, dC_name)
