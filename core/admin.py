from django.contrib import admin
from .models import Profile, Patient, MedicalRecord

# Register your models here.
admin.site.register(Profile)
admin.site.register(Patient)
admin.site.register(MedicalRecord)