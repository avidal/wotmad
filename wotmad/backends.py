import json
import logging
import subprocess

from django.conf import settings

from django_browserid.auth import BrowserIDBackend as MozBrowserIDBackend

log = logging.getLogger(__name__)


class BrowserIDBackend(MozBrowserIDBackend):
    """Authenticate users by verifying their browser id credentials.

    This is a subclass of the django_browserid backend, specifically to
    override the `authenticate` method, which fails for some reason for me.

    Instead of using the `verify` function shipped with the module, we'll just
    have cURL POST for the verification.
    """

    def authenticate(self, assertion=None, audience=None):
        payload = "assertion={0}&audience={1}".format(assertion, audience)
        curl = subprocess.Popen(["curl", "-d", payload,
                                "https://browserid.org/verify"],
                                stdout=subprocess.PIPE)

        # FIXME: This entire class should go away, but if it can't then
        # at the very least we should probably catch errors here.
        try:
            result = json.loads(curl.communicate()[0])
        except ValueError:
            result = None

        # Below this point the code was taken directly from django_browserid

        email = result['email']

        # in the rare case that two user accounts have the same email address,
        # log and bail. randomly selecting one seems really wrong.
        users = self.filter_users_by_email(email=email)
        if len(users) > 1:
            log.warn('%d users with email address %s.' % (len(users), email))
            return None
        if len(users) == 1:
            return users[0]

        create_user = getattr(settings, 'BROWSERID_CREATE_USER', False)
        if not create_user:
            return None
        elif create_user == True:
            return self.create_user(email)
        else:
            # Find the function to call, call it and throw in the email.
            return self._load_module(create_user)(email)
