from dateutil.tz import tzlocal
from datetime import *


def get_current_datetime_with_tz(secs):
    current_date = datetime.fromtimestamp(secs)
    local_tz = tzlocal()
    current_date = current_date.replace(tzinfo=local_tz)
    current_date = current_date.astimezone(local_tz)
    return current_date
