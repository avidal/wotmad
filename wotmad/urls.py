from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from wotmad.views import HomeView
from wotmad.account.views import Verify, LoginRedirect, Logout, AccountSetup

from wotmad.artofwar.views import SubmitLog, LogDetail

urlpatterns = patterns(
    '',
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'login/redirect/$', LoginRedirect.as_view(), name='login-redirect'),
    url(r'logout/$', Logout.as_view(), name='logout'),
    url(r'account/verify/$', Verify.as_view(), name='account-verify'),
    url(r'account/setup/$', AccountSetup.as_view(), name='account-setup'),

    url(r'art-of-war/submit/$', SubmitLog.as_view(), name='submit-log'),
    url(r'art-of-war/(?P<pk>\d+)/(?P<slug>[a-z0-9\-_]+)/', LogDetail.as_view(),
        name='view-log'),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^browserid/', include('django_browserid.urls')),
)
