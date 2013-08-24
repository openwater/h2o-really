# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Measurement.observations'
        db.add_column(u'observations_measurement', 'observations',
                      self.gf('django_hstore.fields.DictionaryField')(db_index=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Measurement.observations'
        db.delete_column(u'observations_measurement', 'observations')


    models = {
        u'observations.measurement': {
            'Meta': {'object_name': 'Measurement'},
            'created_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'observations': ('django_hstore.fields.DictionaryField', [], {'db_index': 'True'}),
            'observer': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'reference_timestamp': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['observations']
