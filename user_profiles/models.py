from django.db import models
from shop.models import Telephone
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=256, null=True)
    second_name = models.CharField(max_length=128, null=True)
    telephone = models.OneToOneField(Telephone, null=True, on_delete=models.SET_NULL)
    email = models.EmailField(unique=True)
    has_premium = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.first_name} {self.second_name} {self.email}"
