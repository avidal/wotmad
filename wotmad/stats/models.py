from django.db import models

SEX_CHOICES = (
    ('male', 'Male'),
    ('female', 'Female'),
)

FACTION_CHOICES = (
    ('human', 'Human'),
    ('darkside', 'Darkside'),
    ('seanchan', 'Seanchan'),
)

CLASS_CHOICES = (
    ('hunter', 'Hunter'),
    ('rogue', 'Rogue'),
    ('warrior', 'Warrior'),
    ('channeler', 'Channeler'),
)

DS_HOMELANDS = (
    ("beaked", "Beaked"),
    ("bearish", "Bearish"),
    ("boarish", "Boarish"),
    ("ramshorned", "Ramshorned"),
    ("wolfish", "Wolfish"),
)

LS_HOMELANDS = (
    ("altara", "Altara"),
    ("amadicia", "Amadicia"),
    ("andor", "Andor"),
    ("araddoman", "Arad Doman"),
    ("arafel", "Arafel"),
    ("borderlands", "Borderlands"),
    ("cairhien", "Cairhien"),
    ("ghealdan", "Ghealdan"),
    ("illian", "Illian"),
    ("kandor", "Kandor"),
    ("mayene", "Mayene"),
    ("murandy", "Murandy"),
    ("saldaea", "Saldaea"),
    ("shienar", "Shienar"),
    ("tarabon", "Tarabon"),
    ("tear", "Tear"),
    ("tworivers", "Two Rivers"),
)

SS_HOMELANDS = (
    ("seandar", "Seandar"),
    ("kirendad", "Kirendad"),
    ("shonkifar", "Shon Kifar"),
    ("rampore", "Rampore"),
    ("tzura", "Tzura"),
    ("norenmshar", "Noren M'shar"),
)

HOMELAND_CHOICES = DS_HOMELANDS + LS_HOMELANDS + SS_HOMELANDS


class Stat(models.Model):

    submitter = models.ForeignKey('auth.User', related_name='stats')
    date_submitted = models.DateTimeField(auto_now_add=True)

    name = models.CharField(max_length=64, default='', blank=True)
    sex = models.CharField(max_length=6, choices=SEX_CHOICES)
    faction = models.CharField(max_length=8, choices=FACTION_CHOICES)
    klass = models.CharField(max_length=9, choices=CLASS_CHOICES)
    homeland = models.CharField(max_length=32, choices=HOMELAND_CHOICES)

    strength = models.PositiveSmallIntegerField()
    intel = models.PositiveSmallIntegerField()
    wil = models.PositiveSmallIntegerField()
    dex = models.PositiveSmallIntegerField()
    con = models.PositiveSmallIntegerField()

    @property
    def stats(self):
        return [self.strength, self.intel, self.wil, self.dex, self.con]

    @property
    def sum(self):
        return sum(self.stats)

    def __unicode__(self):
        parts = []
        parts.append("{faction} {sex} {klass} from {homeland}")
        parts.append("[{strength} {intel} {wil} {dex} {con}]")

        return " ".join(parts).format(faction=self.get_faction_display(),
                                      sex=self.get_sex_display(),
                                      klass=self.get_klass_display(),
                                      homeland=self.get_homeland_display(),
                                      strength=self.strength,
                                      intel=self.intel,
                                      wil=self.wil,
                                      dex=self.dex,
                                      con=self.con)
