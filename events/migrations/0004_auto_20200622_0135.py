# Generated by Django 2.2.13 on 2020-06-22 01:35

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_auto_20200622_0119'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='client',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='event_client', to='events.Client'),
        ),
        migrations.AlterField(
            model_name='event',
            name='slug',
            field=models.SlugField(default='my_name', max_length=149),
        ),
        migrations.CreateModel(
            name='LivePlayer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_video', models.PositiveSmallIntegerField(choices=[(1, 'Live'), (2, 'SimulatedLive'), (3, 'VideoPlaceholder')], default=1)),
                ('live_video', models.TextField(blank=True, null=True)),
                ('simmulated_live', models.TextField(blank=True, null=True)),
                ('start_date', models.DateField(default=django.utils.timezone.now)),
                ('end_date', models.DateField(default=django.utils.timezone.now)),
                ('thumbnail', models.FileField(blank=True, null=True, upload_to='pictures/')),
                ('pre_live_video', models.TextField(blank=True, null=True)),
                ('event', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='liveplayer_event', to='events.Event')),
            ],
        ),
        migrations.CreateModel(
            name='Landing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='landing_event', to='events.Event')),
            ],
        ),
    ]
