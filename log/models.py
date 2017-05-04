# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
#from django.forms import ModelForm
from django.db.models.signals import post_save
from django.dispatch import receiver
from django import forms


from jsonfield import JSONField
from django.conf import settings
import os
import numpy as np
   
       

class Profile(models.Model):  
                
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # La liaison OneToOne vers le modèle User
    region = models.CharField(default='', max_length=30)
    area = models.CharField(default='',max_length=30)
    #age = models.CharField(choices=age_range,max_length=30)
    age = models.CharField(default='',max_length=30)
    sex = models.CharField(default='',max_length=30)

    def __str__(self):
        return "Profil de {0}".format(self.user.username)

    
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)


User.profile = property(lambda u:Profile.objects.get_or_create(user=u)[0])






class Tracks(models.Model):
    track_name=models.CharField(default='',max_length=250)
    track_pseudo=models.CharField(default='',max_length=250)
    track_popularity=models.FloatField(default=0)
    track_genre=models.CharField(default='pop',max_length=250)
    
    
    Artist=models.CharField(default='',max_length=250)
    
    track_link=models.CharField(default='',max_length=250)
    
    Artist_popularity=models.FloatField(default=0)
    #Artist_genre=models.CharField(default='',max_length=50)
    Artist_image=models.URLField(blank=True)
    
    Album_name=models.CharField(default='',max_length=250)
    Album_cover=models.URLField(blank=True)
    
    #lyrics=models.CharField(default='',max_length=250) ## save in a text file
    
    duration=models.FloatField(default=0)  ## lenght of the song in ms
    preview=models.URLField(blank=True)  ## preview of 30sec
    nb_rating=models.IntegerField(default=1)
    
    featuring=models.CharField(default='',max_length=250,blank=True)
    #wordcloud=models.CharField(default='',max_length=250)
    
    acousticness=models.FloatField(default=0)
    danceability=models.FloatField(default=0) 
    energy=models.FloatField(default=0)
    instrumentalness=models.FloatField(default=0)
    key=models.IntegerField(default=0)
    liveness=models.FloatField(default=0)
    loudness=models.IntegerField(default=0)
    speechiness=models.FloatField(default=0)
    tempo=models.FloatField(default=0)
    time_signature=models.IntegerField(default=0)
    valence=models.FloatField(default=0)
    
    def __str__(self):
        return self.track_name
    

class Track_Coments(models.Model):
    user=models.ForeignKey(User)
    track=models.ForeignKey(Tracks, on_delete=models.CASCADE)
    rating=models.FloatField(default=0)
    wordcloud=models.CharField(default='',max_length=250)
    time=models.DateTimeField()
    
def my_default():
    return ['']

#def gen():
#    caracteres = string.ascii_letters + string.digits
#    aleatoire = [random.choice(caracteres) for _ in range(6)]
#    return ''.join(aleatoire)
 
class Traj(models.Model):
    user=models.ForeignKey(User)
    path=JSONField(default=my_default)
    start_time = models.DateTimeField(auto_now_add=True, auto_now=False) 
    key=models.CharField(default='',max_length=50)
    def append(self,txt):
        self.path.append(txt)

    def __str__(self):  # __unicode__ on Python 2
       return self.key

   
def default_songs():
    songs_list=np.load(os.path.join(settings.STATIC_ROOT, 'data/songs_list.npy')).item()
    novelty={}
    for i in songs_list:
        novelty[i]=np.ones(shape=(len(songs_list[i]),1))*5
    return novelty
    
    
    
    
class history(models.Model):
    user=models.ForeignKey(User)
    path=JSONField(default=my_default)
    start_time = models.DateTimeField(auto_now_add=True, auto_now=False) 
    key_traj=JSONField(default=my_default)
    novelty=JSONField(default=default_songs)
    
    def append(self,txt):
        self.path.append(txt)
        
    def append_key(self,txt):
        self.key_traj.append(txt)
        
    def __str__(self):  # __unicode__ on Python 2
       return 'history'
    

    
    
    
    
    
