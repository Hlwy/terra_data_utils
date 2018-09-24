# -*- coding: utf-8 -*-
#!/usr/bin/env python

"""
	Created by: Hunter Young

	@description: The following contains functions that are designed specifically
for aiding in the creation/access of a 'manifest', which are used to keep track
of the various aspects of (and associated data with) any type of application.

"""

import os
import collections

# ========================================================
#					Manifest Utilities
# ========================================================
def add_manifest_entry(manifest, id, entry, verbose=False):
	# For now only allow OrderdDict
	# if isinstance(manifest, collections.OrderedDict()):
	if isinstance(manifest, collections.OrderedDict):
		# manifest[os.path.basename(str(exp))] = line
		manifest[str(id)] = str(entry)
		if(verbose): print("[Success!] Added entry \'%s\' to manifest with key \'%s\'" % (entry, id))
	else:
		print("[ERROR] \t Manifest should be of type \'OrderedDict()\' from \'collections\'")

	return manifest

# ========================================================
#				 	  MAIN SYSTEM CALL
# ========================================================
if __name__ == '__main__':

	dummy_collection_dict1 = {
		'id':1,
		'system_data':[],
		'camera_data':{
			'log_data':[],
			'video_data':"/path/to/location/of/recorded/video1.mp4"
		},
		'lidar_data':[],
		'perception_lidar_data':{
			'config':[],
			'data':[]
		}
	}
	dummy_collection_dict2 = {
		'id':2,
		'system_data':[],
		'camera_data':{
			'log_data':[],
			'video_data':"/path/to/location/of/recorded/video2.mp4"
		},
		'lidar_data':[],
		'perception_lidar_data':{
			'config':[],
			'data':[]
		}
	}

	# Example of what a manifest could be like
	eg_manifest = {
		'name':"sim_validation_experiment",
		'id':"experiment_manifest",
		'creator':"Hunter_Young",
		'date':"09_26_1992",
		'description':"Shows an example manifest used to keep track of all the essential information for later playback and retrieval of data used from experiment",
		'collections':[dummy_collection_dict1, dummy_collection_dict2],
	}
