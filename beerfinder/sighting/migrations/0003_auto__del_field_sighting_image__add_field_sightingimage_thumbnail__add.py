# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Sighting.image'
        db.delete_column(u'sighting_sighting', 'image')

        # Adding field 'SightingImage.thumbnail'
        db.add_column(u'sighting_sightingimage', 'thumbnail',
                      self.gf('django.db.models.fields.files.ImageField')(default='', max_length=250, blank=True),
                      keep_default=False)

        # Adding field 'SightingImage.thumbnail_height'
        db.add_column(u'sighting_sightingimage', 'thumbnail_height',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'SightingImage.thumbnail_width'
        db.add_column(u'sighting_sightingimage', 'thumbnail_width',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'SightingImage.small'
        db.add_column(u'sighting_sightingimage', 'small',
                      self.gf('django.db.models.fields.files.ImageField')(default='', max_length=250, blank=True),
                      keep_default=False)

        # Adding field 'SightingImage.small_height'
        db.add_column(u'sighting_sightingimage', 'small_height',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'SightingImage.small_width'
        db.add_column(u'sighting_sightingimage', 'small_width',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'SightingImage.medium'
        db.add_column(u'sighting_sightingimage', 'medium',
                      self.gf('django.db.models.fields.files.ImageField')(default='', max_length=250, blank=True),
                      keep_default=False)

        # Adding field 'SightingImage.medium_height'
        db.add_column(u'sighting_sightingimage', 'medium_height',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'SightingImage.medium_width'
        db.add_column(u'sighting_sightingimage', 'medium_width',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Sighting.image'
        db.add_column(u'sighting_sighting', 'image',
                      self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True),
                      keep_default=False)

        # Deleting field 'SightingImage.thumbnail'
        db.delete_column(u'sighting_sightingimage', 'thumbnail')

        # Deleting field 'SightingImage.thumbnail_height'
        db.delete_column(u'sighting_sightingimage', 'thumbnail_height')

        # Deleting field 'SightingImage.thumbnail_width'
        db.delete_column(u'sighting_sightingimage', 'thumbnail_width')

        # Deleting field 'SightingImage.small'
        db.delete_column(u'sighting_sightingimage', 'small')

        # Deleting field 'SightingImage.small_height'
        db.delete_column(u'sighting_sightingimage', 'small_height')

        # Deleting field 'SightingImage.small_width'
        db.delete_column(u'sighting_sightingimage', 'small_width')

        # Deleting field 'SightingImage.medium'
        db.delete_column(u'sighting_sightingimage', 'medium')

        # Deleting field 'SightingImage.medium_height'
        db.delete_column(u'sighting_sightingimage', 'medium_height')

        # Deleting field 'SightingImage.medium_width'
        db.delete_column(u'sighting_sightingimage', 'medium_width')


    models = {
        u'accounts.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '100', 'db_index': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'send_watchlist_email': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'show_name_on_sightings': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'unique': 'True', 'max_length': '50', 'blank': 'True'})
        },
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'beer.beer': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('name', 'brewery'),)", 'object_name': 'Beer'},
            'brewery': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['beer.Brewery']"}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accounts.User']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '75'}),
            'normalized_name': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '75', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '150'}),
            'style': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['beer.Style']", 'null': 'True', 'blank': 'True'})
        },
        u'beer.brewery': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Brewery'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '75'}),
            'normalized_name': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '75', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '75'})
        },
        u'beer.servingtype': {
            'Meta': {'ordering': "('name',)", 'object_name': 'ServingType'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '25'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '25', 'blank': 'True'})
        },
        u'beer.style': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Style'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'blank': 'True'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'sighting.comment': {
            'Meta': {'ordering': "('-date_created', 'sighting')", 'object_name': 'Comment'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sighting': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'comments'", 'to': u"orm['sighting.Sighting']"}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accounts.User']"})
        },
        u'sighting.sighting': {
            'Meta': {'ordering': "('-date_sighted', 'beer', 'venue__name')", 'object_name': 'Sighting'},
            'beer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['beer.Beer']"}),
            'comment': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_sighted': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'serving_types': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['beer.ServingType']", 'symmetrical': 'False', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accounts.User']", 'blank': 'True'}),
            'venue': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['venue.Venue']"})
        },
        u'sighting.sightingconfirmation': {
            'Meta': {'ordering': "('-date_created', 'sighting')", 'object_name': 'SightingConfirmation'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_available': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'sighting': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sighting.Sighting']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accounts.User']", 'blank': 'True'})
        },
        u'sighting.sightingimage': {
            'Meta': {'object_name': 'SightingImage'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'medium': ('django.db.models.fields.files.ImageField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'medium_height': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'medium_width': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'original': ('django.db.models.fields.files.ImageField', [], {'max_length': '250'}),
            'original_height': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'original_width': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'sighting': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sighting_images'", 'to': u"orm['sighting.Sighting']"}),
            'small': ('django.db.models.fields.files.ImageField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'small_height': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'small_width': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'thumbnail': ('django.db.models.fields.files.ImageField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'thumbnail_height': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'thumbnail_width': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accounts.User']", 'blank': 'True'})
        },
        u'venue.venue': {
            'Meta': {'object_name': 'Venue'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'foursquare_id': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'point': ('django.contrib.gis.db.models.fields.PointField', [], {}),
            'postal_code': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'street_address': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'})
        }
    }

    complete_apps = ['sighting']