
import os
#Setting up environment variable for django to work
os.environ['DJANGO_SETTINGS_MODULE'] = 'maquette.settings'

#Importing models from django project
from django.db import transaction
print(os.getcwd())
from log import models
from models import Restaurant 
as main_app_models
## makemigrations




from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator

from log.models import Restaurant


from bs4 import BeautifulSoup
import urllib.request

auth = Oauth1Authenticator(
    consumer_key='MRN4Fmsl1VT-_sO2ta3PAw',
    consumer_secret='J_01DtIWRBMCdnvyjGOB366nnW0',
    token='pPCDlWI9d-VmT2k6Biva3DZbGK06I7Rw',
    token_secret='M-STsHV-gTZP_614PsVoOAoqvCU'
)

    
i=0
client = Client(auth)
for i in range(0,25):
# max offset=960
    params = {
        'limit': 40,
        'offset': 40*i,
        #'sort': 2,    
        #'price':'2',
       'term':'Restaurants',
    }

    res=client.search('Montreal',**params)
#res=client.search('Montreal',{'sort':1,'limit':40,'offset':40})
    l=res.businesses      
    for i in range(len(l)):
        a=Restaurant(name=l[i].name,                  
                    #site_web=l[i].url,   
                    main_photos=l[i].url.replace('biz','biz_photos'),
                    photos_url=l[i].image_url,
                    nb_reviews=l[i].review_count,
                    rating=l[i].rating,
                    adress=l[i].location.address[0],
                    postal_code=l[i].location.postal_code,
                    neighborhood=l[i].location.neighborhoods[0],
                    phone_number=l[i].display_phone,
                    longitude=l[i].location.coordinate.longitude,
                    latitude=l[i].location.coordinate.latitude)
        #type of food
        c=''
        for r in l[i].categories:
            c+=r[0]+','
        a.type_of_food=c[:-1]
        
        # beautifoulSoup parser
        r = urllib.request.urlopen(l[i].url).read()
        soup = BeautifulSoup(r,'lxml')
        
        #price range
        c=soup.find_all('span',attrs={'class':'business-attribute price-range'})
        if len(c)!=0:
            a.price_range=c[0].next_element
                           
        # price coments
        c=soup.find_all('dd',attrs={'class':'nowrap price-description'})
        if len(c)!=0:
            a.price_coments=c[0].next_element.replace('\n','').strip()
        
        #website of the restaurant
        c=soup.find_all('a',rel='noopener')
        if len(c)!=0:
            a.site_web=c[0].next_element
                        
        # business hours
        c=soup.find('div',attrs={'class':'ywidget biz-hours'})
        a.biz_hours=c.prettify().replace('\n','').replace('Closed now','').replace('Open now','')
        
        
        a.save()
        
        
   
   
    



