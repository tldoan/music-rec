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
from django.conf import settings
import os


from log.models import Tracks
from spotipy.oauth2 import SpotifyClientCredentials

#from PyLyrics import *
import lyricwikia

import re
from six.moves import urllib

from bs4 import BeautifulSoup


from tinytag import TinyTag

## il faudrait prendre le chemin du fichier csv et copier les fichiers enfin les lire 
class Command(BaseCommand):
    def _create_tracks(self):
        
        print os.getcwd()
        client_credentials_manager = SpotifyClientCredentials('980cf3bf846147ef8ed6f1a108a3507b', '01d3ffa8764d4b53951280395b4c488d')
        sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

        sp.trace=False
        
        url=os.path.join(settings.STATIC_ROOT, 'list/song_list-Copy.csv')

        k=1
        with open(url, 'rb') as csvfile:
            text = csv.reader(csvfile, delimiter=',')
            next(text)

            for row in text: 

                if row[0]=='Mercy':
                     url='/home/thang/Songs/Shawn_Mendes_Mercy.m4a'
                     tag = TinyTag.get(url)
                     duration=tag.duration
                     if not Tracks.objects.filter(track_pseudo='mercy',Artist='Shawn Mendes').exists():
        	                    a=Tracks(
        	                    track_name='Mercy',
        	                    track_pseudo='mercy',
        	                    track_popularity=float(4.0),
        	                    track_genre='Pop',
        	                    Artist='Shawn Mendes',
        	                    track_link='Shawn_Mendes_Mercy',
        	                    Artist_popularity=84.0,
        	                    Artist_image='https://i.scdn.co/image/9a3488787c85c2b250b41f9cc11bd680e1bc10ff',
        	                    Album_name='Illuminate (Deluxe)',
        	                    Album_cover='https://i.scdn.co/image/0c1fe77b4d329bebc8c8e17cc448101a966e1307',
        	    
        	                    duration=duration,
        	    
        	                    preview="https://p.scdn.co/mp3-preview/3a3c613df5bd4c2fb42d1316c225f0b3dd1b281a?cid=980cf3bf846147ef8ed6f1a108a3507b",
        	                    featuring='',
        	                    acousticness=0.113,
        	                    danceability=0.568,
        	                    energy=0.686,
        	                    instrumentalness=0,
        	                    key=11,
        	                    liveness=0.11,
        	                    loudness=-4,
        	                    speechiness=0.0903,
        	                    tempo=148.294,
        	                    time_signature=4,
        	                    valence=0.38 )
        	    
        	                    a.save()
        	                    print k
        	                    k=k+1
                else:

        		        results = sp.search(q=row[0]+' - '+row[1], limit=1,type='track')
        
        		        
        		        
        		        d=results['tracks']['items'][0]['name']
        		        dd=unicodedata.normalize('NFKD',d).encode('ascii','ignore')
        		        r=[word[0].upper() + word[1:] for word in dd.split()]
        		        dd=" ".join(r)
        		        dd=dd.replace(' - With Camila Cabello','')
        		        dd=dd.replace(' (Original Song From DreamWorks Animation\'s "TROLLS")','')
        		        dd=dd.replace('How Far I\'ll Go - From "Moana"',"How Far I'll Go - From Moana")
        		        dd=dd.replace('ISpy','iSpy')
        		        dd=dd.replace('(Cry)','Cry').replace('PILLOWTALK','Pillowtalk')
        		       
        		        ## il existe un featuring
        		        if len(dd.split("("))==2:
        
        		            track_name=dd.split("(")[0].strip()
        		            featuring=dd[dd.find("(")+1:dd.find(")")]
        		        else:
        		            track_name=dd
        		            featuring=''
        		            
        		        
        		        track_popularity=round(float(results['tracks']['items'][0]['popularity'])/20,2)
        		        Album_name=results['tracks']['items'][0]['album']['name'].encode('utf-8').replace("Jonat\xc3\xa1n S\xc3\xa1nchez",'Jonatan Sanchez')
        		        Album_cover=results['tracks']['items'][0]['album']['images'][0]['url'].encode('utf-8')
        
        		        Artist=results['tracks']['items'][0]['album']['artists'][0]['name'].encode('utf-8')
        		        if track_name=="How Far I'll Go":
        		            Artist="Auli'i Cravalho"
        		        if Artist=='Various Artists' and track_name=="CAN'T STOP THE FEELING!":
        		            Artist='Justin Timberlake'
        		        if Artist=='Prince Royce' and track_name=="Deja Vu":
        		            track_name='Deja Vu_'
        		            
        		        track_pseudo=track_name.replace(' ','_').replace("'",'').replace(",","").lower()
        		        
        		        track_pseudo=track_pseudo.replace('h.o.l.y.','holy')
        		        
        		        
        		        Artist=Artist.replace(' & Like Mike','').replace('ZAYN','Zayn')
        		        r=[word[0].upper() + word[1:] for word in Artist.split()]
        		        Artist=" ".join(r)
        		        Artist=Artist.replace('Jory Boy','Bad Bunny').replace("Jonat\xc3\xa1n S\xc3\xa1nchez",'Jonatan Sanchez')
        		        
        		        preview=results['tracks']['items'][0]['preview_url'].encode('utf-8')
        		        track_link=Artist.replace(' ','_')+'_'+track_name.replace(' ','_')
        		      
        		        url='/home/thang/Songs/'+track_link+'.m4a'
        
        		        
        		        
        		        tag = TinyTag.get(url)
        		        duration=tag.duration
        		      
        		   
        		        
        		        id_=results['tracks']['items'][0]['id'].encode('utf-8')
        		        
        		        
        		        results = sp.search(q=row[1],type='artist')
        		        Artist_image=results['artists']['items'][0]['images'][2]['url'].encode('utf-8')
        		        Artist_popularity=results['artists']['items'][0]['popularity']

        		        
        		        
        		        features = sp.audio_features(id_)
        		        
        		        
        		        acousticness=features[0]['acousticness']
        		        danceability=features[0]['danceability']
        		        energy=features[0]['energy']
        		        instrumentalness=features[0]['instrumentalness']
        		        key=features[0]['key']
        		        liveness=features[0]['liveness']
        		        loudness=features[0]['loudness']
        		        speechiness=features[0]['speechiness']
        		        tempo=features[0]['tempo']
        		        time_signature=features[0]['time_signature']
        		        valence=features[0]['valence']
        
        	                if not Tracks.objects.filter(track_pseudo=track_pseudo,Artist=Artist).exists():
        	                    a=Tracks(
        	                    track_name=track_name,
        	                    track_pseudo=track_pseudo,
        	                    track_popularity=track_popularity,
        	                    track_genre=row[2],
        	                    Artist=Artist,
        	                    track_link=track_link,
        	                    Artist_popularity=Artist_popularity,
        	                    Artist_image=Artist_image,
        	                    Album_name=Album_name,
        	                    Album_cover=Album_cover,
        	    
        	                    duration=duration,
        	    
        	                    preview=preview,
        	                    featuring=featuring,
        	                    acousticness=acousticness,
        	                    danceability=danceability,
        	                    energy=energy,
        	                    instrumentalness=instrumentalness,
        	                    key=key,
        	                    liveness=liveness,
        	                    loudness=loudness,
        	                    speechiness=speechiness,
        	                    tempo=tempo,
        	                    time_signature=time_signature,
        	                    valence=valence )
        	    
        	                    a.save()
        	                    print k
        	                    k=k+1
        	#     
        	
        	
        	
        	                try:    
        	                    try: 
        	                        lyrics = lyricwikia.get_lyrics(row[1], row[0])
        	                        lyrics=unicodedata.normalize('NFKD',lyrics).encode('ascii','ignore').replace('\n','<br>')
        	                                
        	                        text=open("log/static/lyrics/" + track_link+ ".txt", 'a')
        	                        text.write(lyrics)
        	                        text.close()
        	#                        print 'RAS lyricwikia'
        	                    except:  
        	                   
        	                        try:       
        	                            artist = row[1].lower()
        	                            song_title = row[0].lower()
        	                            # remove all except alphanumeric characters from artist and song_title
        	                            artist = re.sub('[^A-Za-z0-9]+', "", artist)
        	                            song_title = re.sub('[^A-Za-z0-9]+', "", song_title)
        	                            
        	                            if artist.startswith("the"):    # remove starting 'the' from artist e.g. the who -> who
        	                                artist = artist[3:]
        	                            url = "http://azlyrics.com/lyrics/"+artist+"/"+song_title+".html"
        	                                    
        	                            content = urllib.request.urlopen(url).read()
        	                            soup = BeautifulSoup(content, 'html.parser')
        	                            lyrics = str(soup)
        	                            # lyrics lies between up_partition and down_partition
        	                            up_partition = '<!-- Usage of azlyrics.com content by any third-party lyrics provider is prohibited by our licensing agreement. Sorry about that. -->'
        	                            down_partition = '<!-- MxM banner -->'
        	                            lyrics = lyrics.split(up_partition)[1]
        	                            lyrics = lyrics.split(down_partition)[0]
        	                            # need brqke lines
        	                            #
        	                            lyrics=lyrics.replace('\n','')
        	                            text=open("log/static/lyrics/" + track_link+ ".txt", 'a')
        	                            text.write(lyrics)
        	                            text.close()
        	                         
        	#                            print 'RAS az lyrics'
        	                      
        	                                        
        	                        except:
        	                            print row[1]+' - '+row[0]
        	                            text=open("log/static/uncomplete/uncomplete.txt", 'a')
        	                            text.write('\n')
        	                            text.write(row[1]+' - '+row[0])
        	                            text.close()
        	                except:
        	                    print 'marche pas'
	 ########################################## DAngerous Woman

               
        results = sp.search(q=" Dangerous Woman - Ariana Grande", limit=3,type='track')
        d=results['tracks']['items'][2]['name']
        dd=unicodedata.normalize('NFKD',d).encode('ascii','ignore')
        track_name=dd
        track_pseudo=track_name.replace(' ','_').lower()
        
        track_popularity=round(float(results['tracks']['items'][2]['popularity'])/20,2)
        Album_name=results['tracks']['items'][2]['album']['name'].encode('utf-8')
        Album_cover=results['tracks']['items'][2]['album']['images'][0]['url'].encode('utf-8')
        preview=results['tracks']['items'][2]['preview_url'].encode('utf-8')
        track_link=Artist.replace(' ','_')+'_'+track_name.replace(' ','_')
        Artist=results['tracks']['items'][2]['artists'][0]['name'].encode('utf-8')
        track_link=Artist.replace(' ','_')+'_'+track_name.replace(' ','_')
        
        url='/home/thang/Songs/'+track_link+'.m4a'
        
        tag = TinyTag.get(url)
        duration=tag.duration
        
        id_=results['tracks']['items'][2]['id'].encode('utf-8')
        
        
        results = sp.search(q='Ariana Grande',type='artist')
        Artist_image=results['artists']['items'][0]['images'][2]['url'].encode('utf-8')
        Artist_popularity=results['artists']['items'][0]['popularity']
        
        features = sp.audio_features(id_)
                
                
        acousticness=features[0]['acousticness']
        danceability=features[0]['danceability']
        energy=features[0]['energy']
        instrumentalness=features[0]['instrumentalness']
        key=features[0]['key']
        liveness=features[0]['liveness']
        loudness=features[0]['loudness']
        speechiness=features[0]['speechiness']
        tempo=features[0]['tempo']
        time_signature=features[0]['time_signature']
        valence=features[0]['valence']
        
        a=Tracks(
                    track_name=track_name,
                    track_pseudo=track_pseudo,
                    track_popularity=track_popularity,
                    track_genre='Pop',
                    Artist=Artist,
                    track_link=track_link,
                    Artist_popularity=Artist_popularity,
                    Artist_image=Artist_image,
                    Album_name=Album_name,
                    Album_cover=Album_cover,
    
                    duration=duration,
    
                    preview=preview,
                    featuring=featuring,
                    acousticness=acousticness,
                    danceability=danceability,
                    energy=energy,
                    instrumentalness=instrumentalness,
                    key=key,
                    liveness=liveness,
                    loudness=loudness,
                    speechiness=speechiness,
                    tempo=tempo,
                    time_signature=time_signature,
                    valence=valence )
    
        a.save()
        
        ############## 24K magic
        
        results = sp.search(q=" 24K Magic - Bruno Mars", limit=3,type='track')
        d=results['tracks']['items'][1]['name']
        dd=unicodedata.normalize('NFKD',d).encode('ascii','ignore')
        track_name=dd
        track_pseudo=track_name.replace(' ','_').lower()
        
        track_popularity=round(float(results['tracks']['items'][1]['popularity'])/20,2)
        Album_name=results['tracks']['items'][1]['album']['name'].encode('utf-8')
        Album_cover=results['tracks']['items'][1]['album']['images'][0]['url'].encode('utf-8')
        preview=results['tracks']['items'][1]['preview_url'].encode('utf-8')
        track_link=Artist.replace(' ','_')+'_'+track_name.replace(' ','_')
        Artist=results['tracks']['items'][1]['artists'][0]['name'].encode('utf-8')
        track_link=Artist.replace(' ','_')+'_'+track_name.replace(' ','_')
        
        url='/home/thang/Songs/'+track_link+'.m4a'
        
        tag = TinyTag.get(url)
        duration=tag.duration
        
        id_=results['tracks']['items'][1]['id'].encode('utf-8')
        
        
        results = sp.search(q='Bruno Mars',type='artist')
        Artist_image=results['artists']['items'][0]['images'][2]['url'].encode('utf-8')
        Artist_popularity=results['artists']['items'][0]['popularity']
        
        features = sp.audio_features(id_)
                
                
        acousticness=features[0]['acousticness']
        danceability=features[0]['danceability']
        energy=features[0]['energy']
        instrumentalness=features[0]['instrumentalness']
        key=features[0]['key']
        liveness=features[0]['liveness']
        loudness=features[0]['loudness']
        speechiness=features[0]['speechiness']
        tempo=features[0]['tempo']
        time_signature=features[0]['time_signature']
        valence=features[0]['valence']
        
        a=Tracks(
                    track_name=track_name,
                    track_pseudo=track_pseudo,
                    track_popularity=track_popularity,
                    track_genre='Pop',
                    Artist=Artist,
                    track_link=track_link,
                    Artist_popularity=Artist_popularity,
                    Artist_image=Artist_image,
                    Album_name=Album_name,
                    Album_cover=Album_cover,
    
                    duration=duration,
    
                    preview=preview,
                    featuring=featuring,
                    acousticness=acousticness,
                    danceability=danceability,
                    energy=energy,
                    instrumentalness=instrumentalness,
                    key=key,
                    liveness=liveness,
                    loudness=loudness,
                    speechiness=speechiness,
                    tempo=tempo,
                    time_signature=time_signature,
                    valence=valence )
    
        a.save()
        
                
                


                
                


                
                    
    

    def handle(self, *args, **options):
        self._create_tracks()       


            

                    
                    
                        
    

