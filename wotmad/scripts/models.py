import datetime

from django.db import models


CLIENT_CHOICES = (
    ('ZMUD', 'zMUD'),
    ('CMUD', 'cMUD'),
    ('TINTIN', 'TinTin'),
    ('TINYFUGUE', 'TinyFugue'),
    ('MUDLET', 'Mudlet'),
    ('ALCLIENT', 'AL Client'),
    ('OTHER', 'Other'),
)


class Script(models.Model):

    slug = models.SlugField(max_length=60)
    title = models.CharField(max_length=60)
    description = models.TextField(blank=True, default=u'')
    last_modified = models.DateTimeField(auto_now=True)

    client = models.CharField(max_length=60, choices=CLIENT_CHOICES)

    submitter = models.ForeignKey('auth.User', related_name='scripts')

    def add_version(self, source):
        """Adds a new script version for this script"""

        # First, mark the old version as not the current one
        version = 0
        latest = self.latest_version
        if latest:
            version = latest.version
            latest.is_current = False
            latest.save()

        newversion = ScriptSource()
        newversion.version = version + 1
        newversion.is_current = True
        newversion.script = self
        newversion.source = source
        newversion.save()

        # Also bump the local last modified
        self.last_modified = datetime.datetime.now()
        self.save()

        return newversion

    @property
    def latest_version(self):
        try:
            return self.versions.get(is_current=True)
        except ScriptSource.DoesNotExist:
            return None

    @models.permalink
    def get_absolute_url(self):
        return ('scripts:detail', [self.pk, self.slug])

    def __unicode__(self):
        return self.title


class ScriptSource(models.Model):

    script = models.ForeignKey(Script, related_name='versions')
    date_submitted = models.DateTimeField(auto_now_add=True)
    is_current = models.BooleanField()

    version = models.IntegerField()
    source = models.TextField()

    def __unicode__(self):
        return u'[V{0}] {1} - {2}'.format(self.version,
                                          self.script.submitter.username,
                                          self.script.title)
