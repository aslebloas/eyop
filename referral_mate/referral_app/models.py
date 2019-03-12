from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(null=True, blank=True, max_length=32)
    last_name = models.CharField(null=True, blank=True, max_length=32)
    city = models.CharField(null=True, blank=True, max_length=32)

    def __str__(self):
        return f'{self.user.username}'


class Code(models.Model):
    code = models.CharField(max_length=256)
    amount = models.IntegerField()
    UOM = models.CharField(max_length=8)  # unit of measure
    criteria = models.TextField(null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.code


class Brand(models.Model):
    brand_name = models.CharField(max_length=128)
    url_pattern = models.CharField(max_length=256, blank=True, null=True)
    logo = models.CharField(max_length=256, blank=True, null=True)

    def __str__(self):
        return self.brand_name
