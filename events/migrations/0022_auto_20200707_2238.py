# Generated by Django 2.2.13 on 2020-07-07 22:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0021_speaker_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='speaker',
            name='slug',
            field=models.SlugField(default=None, max_length=149),
        ),
    ]
