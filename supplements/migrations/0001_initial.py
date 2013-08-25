# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'License'
        db.create_table(u'supplements_license', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('version', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('body', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'supplements', ['License'])

        # Adding model 'DataSource'
        db.create_table(u'supplements_datasource', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('attribution', self.gf('django.db.models.fields.TextField')()),
            ('year', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('license', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['supplements.License'])),
        ))
        db.send_create_signal(u'supplements', ['DataSource'])


    def backwards(self, orm):
        # Deleting model 'License'
        db.delete_table(u'supplements_license')

        # Deleting model 'DataSource'
        db.delete_table(u'supplements_datasource')


    models = {
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

    complete_apps = ['supplements']