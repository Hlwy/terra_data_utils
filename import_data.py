# -*- coding: utf-8 -*-

# Clean all variables - comment the next two lines if not using Spyder
#from IPython import get_ipython
#get_ipython().magic('reset -sf')

import pandas as pd
from pathlib import Path
import os
import glob
from collections import OrderedDict
import re #for split
DEBUG = True
IMPORT_LIDAR_MEASUREMENTS = True

exec(open("exp_path.py").read())

# Datalog file names
datafile_name = '*data.txt'
lidar_folder = 'lidar'
system_folder = 'datalog'
cam_right_folder = 'cam_right'
cam_front_folder = 'cam_front'
cam_left_folder = 'cam_left'
data_fn = 'data.txt'
lidar_fn = 'lidar_log'
pretend_lidar_fn = 'pretend_lidar.txt'
pTS_fn = 'perception_lidar_log'
pN_fn = 'perception_log_new'
system_fn = 'system_log'
pJFR_fn = 'perception_jfr'
pP_fn = 'pretend_perception.txt'

exps_dir = []
data = OrderedDict()
datalog = OrderedDict()
lidar = OrderedDict()
pretend_lidar = OrderedDict()
pTS=OrderedDict()
pTS_configs=OrderedDict()
pN=OrderedDict()
pJFR=OrderedDict()
pP=OrderedDict()
camR=OrderedDict()
camF=OrderedDict()
camL=OrderedDict()
camRfp=OrderedDict()
camFfp=OrderedDict()
camLfp=OrderedDict()
name=OrderedDict()


days_dir = [x for x in Path(data_dir).iterdir() if x.is_dir()]
exps_dir = [x for x in Path(data_dir).iterdir() if x.is_dir()]
#for day in iter(days_dir):
#    for exp in day.iterdir():
#        if DEBUG:
#            print(exp)
#        exps_dir.append(exp)
#exps_dir.sort()
for exp in iter(exps_dir):
    # for files directly inside an exp folder
    filepath = glob.glob(os.path.join(str(exp), datafile_name))
    aux_file = os.path.join(str(exp),'name.txt')
    if os.path.isfile(aux_file):
        fp = open(str(aux_file),'r')
        line = fp.readline()
        fp.close()
        print('\nNAME.TXT: ' + aux_file + '\t' + line)
        name[os.path.basename(str(exp))] = line
    ## for files inside folders in an exp folder
    for sub in exp.iterdir():
        if DEBUG:
            print("\tsub: " + str(sub) + " lidar: " + os.path.basename(str(sub)) )
        if(os.path.basename(str(sub)) == cam_front_folder):
            print('cam_front: ' + str(sub))
            cam_front_fn = os.listdir(str(sub))
            aux_fp = os.path.join(str(sub),cam_front_fn[0]);
            cam_front_video_fp = os.path.join(str(sub),cam_front_fn[1]);
            try:
                dnames=['capture_time_ms',
                        'capture_period_ms',
                        'capture_latency_ms',
                        'process_latency_ms',
                        'stream_latency_ms',
                        'record_latency_ms'];
                df = pd.read_csv(aux_fp,sep=",",skiprows=1,names=dnames)
                camF[os.path.basename(str(exp))] = df
                camFfp[os.path.basename(str(exp))] = os.path.join(str(sub),cam_front_fn[1]);
                del dnames
            except:
                print("Cam Right empty file?")

        if(os.path.basename(str(sub)) == cam_right_folder):
            print('cam_right: ' + str(sub))
            cam_right_fn = os.listdir(str(sub))
            aux_fp = os.path.join(str(sub),cam_right_fn[0]);
            cam_right_video_fp = os.path.join(str(sub),cam_right_fn[1]);
            try:
                dnames=['capture_time_ms',
                        'capture_period_ms',
                        'capture_latency_ms',
                        'process_latency_ms',
                        'stream_latency_ms',
                        'record_latency_ms'];
                df = pd.read_csv(aux_fp,sep=",",skiprows=1,names=dnames)
                camR[os.path.basename(str(exp))] = df
                camRfp[os.path.basename(str(exp))] = os.path.join(str(sub),cam_right_fn[1]);
                del dnames
            except:
                print("Cam Right empty file?")

        if(os.path.basename(str(sub)) == cam_left_folder):
            print('cam_left: ' + str(sub))
            cam_left_fn = os.listdir(str(sub))
            aux_fp = os.path.join(str(sub),cam_left_fn[0]);
            cam_left_video_fp = os.path.join(str(sub),cam_left_fn[1]);
            try:
                dnames=['capture_time_ms',
                        'capture_period_ms',
                        'capture_latency_ms',
                        'process_latency_ms',
                        'stream_latency_ms',
                        'record_latency_ms'];
                df = pd.read_csv(aux_fp,sep=",",skiprows=1,names=dnames)
                camL[os.path.basename(str(exp))] = df
                camLfp[os.path.basename(str(exp))] = os.path.join(str(sub),cam_left_fn[1]);
                del dnames
            except:
                print("Cam left empty file?")

        if(os.path.basename(str(sub)) == system_folder):
            # Parsing system_log files
            sys_fp = os.path.join(str(sub), system_fn)
            if os.path.isfile(sys_fp):
                print('datalog')
                try:
                    dnames = ["linux_time_ms",
                              "uptime_ms",
                              "drive_mode",
                              "mpc_step_counter",
                              "mpc_origin_latitude",
                              "mpc_origin_longitude__deg",
                              "closest_trajectory_point_index_to_robot",
                              "mpc_error_x_W_E_m",
                              "mpc_error_y_W_E_m",
                              "abs_mpc_error_m",
                              "input_x_for_mhe_m",
                              "input_y_for_mhe_m",
                              "input_speed_for_mhe_m_s",
                              "input_vyaw_for_mhe_rad_s",
                              "mhe_output_x_m",
                              "mhe_output_y_m",
                              "mhe_output_speed_m_s",
                              "mhe_output_yaw_rad",
                              "mpc_reference_heading_rad",
                              "mpc_turn_rate_command_rad_s",
                              "turn_rate_command_as_PWM",
                              "throttle_command_as_PWM",
                              "primary_gps_latitude_deg",
                              "primary_gps_longitude_deg",
                              "secondary_gps_latitude_deg",
                              "secondary_gps_longitude_deg",
                              "accelerometer_x_m_s2",
                              "accelerometer_y_m_s2",
                              "accelerometer_z_m_s2",
                              "gyro_yaw_rate_rad_s",
                              "gyro_pitch_rate_rad_s",
                              "gyro_roll_rate_rad_s",
                              "yaw_rad",
                              "pitch_rad",
                              "roll_rad",
                              "sonar1_measurement_m",
                              "ultrasonic_sensor_measurement_m",
                              "primary_gps_time_s",
                              "normalized_turn_rate_command",
                              "normalized_throttle_command",
                              "speed_calculation_from_encoder_left_m_s",
                              "speed_calculation_from_encoder_right_m_s",
                              "front_gimbal_target_angle_degrees_from_straight_down",
                              "left_gimbal_target_angle_degrees_from_straight_down",
                              "right_gimbal_target_angle_degrees_from_straight_down",
                              "front_gimbal_measured_angle_degrees_from_straight_down",
                              "left_gimbal_measured_angle_degrees_from_straight_down",
                              "right_gimbal_measured_angle_degrees_from_straight_down",
                              "internal_temperature_C",
                              "battery_voltage_V",
                              "primary_gps_type",
                              "secondary_gps_type",
                              "MPC_R_value",
                              "MPC_Q0_value",
                              "aux","aux2","aux3","aux4","aux5"];
                    df = pd.read_csv(sys_fp,sep=",",skiprows=2,names=dnames)
                    datalog[os.path.basename(str(exp))] = df
                    del dnames
                except:
                    print("Empty file?")

        if(os.path.basename(str(sub)) == lidar_folder):
            if IMPORT_LIDAR_MEASUREMENTS:
                aux_fp = os.path.join(str(sub), lidar_fn);
                print(aux_fp)
                if os.path.isfile(aux_fp) == False:
                    aux_fp = os.path.normpath(str(aux_fp)+'.txt');
                # Parsing lidar measurements
                try:
                    lidar_fp = aux_fp
                    df = pd.read_csv(lidar_fp, header=None, sep=",")
                    print(df.shape)
                    if df.shape[1] <= 1082:
                        ts = df[0]
                        lm = df.loc[:,1:1080].values.tolist()
                    elif df.shape[1] == 1083:
                        print("Used this...")
                        ldf = df
                        ts = df[2]
                        lm = df.loc[:,3:1083].values.tolist()
                    else:
                        print("Check lidar column size")

                    print("\nsize ts: " + str(len(ts)) + "\tlm: " + str(len(lm)) + "/" + str(len(lm[0])))
                    lidar[os.path.basename(str(exp))] = OrderedDict(zip(ts,lm))
                    print(len(lidar[os.path.basename(str(exp))]))
                except:
                    print("Empty file?" + str(sub))
                # Parsing pretend lidar measurements
                try:
                    lidar_fp = os.path.join(str(sub), pretend_lidar_fn);
                    df = pd.read_csv(lidar_fp, header=None, sep=",")
                    print(df.shape)
                    if df.shape[1] <= 1082:
                        ts = df[0]
                        lm = df.loc[:,1:1080].values.tolist()
                    elif df.shape[1] == 1083:
                        print("Used this...")
                        ldf = df
                        ts = df[2]
                        lm = df.loc[:,3:1083].values.tolist()
                    else:
                        print("Check lidar column size")

                    print("\nsize ts: " + str(len(ts)) + "\tlm: " + str(len(lm)) + "/" + str(len(lm[0])))
                    pretend_lidar[os.path.basename(str(exp))] = OrderedDict(zip(ts,lm))
                    print(len(lidar[os.path.basename(str(exp))]))
                except:
                    print("Empty file(pretend_lidar)?" + str(sub))
            else:
                print('IMPORT_LIDAR_MEASUREMENTS DISABLED')

            # Parsing variables saved as 'data.txt' files
            data_fp = os.path.join(str(sub), data_fn)
            if os.path.isfile(data_fp):
                try:
                    df = pd.read_table(data_fp,  sep=",")
                    data[os.path.basename(str(exp))] = df
                except:
                    print("Empty file?")

            # Parsing perception lidar variables saved as 'perception_lidar_log' files [TS### standard]
            pTS_fp = os.path.join(str(sub), pTS_fn)
            if os.path.isfile(pTS_fp) == 0:
                pTS_fp = os.path.normpath(str(pTS_fp)+'.txt');
            try:
                aux = {}
                f = open(pTS_fp)
                lines = f.readlines()
                a = re.split(',|\n',lines[0])
                for i in range(0, len(a)-1,2):
                    aux[a[i]] = float(a[i+1])
                pTS_configs[os.path.basename(str(exp))] = aux
                df = pd.read_table(pTS_fp,  sep=",", header=1)
                pTS[os.path.basename(str(exp))] = df
            except:
                print("Empty file?" + str(pTS_fp))

            # Parsing variables saved as 'perception_log_new' files
            pJFR_fp = os.path.join(str(sub), pJFR_fn)
            if os.path.isfile(pJFR_fp):
                try:
                    df = pd.read_table(pJFR_fp,  sep=",", header=0)
                    pJFR[os.path.basename(str(exp))] = df
                    print(str(pJFR_fp))
                except:
                    print("Empty file?")

            # Parsing variables saved as 'perception_log_new' files
            pN_fp = os.path.join(str(sub), pN_fn)
            if os.path.isfile(pN_fp):
                try:
                    df = pd.read_table(pN_fp,  sep=",", header=1)
                    pN[os.path.basename(str(exp))] = df
                    print(str(pN_fp))
                except:
                    print("Empty file?")

            # Parsing variables saved as 'perception_log_new' files
            pP_fp = os.path.join(str(sub), pP_fn)
            if os.path.isfile(pP_fp):
                try:
                    df = pd.read_table(pP_fp,  sep=",", header=1)
                    pP[os.path.basename(str(exp))] = df
                    print(str(pP_fp))
                except:
                    print("Empty file?")
            if DEBUG:
                #print("\t\tlidar sub: " + str(sub) + "\t\t\tlidar_fp: " + str(lidar_fp))
                print("\t\t\tdata_fp: " + str(data_fp))
                print("\t\t\tperception1_fp: " + str(pTS_fp))
                print("\t\t\tperception1_fp: " + str(pN_fp))

#
#if 'lm' in dir():
    #del lm,ts,lidar_fp
#del data_dir, data_fn,data_fp,datafile_name,filepath,lidar_fn,lidar_folder,pTS_fp, pTS_fn, pN_fn, pN_fp

if 'exp' is not locals():
#    exps = list(datalog)
    exps = list(pTS)
    exp = exps[-1]
