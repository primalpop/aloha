# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Exam'
        db.create_table('allotter_exam', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('exam_code', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('exam_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('allotter', ['Exam'])

        # Adding model 'Option'
        db.create_table('allotter_option', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('opt_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('opt_code', self.gf('django.db.models.fields.IntegerField')(max_length=3)),
            ('opt_location', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal('allotter', ['Option'])

        # Adding M2M table for field exam on 'Option'
        db.create_table('allotter_option_exam', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('option', models.ForeignKey(orm['allotter.option'], null=False)),
            ('exam', models.ForeignKey(orm['allotter.exam'], null=False))
        ))
        db.create_unique('allotter_option_exam', ['option_id', 'exam_id'])

        # Adding model 'Application'
        db.create_table('allotter_application', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('options_selected', self.gf('django.db.models.fields.CharField')(max_length=5000, blank=True)),
            ('np', self.gf('django.db.models.fields.IntegerField')(max_length=2)),
            ('first_paper', self.gf('django.db.models.fields.related.ForeignKey')(related_name='first_paper', to=orm['allotter.Exam'])),
            ('second_paper', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='second_paper', null=True, to=orm['allotter.Exam'])),
            ('nat', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('gender', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('cent', self.gf('django.db.models.fields.IntegerField')(max_length=10)),
            ('cgy', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('pd', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('submitted', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('allotter', ['Application'])

        # Adding model 'Profile'
        db.create_table('allotter_profile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('dob', self.gf('django.db.models.fields.DateField')()),
            ('secondary_email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('phone_number', self.gf('django.db.models.fields.IntegerField')(max_length=10)),
            ('application', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['allotter.Application'])),
        ))
        db.send_create_signal('allotter', ['Profile'])

    def backwards(self, orm):
        # Deleting model 'Exam'
        db.delete_table('allotter_exam')

        # Deleting model 'Option'
        db.delete_table('allotter_option')

        # Removing M2M table for field exam on 'Option'
        db.delete_table('allotter_option_exam')

        # Deleting model 'Application'
        db.delete_table('allotter_application')

        # Deleting model 'Profile'
        db.delete_table('allotter_profile')

    models = {
        'allotter.application': {
            'Meta': {'object_name': 'Application'},
            'cent': ('django.db.models.fields.IntegerField', [], {'max_length': '10'}),
            'cgy': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'first_paper': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'first_paper'", 'to': "orm['allotter.Exam']"}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nat': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'np': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'options_selected': ('django.db.models.fields.CharField', [], {'max_length': '5000', 'blank': 'True'}),
            'pd': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'second_paper': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'second_paper'", 'null': 'True', 'to': "orm['allotter.Exam']"}),
            'submitted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'allotter.exam': {
            'Meta': {'object_name': 'Exam'},
            'exam_code': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'exam_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'allotter.option': {
            'Meta': {'object_name': 'Option'},
            'exam': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['allotter.Exam']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'opt_code': ('django.db.models.fields.IntegerField', [], {'max_length': '3'}),
            'opt_location': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'opt_name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'allotter.profile': {
            'Meta': {'object_name': 'Profile'},
            'application': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['allotter.Application']"}),
            'dob': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'phone_number': ('django.db.models.fields.IntegerField', [], {'max_length': '10'}),
            'secondary_email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
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
        }
    }

    complete_apps = ['allotter']