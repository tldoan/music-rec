# -*- coding: utf-8 -*-
"""
Created on Sat Mar 18 01:23:36 2017

@author: THANGLONG
"""
from django.core.management.base import BaseCommand
from log.models import Tracks

## il faudrait prendre le chemin du fichier csv et copier les fichiers enfin les lire 
class Command(BaseCommand):
    def _create_tracks(self):
        a = Tracks(track_name='Kygo')
        a.save()

    def handle(self, *args, **options):
        self._create_tracks()