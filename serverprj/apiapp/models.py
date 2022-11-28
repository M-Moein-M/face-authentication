from django.db import models


class Verified(models.Model):
    name = models.CharField(max_length=100)
    feat = models.BinaryField(max_length=1000)

    # to specify access for specific device
    device = models.CharField(
        max_length=1000,
        default="maindevice_DkCZVCJpTUYTfoHchNWP")
