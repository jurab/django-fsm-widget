from django.contrib import admin

from example.models import Meatball, Noodle, Spaghetti
from example.forms import SpaghettiForm


class SpaghettiAdmin(admin.ModelAdmin):
    model = Spaghetti
    form = SpaghettiForm


admin.site.register(Meatball)
admin.site.register(Noodle)
admin.site.register(Spaghetti, SpaghettiAdmin)