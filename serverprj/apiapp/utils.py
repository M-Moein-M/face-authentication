import numpy as np
import os
from apiapp.models import Verified, Log
from notificationapi_python_server_sdk import (notificationapi)
import datetime
from django.contrib.auth.models import User
from django.utils import timezone


THRESHOLD = .6


def match(posted, device):
    """ checks the posted feat with all the records in db
        :returns corresponding row of the match or None
    """
    for row in Verified.objects.filter(device=device):
        reg = np.frombuffer(row.feat, dtype=np.float64)
        norm = np.linalg.norm(reg - posted)
        if norm < THRESHOLD:
            return row
    return None


def log_login(user):
    """ insert new Log model entry """
    log = Log(verified=user, type=Log.LOGING_TYPE, created=timezone.now())
    log.save()


def notify_login(user):
    """ send emails to user and admins registered """
    log_login(user)
    info = {"name": user.name,
            "email": user.email,
            "time": str(datetime.datetime.now()),
            "device": user.device}
    send_login_email(info)

    for admin in User.objects.filter(is_superuser=True):
        info.update({"email": admin.email})
        send_login_email(info)

    info.update({"email": user.email})


def send_login_email(info):
    """ sends an email to <email> """
    notificationapi.init(str(os.getenv("NOTIF_CLIENT_ID")), str(os.getenv("NOTIF_CLIENT_SEC")))
    notificationapi.send(
        {
            "notificationId": str(os.getenv("NOTIF_LOGIN_ID")),
            "user": {"id": "1000", "email": info["email"]},
            "mergeTags": {"name": info["name"],
                          "email": info["email"],
                          "time": str(datetime.datetime.now()),
                          "device": info["device"]},
        }
    )
