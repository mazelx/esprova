from django.contrib import admin
from core.models import *


class StageDistanceDefaultInline(admin.StackedInline):
    model = StageDistanceDefault


class DistanceCategoryAdmin(admin.ModelAdmin):
    inlines = [StageDistanceDefaultInline, ]
    # fields = ('name', 'sport', 'long_name')
    # list_filter    = ('auteur','categorie', )
    # date_hierarchy = 'date'
    # ordering       = ('date', )
    # search_fields  = ('titre', 'contenu')


class RaceAdmin(admin.ModelAdmin):
    list_display = ('sport', 'event', 'date', 'distance_cat', 'location')
    list_filter = ('sport', 'event', 'date', 'distance_cat', 'location')
    date_hierarchy = 'date'
    ordering = ('date', )
    search_fields = ('event', 'distance_cat')


admin.site.register(DistanceCategory, DistanceCategoryAdmin)
admin.site.register(Race, RaceAdmin)
admin.site.register(EventEdition)
admin.site.register(EventReference)
admin.site.register(Season)
admin.site.register(Sport)
admin.site.register(Contact)
admin.site.register(Federation)
admin.site.register(Label)
admin.site.register(Location)
admin.site.register(Organizer)
admin.site.register(SportStage)
