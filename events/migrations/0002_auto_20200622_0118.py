# Generated by Django 2.2.13 on 2020-06-22 01:18

import colorfield.fields
import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=149, unique=True)),
                ('slug', models.SlugField(default='my_name', max_length=149)),
                ('picture', models.FileField(blank=True, null=True, upload_to='pictures/')),
            ],
        ),
        migrations.AddField(
            model_name='note',
            name='title',
            field=models.CharField(default='', max_length=149),
        ),
        migrations.AlterField(
            model_name='note',
            name='text',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=149, unique=True)),
                ('slug', models.SlugField(default='my name', max_length=149)),
                ('start_date', models.DateField(default=datetime.datetime(2020, 6, 22, 1, 18, 56, 102609, tzinfo=utc))),
                ('end_date', models.DateField(default=datetime.datetime(2020, 6, 22, 1, 18, 56, 102637, tzinfo=utc))),
                ('language', models.CharField(max_length=149, unique=True)),
                ('country', django_countries.fields.CountryField(max_length=2)),
                ('description', models.TextField(blank=True, null=True)),
                ('event_logo', models.FileField(blank=True, null=True, upload_to='pictures/')),
                ('event_banner_1', models.FileField(blank=True, null=True, upload_to='pictures/')),
                ('event_banner_2', models.FileField(blank=True, null=True, upload_to='pictures/')),
                ('have_live_player', models.BooleanField(default=False)),
                ('have_chat', models.BooleanField(default=False)),
                ('brand_color_1', colorfield.fields.ColorField(default='#FF0000', max_length=18)),
                ('brand_color_2', colorfield.fields.ColorField(default='#FF0000', max_length=18)),
                ('brand_color_3', colorfield.fields.ColorField(default='#FF0000', max_length=18)),
                ('client', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='event_client', to='events.Client')),
            ],
        ),
    ]