from django.contrib import admin

from .models import Beer, Brewery, ServingType, Style

class BeerAdmin(admin.ModelAdmin):
    list_filter = ('style', )
    list_display = ('name', 'brewery', 'date_created')
    search_fields = ('style__name', 'brewery__name', 'name')

admin.site.register(Beer, BeerAdmin)
admin.site.register(Brewery)
admin.site.register(ServingType)
admin.site.register(Style)
