# Generated by Django 2.2.13 on 2020-06-23 23:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0014_auto_20200623_2332'),
    ]

    operations = [
        migrations.RenameField(
            model_name='note',
            old_name='content',
            new_name='text',
        ),
    ]
