import base64
import hashlib
import random

from django.db import models
from django.contrib.auth.models import User


class APIKey(models.Model):

    user = models.OneToOneField('auth.User')
    key = models.CharField(max_length=38, unique=True)
    generated = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u'{0} - {1}'.format(self.user.username, self.key)

    @classmethod
    def generate_key(cls):
        """Generates a random 38 byte alphanumeric key"""

        # Get a 256 bit number via Mersenne Twister
        key = str(random.getrandbits(256))

        # Hash it using sha256
        key = hashlib.sha256(key).hexdigest()

        # Set up a few character pairs that will be randomly selected
        # to replace the special characters in the below base64
        # encoding
        pair = random.choice(['rA', 'aZ', 'gQ', 'hH', 'hG', 'aR', 'DD'])

        # base64 encode the key using the random pair from above to replace
        # the special characters
        key = base64.b64encode(key, pair)

        # Strip off the trailing == if it exists
        key = key.rstrip('==')

        # Reduce it down to 38 characters
        key = key[:38]

        # If this key has been taken already, then try again
        if cls.objects.filter(key=key).count():
            return cls.generate_key()

        return key


# Attach to user saving to create an API key if they don't have one already
def _create_key(sender, **kwargs):
    instance = kwargs.get('instance')

    # If the user doesn't have a key already then create one now
    has_key = APIKey.objects.filter(user=instance).count()

    if has_key:
        return

    key = APIKey.generate_key()

    # Create a new APIKey object and save it
    APIKey.objects.create(user=instance, key=key)

models.signals.post_save.connect(_create_key,
                                 sender=User,
                                 weak=False,
                                 dispatch_uid='accounts._create_key')
