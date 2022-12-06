from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.http import HttpResponse
from django.views import View
from django.http import HttpResponseRedirect
from django.shortcuts import render

from django.core.files.storage import FileSystemStorage


class VerificationCheck(APIView):
    """
    check validity of the device and feature
    """

    def post(self, request, format=None):
        print(request.data)
        print('- ' * 20)
        return Response({"hasperm": "yes"}, status=status.HTTP_200_OK)


class NewFaceRegister(View):

    def post(self, request, *args, **kwargs):
        if request.FILES['facefile']:
            upload = request.FILES['facefile']
            self.register_uploaded_face(upload, request.POST.get("secrete"))



            return HttpResponseRedirect('/face')
        else:
            return HttpResponse("ERROR")

    def get(self, request):
        return render(request, 'new_face_register.html')

    def register_uploaded_face(self, upload, secrete):
        """ Extract new features and save new record in databse """
        file_name = "new_face.jpg"
        fss = FileSystemStorage()
        fss.save(file_name, upload)
