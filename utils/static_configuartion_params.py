# -*- coding: utf-8 -*-

## Specify the experiment you want to plot

# If collection's lidar_log is located at /home/user/Data/collection###/lidar,
# then use data_dir = /home/user/Data

data_dir = 'PlotData'
root_dir = 'experiments'

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




cam_log_headers=['capture_time_ms',
		'capture_period_ms',
		'capture_latency_ms',
		'process_latency_ms',
		'stream_latency_ms',
		'record_latency_ms'];


sys_log_headers = ["linux_time_ms",
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
