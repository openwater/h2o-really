# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Test'
        db.create_table(u'observations_test', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('parameter', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['observations.Parameter'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('vendor_or_authority', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('unit', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('meta', self.gf('django_hstore.fields.DictionaryField')(db_index=True)),
            ('test_type', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal(u'observations', ['Test'])

        # Adding model 'Parameter'
        db.create_table(u'observations_parameter', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'observations', ['Parameter'])

        # Adding model 'TestValue'
        db.create_table(u'observations_testvalue', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('test', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['observations.Test'])),
            ('measurement', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['observations.Measurement'])),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'observations', ['TestValue'])


    def backwards(self, orm):
        # Deleting model 'Test'
        db.delete_table(u'observations_test')

        # Deleting model 'Parameter'
        db.delete_table(u'observations_parameter')

        # Deleting model 'TestValue'
        db.delete_table(u'observations_testvalue')


    models = {
        u'observations.measurement': {
            'Meta': {'ordering': "('-reference_timestamp',)", 'object_name': 'Measurement'},
            'created_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.contrib.gis.db.models.fields.PointField', [], {}),
            'location_reference': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'observations': ('django_hstore.fields.DictionaryField', [], {'db_index': 'True'}),
            'observer': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'parameters': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['observations.Test']", 'through': u"orm['observations.TestValue']", 'symmetrical': 'False'}),
            'reference_timestamp': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['supplements.DataSource']", 'null': 'True', 'blank': 'True'})
        },
        u'observations.parameter': {
            'Meta': {'object_name': 'Parameter'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'observations.test': {
            'Meta': {'object_name': 'Test'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'meta': ('django_hstore.fields.DictionaryField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'parameter': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['observations.Parameter']"}),
            'test_type': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'unit': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'vendor_or_authority': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'observations.testvalue': {
            'Meta': {'object_name': 'TestValue'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'measurement': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['observations.Measurement']"}),
            'test': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['observations.Test']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'supplements.datasource': {
            'Meta': {'object_name': 'DataSource'},
            'attribution': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'license': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['supplements.License']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'year': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        u'supplements.license': {
            'Meta': {'object_name': 'License'},
            'body': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'version': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['observations']