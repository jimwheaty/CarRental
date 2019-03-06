from django.contrib import admin

# Register your models here.

from .models import Observation, Company, Price

admin.site.register(Observation)
admin.site.register(Company)
admin.site.register(Price)
