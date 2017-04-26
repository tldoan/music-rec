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
   
       
rates=[('1','1'),
       ('2','2'),
       ('3','3'),
       ('4','4'),
       ('5','5'),
     ]

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





class Restaurant(models.Model):  
    
    # name of the restaurant
    name=models.CharField(max_length=50, unique=True)
    pseudo=models.CharField(max_length=50, unique=True,default='')
     
    # URL 
    site_web=models.URLField(blank=True)
    yelp_website=models.URLField(blank=True)  
     
    #   mosaiq of photos
    main_photos=models.URLField(blank=True)  
    photos_url=models.URLField(blank=True) 
    
    #type of restaurant
    type_of_food=models.CharField(max_length=50,default='')
    
    # reviews and ratings
    nb_reviews=models.IntegerField(default=0)
    rating=models.FloatField(default=0)
    
    
    price_range=models.IntegerField( default=1)
    price_range_display=models.CharField( max_length=15,default='')
    price_coments=models.CharField( max_length=15,default='')
    
    nb_rating=models.IntegerField(default=0)
    nb_rating_1=models.IntegerField(default=0)
    nb_rating_2=models.IntegerField(default=0)
    nb_rating_3=models.IntegerField(default=0)
    nb_rating_4=models.IntegerField(default=0)
    nb_rating_5=models.IntegerField(default=0)
    
    ###############  add state code 
    
    # contact informations
    address=models.CharField(max_length=40)
    address_display=models.CharField(max_length=60,default='')
    postal_code = models.CharField(null=True, blank=True,max_length=7)
    country=models.CharField(max_length=20,default='')
    neighborhood = models.CharField(max_length=50)
    phone_number=models.CharField(max_length=15)
    longitude=models.FloatField(null=True)
    latitude=models.FloatField(null=True)
    state=models.CharField(max_length=10,default='')
    
    biz_hours=models.CharField(max_length=10000,default='')
    ############# biz hours
    ### morning
    morning_day0_start=models.CharField(max_length=10,default='Closed')
    morning_day0_end=models.CharField(max_length=10,default='Closed')
    morning_day1_start=models.CharField(max_length=10,default='Closed')
    morning_day1_end=models.CharField(max_length=10,default='Closed')
    morning_day2_start=models.CharField(max_length=10,default='Closed')
    morning_day2_end=models.CharField(max_length=10,default='Closed')
    morning_day3_start=models.CharField(max_length=10,default='Closed')
    morning_day3_end=models.CharField(max_length=10,default='Closed')
    morning_day4_start=models.CharField(max_length=10,default='Closed')
    morning_day4_end=models.CharField(max_length=10,default='Closed')
    morning_day5_start=models.CharField(max_length=10,default='Closed')
    morning_day5_end=models.CharField(max_length=10,default='Closed')
    morning_day6_start=models.CharField(max_length=10,default='Closed')
    morning_day6_end=models.CharField(max_length=10,default='Closed')
    
    
    ### night
    night_day0_start=models.CharField(max_length=10,default='Closed')
    night_day0_end=models.CharField(max_length=10,default='Closed')
    night_day1_start=models.CharField(max_length=10,default='Closed')
    night_day1_end=models.CharField(max_length=10,default='Closed')
    night_day2_start=models.CharField(max_length=10,default='Closed')
    night_day2_end=models.CharField(max_length=10,default='Closed')
    night_day3_start=models.CharField(max_length=10,default='Closed')
    night_day3_end=models.CharField(max_length=10,default='Closed')
    night_day4_start=models.CharField(max_length=10,default='Closed')
    night_day4_end=models.CharField(max_length=10,default='Closed')
    night_day5_start=models.CharField(max_length=10,default='Closed')
    night_day5_end=models.CharField(max_length=10,default='Closed')
    night_day6_start=models.CharField(max_length=10,default='Closed')
    night_day6_end=models.CharField(max_length=10,default='Closed')
    

    def __str__(self):
        return self.name
    
class Coments(models.Model):
    user=models.ForeignKey(User)
    restaurant=models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    restaurant_name=models.CharField(default='',max_length=30)
    rating=models.CharField(choices=rates, max_length=3)
    review=models.CharField(default='',max_length=300)


## import datetime
## day of the week 
## datetime.datetime.today().weekday()
## date 
## datetime.date.today()
## 0 = MONDAY

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
        novelty[i]=np.zeros(shape=(len(songs_list[i]),1))
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
    

    
    
    
    
    
