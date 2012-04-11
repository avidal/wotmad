# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Stat'
        db.create_table('stats_stat', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('submitter', self.gf('django.db.models.fields.related.ForeignKey')(related_name='stats', to=orm['auth.User'])),
            ('date_submitted', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='', max_length=64, blank=True)),
            ('sex', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('faction', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('klass', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('homeland', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('hitpoints', self.gf('django.db.models.fields.IntegerField')()),
            ('moves', self.gf('django.db.models.fields.IntegerField')()),
            ('spellpoints', self.gf('django.db.models.fields.IntegerField')()),
            ('strength', self.gf('django.db.models.fields.IntegerField')()),
            ('intel', self.gf('django.db.models.fields.IntegerField')()),
            ('wil', self.gf('django.db.models.fields.IntegerField')()),
            ('dex', self.gf('django.db.models.fields.IntegerField')()),
            ('con', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('stats', ['Stat'])

    def backwards(self, orm):
        # Deleting model 'Stat'
        db.delete_table('stats_stat')

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
            'con': ('django.db.models.fields.IntegerField', [], {}),
            'date_submitted': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'dex': ('django.db.models.fields.IntegerField', [], {}),
            'faction': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'hitpoints': ('django.db.models.fields.IntegerField', [], {}),
            'homeland': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'intel': ('django.db.models.fields.IntegerField', [], {}),
            'klass': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'moves': ('django.db.models.fields.IntegerField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '64', 'blank': 'True'}),
            'sex': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'spellpoints': ('django.db.models.fields.IntegerField', [], {}),
            'strength': ('django.db.models.fields.IntegerField', [], {}),
            'submitter': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stats'", 'to': "orm['auth.User']"}),
            'wil': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['stats']