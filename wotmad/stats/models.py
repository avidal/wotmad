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

DS_HOMELANDS = (
    ("Beaked", "Beaked"),
    ("Bearish", "Bearish"),
    ("Boarish", "Boarish"),
    ("Ramshorned", "Ramshorned"),
    ("Wolfish", "Wolfish"),
)

LS_HOMELANDS = (
    ("Altara", "Altara"),
    ("Amadicia", "Amadicia"),
    ("Andor", "Andor"),
    ("Arad Doman", "Arad Doman"),
    ("Arafel", "Arafel"),
    ("Borderlands", "Borderlands"),
    ("Cairhien", "Cairhien"),
    ("Ghealdan", "Ghealdan"),
    ("Illian", "Illian"),
    ("Kandor", "Kandor"),
    ("Mayene", "Mayene"),
    ("Murandy", "Murandy"),
    ("Saldaea", "Saldaea"),
    ("Shienar", "Shienar"),
    ("Tarabon", "Tarabon"),
    ("Tear", "Tear"),
    ("Two Rivers", "Two Rivers"),
)

SS_HOMELANDS = (
    ("Seandar", "Seandar"),
    ("Kirendad", "Kirendad"),
    ("Shon Kifar", "Shon Kifar"),
    ("Rampore", "Rampore"),
    ("Tzura", "Tzura"),
    ("Noren M'shar", "Noren M'shar"),
)

HOMELAND_CHOICES = DS_HOMELANDS + LS_HOMELANDS + SS_HOMELANDS


class Stat(models.Model):

    submitter = models.ForeignKey('auth.User', related_name='stats')
    date_submitted = models.DateTimeField(auto_now_add=True)

    name = models.CharField(max_length=64, default='', blank=True)
    sex = models.CharField(max_length=1, choices=SEX_CHOICES)
    faction = models.CharField(max_length=1, choices=FACTION_CHOICES)
    klass = models.CharField(max_length=1, choices=CLASS_CHOICES)
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
                                      homeland=self.homeland,
                                      strength=self.strength,
                                      intel=self.intel,
                                      wil=self.wil,
                                      dex=self.dex,
                                      con=self.con)
