# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-02 00:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('log', '0021_auto_20170301_1905'),
    ]

    operations = [
        migrations.AddField(
            model_name='tracks',
            name='Artist_image',
            field=models.URLField(blank=True),
        ),
    ]