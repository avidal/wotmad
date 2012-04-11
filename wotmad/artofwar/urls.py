from django.conf.urls import patterns, url

from .views import LogList, SubmitLog, LogDetail

urlpatterns = patterns(
    'wotmad.artofwar.views',

    url(r'art-of-war/$', LogList.as_view(), name='list'),
    url(r'art-of-war/submit/$', SubmitLog.as_view(), name='submit'),
    url(r'art-of-war/(?P<pk>\d+)/(?P<slug>[a-z0-9\-_]+)/', LogDetail.as_view(),
        name='detail'),
)
