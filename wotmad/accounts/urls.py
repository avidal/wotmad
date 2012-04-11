from django.conf.urls import patterns, url

from .views import LoginRedirect, Logout, Verify, AccountSetup

urlpatterns = patterns(
    'wotmad.accounts.views',

    url(r'login/redirect/$', LoginRedirect.as_view(), name='login-redirect'),
    url(r'logout/$', Logout.as_view(), name='logout'),
    url(r'account/verify/$', Verify.as_view(), name='verify'),
    url(r'account/setup/$', AccountSetup.as_view(), name='setup'),
)
