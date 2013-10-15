# -*- coding: utf-8 -*-

from ..core import db
from ..helpers import JsonSerializer


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


class Stat(JsonSerializer, db.Model):

    id = db.Column(db.Integer(), primary_key=True)

    submitter_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date_submitted = db.Column(db.DateTime())

    name = db.Column(db.String(64), default=u'')
    sex = db.Column(db.String(6))
    faction = db.Column(db.String(8))
    klass = db.Column(db.String(9))
    homeland = db.Column(db.String(32))

    strength = db.Column(db.SmallInteger)
    intel = db.Column(db.SmallInteger)
    wil = db.Column(db.SmallInteger)
    dex = db.Column(db.SmallInteger)
    con = db.Column(db.SmallInteger)

    @property
    def stats(self):
        return [self.strength, self.intel, self.wil, self.dex, self.con]

    @property
    def sum(self):
        return sum(self.stats)

    def get_x_display(self, choices, field):
        return dict(choices)[getattr(self, field)]

    def get_sex_display(self):
        return self.get_x_display(SEX_CHOICES, 'sex')

    def get_faction_display(self):
        return self.get_x_display(FACTION_CHOICES, "faction")

    def get_klass_display(self):
        return self.get_x_display(CLASS_CHOICES, "klass")

    def get_homeland_display(self):
        return self.get_x_display(HOMELAND_CHOICES, "homeland")

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
