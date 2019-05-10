django-fsm-widget
=================

What is it?
-----------
A select multiple widget that allows for filtering and lazy loading. It is inspired by Django's `FilteredSelectMultiple widget <https://github.com/django/django/blob/1.11.20/django/contrib/admin/widgets.py#L21>`_, but with a few improvements:

* Lazy loading and asynchronous loading for the initial choices make it quicker to work with very large data sets.
* The ability to specify the field and lookup types the filter is being applied on.
* Easy to use both inside the admin and out since all of the required javascript and (minimal) css are included in the widget.

_________________

Requirements
------------
django-fsm-widget requires Django 1.11 or later.


Installation
------------
To install the latest version of django-fsm-widget:

``pip install git+git://github.com/DirectEmployers/django-fsm-widget.git@v1.11.1``


Getting Started
----------------

To use the widget in a form, specify the widget when creating the field::

    from django import forms
    from django.core.urlresolvers import reverse_lazy
    from example.models import Meatball, Noodle, Spaghetti
    from fsm.widget import FSM


    class SpaghettiForm(forms.ModelForm):
        class Meta:
            model = Spaghetti

        meatball_widget = FSM('Meatballs', reverse_lazy('meatball_filter')
        meatballs = forms.ModelMultipleChoiceField(Meatball.objects.all(), widget=meatball_widget)

The available params for the FSM widget are:

* ``verbose_name`` (required): A name for the object that the widget is being used on that is used when describing the object. Usually the field label  will work for this.
* ``url`` (required): The url used for filtering/autocomplete and lazy loading. The endpoint should be a subclass of the ``FSMView`` view class covered below.
* ``use_async`` (``default==False``): True if you want to load the initial choices after the page has loaded, otherwise False. Note: If ``use_async==True`` and ``lazy==False`` the initial choices will be loaded twice.
* ``attrs``: Form element attributes. Same as most other Django widgets.
* ``choices``: The initial choices to select from.
* ``lazy`` (``default==False``): Prevent loading of initial choices until filter terms have been entered by the user.


The ``FSMView`` class serves as an endpoint for the filter. There needs to be at least one subclass of ``FSMView`` for every model that's being filtered using the ``FSM`` widget. Setting up the filter endpoint is as easy as::

    class MeatballFilter(FSMView):
        model = Meatball

The fields that are filtered on can be specified by adding the variable ``fields = ('fieldname__lookuptype', 'fieldname', ...)`` to the subclass.

An example of all of this can be found in the ``example/`` directory of this project. The example project is fully functional and can be run using runserver.

_________________


License
-------
MIT
