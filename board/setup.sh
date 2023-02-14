#! /bin/bash
apt update
apt install python3-picamera
apt install build-essential cmake pkg-config
apt install libx11-dev libatlas-base-dev
apt install libgtk-3-dev libboost-python-dev
apt install espeak


echo "Next command may take few minutes to finish"
pip install dlib

wget http://dlib.net/files/shape_predictor_5_face_landmarks.dat.bz2
bunzip2 shape_predictor_5_face_landmarks.dat.bz2

wget http://dlib.net/files/dlib_face_recognition_resnet_model_v1.dat.bz2
bunzip2 dlib_face_recognition_resnet_model_v1.dat.bz2

mkdir samples

