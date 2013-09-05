# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Measurement.observations'
        db.alter_column(u'observations_measurement', 'observations', self.gf('django_hstore.fields.DictionaryField')(null=True))

    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'Measurement.observations'
        raise RuntimeError("Cannot reverse this migration. 'Measurement.observations' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'Measurement.observations'
        db.alter_column(u'observations_measurement', 'observations', self.gf('django_hstore.fields.DictionaryField')())

    models = {
        u'observations.measurement': {
            'Meta': {'ordering': "('-reference_timestamp',)", 'object_name': 'Measurement'},
            'created_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.contrib.gis.db.models.fields.PointField', [], {}),
            'location_reference': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'observations': ('django_hstore.fields.DictionaryField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
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