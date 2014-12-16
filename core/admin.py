from django.contrib import admin
from core.models import DistanceCategory, StageDistanceDefault, Race, Sport, Contact, Federation, Label, Event, Location


class StageDistanceDefaultInline(admin.StackedInline):
    model = StageDistanceDefault


class DistanceCategoryAdmin(admin.ModelAdmin):
    inlines = [StageDistanceDefaultInline, ]
    # fields = ('name', 'sport', 'long_name')
    # list_filter    = ('auteur','categorie', )
    # date_hierarchy = 'date'
    # ordering       = ('date', )
    # search_fields  = ('titre', 'contenu')


admin.site.register(DistanceCategory, DistanceCategoryAdmin)
admin.site.register(Race)
admin.site.register(Event)
# admin.site.register(Sport)
admin.site.register(Contact)
admin.site.register(Federation)
admin.site.register(Label)
admin.site.register(Location)

