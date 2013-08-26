# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'DataLayer'
        db.create_table(u'supplements_datalayer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('source', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['supplements.DataSource'])),
            ('info', self.gf('django_hstore.fields.DictionaryField')(db_index=True, null=True, blank=True)),
        ))
        db.send_create_signal(u'supplements', ['DataLayer'])
        sql = """
        SELECT AddGeometryColumn('supplements_datalayer', 'shape', 4326, 'GEOMETRY', 2);
        ALTER TABLE "supplements_datalayer" ALTER "shape" SET NOT NULL;
        CREATE INDEX "supplements_datalayer_shape_id" ON "supplements_datalayer" USING GIST ( "shape" );
        """
        db.execute(sql)


    def backwards(self, orm):
        # Deleting model 'DataLayer'
        db.delete_table(u'supplements_datalayer')


    models = {
        u'supplements.datalayer': {
            'Meta': {'object_name': 'DataLayer'},
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django_hstore.fields.DictionaryField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'shape': ('django.contrib.gis.db.models.fields.GeometryField', [], {}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['supplements.DataSource']"})
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

    complete_apps = ['supplements']
