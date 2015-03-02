from django import template
from datetime import date, timedelta
import locale, datetime

register = template.Library()

@register.filter(name='datefr')
def datefr(value):
    locale.setlocale(locale.LC_TIME, "fr_FR")
    return value.strftime("%A %d/%m/%Y à %H:%M")