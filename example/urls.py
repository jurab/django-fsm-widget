from django.conf.urls import patterns, include, url
from django.contrib import admin

from example.views import home, MeatballFilter, NoodleFilter, EditSpaghetti


admin.autodiscover()


urlpatterns = patterns(
    '',
    url(r'^$', home),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^meatball/filter/', MeatballFilter.as_view(), name='meatball_filter'),
    url(r'^noodle/filter/', NoodleFilter.as_view(), name='noodle_filter'),
    url(r'^test_form/add/$', EditSpaghetti.as_view(), name='add'),
    url(r'^test_form/edit/(?P<pk>\d+)/$', EditSpaghetti.as_view(), name='edit'),
)
