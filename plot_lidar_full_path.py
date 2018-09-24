# -*- coding: utf-8 -*-
"""
Created on Mon Jul  9 19:07:18 2018

@author: vahh
"""

exec(open("import_data.py").read())

import matplotlib.pyplot as plt
import numpy as np
import math
from matplotlib.widgets import Slider, Button, RadioButtons
from matplotlib import gridspec
import scipy.io as sio
import collections


def fcnProjectLidar (lidar, ang, lim_x_i, lim_x_s, lim_y_i, lim_y_s, theta):
    x_f = []
    y_f = []
    x = [0]*len(lidar)
    y = [0]*len(lidar)

    for i in range(0, len(lidar)):
        if lidar[i] == -1000:
            lidar[i] = 65533
        x=(lidar[i]*math.cos(ang[i]*math.pi/180 + theta))/1000;
        y=(lidar[i]*math.sin(ang[i]*math.pi/180 + theta))/1000;
        if x < lim_x_s and x> lim_x_i and y < lim_y_s and y > lim_y_i:
            x_f.append(x);
            y_f.append(y);

    return x_f, y_f

scan_step = 1

b_plot_lateral_distance = True

# timestamp for LiDAR measurements
p = pTS[exp]
l_ts = list(lidar[exp])
lts = p.lidar_ts_ms
ts = p.timestamp
pc = pTS_configs[exp]
d = datalog[exp]
dl = p.distance_left
dr = p.distance_right
heading = p.heading
el = d.speed_calculation_from_encoder_left_m_s
er = d.speed_calculation_from_encoder_right_m_s

estimated_center = dr - dl - pc['middle_ref_m']
enc_speed= (el + er)/ 2
avg_speed_m_s = np.nanmean(enc_speed)

maxy = 0

# LiDAR measurement angles [degrees]
angle = np.linspace(-45,225,1080, endpoint = False)

index0 = 1
x_raw=[]
y_raw=[]
for scan in range (index0, len(estimated_center)):
    required_ts = lts[scan]
    b_continue = True
    i = 0
    while i < len(l_ts) - 1 and b_continue:
        if required_ts < l_ts[i]:
            scan_number = i
            b_continue = False
        elif required_ts >= l_ts[i] and required_ts < l_ts[i+1]:
            scan_number = i
            b_continue = False
        elif i == len(l_ts) - 2:
            scan_number = len(l_ts) -2
            b_continue = False
        i +=1
    l = lidar[exp][l_ts[scan_number]]
    xf, yf = fcnProjectLidar(l,angle, -pc['LANE_WIDTH'], pc['LANE_WIDTH'], \
                                         pc['lim_y_i'],pc['lim_y_s'], p.heading[scan] )
    E = 0.1
    E0 = 0.06
    xf1 = []
    yf1 = []
    for i in range (0, len(yf)):
        if abs(yf[i]) < E:
            yf1.append(yf[i])
            xf1.append(xf[i])

    xf2 = []
    yf2 = []
    for i in range (0, len(xf1)):
        if abs(xf1[i]) > E0:
            yf2.append(yf1[i])
            xf2.append(xf1[i])
#        xf = [x for x in xf if abs(y) < E]
#        yf = [y for y in yf if abs(y) < E]
#
#        yf = [x for x in xf if abs(x) < E0]
#        xf = [x for x in xf if abs(x) < E0]

    xf2 = np.array(xf2) - pc['middle_ref_m']
    yf2 = np.array(yf2) + avg_speed_m_s*(ts[scan] - ts[0])*pow(10,-3)
    if len(yf2) > 0:
        aux_maxy = max(yf2)
        if aux_maxy > maxy:
            maxy = aux_maxy
    x_raw = np.append(x_raw,xf2)
    y_raw = np.append(y_raw,yf2)

y_robot = avg_speed_m_s*(np.array(ts[1:])-ts[0])*pow(10,-3)

plt.figure(1)
plt.cla()
#plot lateral rows
plt.plot(y_raw-y_raw[0], x_raw,'g*', marker='.', linestyle='None')
#plot estimated position of the robot
plt.plot(y_robot-y_raw[0],-estimated_center[1:],'k',lw=2)
#plot estimated left lateral distance
plt.plot(y_robot-y_raw[0],dl[1:],'r-',lw=2)
#plot estimated right lateral distance
plt.plot(y_robot-y_raw[0],-dr[1:],'r-',lw=2)
ax = plt.gca()
ax.set_aspect('equal', 'datalim')
plt.show()
