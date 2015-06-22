from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView


class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, *initargs, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(*initargs, **initkwargs)
        return login_required(view)


# List and view
class IntroView(TemplateView):
    template_name = 'core/introduction.html'
