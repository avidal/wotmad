from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from wotmad.views import HomeView
from wotmad.account.views import Verify, LoginRedirect, Logout, AccountSetup

urlpatterns = patterns(
    '',
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'login/redirect/$', LoginRedirect.as_view(), name='login-redirect'),
    url(r'logout/$', Logout.as_view(), name='logout'),
    url(r'account/verify/$', Verify.as_view(), name='account-verify'),
    url(r'account/setup/$', AccountSetup.as_view(), name='account-setup'),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^browserid/', include('django_browserid.urls')),
)
