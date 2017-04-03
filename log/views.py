from django.shortcuts import render,redirect, get_object_or_404
from .forms import (
        ProfileForm,
        UserForm, ComentsForm,TracksForm)
    
        
from .models import Profile,Restaurant,Coments, Tracks, Track_Coments  , Traj
from django.views.generic import View
from django.urls import reverse
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
import datetime
from datetime import time

from django.conf import settings
import os
from wordcloud import WordCloud
import random
#import matplotlib.pyplot as plt

from PIL import Image
import numpy as np

from django.db.models import Avg

def loggin(request):  
    logout(request)
    #form=UserForm(None)
    return render(request, 'login.html')    
    
def auth(request):
        error=False
        username=request.POST.get('username','')
        password=request.POST.get('password','')
        user=authenticate(username=username,password=password)
        
        if user is not None:
                if user.is_active:
                    login(request,user)
                    if Profile.objects.filter(user=request.user).exists():
                        prof = get_object_or_404(Profile, user=request.user)
                        #prof=Profile.objects.filter(user=request.user)
                   
                        if (prof.area=='' or prof.age=='' or prof.region=='' or prof.sex==''):
                            return redirect('profil')
                        else:
                            return redirect(reverse('homepage'))                       
                    else: 
                        #return render(request,'home.html',locals())
                        return redirect('profil')
        else:
            error=True
            return render(request,'login.html',{'error':error})

def loggout(request):
    logout(request)
    return redirect(reverse('login'))


@login_required
def homepage(request):
    """'affiche la liste des tracks'""" 
    #prof = get_object_or_404(Profile, user=request.user)
    if request.method=='GET':  
        if Profile.objects.filter(user=request.user).exists():
            prof = get_object_or_404(Profile, user=request.user)
            #prof=Profile.objects.filter(user=request.user).exists()        
            if (prof.area=='' or prof.age=='' or prof.region=='' or prof.sex==''):
                return redirect('profil')
            else:
                track_list = Tracks.objects.order_by('track_name')
                return render(request,'home.html',locals())
        else:     
            return redirect('profil')
    elif request.method=='POST' :
            if 'next_song' in request.POST:  
            #if 'next_song' in request.post:
            ## start creating the trajectory  
                c=request.POST.get('next_song','')             
                t=Traj(path=['start']) 
                t.user=request.user
                t.save()           
                return redirect(reverse('fiche_track',kwargs={'track_pseudo': c}))
            if 'profil' in request.POST:  
                track_list = Tracks.objects.order_by('track_name')
                return render(request,'home.html',locals())

@login_required
def profil(request):  
    if request.method=='POST':       
        valid=True
#        if 'profil' in request.POST:
#            pp=get_object_or_404(Profile, user=request.user)
#            #pp=Profile.objects.get(user=request.user)  
#            return render(request,'profil.html',locals())
        if 'age' in request.POST:
            if Profile.objects.filter(user=request.user).exists():   
                
                pp=Profile.objects.get(user=request.user)   
                pp.age=request.POST.get('age','')
                pp.region=request.POST.get('region','')
                pp.sex=request.POST.get('sex','')
                pp.area=request.POST.get('area','')
              
                pp.save()
                return render(request,'profil.html',locals())         
            else: 
                profil=ProfileForm
                form=profil(request.POST) 
                age=request.POST.get('age','')
                region=request.POST.get('region','')
                sex=request.POST.get('sex','')
                area=request.POST.get('area','')
                   
                pp=form.save(commit=False)
                pp.age=age
                pp.region=region
                pp.area=area    
                pp.sex=sex      
                pp.user=request.user
                pp.save() 
                return render(request,'profil.html',locals())        
    else:
        if Profile.objects.filter(user=request.user).exists():   
            pp=Profile.objects.get(user=request.user)  
#        if Profile.objects.filter(user=request.user).exists():
#            has_filled_profil=True            
        return render(request,'profil.html',locals())
               
def register(request):
    if request.method=='POST':
        #user_is_created=False
        form=UserForm(request.POST)
        #user_is_created=False
        
        if form.is_valid():
            user=form.save(commit=False)
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            user.set_password(password)
            user.save()
            #user_is_created=True
            user=authenticate(username=username,password=password)
            login(request,user)
            return redirect('profil')  
        #,{'username':username,'user':user}
        else:
            return render(request,'registration_form.html',{'form':form})
    else:
        form=UserForm(None)
        return render(request,'registration_form.html',{'form':form})
 
@login_required       
def fiche_track(request, track_pseudo):
    track = get_object_or_404(Tracks, track_pseudo=track_pseudo)
    has_yet_rated=True  
    path='wcloud_pictures/'+track_pseudo+'.png'
    l=['shape_of_you','the_hills','closer']
    liste=[]
    for i in range(len(l)):
        liste.append(get_object_or_404(Tracks, track_pseudo=l[i]))    
    try:
        REVIEW=Track_Coments.objects.get(user=request.user,track=track)  
        #REVIEW=get_object_or_404(user=request.user, track_name=track_name)
    except:
        has_yet_rated=False
        #REVIEW='None'       
    load_wordcloud(track_pseudo,'')
    if request.method=='GET':
        # check si existe pas deja
        t=Traj.objects.filter(user=request.user).order_by('-start_time')[0]
        length=len(t.path)
#        print type(t.path[length-1]) 
#        print t.path[length-1] 
#        print type(track_pseudo)
#        print track_pseudo
        if type(t.path[length-1])==list:                      
            t.path.append(track_pseudo)
            t.save() 
            return render(request,'fiche_track.html',locals())
        elif type(t.path[length-1].encode('ascii','ignore'))==str: 
            if t.path[length-1]!=track_pseudo:    
                
                t.path.append(track_pseudo)
                t.save() 
                return render(request,'fiche_track.html',locals())
            else:  
                
                return render(request,'fiche_track.html',locals()) 
        else:  
            
            return render(request,'fiche_track.html',locals())                
    elif request.method=='POST':
        if 'rating' in request.POST:
            if Track_Coments.objects.filter(user=request.user,track=track).exists():
                return render(request,'fiche_track.html',locals())
            else:
            ## method POST mais du rating form
                track_coment=TracksForm
                form=track_coment(request.POST) 
                rating=request.POST.get('rating','')
                wordcloud=request.POST.get('wordcloud','')
                Wrong=True
                if rating !='':
                    wrong=False
                    rev=form.save(commit=False)
                    rev.rating=float(rating)
                    rev.user=request.user
                    rev.track=track
                    rev.time=datetime.datetime.now()
                    rev.wordcloud=wordcloud
                    rev.save() 
                    
                    ### s il existe des lignes on fait la moyenne en faisant un loop up dans la db
                    if Track_Coments.objects.filter(track=track).count()>=10:                        
                        ## it is a dictionnary convert it now to float  
                        ## il existera toujours car le mec vient de submit en fait 
                        
                        track.track_popularity=Track_Coments.objects.filter(track=track).aggregate(Avg('rating'))['rating__avg']
#                    else:
                    ########## sinon c est juste la moyenne entre le rate et le prior rate du depart   
#                        print '----------------------------------------'
#                        print '----------------------------------------'
#                        print float(track.track_popularity)
#                        print float(rating)
#                        print float(track.track_popularity)+float(rating)
#                        print (float(track.track_popularity)+float(rating))/2
#                        track.track_popularity=(float(track.track_popularity)+float(rating))/2
                        
#                    track.nb_rating+=1
                    Track_Coments.objects.filter(track=track).count()
                    track.save()  
                    has_yet_rated=True
                    if wordcloud!='':
                        load_wordcloud(track_pseudo,wordcloud)
                    has_just_commented=True
                    print '-------------------'
                    print request.POST.get('time_before_rated','')
                    time_before=float(request.POST.get('time_before_rated',''))             
                return render(request,'fiche_track.html',locals())
        elif 'queue' in request.POST:
             print 'methode = POST  titre_1_________________'
             #c=request.POST.get('next_song','') 
             titre_1=request.POST.get('titre_1','')
             titre_2=request.POST.get('titre_2','')
             print(titre_1)
             print(titre_2)
             t=Traj.objects.filter(user=request.user).order_by('-start_time')[0]          
#            ## collecting data        
             listening_time=request.POST.get('listening_time','') 
             if listening_time=='':
                listening_time=0  
             else:
                listening_time=round(float(listening_time),2)              
             percentage=request.POST.get('percentage','')
             if percentage=='':
                percentage=0
             else:
                percentage=round(float(percentage),2)           
             ## update the database 
             t.path.append([listening_time,percentage])
             liste=request.POST.get('liste2','')
             t.path.append(liste)
#            t.path.append(track_pseudo)
             t.save()
             print 'queue___________'
             
             if titre_2=='empty':                                    
                 return redirect(reverse('fiche_track',kwargs={'track_pseudo': titre_1}))
             else:   
                 print 22
                 print(titre_1)
                 print(titre_2)
                 return redirect(reverse('solo',kwargs={'titre_1': titre_1,'titre_2':titre_2}))
#        elif 'next_song' in request.POST:
#             print 'methode = POST _________________'
#             c=request.POST.get('next_song','')  
#             t=Traj.objects.filter(user=request.user).order_by('-start_time')[0]          
##            ## collecting data        
#             listening_time=request.POST.get('listening_time','') 
#             if listening_time=='':
#                listening_time=0  
#             else:
#                listening_time=round(float(listening_time),2)              
#             percentage=request.POST.get('percentage','')
#             if percentage=='':
#                percentage=0
#             else:
#                percentage=round(float(percentage),2)           
#             
#             ## update the database
#             
#             t.path.append([listening_time,percentage])
#             liste=request.POST.get('liste2','')
#             t.path.append(liste)
##            t.path.append(track_pseudo)
#             t.save()
#             return redirect(reverse('fiche_track',kwargs={'track_pseudo': c}))
        elif 'liste' in request.POST:
            t=Traj.objects.filter(user=request.user).order_by('-start_time')[0]
            
            listening_time=request.POST.get('listening_time2','')
            percentage=request.POST.get('percentage2','')
            
            if listening_time=='':
                listening_time=0
            else:
                listening_time=round(float(listening_time),2)
            if percentage=='':
                percentage=0
            else:
                percentage=round(float(percentage),2)
                       
            t.path.append([listening_time,percentage])
            liste=request.POST.get('liste','')
            t.path.append(liste)
            
            t.path.append('end')
            t.save()
            return redirect(reverse('homepage'))
        elif 'liste3' in request.POST:
            t=Traj.objects.filter(user=request.user).order_by('-start_time')[0]
            
            listening_time=request.POST.get('listening_time2','')
            percentage=request.POST.get('percentage2','')
            
            if listening_time=='':
                listening_time=0
            else:
                listening_time=round(float(listening_time),2)
            if percentage=='':
                percentage=0
            else:
                percentage=round(float(percentage),2)
                       
            t.path.append([listening_time,percentage])
            liste=request.POST.get('liste3','')
            t.path.append(liste)
            
            ## checker si end n est pqs deja mis
            ## voir si on keep track de la note de la zik aussi
            t.path.append('end')
            t.save()
            return redirect(reverse('logout'))
@login_required         
def solo(request,titre_1,titre_2):
    base_2=True
    track = get_object_or_404(Tracks, track_pseudo=titre_1)
    track2= get_object_or_404(Tracks, track_pseudo=titre_2)
    path='wcloud_pictures/'+titre_1+'.png'
    if Track_Coments.objects.filter(track=track,user=request.user).exists():
        has_yet_rated=True
        review=Track_Coments.objects.filter(track=track)
    else:
        has_yet_rated=False
    print has_yet_rated
    if request.method=='GET':
        print 'methode GET____________________'
        # check si existe pas deja
        t=Traj.objects.filter(user=request.user).order_by('-start_time')[0]
        length=len(t.path)
        print '_______________________________'
        if type(t.path[length-1])==list:
            print '_______________________________'
            print 1               
            t.path.append(titre_1)
            t.save() 
            #return render(request,'fiche_track2.html',locals())
        elif type(t.path[length-1].encode('ascii','ignore'))==str: 
            if t.path[length-1]!=titre_1:    
                print 2
                print '_______________________________'
                print '_______________________________'
                t.path.append(titre_1)
                t.save() 
        return render(request,'fiche_track2.html',locals())         
    else: ## methode=POST
        if 'rating' in request.POST:
            if Track_Coments.objects.filter(user=request.user,track=track).exists():
                return render(request,'fiche_track2.html',locals())
            else:
            ## method POST mais du rating form
                track_coment=TracksForm
                form=track_coment(request.POST) 
                rating=request.POST.get('rating','')
                wordcloud=request.POST.get('wordcloud','')
                Wrong=True
                if rating !='':
                    wrong=False
                    rev=form.save(commit=False)
                    rev.rating=float(rating)
                    rev.user=request.user
                    rev.track=track
                    rev.time=datetime.datetime.now()
                    rev.wordcloud=wordcloud
                    rev.save()            
                    ### s il existe des lignes on fait la moyenne en faisant un loop up dans la db
                    print Track_Coments.objects.filter(track=track).count()
                    if Track_Coments.objects.filter(track=track).count()>=10:                        
                        ## it is a dictionnary convert it now to float  
                        ## il existera toujours car le mec vient de submit en fait 
                        track.track_popularity=Track_Coments.objects.filter(track=track).aggregate(Avg('rating'))['rating__avg']

#                    track.nb_rating+=1
                    track.save()  
                    has_yet_rated=True
                    if wordcloud!='':
                        load_wordcloud(titre_1,wordcloud)
                    has_just_commented=True
                    time_before=float(request.POST.get('time_before_rated',''))
                return render(request,'fiche_track2.html',locals())
        elif 'solo' in request.POST:
             print 'methode = POST _solo________________'
             #c=request.POST.get('titre_2','')  
             t=Traj.objects.filter(user=request.user).order_by('-start_time')[0]          
#            ## collecting data        
             listening_time=request.POST.get('listening_time','') 
             if listening_time=='':
                listening_time=0  
             else:
                listening_time=round(float(listening_time),2)              
             percentage=request.POST.get('percentage','')
             if percentage=='':
                percentage=0
             else:
                percentage=round(float(percentage),2)           
             ## update the database
             t.path.append([listening_time,percentage])
             #liste=request.POST.get('liste2','')
            
             t.path.append(['None',titre_2])
#          
             t.save()
             return redirect(reverse('fiche_track',kwargs={'track_pseudo': titre_2}))
        elif 'home' in request.POST:
            t=Traj.objects.filter(user=request.user).order_by('-start_time')[0]         
            listening_time=request.POST.get('listening_time2','')
            percentage=request.POST.get('percentage2','')
            
            if listening_time=='':
                listening_time=0
            else:
                listening_time=round(float(listening_time),2)
            if percentage=='':
                percentage=0
            else:
                percentage=round(float(percentage),2)
                       
            t.path.append([listening_time,percentage])
           
            t.path.append(['None',titre_2])
            
            ## checker si end n est pqs deja mis
            ## voir si on keep track de la note de la zik aussi
            t.path.append('end')
            t.save()
            return redirect(reverse('homepage'))
        elif 'liste3' in request.POST:
            t=Traj.objects.filter(user=request.user).order_by('-start_time')[0]
            
            listening_time=request.POST.get('listening_time2','')
            percentage=request.POST.get('percentage2','')
            
            if listening_time=='':
                listening_time=0
            else:
                listening_time=round(float(listening_time),2)
            if percentage=='':
                percentage=0
            else:
                percentage=round(float(percentage),2)
            t.path.append([listening_time,percentage])
            t.path.append(['None',titre_2])
            
            ## checker si end n est pqs deja mis
            ## voir si on keep track de la note de la zik aussi
            t.path.append('end')
            t.save()
            return redirect(reverse('logout'))


#def update_restaurant_information(request):
@login_required    
def change_rating(request,track): 
    TRACK = get_object_or_404(Tracks, track_name=track)
    REVIEW=Track_Coments.objects.get(user=request.user,track=TRACK)
    #REVIEW=get_object_or_404(Track_Coments, track=track,user=request.user)
    REVIEW.delete()
    #has_yet_rated=False  
    #return render(request,'fiche_track.html',locals())
    return redirect(reverse('fiche_track',kwargs={'track_name': track}))
                  

def change_password(request):
    if request.method=='POST':
        form=PasswordChangeForm(data=request.POST,user=request.user)
        
        if form.is_valid():
            form.save()
            ### ca va deconnecter l user
            update_session_auth_hash(request, form.user)
            return render(request,'home.html')
        else:
            return redirect('change_password')
    else:
        form=PasswordChangeForm(user=request.user)
        return render(request,'change_password.html',locals())
   
    
def grey_color_func(word, font_size, position, orientation, random_state=None,
                    **kwargs):
    return "hsl(0, 0%%, %d%%)" % random.randint(60, 100)
         

def load_wordcloud(track_pseudo,brainstorm):
    #text = open(os.path.join(settings.STATIC_URL+'wordcloud_txt/', track_name+'.txt'), 'a')
    text=open(os.path.join(settings.STATIC_ROOT, "wordcloud_txt/" + track_pseudo+ ".txt"), 'a')
    ## add words 
    text.write('\n')
    text.write(brainstorm)
    text.close()
    text = open(os.path.join(settings.STATIC_ROOT+'wordcloud_txt/', track_pseudo+'.txt')).read()
    ## now that we have written in the text, let's generate it
#    image = wordcloud.to_image()
#    image.save(os.path.join(settings.STATIC_ROOT+'wcloud_pictures/', track_pseudo+'.png'),'png')  
    mask = np.array(Image.open(os.path.join(settings.STATIC_ROOT+'wcloud_pictures/', 'play_icon'+'.jpg')))
    #default_colors = wordcloud.to_array()
    wordcloud = WordCloud(relative_scaling = 0.60,mask=mask).generate(text)
#    plt.imshow(wordcloud.recolor(color_func=grey_color_func, random_state=1),
#           interpolation="bilinear")
    wordcloud.recolor(color_func=grey_color_func, random_state=1)
    wordcloud.to_file(os.path.join(settings.STATIC_ROOT+'wcloud_pictures/', track_pseudo+'.jpg'))




##############################################################################
##############################################################################
##############################################################################
##############################################################################
def is_open(resto):
    #resto = get_object_or_404(Restaurant, pseudo=pseudo)
    
    #### defining day of the week, hour and minutes
    day=datetime.datetime.today().weekday()
    now = datetime.datetime.now()
#    minute=now.minute
#    hour=now.hour
#    now = datetime.now()
    ouvert=False
    
    if day==0:
        if (resto.morning_day0_start!='Closed' or resto.morning_day0_end!='Closed'):            
            if (time(int(resto.morning_day0_start[0:2]),int(resto.morning_day0_start[3:])) <=  now.time() <= time(int(resto.morning_day0_end[0:2]),int(resto.morning_day0_end[3:]))):
                ouvert=True
        elif (resto.night_day0_start!='Closed' or resto.night_day0_end!='Closed'): 
            if (time(int(resto.night_day0_start[0:2]),int(resto.night_day0_start[3:])) <=  now.time() <= time(int(resto.night_day0_end[0:2]),int(resto.night_day0_end[3:]))):
                ouvert=True  
   
    if day==1:
        if (resto.morning_day1_start!='Closed' or resto.morning_day1_end!='Closed'):            
            if (time(int(resto.morning_day1_start[0:2]),int(resto.morning_day1_start[3:])) <=  now.time() <= time(int(resto.morning_day1_end[0:2]),int(resto.morning_day1_end[3:]))):
                ouvert=True
        elif (resto.night_day1_start!='Closed' or resto.night_day1_end!='Closed'): 
            if (time(int(resto.night_day1_start[0:2]),int(resto.night_day1_start[3:])) <=  now.time() <= time(int(resto.night_day1_end[0:2]),int(resto.night_day1_end[3:]))):
                ouvert=True  
    
    if day==2:
        if (resto.morning_day2_start!='Closed' or resto.morning_day2_end!='Closed'):            
            if (time(int(resto.morning_day2_start[0:2]),int(resto.morning_day2_start[3:])) <=  now.time() <= time(int(resto.morning_day2_end[0:2]),int(resto.morning_day2_end[3:]))):
                ouvert=True
        elif (resto.night_day2_start!='Closed' or resto.night_day2_end!='Closed'): 
            if (time(int(resto.night_day2_start[0:2]),int(resto.night_day2_start[3:])) <=  now.time() <= time(int(resto.night_day2_end[0:2]),int(resto.night_day2_end[3:]))):
                ouvert=True  
    
    if day==3:
        if (resto.morning_day3_start!='Closed' or resto.morning_day3_end!='Closed'):            
            if (time(int(resto.morning_day3_start[0:2]),int(resto.morning_day3_start[3:])) <=  now.time() <= time(int(resto.morning_day3_end[0:2]),int(resto.morning_day3_end[3:]))):
                ouvert=True
        elif (resto.night_day3_start!='Closed' or resto.night_day3_end!='Closed'): 
            if (time(int(resto.night_day3_start[0:2]),int(resto.night_day3_start[3:])) <=  now.time() <= time(int(resto.night_day3_end[0:2]),int(resto.night_day3_end[3:]))):
                ouvert=True  
            
    if day==4:
        if (resto.morning_day4_start!='Closed' or resto.morning_day4_end!='Closed'):            
            if (time(int(resto.morning_day4_start[0:2]),int(resto.morning_day4_start[3:])) <=  now.time() <= time(int(resto.morning_day4_end[0:2]),int(resto.morning_day4_end[3:]))):
                ouvert=True
        elif (resto.night_day4_start!='Closed' or resto.night_day4_end!='Closed'): 
            if (time(int(resto.night_day4_start[0:2]),int(resto.night_day4_start[3:])) <=  now.time() <= time(int(resto.night_day4_end[0:2]),int(resto.night_day4_end[3:]))):
                ouvert=True                 
                
    if day==5:
        if (resto.morning_day5_start!='Closed' or resto.morning_day5_end!='Closed'):            
            if (time(int(resto.morning_day5_start[0:2]),int(resto.morning_day5_start[3:])) <=  now.time() <= time(int(resto.morning_day5_end[0:2]),int(resto.morning_day5_end[3:]))):
                ouvert=True
        elif (resto.night_day5_start!='Closed' or resto.night_day5_end!='Closed'): 
            if (time(int(resto.night_day5_start[0:2]),int(resto.night_day5_start[3:])) <=  now.time() <= time(int(resto.night_day5_end[0:2]),int(resto.night_day5_end[3:]))):
                ouvert=True 
                
                
    if day==6:
        if (resto.morning_day6_start!='Closed' or resto.morning_day6_end!='Closed'):            
            if (time(int(resto.morning_day6_start[0:2]),int(resto.morning_day6_start[3:])) <=  now.time() <= time(int(resto.morning_day6_end[0:2]),int(resto.morning_day6_end[3:]))):
                ouvert=True
        elif (resto.night_day6_start!='Closed' or resto.night_day6_end!='Closed'): 
            if (time(int(resto.night_day6_start[0:2]),int(resto.night_day6_start[3:])) <=  now.time() <= time(int(resto.night_day6_end[0:2]),int(resto.night_day6_end[3:]))):
                ouvert=True  
        
    return ouvert

    

def fiche_resto(request, pseudo):
    """  Fiche du restau """
    resto = get_object_or_404(Restaurant, pseudo=pseudo)
    ## create a variable that tells if the user already rated the restaurant
    has_yet_rated=True
    ouvert=is_open(resto)
    
    try:
        REVIEW=Coments.objects.get(user=request.user,restaurant=resto)
    except:
        has_yet_rated=False
        REVIEW='None'        
     
    #rest=Restaurant.objects.get(name=resto.name)
    sauvegarde = False  
    ### liste of returned response
    l=['boustan','le_majestique','romados']
    liste=[]
    for i in range(len(l)):
        liste.append(get_object_or_404(Restaurant, pseudo=l[i]))        
    coment=ComentsForm   
    
    if request.method=='GET':               
            form=coment(None)
            return render(request,'fiche_resto.html',{'resto':resto,'liste':liste,
                                                  'form':form,
                                                  'resto':resto,
                                                  'has_yet_rated':has_yet_rated,'REVIEW':REVIEW,'ouvert':ouvert})
        
    else: # request.method=='POST':
    ## si c est False c est qu il n a pas encore rate le restaurant
        form=coment(request.POST)        
        
        if form.is_valid():       
            rev=form.save(commit=False)
            #form=coment(User=request.user,restaurant=rest)
            rev.rating=form.cleaned_data['rating']
            rev.review=form.cleaned_data["review"]
            rev.restaurant=resto
            rev.restaurant_name=resto.pseudo
            rev.user=request.user
            rev.save()            
            sauvegarde = True     
            ## update in the database
            if rev.review!='':
                resto.nb_reviews+=1
                resto.save()
            if rev.rating=='1':
                resto.nb_rating_1+=1
                
            elif rev.rating=='2':
                resto.nb_rating_2+=1
            
            elif rev.rating=='3':
                resto.nb_rating_3+=1  
                
            elif rev.rating=='4':
                resto.nb_rating_4+=1
                
            elif rev.rating=='5':
                resto.nb_rating_5+=1
                
            resto.rating=float((resto.rating*resto.nb_rating+float(rev.rating))/float(resto.nb_rating+1))
            resto.nb_rating+=1    
            resto.save()
            has_yet_rated=True
            return render(request,'fiche_resto.html',{'resto':resto,
            'liste':liste,'form':form,
            'sauvegarde':sauvegarde,
            'has_yet_rated':has_yet_rated,'REVIEW':rev,'ouvert':ouvert})
        else:
            return render(request,'fiche_resto.html',{'resto':resto,
            'liste':liste,
            'sauvegarde':sauvegarde,
            'has_yet_rated':has_yet_rated,'ouvert':ouvert})
    
