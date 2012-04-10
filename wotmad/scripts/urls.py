from django.conf.urls import patterns, url

from .views import ScriptList, SubmitScript, ScriptDetail

urlpatterns = patterns(
    'wotmad.scripts.views',

    url(r'^submit/$', SubmitScript.as_view(), name='submit'),
    url(r'^(?P<pk>\d+)/(?P<slug>[a-z0-9\-_]+)/$', ScriptDetail.as_view(),
        name='detail'),
    url(r'^(?:(?P<client>[a-z]+)/)?$', ScriptList.as_view(), name='list'),
)
