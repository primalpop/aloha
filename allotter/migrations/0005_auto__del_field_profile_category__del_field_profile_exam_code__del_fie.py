# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'Profile.category'
        db.delete_column('allotter_profile', 'category')

        # Deleting field 'Profile.exam_code'
        db.delete_column('allotter_profile', 'exam_code')

        # Deleting field 'Profile.application_number'
        db.delete_column('allotter_profile', 'application_number')

        # Deleting field 'Profile.pd'
        db.delete_column('allotter_profile', 'pd')

        # Deleting field 'Profile.gender'
        db.delete_column('allotter_profile', 'gender')

        # Deleting field 'Profile.rank'
        db.delete_column('allotter_profile', 'rank')

        # Deleting field 'Option.seats'
        db.delete_column('allotter_option', 'seats')

        # Adding field 'Option.opt_code'
        db.add_column('allotter_option', 'opt_code', self.gf('django.db.models.fields.IntegerField')(default='', max_length=3), keep_default=False)

        # Deleting field 'Application.status'
        db.delete_column('allotter_application', 'status')

        # Deleting field 'Application.exam_taken'
        db.delete_column('allotter_application', 'exam_taken_id')

        # Deleting field 'Application.editable'
        db.delete_column('allotter_application', 'editable')

        # Adding field 'Application.options_selected'
        db.add_column('allotter_application', 'options_selected', self.gf('django.db.models.fields.CharField')(default='', max_length=5000), keep_default=False)

        # Adding field 'Application.np'
        db.add_column('allotter_application', 'np', self.gf('django.db.models.fields.IntegerField')(default=1, max_length=2), keep_default=False)

        # Adding field 'Application.first_paper'
        db.add_column('allotter_application', 'first_paper', self.gf('django.db.models.fields.related.ForeignKey')(default='', related_name='first_paper', to=orm['allotter.Exam']), keep_default=False)

        # Adding field 'Application.second_paper'
        db.add_column('allotter_application', 'second_paper', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='second_paper', null=True, to=orm['allotter.Exam']), keep_default=False)

        # Adding field 'Application.nat'
        db.add_column('allotter_application', 'nat', self.gf('django.db.models.fields.CharField')(default='', max_length=10), keep_default=False)

        # Adding field 'Application.gender'
        db.add_column('allotter_application', 'gender', self.gf('django.db.models.fields.CharField')(default='', max_length=2), keep_default=False)

        # Adding field 'Application.cent'
        db.add_column('allotter_application', 'cent', self.gf('django.db.models.fields.IntegerField')(default='', max_length=10), keep_default=False)

        # Adding field 'Application.cgy'
        db.add_column('allotter_application', 'cgy', self.gf('django.db.models.fields.CharField')(default='', max_length=10), keep_default=False)

        # Adding field 'Application.pd'
        db.add_column('allotter_application', 'pd', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)

        # Removing M2M table for field options on 'Application'
        db.delete_table('allotter_application_options')


    def backwards(self, orm):
        
        # Adding field 'Profile.category'
        db.add_column('allotter_profile', 'category', self.gf('django.db.models.fields.CharField')(default='', max_length=30), keep_default=False)

        # Adding field 'Profile.exam_code'
        db.add_column('allotter_profile', 'exam_code', self.gf('django.db.models.fields.CharField')(default='', max_length=30), keep_default=False)

        # Adding field 'Profile.application_number'
        db.add_column('allotter_profile', 'application_number', self.gf('django.db.models.fields.IntegerField')(default='', max_length=20), keep_default=False)

        # Adding field 'Profile.pd'
        db.add_column('allotter_profile', 'pd', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)

        # Adding field 'Profile.gender'
        db.add_column('allotter_profile', 'gender', self.gf('django.db.models.fields.CharField')(default='', max_length=10), keep_default=False)

        # Adding field 'Profile.rank'
        db.add_column('allotter_profile', 'rank', self.gf('django.db.models.fields.IntegerField')(default='', max_length=6), keep_default=False)

        # Adding field 'Option.seats'
        db.add_column('allotter_option', 'seats', self.gf('django.db.models.fields.IntegerField')(default=''), keep_default=False)

        # Deleting field 'Option.opt_code'
        db.delete_column('allotter_option', 'opt_code')

        # Adding field 'Application.status'
        db.add_column('allotter_application', 'status', self.gf('django.db.models.fields.CharField')(default='', max_length=24), keep_default=False)

        # Adding field 'Application.exam_taken'
        db.add_column('allotter_application', 'exam_taken', self.gf('django.db.models.fields.related.ForeignKey')(default='', to=orm['allotter.Exam']), keep_default=False)

        # Adding field 'Application.editable'
        db.add_column('allotter_application', 'editable', self.gf('django.db.models.fields.BooleanField')(default=True), keep_default=False)

        # Deleting field 'Application.options_selected'
        db.delete_column('allotter_application', 'options_selected')

        # Deleting field 'Application.np'
        db.delete_column('allotter_application', 'np')

        # Deleting field 'Application.first_paper'
        db.delete_column('allotter_application', 'first_paper_id')

        # Deleting field 'Application.second_paper'
        db.delete_column('allotter_application', 'second_paper_id')

        # Deleting field 'Application.nat'
        db.delete_column('allotter_application', 'nat')

        # Deleting field 'Application.gender'
        db.delete_column('allotter_application', 'gender')

        # Deleting field 'Application.cent'
        db.delete_column('allotter_application', 'cent')

        # Deleting field 'Application.cgy'
        db.delete_column('allotter_application', 'cgy')

        # Deleting field 'Application.pd'
        db.delete_column('allotter_application', 'pd')

        # Adding M2M table for field options on 'Application'
        db.create_table('allotter_application_options', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('application', models.ForeignKey(orm['allotter.application'], null=False)),
            ('option', models.ForeignKey(orm['allotter.option'], null=False))
        ))
        db.create_unique('allotter_application_options', ['application_id', 'option_id'])


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
            'options_selected': ('django.db.models.fields.CharField', [], {'max_length': '5000'}),
            'pd': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'profile': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['allotter.Profile']"}),
            'second_paper': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'second_paper'", 'null': 'True', 'to': "orm['allotter.Exam']"}),
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
            'exam': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['allotter.Exam']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'opt_code': ('django.db.models.fields.IntegerField', [], {'max_length': '3'}),
            'opt_name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'allotter.profile': {
            'Meta': {'object_name': 'Profile'},
            'dob': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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
