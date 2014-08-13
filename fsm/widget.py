from django.forms import Media, SelectMultiple
from django.forms.util import flatatt
from django.utils.safestring import mark_safe
from django.contrib.admin.templatetags.admin_static import static
from django.template.loader import render_to_string


class FSM(SelectMultiple):
    def __init__(self, verbose_name, url, async=False, attrs={},
                 choices=(), lazy=False, **kwargs):

        super(FSM, self).__init__(attrs, choices, **kwargs)

        # If lazy is True the initial choices are not loaded with the template.
        self.lazy = lazy

        # The url used by the filter. Should route to a FormView that inherits
        # off of fsm.views.FSM.
        self.query_url = url

        # If async is True the initial choices are loaded after the <select>
        # fields used by the widget are finished loading. The initial choices
        # will be loaded using the query_url.
        self.async = async

        # The field name to be used for the widget.
        self.verbose_name = verbose_name

    @property
    def media(self):
        js = [static('fsm/js/fsm.js')]
        css = {'all': (static('fsm/css/fsm.css'), )}
        return Media(js=js, css=css)

    def render(self, name, selected, attrs=None, choices=None):
        selected = selected or []
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

        data = {
            'async': self.async,
            'attrs': attrs,
            # If lazy-loading, don't pass in the choices.
            'choices': set(tuple(choices.items())) if not self.lazy else [],
            'final_attrs': flatatt(self.build_attrs(attrs, name=name)),
            'name': name,
            'query_url': self.query_url,
            'selected': selected_list,
            'verbose_name': self.verbose_name,
        }
        output = render_to_string('fsm/fsm.html', data)

        return mark_safe(output)