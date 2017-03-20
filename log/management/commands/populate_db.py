# -*- coding: utf-8 -*-
"""
Created on Sat Mar 18 01:23:36 2017

@author: THANGLONG
"""
import os

from django.core.management.base import BaseCommand

import csv
import spotipy
import unicodedata


from PyLyrics import *
from log.models import Tracks




## il faudrait prendre le chemin du fichier csv et copier les fichiers enfin les lire 
class Command(BaseCommand):
    def _create_tracks(self):
        print os.getcwd()
        sp = spotipy.Spotify()
        with open('log/static/list/song_list.csv', 'rb') as csvfile:
            text = csv.reader(csvfile, delimiter=';')
            next(text)
            ## on skip la 1ere ligne/header
            for row in text:
#                print row[0]
                results = sp.search(q=row[0], limit=1,type='track')
                d=results['tracks']['items'][0]['name']
                dd=unicodedata.normalize('NFKD',d).encode('ascii','ignore')
                
                ## il existe un featuring
                if len(dd.split("("))==2:
                    print 2
                    print dd.split("(")[0].strip()
                    ## strip enleve les espaces
                    print dd[dd.find("(")+1:dd.find(")")]
                    track_name=dd.split("(")[0].strip()
                    featuring=dd[dd.find("(")+1:dd.find(")")]
                else:
                    print 1
                    print dd
                    track_name=dd
                track_pseudo=track_name.replace(' ','_').lower()
                track_popularity=results['tracks']['items'][0]['popularity']
                Album_name=results['tracks']['items'][0]['album']['artists'][0]['name'].encode('utf-8')
                Album_cover=results['tracks']['items'][0]['album']['images'][0]['url'].encode('utf-8')
                Artist=results['tracks']['items'][0]['album']['artists'][0]['name'].encode('utf-8')
                preview=results['tracks']['items'][0]['preview_url'].encode('utf-8')
                track_link=Artist.replace(' ','_')+'_'+track_name.replace(' ','_')
                
                
                results = sp.search(q=row[1],type='artist')
                Artist_image=results['artists']['items'][0]['images'][2]['url'].encode('utf-8')
                Artist_popularity=results['artists']['items'][0]['popularity']
                print track_pseudo
                print track_popularity
                print Album_name
                print Album_cover
                print preview
                print track_link     
                print track_name
                print Artist_image
                print Artist_popularity
                
#                a=Tracks(
#                        track_name=track_name,
#                        track_pseudo=track_name.replace('','_').lower(),
#                        track_popularity=track_popularity,
#                        track_genre=row[3],
#                        Artist=Artist,
#                        track_link=track_link,
#                        Artist_popularity=Artist_popularity,
#                        Artist_image=Artist_image,
#                        Album_name=Album_name,
#                        Album_cover=Album_cover,
#                        duration=row[2],
#                        preview=preview,
#                        featuring=featuring)
#                a.save()
#                print os.path.join(os.getcwd(), "log/static/lyrics/" + track_link+ ".txt")
                
            
                try:
                  
                    lyrics=PyLyrics.getLyrics(row[1],row[0]).replace('\n','<br>')
                    lyrics=unicodedata.normalize('NFKD',lyrics).encode('ascii','ignore')
                    
                    text=open("log/static/lyrics/" + track_link+ ".txt", 'a')
                    text.write(lyrics)
                    text.close()
                                
                except Exception as e:
                    print str(e)
                    print 'artist '+ row[1]
                    print 'track name '+row[0]
                    
                    
                        
    

    def handle(self, *args, **options):
        self._create_tracks()