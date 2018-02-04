from django.contrib import admin
from .models import City, Country, Countrylanguage
# Register your models here.
admin.site.register(City)
admin.site.register(Country)
admin.site.register(Countrylanguage)
