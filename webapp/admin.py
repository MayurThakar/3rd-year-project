from django.contrib import admin
from webapp import models
# Register your models here.

admin.site.register(models.Faculty)
admin.site.register(models.Student)
admin.site.register(models.OTP)
admin.site.register(models.Announce)
