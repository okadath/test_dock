# Generated by Django 2.2.13 on 2020-07-08 00:50

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0022_auto_20200707_2238'),
    ]

    operations = [
        migrations.RenameField(
            model_name='liveplayer',
            old_name='pre_live_video',
            new_name='placeholder_video',
        ),
        migrations.RenameField(
            model_name='liveplayer',
            old_name='simmulated_live',
            new_name='simulated_live',
        ),
        migrations.RemoveField(
            model_name='liveplayer',
            name='end_date',
        ),
        migrations.RemoveField(
            model_name='liveplayer',
            name='start_date',
        ),
        migrations.RemoveField(
            model_name='liveplayer',
            name='type_video',
        ),
        migrations.AddField(
            model_name='liveplayer',
            name='simulated_live_ends',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='liveplayer',
            name='simulated_live_start',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='liveplayer',
            name='use_live_video',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='liveplayer',
            name='use_placeholder_video',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='liveplayer',
            name='use_simulated_live',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='room',
            name='placeholder_video',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='room',
            name='simulated_live',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='room',
            name='simulated_live_ends',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='room',
            name='simulated_live_start',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='room',
            name='use_live_video',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='room',
            name='use_placeholder_video',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='room',
            name='use_simulated_live',
            field=models.BooleanField(default=False),
        ),
    ]
