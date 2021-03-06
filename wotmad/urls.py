from django.conf import settings
from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from wotmad.views import HomeView, SearchView

urlpatterns = patterns(
    '',
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^search/$', SearchView.as_view(), name='search'),

    url(r'^accounts/', include('wotmad.accounts.urls', namespace='accounts')),
    url(r'^art-of-war/', include('wotmad.artofwar.urls', namespace='artofwar')),
    url(r'^scripts/', include('wotmad.scripts.urls', namespace='scripts')),
    url(r'^stats/', include('wotmad.stats.urls', namespace='stats')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('django_browserid.urls')),

    url(r'^_/(?P<template>.*)', 'django.views.generic.simple.direct_to_template'),
)

if not settings.DEBUG:
    urlpatterns += patterns(
        'django.views.static',
        url(r'^static/(?P<path>.*)$', 'serve', {'document_root': settings.STATIC_ROOT}),
    )
