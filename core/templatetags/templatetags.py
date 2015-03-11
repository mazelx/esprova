from django.template import Library, Node
from core.models import Sport
from django.conf import settings
from datetime import datetime, date

register = Library()


# get sports
class GetSportList(Node):
    def render(self, context):
        context['sports'] = Sport.objects.filter(hidden=False).order_by('name')
        return ''


def get_sports(parser, token):
    return GetSportList()
get_sports = register.tag(get_sports)


# nextyear
@register.simple_tag
def nextyear(date_format):
    d = datetime.now()
    years = 1
    date_format = '-'.join(['%' + x for x in date_format.split('-')])
    try:
        d = d.replace(year=d.year + years)
    except ValueError:
        d = d + (date(d.year + years, 1, 1) - date(d.year, 1, 1))
    return d.strftime(date_format)


# get settings value
@register.simple_tag
def settings_value(name):
    return getattr(settings, name, "")

