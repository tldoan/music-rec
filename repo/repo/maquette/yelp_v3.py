## import model restaurant
from log.models import Restaurant


## login parameters for YELP API


from bs4 import BeautifulSoup
import urllib.request

import requests
#### identification
app_id = '_GKmTfqIvMGTE3EF4dkmWA'
app_secret = 'dovCtimn1ppruNsJAdJbykrVkn5D8wWwQgVedov1onVpYSlqiULhJxBkBoZ6WycA'
data = {'grant_type': 'client_credentials',
        'client_id': app_id,
        'client_secret': app_secret}
token = requests.post('https://api.yelp.com/oauth2/token', data=data)
access_token = token.json()['access_token']
url = 'https://api.yelp.com/v3/businesses/search'
headers = {'Authorization': 'bearer %s' % access_token}


for p in range(0,1):
    
    print('p: '+str(p))
#    p=0
### parameters of the search
    params = {'location': 'Montreal',
              #'categories': 'breakfast_brunch',
              'limit':'1',
              'offset':0,
              'term':'GaNadaRa'
              #'sort_by': 'rating',
              
             }
    
    
    ### response
    resp = requests.get(url=url, params=params, headers=headers)
    l=resp.json()
    l

#for i in range(len(l['businesses'])):
#    print(l['businesses'][i]['name'])




#for i in c:
#    cc+=i['title']+','
#cc[:-1]

    for i in range(len(l['businesses'])):
        print('restaurant numero:'+str(i))
        a=Restaurant(
                
                ## Contact information                
                name=l['businesses'][i]['name'],                
                pseudo=l['businesses'][i]['name'].replace(' ','_').replace("'",'_').lower(),
                phone_number=l['businesses'][i]['display_phone'],
                yelp_website=l['businesses'][i]['url'],
                nb_reviews=l['businesses'][i]['review_count'],
                nb_rating=l['businesses'][i]['review_count']-round(0.1*l['businesses'][i]['review_count']),
                rating=l['businesses'][i]['rating'],
                        
                ### location
                address=l['businesses'][i]['location']['address1'],
                address_display=' '.join(l['businesses'][i]['location']['display_address']),     
                postal_code=l['businesses'][i]['location']['zip_code'], 
                state=l['businesses'][i]['location']['state'],
                country=l['businesses'][i]['location']['country'],
                longitude=l['businesses'][i]['coordinates']['longitude'],
                latitude=l['businesses'][i]['coordinates']['latitude'],
                
                )
    ## type of food 
        c=''
        for rr in l['businesses'][i]['categories']:
            c+=rr['alias']+' , '
            
        a.type_of_food=c[:-3]
        
        ## get restaurant link
        print('soup entre en scene')
        r = urllib.request.urlopen(l['businesses'][i]['url']).read()
        soup = BeautifulSoup(r,'lxml')
        
        ## website of the restaurant
        c=soup.find_all('a',rel='noopener')
        if len(c)!=0:
            a.site_web=c[0].next_element
                        
        ## neighborhood of the restaurant
        c=soup.find_all('span',attrs={'class':'neighborhood-str-list'})
        if len(c)!=0:
            a.neighborhood=c[0].next_element.replace('\n','').strip()
    
    
        ## get businesses hours        
        
#        business_id='GaNadaRa-Montréal'
        business_id=l['businesses'][i]['id']
        
        url='https://api.yelp.com/v3/businesses/'+business_id
        c = requests.get(url=url, headers=headers).json()
        ## price range
        a.price_range_display=c['price']
        if c['price']=='$':
            a.price_range=1
        elif c['price']=='$$':
            a.price_range=2
        elif c['price']=='$$$':
            a.price_range=3
        elif c['price']=='$$$$':
            a.price_range=4
        else:
            a.price_range=5
        monday=0
        tuesday=0
        wednesday=0
        thursday=0
        friday=0
        saturday=0
        sunday=0
        if len(c['hours'][0]['open'])!=0: 
            for i in c['hours'][0]['open']:
                print('day :'+str(i['day']))
                ### MONDAY
                if i['day']==0 and monday==1:
                    print('on upload le night 0')
                    a.night_day0_start=i['start'][:2]+':'+i['start'][2:]
                    a.night_day0_end=i['end'][:2]+':'+i['end'][2:]
                if i['day']==0 and monday!=1:
                    monday+=1
                    a.morning_day0_start=i['start'][:2]+':'+i['start'][2:]
                    a.morning_day0_end=i['end'][:2]+':'+i['end'][2:]
                
                
                ### TUESDAY
                if i['day']==1 and tuesday==1:
                    a.night_day1_start=i['start'][:2]+':'+i['start'][2:]
                    a.night_day1_end=i['end'][:2]+':'+i['end'][2:]
                if i['day']==1 and tuesday!=1:
                    tuesday+=1
                    a.morning_day1_start=i['start'][:2]+':'+i['start'][2:]
                    a.morning_day1_end=i['end'][:2]+':'+i['end'][2:]
                    
                
                
                ### WEDNESDAY
                if i['day']==2 and wednesday==1:
                    a.night_day2_start=i['start'][:2]+':'+i['start'][2:]
                    a.night_day2_end=i['end'][:2]+':'+i['end'][2:]   
                if i['day']==2 and wednesday!=1:
                    wednesday+=1
                    a.morning_day2_start=i['start'][:2]+':'+i['start'][2:]
                    a.morning_day2_end=i['end'][:2]+':'+i['end'][2:]
                    
                 
                    
                ### THURSDAY   
                if i['day']==3 and thursday==1:
                    a.night_day3_start=i['start'][:2]+':'+i['start'][2:]
                    a.night_day3_end=i['end'][:2]+':'+i['end'][2:]
                 
                if i['day']==3 and thursday!=1:
                    
                    thursday+=1
                    a.morning_day3_start=i['start'][:2]+':'+i['start'][2:]
                    a.morning_day3_end=i['end'][:2]+':'+i['end'][2:]
                    
                
                    
                ### FRIDAY   
                if i['day']==4 and friday==1:
                    a.night_day4_start=i['start'][:2]+':'+i['start'][2:]
                    a.night_day4_end=i['end'][:2]+':'+i['end'][2:]  
                
                if i['day']==4 and friday!=1:
                    friday+=1
                    a.morning_day4_start=i['start'][:2]+':'+i['start'][2:]
                    a.morning_day4_end=i['end'][:2]+':'+i['end'][2:]
                    
                 
                    
                ### SATURDAY   
                if i['day']==5 and saturday==1:
                    a.night_day5_start=i['start'][:2]+':'+i['start'][2:]
                    a.night_day5_end=i['end'][:2]+':'+i['end'][2:]
                if i['day']==5 and saturday!=1:
                    saturday+=1
                    a.morning_day5_start=i['start'][:2]+':'+i['start'][2:]
                    a.morning_day5_end=i['end'][:2]+':'+i['end'][2:]
                
                
                    
                ### SUNDAY
                if i['day']==6 and sunday==1:
                    a.night_day6_start=i['start'][:2]+':'+i['start'][2:]
                    a.night_day6_end=i['end'][:2]+':'+i['end'][2:]
                
                if i['day']==6 and sunday!=1:
                    sunday+=1
                    a.morning_day6_start=i['start'][:2]+':'+i['start'][2:]
                    a.morning_day6_end=i['end'][:2]+':'+i['end'][2:]
                    
                
                
            
        a.save()   
                
                
                
                
            
        

import time
from datetime import date
import datetime as dt
from datetime import datetime
import datetime
from datetime import time

now.time()



#####################################        
n = datetime.now()
t = n.timetuple()
y, m, d, h, min, sec, wd, yd, i = t


######################################
now = datetime.datetime.now()
minute=now.minute
hour=now.hour

year, month, day, hour, minute = time.strftime("%Y,%m,%d,%H,%M").split(',')



#### jour de la semaine 
datetime.datetime.today().weekday()

a=Restaurant.objects.filter(pseudo='ganada').delete()


        
        