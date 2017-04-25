#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 16:58:22 2017

@author: thang-long
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Mar 18 01:23:36 2017

@author: THANGLONG
"""
import os

from django.core.management.base import BaseCommand

import csv


from django.conf import settings



from log.models import Tracks




## il faudrait prendre le chemin du fichier csv et copier les fichiers enfin les lire 
class Command(BaseCommand):
    def _create_tracks(self):
        k=0
        c=Tracks.objects.all()
        artists_list={}
        for i in c:
             if (i.Artist not in artists_list.keys()):
                 artists_list[i.Artist]=k
                 print k
                 k=k+1             
#                

        s=sorted(artists_list)
        new={}
        k=0
        for i in s:
            print i
            new[i]=k
            k=k+1
        print new
        print new.items()
        
        url=os.path.join(settings.STATIC_ROOT, 'csv/artists_list.csv')
        # open csv file
        with open(url, "w") as myfile:            
            w = csv.writer(myfile,delimiter=',')
            for key, val in new.items():
                w.writerow([key, val])
        
    

                
                    
    

    def handle(self, *args, **options):
        self._create_tracks()       