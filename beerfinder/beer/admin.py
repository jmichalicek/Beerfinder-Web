from django.contrib import admin

from .models import Beer, Brewery, ServingType, Style

admin.site.register(Beer)
admin.site.register(Brewery)
admin.site.register(ServingType)
admin.site.register(Style)
