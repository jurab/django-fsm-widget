from django import forms
from django.core.urlresolvers import reverse_lazy

from example.models import Meatball, Noodle, Spaghetti
from fsm.widget import FSM


class SpaghettiForm(forms.ModelForm):
    class Meta:
        model = Spaghetti

    meatballs = forms.ModelMultipleChoiceField(Meatball.objects.all(),
                                               widget=FSM('Meatballs',
                                               reverse_lazy('meatball_filter')))
    noodles = forms.ModelMultipleChoiceField(Noodle.objects.all(),
                                             widget=FSM('Noodles',
                                             reverse_lazy('noodle_filter'),
                                             lazy=True, use_async=True))

    def __init__(self, *args, **kwargs):
        super(SpaghettiForm, self).__init__(*args, **kwargs)
        self.fields['meatballs'].help_text = "Meatballs filters only on the " \
                                             "default field term==pk."
        self.fields['noodles'].help_text = "Noodles filters on the custom " \
                                           "defined fields length or pk " \
                                           "contains term."