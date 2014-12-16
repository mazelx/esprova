from django.conf import settings # import the settings file


def global_settings(request):
# return any necessary values
    return {
        'GOOGLE_API_KEY': settings.GOOGLE_API_KEY
    }
