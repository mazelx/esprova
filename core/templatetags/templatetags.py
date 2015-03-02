from django.template import Library, Node
from core.models import Sport
from django.conf import settings

register = Library()


# get sports
class GetSportList(Node):
    def render(self, context):
        context['sports'] = Sport.objects.all()
        return ''


def get_sports(parser, token):
    return GetSportList()
get_sports = register.tag(get_sports)


# get settings value
@register.simple_tag
def settings_value(name):
    return getattr(settings, name, "")

