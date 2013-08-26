# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Measurement.location_reference'
        db.add_column(u'observations_measurement', 'location_reference',
                      self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Measurement.source'
        db.add_column(u'observations_measurement', 'source',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['supplements.DataSource'], null=True, blank=True),
                      keep_default=False)


        # Changing field 'Measurement.observer'
        db.alter_column(u'observations_measurement', 'observer', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True))

    def backwards(self, orm):
        # Deleting field 'Measurement.location_reference'
        db.delete_column(u'observations_measurement', 'location_reference')

        # Deleting field 'Measurement.source'
        db.delete_column(u'observations_measurement', 'source_id')


        # User chose to not deal with backwards NULL issues for 'Measurement.observer'
        raise RuntimeError("Cannot reverse this migration. 'Measurement.observer' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'Measurement.observer'
        db.alter_column(u'observations_measurement', 'observer', self.gf('django.db.models.fields.EmailField')(max_length=75))

    models = {
        u'observations.measurement': {
            'Meta': {'object_name': 'Measurement'},
            'created_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.contrib.gis.db.models.fields.PointField', [], {}),
            'location_reference': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'observations': ('django_hstore.fields.DictionaryField', [], {'db_index': 'True'}),
            'observer': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'reference_timestamp': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['supplements.DataSource']", 'null': 'True', 'blank': 'True'})
        },
        u'supplements.datasource': {
            'Meta': {'object_name': 'DataSource'},
            'attribution': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'license': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['supplements.License']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
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