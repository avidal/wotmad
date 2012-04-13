from django.db import models

SEX_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
)

FACTION_CHOICES = (
    ('H', 'Human'),
    ('D', 'Darkside'),
    ('S', 'Seanchan'),
)

CLASS_CHOICES = (
    ('H', 'Hunter'),
    ('R', 'Rogue'),
    ('W', 'Warrior'),
    ('C', 'Channeler'),
)


class Stat(models.Model):

    submitter = models.ForeignKey('auth.User', related_name='stats')
    date_submitted = models.DateTimeField(auto_now_add=True)

    name = models.CharField(max_length=64, default='', blank=True)
    sex = models.CharField(max_length=1, choices=SEX_CHOICES)
    faction = models.CharField(max_length=1, choices=FACTION_CHOICES)
    klass = models.CharField(max_length=1, choices=CLASS_CHOICES)
    homeland = models.CharField(max_length=32)

    strength = models.PositiveSmallIntegerField()
    intel = models.PositiveSmallIntegerField()
    wil = models.PositiveSmallIntegerField()
    dex = models.PositiveSmallIntegerField()
    con = models.PositiveSmallIntegerField()

    def __unicode__(self):
        parts = []
        parts.append("{faction} {sex} {klass} from {homeland}")
        parts.append("[{strength} {intel} {wil} {dex} {con}]")

        return " ".join(parts).format(faction=self.get_faction_display(),
                                      sex=self.get_sex_display(),
                                      klass=self.get_klass_display(),
                                      homeland=self.homeland,
                                      strength=self.strength,
                                      intel=self.intel,
                                      wil=self.wil,
                                      dex=self.dex,
                                      con=self.con)
