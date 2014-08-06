from django.core.urlresolvers import resolve
from django.shortcuts import render_to_response
from django.views.generic.edit import FormView, ModelFormMixin
from django.views.generic.detail import SingleObjectMixin

from example.forms import SpaghettiForm
from example.models import Meatball, Noodle, Spaghetti
from fsm.views import FSMView


class MeatballFilter(FSMView):
    model = Meatball


class NoodleFilter(FSMView):
    model = Noodle
    fields = ('pk__icontains', 'length__icontains')


class EditSpaghetti(FormView, ModelFormMixin, SingleObjectMixin):
    model = Spaghetti
    form_class = SpaghettiForm
    success_url = '/'
    template_name = 'form.html'

    def get_queryset(self):
        return Spaghetti.objects.all()

    def set_object(self, request):
        if not resolve(request.path).url_name == 'add':
            queryset = self.get_queryset()
            self.object = self.get_object(queryset=queryset)
        else:
            self.object = None

    def get(self, request, *args, **kwargs):
        self.set_object(request)
        return super(EditSpaghetti, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.set_object(request)
        return super(EditSpaghetti, self).post(request, *args, **kwargs)


def home(request):
    data = {
        'objs': Spaghetti.objects.all()
    }
    return render_to_response('home.html', data)