import json
import logging
import subprocess

from django.contrib.auth.models import User

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
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # FIXME: This entire class should go away, but if it can't then
        # at the very least we should probably catch errors here.
        try:
            out, err = curl.communicate()
            result = json.loads(out)
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

        return self.create_user(email)

    def create_user(self, email):
        """Deal with creating new users.

        We will set their username temporarily to the first part of their
        email address, with a .2, .3, .4 as necessary to ensure uniqueness.

        """

        candidate = email.split('@')[0]
        existing = User.objects.filter(username__startswith=candidate)

        if existing:
            username = "{0}.{1}".format(candidate, existing.count())
        else:
            username = candidate

        user = User.objects.create_user(username, email)
        user.is_active = False
        user.save()

        return user
