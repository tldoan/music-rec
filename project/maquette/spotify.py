# -*- coding: utf-8 -*-
"""
Created on Wed Mar 01 18:36:17 2017

@author: tdoan8
"""

from log.models import Tracks
import os

import spotipy
sp = spotipy.Spotify()
#results = sp.search(q='the weeknd - the hills', limit=1,type='track')
#results = sp.search(q='Ed Sheeran - Shape of You', limit=1,type='track') 
results = sp.search(q='The Chainsmokers – Closer', limit=1,type='track') 

a=Tracks(
        track_name=results['tracks']['items'][0]['name'].encode('utf-8'),
        
        
        ###############################
        track_pseudo=results['tracks']['items'][0]['name'].encode('utf-8').replace(' ','_').lower().encode('utf-8'),
        ###############################
        
        track_popularity=results['tracks']['items'][0]['popularity'],
        duration=results['tracks']['items'][0]['duration_ms'],
        preview=results['tracks']['items'][0]['preview_url'].encode('utf-8'),
        
        Artist=results['tracks']['items'][0]['album']['artists'][0]['name'].encode('utf-8'),
        
        track_link=results['tracks']['items'][0]['album']['artists'][0]['name'].encode('utf-8').replace(' ','_')+'_'+results['tracks']['items'][0]['name'].encode('utf-8').replace(' ','_'),

       
        
        
        Album_name=results['tracks']['items'][0]['album']['name'].encode('utf-8'),
        Album_cover=results['tracks']['items'][0]['album']['images'][0]['url'].encode('utf-8'))

r=results['tracks']['items'][0]['album']['artists'][0]['name'].encode('utf-8').replace(' ','_')+'_'+results['tracks']['items'][0]['name'].encode('utf-8').replace(' ','_')


#results = sp.search(q='artist:' + 'the weeknd', type='artist')
#results = sp.search(q='Ed Sheeran',type='artist')
results = sp.search(q='The Chainsmokers',type='artist')


a.Artist_image=results['artists']['items'][0]['images'][2]['url'].encode('utf-8')
a.Artist_popularity=results['artists']['items'][0]['popularity']
        
#l=[]
#for i in results['artists']['items'][0]['genres']:
#    l.append(i.encode('utf-8'))   
#
#a.track_genre=l     

a.save()

        
import lyricwikia
try:
    #lyrics = lyricwikia.get_lyrics("the weeknd","the hills").replace('\n','<br>')
    #lyrics = lyricwikia.get_lyrics("Ed Sheeran","Shape of You").replace('\n','<br>')
    lyrics = lyricwikia.get_lyrics("The Chainsmokers","Closer").replace('\n','<br>')
    
    
except Exception as e:
    print "Exception occurred \n" +str(e)

## pour ed sheeran peut pas download

c=lyrics.encode('utf-8')
c=c.encode('ascii', 'ignore').decode('ascii')

text=open(os.path.join(os.getcwd(), "log/static/lyrics/" + r+ ".txt"), 'a')
text.write(c)
text.close()


   

# a.encode('ascii','ignore')
# a.encode('ascii','replace')

    
    
   
    
   
    
    
    
   
    
  
    
    
   
    
  
        