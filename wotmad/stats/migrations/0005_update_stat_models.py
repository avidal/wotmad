# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

import re


class Migration(DataMigration):

    def forwards(self, orm):
        Stat = orm.Stat

        print "Updating sex."
        Stat.objects.filter(sex='M').update(sex='male')
        Stat.objects.filter(sex='F').update(sex='female')

        print "Updating factions."
        Stat.objects.filter(faction='H').update(faction='human')
        Stat.objects.filter(faction='D').update(faction='darkside')
        Stat.objects.filter(faction='S').update(faction='seanchan')

        print "Updating classes."
        Stat.objects.filter(klass='H').update(klass='hunter')
        Stat.objects.filter(klass='R').update(klass='rogue')
        Stat.objects.filter(klass='W').update(klass='warrior')
        Stat.objects.filter(klass='C').update(klass='channeler')

        print "Updating homelands."

        print "    Getting a list of homelands."
        # Get a list of all of our homelands
        xs = Stat.objects.values_list('homeland', flat=True)

        # Make it a set
        xs = set(xs)
        print "    Unique number of homelands", len(xs)

        # For each homeland, figure out the normalized version
        for x in xs:
            hl = x.lower()
            if hl.endswith(' trolloc'):
                hl = hl[:-8]

            if hl.startswith('the '):
                hl = hl[4:]

            # Remove everything but letters
            hl = re.sub(r'[^a-z]', '', hl)

            # And clean it up..
            print "    Updating homeland", x, "to", hl
            Stat.objects.filter(homeland=x).update(homeland=hl)

    def backwards(self, orm):
        raise RuntimeError("Cannot reverse this migration.")

    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'stats.stat': {
            'Meta': {'object_name': 'Stat'},
            'con': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'date_submitted': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'dex': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'faction': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'homeland': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'intel': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'klass': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '64', 'blank': 'True'}),
            'sex': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'strength': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'submitter': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stats'", 'to': "orm['auth.User']"}),
            'wil': ('django.db.models.fields.PositiveSmallIntegerField', [], {})
        }
    }

    complete_apps = ['stats']
