from django.contrib import admin

from .models import Beer, Brewery

admin.site.register(Beer)
admin.site.register(Brewery)
