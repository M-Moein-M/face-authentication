import time
import sys
import os
import dlib
import glob
import numpy as np
from subprocess import call

import requests

from picamera import PiCamera
from time import sleep

SERVER_PERMISSION_CHECK_URL = 'http://192.168.1.106:8000/api'

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
    data = {'feat': feat, 'device': DEVICE_ID}
    print("Sending request")
    print(data)
    r = requests.post(SERVER_PERMISSION_CHECK_URL, data)
    if (str(r.status_code)).startswith('5'):
        print("Server Error")
    else:
        print("Response received")
        print(r.json())
        print(r.status_code)
        if r.status_code == 200:
            grant_access(r)
        if r.status_code == 401:
            deny_access(r)


def deny_access(req):
    """ handles access denial routine """
    msg = "Access denied"
    speak(msg)


def grant_access(req):
    """ handles access grant routine """
    msg = "Access granted"
    speak(msg)


def speak(msg):
    """ outputs the msg using espeak command"""
    call([f'espeak -g 50 "{msg}" 2>/dev/null'], shell=True)
    print(msg)


camera = PiCamera()

while True:
    to = 15
    print(f"Pausing face detection for {to} seconds")
    time.sleep(to)

    print("Capturing new image")
    camera.capture(img_path)
    feat = process_img()
    
    if feat is None:
        # no faces detected
        print("No faces detected")
        print("Resuming face detection")
        continue

    print("Features extracted. Requesting authentication check")
    has_permission(feat)

