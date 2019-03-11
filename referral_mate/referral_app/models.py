from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(null=True, blank=True, max_length=32)
    last_name = models.CharField(null=True, blank=True, max_length=32)
    city = models.CharField(null=True, blank=True, max_length=32)

    def __str__(self):
        return f'{self.user.username}'
