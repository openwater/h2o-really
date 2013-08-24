# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Measurement'
        db.create_table(u'quality_measurement', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('reference_timestamp', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('observer', self.gf('django.db.models.fields.EmailField')(max_length=75)),
        ))
        db.send_create_signal(u'quality', ['Measurement'])


    def backwards(self, orm):
        # Deleting model 'Measurement'
        db.delete_table(u'quality_measurement')


    models = {
        u'quality.measurement': {
            'Meta': {'object_name': 'Measurement'},
            'created_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'observer': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'reference_timestamp': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['quality']