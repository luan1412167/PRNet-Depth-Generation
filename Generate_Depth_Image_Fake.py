import numpy as np
import scipy.io as sio
from skimage.io import imread, imsave
import cv2
import os

from api import PRN
import utils.depth_image as DepthImage
import glob
import time
os.environ['CUDA_VISIBLE_DEVICES'] = '0'

live_path = "/home/dmp/PRNet-Depth-Generation/val/live"
live_depth_path = "/home/dmp/PRNet-Depth-Generation/val/live_depth"
fake_path = "/home/dmp/PRNet-Depth-Generation/val/fake"

prn = PRN(is_dlib = False, is_opencv = False) 

img_path = "/home/dmp/Videos/val/fake"
video_paths = glob.glob(img_path + "/*")
videos = []
for video_path in video_paths:
    print(video_path)
    if video_path in videos:
        continue
    cap = cv2.VideoCapture(video_path)
    frame_number = 0
    while cap.isOpened():
        if frame_number%8!=0:
            frame_number+=1
            continue
        ret, image = cap.read()
        if not ret:
            break 
        image_shape = [image.shape[0], image.shape[1]]
        try:
            pos, bbox = prn.process(image, None, None, image_shape)
            if bbox is None:
                continue
            # kpt = prn.get_landmarks(pos)
            x1 = max(bbox[0][0] - 32, 0)
            y1 = max(bbox[0][1] - 32, 0)
            x2 = min(bbox[0][2] + 32, image_shape[1])
            y2 = min(bbox[0][3] + 32, image_shape[0])

            # 3D vertices
            # vertices = prn.get_vertices(pos)
            name = str(round(time.time() * 1000)) + "-" + str(frame_number) 
            face_name = name + ".bmp"
            # depth_name = name + ".jpg"
            # depth_scene_map = DepthImage.generate_depth_image(vertices, kpt, image.shape, isMedFilter=True)
            face = image[y1:y2, x1:x2]
            # depth = depth_scene_map[y1:y2, x1:x2]
            face = cv2.resize(face, (128, 128))
            # depth = cv2.resize(depth, (256, 256))
            # cv2.imshow('image', image)
            # cv2.imshow('face', face)
            # cv2.imshow('DEPTH', depth)

            cv2.imwrite(fake_path + "/" + face_name, face)
            # cv2.imwrite(live_depth_path + "/" + depth_name, depth)
        except:
            ...
        frame_number += 1
        # cv2.waitKey(1)
