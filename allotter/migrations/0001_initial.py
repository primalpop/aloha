# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Option'
        db.create_table('allotter_option', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('opt_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('seats', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('allotter', ['Option'])

        # Adding model 'Exam'
        db.create_table('allotter_exam', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('exam_code', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('exam_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('allotter', ['Exam'])

        # Adding model 'Profile'
        db.create_table('allotter_profile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('roll_number', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('dob', self.gf('django.db.models.fields.DateTimeField')()),
            ('category', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal('allotter', ['Profile'])

        # Adding model 'Application'
        db.create_table('allotter_application', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('profile', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['allotter.Profile'])),
            ('exam_taken', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['allotter.Exam'])),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=24)),
            ('editable', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('allotter', ['Application'])

        # Adding M2M table for field options on 'Application'
        db.create_table('allotter_application_options', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('application', models.ForeignKey(orm['allotter.application'], null=False)),
            ('option', models.ForeignKey(orm['allotter.option'], null=False))
        ))
        db.create_unique('allotter_application_options', ['application_id', 'option_id'])


    def backwards(self, orm):
        
        # Deleting model 'Option'
        db.delete_table('allotter_option')

        # Deleting model 'Exam'
        db.delete_table('allotter_exam')

        # Deleting model 'Profile'
        db.delete_table('allotter_profile')

        # Deleting model 'Application'
        db.delete_table('allotter_application')

        # Removing M2M table for field options on 'Application'
        db.delete_table('allotter_application_options')


    models = {
        'allotter.application': {
            'Meta': {'object_name': 'Application'},
            'editable': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'exam_taken': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['allotter.Exam']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'options': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['allotter.Option']", 'symmetrical': 'False'}),
            'profile': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['allotter.Profile']"}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '24'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'allotter.exam': {
            'Meta': {'object_name': 'Exam'},
            'exam_code': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'exam_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'allotter.option': {
            'Meta': {'object_name': 'Option'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'opt_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'seats': ('django.db.models.fields.IntegerField', [], {})
        },
        'allotter.profile': {
            'Meta': {'object_name': 'Profile'},
            'category': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'dob': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'roll_number': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
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
