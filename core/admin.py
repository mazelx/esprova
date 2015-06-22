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

admin.site.register(DistanceCategory, DistanceCategoryAdmin)
admin.site.register(Season)
admin.site.register(Sport)
admin.site.register(Federation)
admin.site.register(SportStage)
