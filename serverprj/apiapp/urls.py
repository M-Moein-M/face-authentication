from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import VerificationCheck, NewFaceRegister

urlpatterns = [
    path('api', VerificationCheck.as_view()),
    path('face', NewFaceRegister.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
