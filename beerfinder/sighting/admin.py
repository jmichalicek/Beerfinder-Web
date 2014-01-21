from django.contrib import admin

from .models import Sighting, Comment, SightingConfirmation

admin.site.register(Sighting)
admin.site.register(SightingConfirmation)
admin.site.register(Comment)
