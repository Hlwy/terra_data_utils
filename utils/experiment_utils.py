# -*- coding: utf-8 -*-
#!/usr/bin/env python

"""
	Created by: Hunter Young

	@description: The following contains functions that are designed specifically
for aiding in the post-processing, and visualization of, any information collected
within an 'experiment' folder.

"""

import os
from pathlib import Path

# ========================================================
#                 Directory & Filepath Importing
# ========================================================
def import_experiment_dirs(root_dir, verbose=False):
	collected_dirs = [dir for dir in Path(root_dir).iterdir() if dir.is_dir()]
	if(verbose):
		i = 1
		print("\n[Success] Collected %d experiments in root directory [%s]:" % (len(collected_dirs), root_dir) )
		for dir in collected_dirs:
			print("\t[Experiment #%d] ----- %s" % (i,dir))
			i += 1
	return collected_dirs

def import_experiment_subdirs(exp_dir, verbose=False):
	collected_subdirs = [dir for dir in Path(exp_dir).iterdir() if dir.is_dir()]
	if(verbose):
		i = 1
		print("\n[Success] Collected %d data collections for [%s]:" % (len(collected_subdirs), exp_dir) )
		for dir in collected_subdirs:
			print("\t[Experiment #%d] ----- %s" % (i,dir))
			i += 1
	return collected_subdirs


def find_experiment(root_dir, exp_dir, verbose=False):
	# Get all available experiments from root directory
	exps = import_experiment_dirs(root_dir)
	for exp in iter(exps):
		sub_name = os.path.basename(str(exp))
		if(verbose): print("%s ---- %s" % (str(exp_dir), sub_name) )

		if str(exp_dir) == sub_name:
			return exp
# ========================================================
#					Miscellaneous
# ========================================================
# # for files inside folders in an exp folder
# for exp in iter(exps_dir):
# for sub in exp.iterdir():


# if 'exp' is not locals():
#     exps = list(pTS)
#     exp = exps[-1]


# ========================================================
#				 	  MAIN SYSTEM CALL
# ========================================================
if __name__ == '__main__':
	# Desired Experiment for data
	desired_experiment_subdirectory = 'corn-2'
	desired_camera = 'cam_front'


	# Read in all available experiments
	exec(open("static_configuartion_params.py").read())

	""" -------	EXPERIMENTS UTILITY TESTS ------- """
	exDir = find_experiment(root_dir, desired_experiment_subdirectory)

	# Get the available data collections within desired experiment's directory
	exp_data_dirs = import_experiment_subdirs(exDir)

	""" -------	COLLECTION UTILITY TESTS ------- """
	# Choose a random data collection directory from test experiment
	tmp_collection = exp_data_dirs[1]
	# Get sample collection's available data
	show_collection_contents(tmp_collection, True)

	# exp_manifest = collections.OrderedDict()
	# test_data_manifest_id = os.path.basename(tmp_collection)
	# dC_name = get_collection_name(tmp_collection)
	# get_collection_info(tmp_collection)
	# add_manifest_entry(exp_manifest, test_data_manifest_id, dC_name)
