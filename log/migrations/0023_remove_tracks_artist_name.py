# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-02 00:11
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('log', '0022_tracks_artist_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tracks',
            name='Artist_name',
        ),
    ]