import numpy as np
import os
from apiapp.models import Verified
from notificationapi_python_server_sdk import (notificationapi)
import datetime
from django.contrib.auth.models import User


THRESHOLD = .6


def match(posted):
    """ checks the posted feat with all the records in db
        :returns corresponding row of the match or None
    """
    for row in Verified.objects.all():
        reg = np.frombuffer(row.feat, dtype=np.float64)
        print(row.email)
        print(reg.shape, posted.shape)
        norm = np.linalg.norm(reg - posted)
        if norm < THRESHOLD:
            return row

    return None


def notify_login(user):
    """ send emails to user and admins registered """
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
