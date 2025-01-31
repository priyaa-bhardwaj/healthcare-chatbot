from django.contrib import admin
from .models import CustomUser, Question, Appointment
models=[CustomUser,Question,Appointment]
admin.site.register(models)
# Register your models here.
