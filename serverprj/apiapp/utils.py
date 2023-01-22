import numpy as np
from apiapp.models import Verified


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
