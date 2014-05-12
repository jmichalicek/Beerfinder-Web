from django.contrib import admin

from .models import Sighting, Comment, SightingConfirmation, SightingImage

class SightingImageInline(admin.StackedInline):
    raw_id_fields = ('user', )
    model = SightingImage


class SightingAdmin(admin.ModelAdmin):
    raw_id_fields =('user', )
    inlines = (SightingImageInline, )
    list_display = ('pk', 'beer', 'user', 'date_created')

    class Meta:
        model = Sighting


class SightingImageAdmin(admin.ModelAdmin):
    list_display = ('pk', 'sighting', 'date_created', 'user')
    raw_id_fields = ('user', 'sighting')

    class Meta:
        models = SightingImage


admin.site.register(Sighting, SightingAdmin)
admin.site.register(SightingConfirmation)
admin.site.register(Comment)
admin.site.register(SightingImage, SightingImageAdmin)
