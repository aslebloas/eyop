from django.contrib import admin
from .models import Profile, Code, Brand, Relationship


# Register your models here.
admin.site.register(Profile)
admin.site.register(Code)
admin.site.register(Brand)
admin.site.register(Relationship)
