# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Article.end_publishing_date'
        db.add_column('aldryn_newsblog_article', 'end_publishing_date',
                      self.gf('django.db.models.fields.DateTimeField')(null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Article.end_publishing_date'
        db.delete_column('aldryn_newsblog_article', 'end_publishing_date')


    models = {
        'aldryn_categories.category': {
            'Meta': {'object_name': 'Category'},
            'depth': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'rgt': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'aldryn_newsblog.article': {
            'Meta': {'object_name': 'Article', 'ordering': "['-publishing_date']"},
            'app_config': ('aldryn_apphooks_config.fields.AppHookConfigField', [], {'to': "orm['aldryn_newsblog.NewsBlogConfig']"}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'to': "orm['aldryn_people.Person']", 'null': 'True'}),
            'categories': ('aldryn_categories.fields.CategoryManyToManyField', [], {'blank': 'True', 'to': "orm['aldryn_categories.Category']", 'symmetrical': 'False'}),
            'content': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.Placeholder']", 'related_name': "'newsblog_article_content'", 'null': 'True'}),
            'end_publishing_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'featured_image': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'to': "orm['filer.Image']", 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_featured': ('django.db.models.fields.BooleanField', [], {'db_index': 'True', 'default': 'False'}),
            'is_published': ('django.db.models.fields.BooleanField', [], {'db_index': 'True', 'default': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'publishing_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'related': ('sortedm2m.fields.SortedManyToManyField', [], {'blank': 'True', 'to': "orm['aldryn_newsblog.Article']", 'related_name': "'related_rel_+'"})
        },
        'aldryn_newsblog.articletranslation': {
            'Meta': {'object_name': 'ArticleTranslation', 'db_table': "'aldryn_newsblog_article_translation'", 'unique_together': "[('language_code', 'slug'), ('language_code', 'master')]"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language_code': ('django.db.models.fields.CharField', [], {'max_length': '15', 'db_index': 'True'}),
            'lead_in': ('djangocms_text_ckeditor.fields.HTMLField', [], {'blank': 'True', 'default': "''"}),
            'master': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['aldryn_newsblog.Article']", 'related_name': "'translations'", 'null': 'True'}),
            'meta_description': ('django.db.models.fields.TextField', [], {'blank': 'True', 'default': "''"}),
            'meta_keywords': ('django.db.models.fields.TextField', [], {'blank': 'True', 'default': "''"}),
            'meta_title': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '255', 'default': "''"}),
            'search_data': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'blank': 'True', 'max_length': '255'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '234'})
        },
        'aldryn_newsblog.newsblogarchiveplugin': {
            'Meta': {'object_name': 'NewsBlogArchivePlugin'},
            'app_config': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['aldryn_newsblog.NewsBlogConfig']"}),
            'cmsplugin_ptr': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'to': "orm['cms.CMSPlugin']", 'primary_key': 'True', 'related_name': "'+'"})
        },
        'aldryn_newsblog.newsblogarticlesearchplugin': {
            'Meta': {'object_name': 'NewsBlogArticleSearchPlugin'},
            'app_config': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['aldryn_newsblog.NewsBlogConfig']"}),
            'cmsplugin_ptr': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'to': "orm['cms.CMSPlugin']", 'primary_key': 'True', 'related_name': "'+'"}),
            'max_articles': ('django.db.models.fields.PositiveIntegerField', [], {'default': '10'})
        },
        'aldryn_newsblog.newsblogauthorsplugin': {
            'Meta': {'object_name': 'NewsBlogAuthorsPlugin'},
            'app_config': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['aldryn_newsblog.NewsBlogConfig']"}),
            'cmsplugin_ptr': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'to': "orm['cms.CMSPlugin']", 'primary_key': 'True', 'related_name': "'+'"})
        },
        'aldryn_newsblog.newsblogcategoriesplugin': {
            'Meta': {'object_name': 'NewsBlogCategoriesPlugin'},
            'app_config': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['aldryn_newsblog.NewsBlogConfig']"}),
            'cmsplugin_ptr': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'to': "orm['cms.CMSPlugin']", 'primary_key': 'True', 'related_name': "'+'"})
        },
        'aldryn_newsblog.newsblogconfig': {
            'Meta': {'object_name': 'NewsBlogConfig'},
            'app_data': ('app_data.fields.AppDataField', [], {'default': "'{}'"}),
            'create_authors': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'namespace': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100', 'default': 'None'}),
            'non_permalink_handling': ('django.db.models.fields.SmallIntegerField', [], {'default': '302'}),
            'paginate_by': ('django.db.models.fields.PositiveIntegerField', [], {'default': '5'}),
            'permalink_type': ('django.db.models.fields.CharField', [], {'max_length': '8', 'default': "'slug'"}),
            'placeholder_base_sidebar': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.Placeholder']", 'related_name': "'aldryn_newsblog_base_sidebar'", 'null': 'True'}),
            'placeholder_base_top': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.Placeholder']", 'related_name': "'aldryn_newsblog_base_top'", 'null': 'True'}),
            'placeholder_detail_bottom': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.Placeholder']", 'related_name': "'aldryn_newsblog_detail_bottom'", 'null': 'True'}),
            'placeholder_detail_footer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.Placeholder']", 'related_name': "'aldryn_newsblog_detail_footer'", 'null': 'True'}),
            'placeholder_detail_top': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.Placeholder']", 'related_name': "'aldryn_newsblog_detail_top'", 'null': 'True'}),
            'placeholder_list_footer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.Placeholder']", 'related_name': "'aldryn_newsblog_list_footer'", 'null': 'True'}),
            'placeholder_list_top': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.Placeholder']", 'related_name': "'aldryn_newsblog_list_top'", 'null': 'True'}),
            'search_indexed': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'template_prefix': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '20', 'null': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'aldryn_newsblog.newsblogconfigtranslation': {
            'Meta': {'object_name': 'NewsBlogConfigTranslation', 'db_table': "'aldryn_newsblog_newsblogconfig_translation'", 'unique_together': "[('language_code', 'master')]"},
            'app_title': ('django.db.models.fields.CharField', [], {'max_length': '234'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language_code': ('django.db.models.fields.CharField', [], {'max_length': '15', 'db_index': 'True'}),
            'master': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['aldryn_newsblog.NewsBlogConfig']", 'related_name': "'translations'", 'null': 'True'})
        },
        'aldryn_newsblog.newsblogfeaturedarticlesplugin': {
            'Meta': {'object_name': 'NewsBlogFeaturedArticlesPlugin'},
            'app_config': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['aldryn_newsblog.NewsBlogConfig']"}),
            'article_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'cmsplugin_ptr': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'to': "orm['cms.CMSPlugin']", 'primary_key': 'True', 'related_name': "'+'"})
        },
        'aldryn_newsblog.newsbloglatestarticlesplugin': {
            'Meta': {'object_name': 'NewsBlogLatestArticlesPlugin'},
            'app_config': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['aldryn_newsblog.NewsBlogConfig']"}),
            'cmsplugin_ptr': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'to': "orm['cms.CMSPlugin']", 'primary_key': 'True', 'related_name': "'+'"}),
            'latest_articles': ('django.db.models.fields.IntegerField', [], {'default': '5'})
        },
        'aldryn_newsblog.newsblogrelatedplugin': {
            'Meta': {'_ormbases': ['cms.CMSPlugin'], 'object_name': 'NewsBlogRelatedPlugin'},
            'cmsplugin_ptr': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'to': "orm['cms.CMSPlugin']", 'primary_key': 'True', 'related_name': "'+'"})
        },
        'aldryn_newsblog.newsblogtagsplugin': {
            'Meta': {'object_name': 'NewsBlogTagsPlugin'},
            'app_config': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['aldryn_newsblog.NewsBlogConfig']"}),
            'cmsplugin_ptr': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'to': "orm['cms.CMSPlugin']", 'primary_key': 'True', 'related_name': "'+'"})
        },
        'aldryn_people.group': {
            'Meta': {'object_name': 'Group'},
            'address': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '255'}),
            'email': ('django.db.models.fields.EmailField', [], {'blank': 'True', 'max_length': '75', 'default': "''"}),
            'fax': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '100', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '100', 'null': 'True'}),
            'postal_code': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '20'}),
            'website': ('django.db.models.fields.URLField', [], {'blank': 'True', 'max_length': '200', 'null': 'True'})
        },
        'aldryn_people.person': {
            'Meta': {'object_name': 'Person'},
            'email': ('django.db.models.fields.EmailField', [], {'blank': 'True', 'max_length': '75', 'default': "''"}),
            'fax': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '100', 'null': 'True'}),
            'groups': ('aldryn_common.admin_fields.sortedm2m.SortedM2MModelField', [], {'blank': 'True', 'to': "orm['aldryn_people.Group']", 'symmetrical': 'False', 'default': 'None', 'related_name': "'people'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mobile': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '100', 'null': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '100', 'null': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'unique': 'True', 'related_name': "'persons'", 'null': 'True', 'to': "orm['auth.User']"}),
            'vcard_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'visual': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'on_delete': 'models.SET_NULL', 'default': 'None', 'null': 'True', 'to': "orm['filer.Image']"}),
            'website': ('django.db.models.fields.URLField', [], {'blank': 'True', 'max_length': '200', 'null': 'True'})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'to': "orm['auth.Permission']", 'symmetrical': 'False'})
        },
        'auth.permission': {
            'Meta': {'object_name': 'Permission', 'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)"},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'blank': 'True', 'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'to': "orm['auth.Group']", 'symmetrical': 'False', 'related_name': "'user_set'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'to': "orm['auth.Permission']", 'symmetrical': 'False', 'related_name': "'user_set'"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'cms.cmsplugin': {
            'Meta': {'object_name': 'CMSPlugin'},
            'changed_date': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now': 'True'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'depth': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '15', 'db_index': 'True'}),
            'numchild': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'to': "orm['cms.CMSPlugin']", 'null': 'True'}),
            'path': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'placeholder': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.Placeholder']", 'null': 'True'}),
            'plugin_type': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'}),
            'position': ('django.db.models.fields.PositiveSmallIntegerField', [], {'blank': 'True', 'null': 'True'})
        },
        'cms.placeholder': {
            'Meta': {'object_name': 'Placeholder'},
            'default_width': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slot': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'object_name': 'ContentType', 'db_table': "'django_content_type'", 'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'filer.file': {
            'Meta': {'object_name': 'File'},
            '_file_size': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True', 'null': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'blank': 'True', 'max_length': '255', 'null': 'True'}),
            'folder': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'to': "orm['filer.Folder']", 'null': 'True', 'related_name': "'all_files'"}),
            'has_all_mandatory_data': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '255', 'default': "''"}),
            'original_filename': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '255', 'null': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'to': "orm['auth.User']", 'null': 'True', 'related_name': "'owned_files'"}),
            'polymorphic_ctype': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'related_name': "'polymorphic_filer.file_set+'", 'null': 'True'}),
            'sha1': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '40', 'default': "''"}),
            'uploaded_at': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'})
        },
        'filer.folder': {
            'Meta': {'object_name': 'Folder', 'ordering': "('name',)", 'unique_together': "(('parent', 'name'),)"},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'to': "orm['auth.User']", 'null': 'True', 'related_name': "'filer_owned_folders'"}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'to': "orm['filer.Folder']", 'null': 'True', 'related_name': "'children'"}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'uploaded_at': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'})
        },
        'filer.image': {
            'Meta': {'object_name': 'Image'},
            '_height': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            '_width': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'author': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '255', 'null': 'True'}),
            'date_taken': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'null': 'True'}),
            'default_alt_text': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '255', 'null': 'True'}),
            'default_caption': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '255', 'null': 'True'}),
            'file_ptr': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'to': "orm['filer.File']", 'primary_key': 'True'}),
            'must_always_publish_author_credit': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'must_always_publish_copyright': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'subject_location': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '64', 'null': 'True', 'default': 'None'})
        }
    }

    complete_apps = ['aldryn_newsblog']