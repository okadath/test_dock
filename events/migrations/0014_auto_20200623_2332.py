# Generated by Django 2.2.13 on 2020-06-23 23:32

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0013_post'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Post',
        ),
        migrations.RemoveField(
            model_name='note',
            name='text',
        ),
        migrations.AddField(
            model_name='note',
            name='content',
            field=ckeditor.fields.RichTextField(default=''),
        ),
    ]
