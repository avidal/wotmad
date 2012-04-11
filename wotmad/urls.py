from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from wotmad.views import HomeView

urlpatterns = patterns(
    '',
    url(r'^$', HomeView.as_view(), name='home'),

    url(r'accounts/', include('wotmad.accounts.urls', namespace='accounts')),
    url(r'art-of-war/', include('wotmad.artofwar.urls', namespace='artofwar')),
    url(r'scripts/', include('wotmad.scripts.urls', namespace='scripts')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^browserid/', include('django_browserid.urls')),
)
