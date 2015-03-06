from django import template
from datetime import date, datetime
import locale

register = template.Library()


@register.filter(name='datefr')
def datefr(value):
    try:
        locale.setlocale(locale.LC_ALL, 'fr_FR.utf8')
    except Exception:
        locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')

    return value.strftime("%A %d/%m/%Y à %H:%M")
