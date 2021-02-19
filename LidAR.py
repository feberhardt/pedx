import pedx.utils as utils
import pedx.data_loader as dl
from Visualization import *
from pprint import pprint
from plyfile import PlyData, PlyElement  ## ply = polygon file
import open3d as o3d
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.colors as mcolors
import os, sys
import cv2
import numpy as np
import json
import glob

dir_labels_2d = '/home/feberhardt/Dokumente/data/labels/2d/20171207T2024/'
dir_labels_3d = '/home/feberhardt/Dokumente/data/labels/3d/segment/20171207T2024/'

capture_date = '20171207T2024'
tracking_id = '15d1ab9781b84825b03a9cf713f52ed5'
frame_id = 55
basedir = '/home/feberhardt/Dokumente/data'
calibration = utils.read_calib_file('/home/feberhardt/Dokumente/data/calib/calib/calib_cam_to_cam_ylw79D0-red707B.txt')

# # load lidar data (nd.array(366003,3)), Read .ply file
# dir_input = '/home/feberhardt/Dokumente/data/pointclouds/'
#
# # Load Input pointcloud of whole scene
# input_file = '/home/feberhardt/Dokumente/data/pointclouds/20171207T2024/20171207T2024_0000059.ply'
# pcd = o3d.io.read_point_cloud(input_file)  # Read the point cloud
#
# # Visualize the point cloud within open3d
# # o3d.visualization.draw_geometries([pcd])
#
# point_cloud_in_numpy = np.asarray(pcd.points)  # shape (366268, 3)
# # print(point_cloud_in_numpy.shape)
#
# # load labels of pedestrian
# input_file = '/home/feberhardt/Dokumente/data/labels/3d/segment/20171207T2024/20171207T2024_0000055_15d1ab9781b84825b03a9cf713f52ed5.ply'
# pcd = o3d.io.read_point_cloud(input_file)  # Read the point cloud
#
# # Visualize the point cloud within open3d
# # o3d.visualization.draw_geometries([pcd])
#
# labels_3d = os.listdir(dir_labels_3d)
#
# bbox_3d_list = []

# for label_ply in labels_3d:
#     input_file = dir_labels_3d + label_ply
#     pcd = o3d.io.read_point_cloud(input_file)  # Read the point cloud
#     # Visualize the point cloud within open3d
#     # o3d.visualization.draw_geometries([pcd])
#     point_cloud_in_numpy = np.asarray(pcd.points)  # shape (var, 3)
#     # print(np.mean(point_cloud_in_numpy, 0), np.std(point_cloud_in_numpy, 0))
#     bbox3d = [(np.max(point_cloud_in_numpy[:, 0]), np.max(point_cloud_in_numpy[:, 1]),
#                np.max(point_cloud_in_numpy[:, 2])),
#               (np.min(point_cloud_in_numpy[:, 0]), np.min(point_cloud_in_numpy[:, 1]),
#                np.min(point_cloud_in_numpy[:, 2]))]
#     print(bbox3d)


capture_dates = ['20171130T2000', '20171207T2024', '20171212T2030']
capture_date = capture_dates[1]

path = os.path.join('/home/feberhardt/Dokumente/data/labels/3d/segment', capture_date, f'{capture_date}_*.ply')
# path = '/home/feberhardt/Dokumente/data/labels/3d/segment/20171207T2024/20171207T2024_*.ply'
filenames = glob.glob(path)
all_frame_ids = [fn.split('_')[-2] for fn in filenames]
all_tracking_ids = [fn.split('_')[-1].strip('.ply') for fn in filenames]
gt_anntotations = {}

for capture_date in capture_dates:  # ['20171130T2000', '20171207T2024', '20171212T2030']
    if capture_date != '20171207T2024': continue
    gt_anntotations[capture_date] = {}
    frame_ids = set(sorted([fn.split('_')[-2] for fn in filenames]))
    for frame_id in frame_ids:
        gt_anntotations[capture_date][str(frame_id)] = {}
        # path = os.path.join(basedir, 'labels/3d', capture_date, f'{capture_date}_{frame_id}_*.ply')
        path = os.path.join('/home/feberhardt/Dokumente/data/labels/3d/segment', capture_date,
                            f'{capture_date}_{frame_id}_*.ply')
        filenames_tracking = glob.glob(path)
        tracking_ids = set(sorted([fn.split('_')[-1].strip('.ply') for fn in filenames_tracking]))
        for tracking_id in tracking_ids:
            fn = os.path.join('/home/feberhardt/Dokumente/data/labels/3d/segment', capture_date,
                              f'{capture_date}_{frame_id}_{tracking_id}.ply')
            pcd = o3d.io.read_point_cloud(fn)
            labels_3d = np.asarray(pcd.points)
            gt_anntotations[capture_date][str(frame_id)][str(tracking_id)] = labels_3d

# print(gt_anntotations)

# unique ids
t_ids = np.array(all_tracking_ids)
t_ids = np.unique(t_ids)
f_ids = np.sort(np.unique(np.array(all_frame_ids)))
# print(t_ids)
# print(f_ids)
capture_date = '20171207T2024'

track_dict = {}

# associate a certain color with Ids
from random import random

print(tuple(np.random.randint(0, 255, 3)))
col = list(mcolors.BASE_COLORS.values())
colors = {}
for i, t_id in enumerate(t_ids):
    colors[t_id] = col[i]



sys.exit()

mode = '2d'

# 2d
if mode == '2d':
    for k, f_id in enumerate(f_ids):
        existing_ids = gt_anntotations[capture_date][f_id].keys()
        if k != 0: plt.cla()
        for i, track_id in enumerate(existing_ids):
            xyz = gt_anntotations[capture_date][f_id][track_id]
            x, y, z = xyz[:, 0], xyz[:, 1], xyz[:, 2]  # birdview; for our case z=y
            print(colors[track_id])
            plt.scatter(y, abs(x), c=colors[track_id])

        plt.xlim(-30, 30)
        plt.ylim(0, 65)
        # plt.axis('equal')
        plt.show(block=False)
        plt.pause(0.5)

elif mode == '3d': # todo implement axis scale
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    for k, f_id in enumerate(f_ids):
        existing_ids = gt_anntotations[capture_date][f_id].keys()
        # xyz = np.zeros((len(existing_ids), 3))
        if k != 0: plt.cla()
        for i, track_id in enumerate(existing_ids):
            xyz = gt_anntotations[capture_date][f_id][track_id]
            x, y, z = xyz[:, 0], xyz[:, 1], xyz[:, 2]
            plt.scatter(z, x, y)
            plt.axis('equal')
        plt.show(block=False)
        plt.pause(0.5)
