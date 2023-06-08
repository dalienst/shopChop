from django.db import models
from django.contrib.auth.models import User

class Userprofile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="userprofile")
    is_vendor = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.user.username