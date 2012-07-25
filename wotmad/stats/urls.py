from django.conf.urls import patterns, url

from .views import StatList, ContributeStat, SubmitStat, ExportStats

urlpatterns = patterns(
    'wotmad.stats.views',

    url(r'^$', StatList.as_view(), name='list'),
    url(r'^contribute/$', ContributeStat.as_view(), name='contribute'),
    url(r'^submit/$', SubmitStat.as_view(), name='submit'),
    url(r'^export/$', ExportStats.as_view(), name='export'),
)
