# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
#from django.forms import ModelForm
from django.db.models.signals import post_save
from django.dispatch import receiver
from django import forms


from jsonfield import JSONField
#from django_mysql.models import ListCharField
#from django.contrib.postgres.fields import JSONField

#from django.contrib.postgres.fields import JSONField

#neighborhoods= (
#    ('1', 'downtown'),
#    ('2', 'plateau'),
#    ('3', 'westmount'),
#)



#age_range=[('1','under 20'),
#            ('2','20-25'),
#            ('3','26-30'),
#            ('4','31-40'),
#            ('5','over 40') ]
#           
#                
#
#regions= [ ('1','North America'),
#           ('2','South America'),
#           ('3','Central America'),
#           ('4','Northern Europe'),
#           ('5','Europe'),
#           ('6','Eastern Europe'),
#           ('8','Oceania'),
#           ('9','Asia'),
#           ('10','Southeast Asia'),
#           ('11','Middle East'),
#           ('12','North Africa'),
#           ('13','Southern Africa'),]
#
#Area= [    	(	"	1	"	,	"	Arts & Humanities	"	)	,
#        	(	"	2	"	,	"	Engineering & Technology	"	)	,
#        	(	"	3	"	,	"	Life Sciences & Medicine	"	)	,
#        	(	"	4	"	,	"	Natural Sciences	"	)	,
#        	(	"	5	"	,	"	Social Sciences & Management	"	)	 ] 
#        		

   
       
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
    track_name=models.CharField(default='',max_length=50)
    track_pseudo=models.CharField(default='',max_length=50)
    track_popularity=models.FloatField(default=0)
    track_genre=models.CharField(default='pop',max_length=50)
    
    
    Artist=models.CharField(default='',max_length=50)
    
    track_link=models.CharField(default='',max_length=50)
    
    Artist_popularity=models.FloatField(default=0)
    #Artist_genre=models.CharField(default='',max_length=50)
    Artist_image=models.URLField(blank=True)
    
    Album_name=models.CharField(default='',max_length=50)
    Album_cover=models.URLField(blank=True)
    
    #lyrics=models.CharField(default='',max_length=250) ## save in a text file
    
    duration=models.FloatField(default=0)  ## lenght of the song in ms
    preview=models.URLField(blank=True)  ## preview of 30sec
    nb_rating=models.IntegerField(default=1)
    
    featuring=models.CharField(default='',max_length=50)
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
 
class Traj(models.Model):
    user=models.ForeignKey(User)
    path=JSONField(default=my_default)
    start_time = models.DateTimeField(auto_now_add=True, auto_now=False) 
    def append(self,txt):
        self.path.append(txt)

    def __str__(self):  # __unicode__ on Python 2
       return 'trajectory'
    
#    from log.models import Trajectories
#    Trajectories.objects.create(path=['4',('a','b'),'90%'])
#   c=Trajectories(path=['4',('a','b'),'90%'])
# c.path.append('blabla')
    
    
    
    
    
