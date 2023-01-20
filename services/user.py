from django.contrib.auth.models import User
from django.core.exceptions import MultipleObjectsReturned


def get_name_by_id(id):
    try:
        user = User.objects.get(id=id)
    except User.DoesNotExist or MultipleObjectsReturned:
        raise
    else:
        name = f"{user.first_name} {user.last_name}"
    return name
