# Generated by Django 2.2.13 on 2020-06-22 18:26

import colorfield.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0011_auto_20200622_0312'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='brand_color_1',
            field=colorfield.fields.ColorField(default='#6F2EFF', max_length=18),
        ),
        migrations.AlterField(
            model_name='event',
            name='brand_color_2',
            field=colorfield.fields.ColorField(default='#6F2EFF', max_length=18),
        ),
        migrations.AlterField(
            model_name='event',
            name='brand_color_3',
            field=colorfield.fields.ColorField(default='#6F2EFF', max_length=18),
        ),
    ]