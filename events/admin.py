from django.contrib import admin
from events.models import *
# Register your models here.


class RaceAdmin(admin.ModelAdmin):
    list_display = ('sport', 'event', 'date', 'distance_cat', 'location', 'created_date')
    list_filter = ('sport', 'event', 'date', 'distance_cat', 'location')
    date_hierarchy = 'date'
    ordering = ('date', )
    search_fields = ('event__name', 'distance_cat__name')


class EventAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'website', 'edition', 'validated', 'event_mod_source', 'event_prev_edition', 'to_be_deleted')
    list_filter = ('name', 'website', 'edition', 'validated', 'event_mod_source', 'event_prev_edition', 'to_be_deleted')
    ordering = ('name', )
    search_fields = ('name', 'validated')


class ContactAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'email', 'phone',)
    list_filter = ('name', 'email', 'phone')
    ordering = ('name', 'email', 'phone')
    search_fields = ('name', 'email', 'phone',)

admin.site.register(Race, RaceAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Organizer)
admin.site.register(Contact, ContactAdmin)
admin.site.register(Label)
admin.site.register(Location)
admin.site.register(Challenge)
