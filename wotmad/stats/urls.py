from django.conf.urls import patterns, url

from .views import StatList, ContributeStat

urlpatterns = patterns(
    'wotmad.stats.views',

    url(r'^$', StatList.as_view(), name='list'),
    url(r'^contribute/$', ContributeStat.as_view(), name='contribute'),
)
