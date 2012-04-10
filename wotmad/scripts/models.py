from django.db import models


CLIENT_CHOICES = (
    ('ZMUD', 'zMUD'),
    ('CMUD', 'cMUD'),
    ('TT', 'TinTin'),
    ('TF', 'TinyFugue'),
    ('MUDLET', 'Mudlet'),
    ('OTHER', 'Other'),
)


class Script(models.Model):

    slug = models.SlugField(max_length=60)
    title = models.CharField(max_length=60)
    description = models.TextField(blank=True, default=u'')
    source = models.TextField()

    client = models.CharField(max_length=60, choices=CLIENT_CHOICES,
                              default='OTHER')

    submitter = models.ForeignKey('auth.User', related_name='scripts')
    date_submitted = models.DateTimeField(auto_now_add=True)

    @models.permalink
    def get_absolute_url(self):
        return ('scripts:detail', [self.pk, self.slug])

    def __unicode__(self):
        return self.title
