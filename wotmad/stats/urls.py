from django.conf.urls import patterns, url

from .views import StatList

urlpatterns = patterns(
    'wotmad.stats.views',

    url(r'^$', StatList.as_view(), name='list'),
)
