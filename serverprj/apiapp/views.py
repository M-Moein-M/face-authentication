from .models import Verified
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class VerificationCheck(APIView):
    """
    check validity of the device and feature
    """
    def post(self, request, format=None):
        print(request.data)
        print('- '*20)
        return Response([], status=status.HTTP_200_OK)
