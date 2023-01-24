import sys
import os
import dlib
import glob
import numpy as np

import requests

from picamera import PiCamera
from time import sleep

SERVER_PERMISSION_CHECK_URL = 'http://192.168.1.105:8000/api'

root_dir = '/home/beorn/board/'
predictor_path = root_dir + 'shape_predictor_5_face_landmarks.dat'
face_rec_model_path = root_dir + 'dlib_face_recognition_resnet_model_v1.dat'
faces_folder_path = root_dir + 'samples'
img_path = os.path.join(faces_folder_path, "captured.jpg")

# Load all the models we need: a detector to find the faces, a shape predictor
# to find face landmarks so we can precisely localize the face, and finally the
# face recognition model.
detector = dlib.get_frontal_face_detector()
sp = dlib.shape_predictor(predictor_path)
facerec = dlib.face_recognition_model_v1(face_rec_model_path)


def process_img():
    # Now process captured image
    img_path = os.path.join(faces_folder_path, "captured.jpg")
    print("Processing file: {}".format(img_path))
    img = dlib.load_rgb_image(img_path)

    dets = detector(img, 1)
    print("Number of faces detected: {}".format(len(dets)))

    # Now process each face we found.
    for k, d in enumerate(dets):
        print("Detection {}: Left: {} Top: {} Right: {} Bottom: {}".format(
            k, d.left(), d.top(), d.right(), d.bottom()))
        # Get the landmarks/parts for the face in box d.
        shape = sp(img, d)

        # Compute the 128D vector that describes the face in img identified by
        # shape.  In general, if two face descriptor vectors have a Euclidean
        # distance between them less than 0.6 then they are from the same
        # person, otherwise they are from different people. Here we just print
        # the vector to the screen.
        face_descriptor = facerec.compute_face_descriptor(img, shape)

        v = np.array(face_descriptor)
        return v


def has_permission(feat):
    """
    Check with server whether <feat> is one one the registered faces
    """
    DEVICE_ID = "RASPI_MAIN_DEVICE"
    print("Sinding features to server")
    data = {'feat': feat, 'device': DEVICE_ID}
    r = requests.post(SERVER_PERMISSION_CHECK_URL, data)
    if (str(r.status_code)).startswith('5'):
        print("Server Error")
    else:
        print(r.json())
        print(r.status_code)


camera = PiCamera()

while True:
    # camera.capture(img_path)
    feat = process_img()
    
    if feat is None:
        # no faces detected
        continue


    print('checking permission...')
    has_permission(feat)

    input("press Enter to capture an image")

