import pedx.utils as utils
import pedx.data_loader as dl
from Visualization import *
from pprint import pprint

import cv2
import numpy as np
import json
import glob

camera_names = dl.list_all_camera_names()
camera_pairs = dl.list_all_camera_pairs()
capture_dates = dl.list_all_capture_dates()
capture_date = capture_dates[1]

frame_id = '0000055'

camera_name = camera_names[1]
basedir = '/home/feberhardt/Dokumente/data'
calib_filepath = basedir + '/calib/calib/' + 'calib_cam_to_cam_ylw79D0-red707B.txt'

# load calibration
calibration = utils.read_calib_file(calib_filepath)
# pprint(calibration['K_01'])


### load lidar data
# nd.array(366003,3)
# pointcloud = dl.load_a_pointcloud(basedir, capture_date, frame_id)

dir_labels_2d = '/home/feberhardt/Dokumente/data/labels/2d/20171207T2024/'
dir_labels_3d = '/home/feberhardt/Dokumente/data/labels/3d/segment/20171207T2024/'

import os, sys

categories = []
liste = os.listdir(dir_labels_2d)

annotations = {}

for fn in liste:
    with open(dir_labels_2d + fn) as f2:
        labels_2d = json.load(f2)
        keypoint_dict = labels_2d['keypoint']
        frame_id = [labels_2d['frame_id']]
        break

# also stored at misc.visualization
pedx_keys = ['reye', 'head', 'lknee', 'neck', 'rwri', 'lwri', 'rknee', 'lelb', 'lsho', 'rhip', 'leye', 'lankl', 'lhip',
             'mouth', 'nose', 'rankl', 'relb', 'rsho']

# differences pedx: mouth, head, neck; coco ears
coco_keys = ["nose", "left_eye", "right_eye", "left_ear", "right_ear", "left_shoulder", "right_shoulder", "left_elbow",
             "right_elbow", "left_wrist", "right_wrist", "left_hip", "right_hip", "left_knee", "right_knee",
             "left_ankle", "right_ankle"]
# 2 times mout instead of ears
pedx_keys_reordered = ['nose', 'leye', 'reye', 'mouth', 'mouth', 'lsho', 'rsho', 'lelb', 'relb', 'lwri', 'rwri', 'lhip',
                       'rhip', 'lknee', 'rknee', 'lankl', 'rankl']



gt_anntotations = {}

path = os.path.join(basedir, 'labels/2d', capture_date, f'{capture_date}_{camera_name}_*.json')
filenames = glob.glob(os.path.join(path))
all_frame_ids = set(sorted([fn.split('_')[-2] for fn in filenames]))
all_tracking_ids = set(sorted([fn.split('_')[-1].strip('.json') for fn in filenames]))

for capture_date in capture_dates:  # ['20171130T2000', '20171207T2024', '20171212T2030']
    if capture_date != '20171207T2024': continue
    gt_anntotations[capture_date] = {}
    for camera_name in camera_names:  # ['ylw79D0', 'red707B', 'blu79CF', 'grn43E3']
        gt_anntotations[capture_date][camera_name] = {}
        frame_ids = set(sorted([fn.split('_')[-2] for fn in filenames]))
        for frame_id in frame_ids:
            gt_anntotations[capture_date][camera_name][str(frame_id)] = {}

            # todo only tracking ids that are actually present in this frame
            path = os.path.join(basedir, 'labels/2d', capture_date, f'{capture_date}_{camera_name}_{frame_id}_*.json')
            filenames_tracking = glob.glob(os.path.join(path))
            tracking_ids = set(sorted([fn.split('_')[-1].strip('.json') for fn in filenames_tracking]))
            for tracking_id in tracking_ids:
                # fn = os.path.join(basedir, 'labels/2d', capture_date, camera_name,
                #              f'{capture_date}_{camera_name}_{frame_id}_{tracking_id}.json')
                fn = f'{capture_date}_{camera_name}_{frame_id}_{tracking_id}.json'
                with open(dir_labels_2d + fn) as f2:
                    labels_2d = json.load(f2)
                gt_anntotations[capture_date][camera_name][str(frame_id)][str(tracking_id)] = labels_2d


image_dir = '/home/feberhardt/Dokumente/data/images/20171207T2024/ylw79D0/' + '20171207T2024_ylw79D0_0000090.jpg'
image = cv2.imread(image_dir)

labels_img = gt_anntotations['20171207T2024']['ylw79D0']['0000090']

for tracking_id in labels_img.keys():
    print(tracking_id)
    keypoint_dict = labels_img[tracking_id]['keypoint']
    print(labels_img[tracking_id]['category'])
    kepts = get_gt_keypoints(keypoint_dict, pedx_keys_reordered)
    image = draw_keypoints(image, kepts)
    skeleton = joints_dict()["coco"]['skeleton']
    confidence_threshold = 0.5
    image = draw_skeleton(image, kepts, skeleton, confidence_threshold=0.5)

cv2.imwrite('Annotations_test3.jpg', image)

# todo collect labels for all instances in image
# todo handle pointclouds


# keys = 'category', 'polygon', 'camera_name', 'capture_date', 'frame_id', 'keypoint', 'tracking_id'

# dl.load_a_pointcloud()
## _3d + '20171207T2024_0000055_14e122a6ca5f4c889fa3d76d2549e18a.ply') as f3:
#   labels_3d = json.load(f3)
