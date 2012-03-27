from django.db import models


class Log(models.Model):

    slug = models.SlugField(max_length=60)
    title = models.CharField(max_length=60)
    text = models.TextField(help_text=u'Paste your log here.')

    submitter = models.ForeignKey('auth.User', related_name='logs')
    date_submitted = models.DateTimeField(auto_now_add=True)

    @models.permalink
    def get_absolute_url(self):
        return ('view-log', [self.pk, self.slug])

    def __unicode__(self):
        return self.title
