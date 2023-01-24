import os

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.http import HttpResponse
from django.views import View
from django.http import HttpResponseRedirect
from django.shortcuts import render

from django.core.files.storage import FileSystemStorage

from apiapp.models import Verified

import apiapp.utils as utils

import dlib
import numpy as np


class VerificationCheck(APIView):
    """
    check validity of the device and feature
    """

    def post(self, request, format=None):
        posted = np.array(request.data.getlist("feat")).astype(np.float64)
        print(posted)
        print('- ' * 20)

        user = utils.match(posted.astype(np.float64), request.data.get("device"))
        if not user:
            return Response({"hasperm": "no"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            utils.notify_login(user)
            return Response({"hasperm": "yes", "name": user.name},
                            status=status.HTTP_200_OK)


class NewFaceRegister(View):

    def post(self, request, *args, **kwargs):
        if request.FILES['facefile'] and request.POST.get("secrete") == str(os.getenv("FACE_REG_SEC")):

            self.register_uploaded_face(request)
            return HttpResponseRedirect('/face')
        else:
            return HttpResponse("ERROR")

    def get(self, request):
        return render(request, 'new_face_register.html')

    def register_uploaded_face(self, request):
        """ Extract new features and save new record in databse """
        upload = request.FILES['facefile']
        file_name = "new_face.jpg"
        fss = FileSystemStorage()
        fss.delete(file_name)
        fss.save(file_name, upload)

        feat = self.get_feature(fss.path(file_name))
        if feat is None:
            print("No faces detected")
            return

        print(feat.dtype)

        rec = Verified(
            name=request.POST.get("name"),
            email=request.POST.get("email"),
            device=request.POST.get("device"),
            feat=feat.tobytes()
        )
        rec.save()

        print(feat)
        fss.delete(file_name)

    @staticmethod
    def get_feature(p):
        fss = FileSystemStorage()

        detector = dlib.get_frontal_face_detector()
        sp = dlib.shape_predictor(fss.path('shape_predictor_5_face_landmarks.dat'))
        facerec = dlib.face_recognition_model_v1(fss.path('dlib_face_recognition_resnet_model_v1.dat'))
        # Now process captured image
        img_path = p
        print("Processing file: {}".format(img_path))
        img = dlib.load_rgb_image(img_path)

        dets = detector(img, 1)
        print("Number of faces detected: {}".format(len(dets)))

        # Now process each face we found.
        for k, d in enumerate(dets):
            # Get the landmarks/parts for the face in box d.
            shape = sp(img, d)

            # Compute the 128D vector
            face_descriptor = facerec.compute_face_descriptor(img, shape)
            v = np.array(face_descriptor)
            return v.astype(np.float64)
