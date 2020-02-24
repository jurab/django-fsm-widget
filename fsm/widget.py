from django.forms import Media, SelectMultiple
from django.forms.utils import flatatt
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string
from django.templatetags.static import static


class FSM(SelectMultiple):
    template_name = 'fsm/fsm.html'

    def __init__(self, verbose_name, url, use_async=False, attrs={},
                 choices=(), lazy=False, **kwargs):

        super(FSM, self).__init__(attrs, choices, **kwargs)

        # If lazy is True the initial choices are not loaded with the template.
        self.lazy = lazy

        # The url used by the filter. Should route to a FormView that inherits
        # off of fsm.views.FSM.
        self.query_url = url

        # If use_async is True the initial choices are loaded after the <select>
        # fields used by the widget are finished loading. The initial choices
        # will be loaded using the query_url.
        self.use_async = use_async

        # The field name to be used for the widget.
        self.verbose_name = verbose_name

    @property
    def media(self):

        js = [static('fsm/js/fsm.js')]
        css = {'all': (static('fsm/css/fsm.css'), )}
        return Media(js=js, css=css)

    def get_context(self, name, value, attrs=None, choices=None):
        context = super().get_context(name, value, attrs)
        selected = value or []
        choices = choices or ()
        attrs = attrs or {}

        choices = dict(list(choices) + list(self.choices))
        selected_list = []

        # Remove the already-selected objects from the choices and put them
        # in the list of selected objects.
        for val in selected:
            if choices and val in choices:
                selection = choices.pop(val)
                selected_list.append((val, selection))

        final_attrs = {k: v for k, v in attrs.items() if k not in ['id', 'name']}

        context['widget'].update({
            'use_async': self.use_async,
            'attrs': attrs,
            # If lazy-loading, don't pass in the choices.
            'choices': set(tuple(choices.items())) if not self.lazy else [],
            'final_attrs': flatatt(final_attrs),
            'name': name,
            'query_url': self.query_url,
            'selected': selected_list,
        })
        return context
