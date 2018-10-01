# -*- coding: utf-8 -*-



import argparse
from utils.perception_lidar_utils import *

def main():
    ap = argparse.ArgumentParser(description='Plots the perception lidar outputs for the entire length of collection')
    ap.add_argument("--experiment", "-e",           type=str,   default='test_data/experiments/corn', help="Name of the directory associated with the experiment user wants to plot data from.")
    # Store parsed arguments into array of variables
    args = vars(ap.parse_args())

    # Extract stored arguments array into individual variables for later usage in script
    exp_path = args["experiment"]

    collection_paths, nFound = find_collections(exp_path, verbose=True)
    print collection_paths
    if nFound == 1:
        sysData = get_system_data(collection_paths, verbose=True)
        lData = get_raw_lidar_data(collection_paths)
        plData, plConfig = get_perception_lidar_data(collection_paths)
        xs, ys, bot_ys, centers, distsL,distsR = process_lidar_logs(lData, [plData, plConfig], sysData)

    plt.figure(1)
    #plot lateral rows
    plt.plot(ys-ys[0], xs,'g*', marker='.', linestyle='None')
    #plot estimated position of the robot
    plt.plot(bot_ys-ys[0],-centers[1:],'k',lw=2)
    #plot estimated left lateral distance
    plt.plot(bot_ys-ys[0],distsL[1:],'r-',lw=2)
    #plot estimated right lateral distance
    plt.plot(bot_ys-ys[0],-distsR[1:],'r-',lw=2)
    ax = plt.gca()
    ax.set_aspect('equal', 'datalim')
    plt.show()

main()

# plt.figure(1)
# plt.cla()
# #plot lateral rows
# plt.plot(y_raw-y_raw[0], x_raw,'g*', marker='.', linestyle='None')
# #plot estimated position of the robot
# plt.plot(y_robot-y_raw[0],-estimated_center[1:],'k',lw=2)
# #plot estimated left lateral distance
# plt.plot(y_robot-y_raw[0],dl[1:],'r-',lw=2)
# #plot estimated right lateral distance
# plt.plot(y_robot-y_raw[0],-dr[1:],'r-',lw=2)
# ax = plt.gca()
# ax.set_aspect('equal', 'datalim')
# plt.show()
