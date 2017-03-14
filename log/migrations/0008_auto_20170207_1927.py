# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-08 00:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('log', '0007_auto_20170207_1846'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='occupation',
            field=models.CharField(choices=[('1', 'undergraduate student'), ('2', 'graduate student'), ('3', 'faculty'), ('4', 'other')], max_length=30),
        ),
        migrations.AlterField(
            model_name='profile',
            name='region',
            field=models.CharField(choices=[('1', 'North America'), ('2', 'South America'), ('3', 'Central America'), ('4', 'Northern Europe'), ('5', 'Europe'), ('6', 'Eastern Europe'), ('8', 'Oceania'), ('9', 'Asia'), ('10', 'Southeast Asia'), ('11', 'Middle East'), ('12', 'North Africa'), ('13', 'Southern Africa')], max_length=30),
        ),
    ]