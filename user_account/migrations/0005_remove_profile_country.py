# Generated by Django 2.2.13 on 2020-06-23 01:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_account', '0004_auto_20200622_2218'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='country',
        ),
    ]
