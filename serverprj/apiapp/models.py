from django.db import models


class Verified(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    feat = models.BinaryField(max_length=8000)

    # to specify access for specific device
    device = models.CharField(
        max_length=100,
        default="maindevice_DkCZVCJpTUYTfoHchNWP")


class Log(models.Model):
    LOGING_TYPE = "Login"
    type = models.CharField(max_length=200)
    verified = models.OneToOneField(
        Verified,
        on_delete=models.CASCADE,
        primary_key=True
    )
    created = models.DateTimeField(auto_now_add=True)
