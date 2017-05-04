from django.shortcuts import render,redirect, get_object_or_404
from .forms import ( ProfileForm, UserForm,TracksForm)

from django.utils import timezone
        
from .models import Profile, Tracks, Track_Coments  , Traj , history
from django.urls import reverse
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required



from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash


import datetime
from datetime import time
import timeit

from django.conf import settings
import os
from wordcloud import WordCloud
import random,string
#import matplotlib.pyplot as plt

from PIL import Image
import numpy as np

from django.db.models import Avg

from itertools import *
import json
from django.http import HttpResponse,Http404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

#from django_ajax.decorators import ajax
 

#import csv


#from keras.models import Sequential
#from keras.layers import Dense, Activation, Input
#import keras
#import tensorflow

from neural_network import predict_type, history_update,evaluate_actions

os.environ['TF_CPP_MIN_LOG_LEVEL']='2'

import timeit

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
    Country=Tracks.objects.filter(track_genre='Country')
    Dance=Tracks.objects.filter(track_genre='Dance/Electronic')
    Hip_Hop=Tracks.objects.filter(track_genre='Hip-Hop/R&B')
    Latin=Tracks.objects.filter(track_genre='Latin')
    Pop=Tracks.objects.filter(track_genre='Pop')
    Rock=Tracks.objects.filter(track_genre='Rock')
    track_list = Tracks.objects.order_by('track_name')
    L=[Country,Dance,Hip_Hop,Latin,Pop,Rock,track_list]

    if request.method=='GET':  
        
      
        if Profile.objects.filter(user=request.user).exists():
            prof = get_object_or_404(Profile, user=request.user)
            if (prof.area=='' or prof.age=='' or prof.region=='' or prof.sex==''):
                return redirect('profil')
            else:
                
#                track_list = Tracks.objects.order_by('track_name')
                
                
                
                return render(request,'home.html',locals())
        else:     
            return redirect('profil')
    elif request.method=='POST' :
            if 'next_song' in request.POST:  
                
            ## start creating the trajectory  
                caracteres = string.ascii_letters + string.digits
                aleatoire = [random.choice(caracteres) for _ in range(6)]
                c=request.POST.get('next_song','')             
                t=Traj(path=['start']) 
                t.user=request.user
                t.key=''.join(aleatoire)
                t.save()          
                
                try:      
                    t3=Traj.objects.filter(user=request.user).order_by('-start_time')[1]                   
                    if (timezone.now()-t3.start_time).seconds >=1800:
                    ## was the last conexion of the user more than 30min ago?
                        t2=history(path=['start'])
                        t2.user=request.user
                        t2.save()              
                except:
                    ## si pas de history
                    t2=history(path=['start']) 
                    t2.user=request.user
                    t2.save()                    
                try:
                    t2=history.objects.filter(user=request.user).order_by('-start_time')[0]
                    
                except:
                    t2=history(path=['start']) 
                    t2.user=request.user               
                ## delimiteur 
                t2.append('XXX')
                t2.append_key(str(t.key))
                t2.save()
               
                return redirect(reverse('fiche_track',kwargs={'track_pseudo': c}))
            
            if 'profil' in request.POST:  
#                track_list = Tracks.objects.order_by('track_name')
                return render(request,'home.html',locals())

@login_required
def profil(request):  
    if request.method=='POST':       
        valid=True
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
        else:
            return render(request,'registration_form.html',{'form':form})
    else:
        form=UserForm(None)
        return render(request,'registration_form.html',{'form':form})
 



@csrf_exempt
def save_rating(request):
    if request.is_ajax():
        if request.method=='POST':
            rating=request.POST.get('rating')
            wordcloud=request.POST.get('wordcloud')
       
            track_pseudo=wcloud=request.POST.get('track_pseudo')
                
            track=get_object_or_404(Tracks, track_pseudo=track_pseudo)
            if not Track_Coments.objects.filter(user=request.user,track=track).exists():               
                t=Track_Coments(rating=rating)
                t.track=track
                t.user=request.user
                t.time=datetime.datetime.now()
                if wcloud!='':      
                    t.wordcloud=wordcloud
                    load_wordcloud(track_pseudo,wordcloud)
 
                    msg={'update_wcloud':True}
                  
                else:
                    msg={'update_wcloud':False}
                t.save()
                          
            
            return HttpResponse(json.dumps(msg),content_type="application/json")
    else:
        msg={'error':'No'}
        return HttpResponse(json.dumps(msg),content_type="application/json")
            

def recommend_songs(request):
    if request.is_ajax():
        print  'yess'
        if request.method=='GET':
            print 'yeees again'
#            track_pseudo = request.POST.get('track_pseudo')
            t=Traj.objects.filter(user=request.user).order_by('-start_time')[0]  
           
            length=len(t.path)
            print t.path
            print 'pathh'
            print type(str(t.path[length-2]))
            if type(t.path[length-1])==unicode:               
                track_pseudo=t.path[length-1]
          
            elif type(t.path[length-1])==list:
                if len(t.path[length-1])<=2:
                    ### de la forme S(i-3) A(i-2) R(i-1)  donc le state est 
                    track_pseudo=t.path[length-3]
                else:
                    #### S A 
                    
                    track_pseudo=t.path[length-2]
                
            print 'longueur'
            print track_pseudo
#            
            track=get_object_or_404(Tracks, track_pseudo=track_pseudo)
           
            
            t2=history.objects.filter(user=request.user).order_by('-start_time')[0] 
            historic=history_update(t2)  
#            N=4
            w=predict_type(request.user,historic,track)              
     
            l=evaluate_actions(request.user,historic,track,w,t2)
            print l
            liste=[]
            for i in range(len(l)):
                liste.append(get_object_or_404(Tracks, track_pseudo=l[i])) 
#              
            data={}
            for i in range(len(l)):
                song=get_object_or_404(Tracks, track_pseudo=l[i])
                index='#Eelement_'+str(i)             
                data[index]=song.Artist+' - '+song.track_name
                index='image_'+str(i)
                data[index]=song.Artist_image
                index='#NOTE_'+str(i)
                data[index]=round(song.track_popularity,2)
                index='.next_song_'+str(i)
                data[index]=song.track_pseudo
#            print data
                
           
        
           
            print 'TT'
            print t.path[length-1]
            print type(t.path[length-1])
            if type(t.path[length-1])==unicode:  
                    print 'ici'
                ### S           
                    t.path.append(l)
                #### S A 
                ##### OK
            elif type(t.path[length-1])==list:
                if t.path[length-2]==track_pseudo:
                    print 'laa'
                    t.path[length-1]=l
            
            t.save()    


                
#            elif type(t.path[length-2])==list:
#                if len(t.path[length-2])<=2:
#                    ### S A   R(i-2)  S
#                    t.path.append(l)
#                elif len(t.path[length-2])>=3:
#                    ### S A   S
#                    ### i la fait retour en arriere
#                    t.path[length-1]=[0,0,0]
#                    t.path.append(track_pseudo)
#                    
#                    
#            ########### il est revenu en arriere
#        
#        
#        
#        
#                if len(t.path[length-1])>=3:
#                    if t.path[length-2]!=track_pseudo:
#                        t.path.append([0.0,0.0])
#                    ### il a juste appuyer sur F5
#                
#            if type(t.path[length-1])==list:     
#                 if len(t.path[length-1])<=2:
#                     ######### S A R >>- S
#                     t.path.append(track_pseudo)
#                     t.path.append(l)
#                     t.save()                    
#                 elif len(t.path[length-1])>=3:
#                     print 'regarde le type'
#                     print type(t.path[length-2])
#                     if t.path[length-2]==str:
#                         if t.path[length-2]==track_pseudo:
#                             print 'apuyeer sur F55555555555555'
##                             t.path[length-1]=l
#                     else:     
#
#                         'nooon'
#                         t.path.append([0.0,0.0])
#                         t.path.append(track_pseudo)
#                         t.save(l)  
#            elif str(t.path[length-1])=='start':
#                print 'ahahah'
#                t.path.append(track_pseudo)
#                t.path.append(l)
#            t.save()
#                
                
                     
                      
#                      
#            elif type(t.path[length-1].encode('ascii','ignore'))==str and t.path[length-1]!=track_pseudo: 
#            ##### il a fait une page precedente donc on va coller  la liste l  puis reward [0,0,0]
#    #             t.path.append(l)
#    #             t.path.append([0.0,0.0])
#                 t.path.append(track_pseudo)
#                 t.save()  
                                            
#            data={'lol':False}
            return HttpResponse(json.dumps(data),content_type="application/json")
    else:
        data={'lol':False}
        return HttpResponse(json.dumps(data),content_type="application/json")
        




    
    
    
    
@login_required       
def fiche_track(request, track_pseudo):
    novelty_parameters=5
    novelty_limit=60
    
    songs_keys=np.load(os.path.join(settings.STATIC_ROOT, 'data/songs_keys.npy')).item()   
    track = get_object_or_404(Tracks, track_pseudo=track_pseudo)

    base_2=False
    has_yet_rated=True  
    path='wcloud_pictures/'+track_pseudo+'.png'
    
    try:
        REVIEW=Track_Coments.objects.get(user=request.user,track=track)        
    except:
        has_yet_rated=False             
        
#    load_wordcloud(track_pseudo,'')
    if request.method=='GET':      
        ## apply weight to the historic      
        
#        t2=history.objects.filter(user=request.user).order_by('-start_time')[0] 
#        historic=history_update(t2)  
#        w=predict_type(request.user,historic,track)              
#     
#        l=evaluate_actions(request.user,historic,track,w,t2)
        
        
        
        
        
#        start = timeit.default_timer()
#        stop = timeit.default_timer()
#        print "tps de evaluate actions"
#        print stop - start 
#        l=['closer','close','alone']
#        print l
        
#        print l
        liste=[]
        N=4
        for i in range(N):
            liste.append('None')   
##       
#
#
#
#
        print 'methode GEET DE FICHE TRACK'
################################################################    
        t=Traj.objects.filter(user=request.user).order_by('-start_time')[0]  
        length=len(t.path)
        print t.path
        if t.path[length-1]=='start':
            t.path.append(track_pseudo)
            print 'iciciiiiicicii'
            ### on obtient START  S
            ### OK
        if type(t.path[length-1])==list:
            print 'alalalal'
            ### S A R  ou  S A
            if len(t.path[length-1])<=2:
                ###  S A R
                print 'susususu'
                t.path.append(track_pseudo)
                ### S A R S
            else:
                print 'ohohoh'
                ### S A
                if t.path[length-2]!=track_pseudo:
                    print 'il a actualiserrrr'
                    t.path.append([0.0,0.0])
                    t.path.append(track_pseudo)
        t.save()
                
                
                
#        if t.path[length-1]!=str:
#            ### car S S  be marchera pas
#            ### S A R   OU S A
#            if t.path[length-1]==list:
#                if len(t.path[length-1])>=2:
#                    ### S A 
#                    if t.path[length-2]!=track_pseudo:
#                        t.path.append([0.0,0.0])
#                        t.path.append(track_pseudo)
#                    ### on obtient S A  [0,0] S
#                else:
#                    ### S A R
#                    t.path.append(track_pseudo)
#                    ### on obtient S A R S
#        t.save() 
#        length=len(t.path)
#        if type(t.path[length-1])==list:                          
#             t.path.append(track_pseudo)
#             t.save()                    
#        elif type(t.path[length-1].encode('ascii','ignore'))==str and t.path[length-1]!=track_pseudo: 
#        ##### il a fait une page precedente donc on va coller  la liste l  puis reward [0,0,0]
##             t.path.append(l)
##             t.path.append([0.0,0.0])
#             t.path.append(track_pseudo)
#             t.save()       
                
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

                    Track_Coments.objects.filter(track=track).count()
                    track.save()  
                    has_yet_rated=True
#                    if wordcloud!='':
#                        load_wordcloud(track_pseudo,wordcloud)
                    has_just_commented=True
                    print '-------------------'
                    print request.POST.get('time_before_rated','')
                    time_before=float(request.POST.get('time_before_rated',''))  
                  
                
                return render(request,'fiche_track.html',locals())
        
        elif 'queue' in request.POST:
             print 'queuuuuuuuuuuuuuuuuuue'
   
             #c=request.POST.get('next_song','') 
             titre_1=request.POST.get('titre_1','')
             titre_2=request.POST.get('titre_2','')
             print titre_1
             print titre_2
             t=Traj.objects.filter(user=request.user).order_by('-start_time')[0]  
#             name=str(t.path[len(t.path)-2])
             
                  
             
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
             
#             liste=request.POST.get('liste2','')
#             t.path.append(liste)
             t.path.append([listening_time,percentage])
#           
             t.save()       
             #### history registering
             t2=history.objects.filter(user=request.user).order_by('-start_time')[0] 
             # on cherche le type de la musique 
#             genre=str(Tracks.objects.filter(track_pseudo=name).track_genre)
             genre=get_object_or_404(Tracks, track_pseudo=track_pseudo).track_genre    
             
    
             # on inscrit le nom du track           
             
             length_t2=len(t2.path)
             
             if str(t2.path[length_t2-2][0])!=track_pseudo:     
                
                 t2.path.append([track_pseudo,genre])    
                 t2.path.append([listening_time,percentage])
                
             
             for l in t2.novelty:
                for p in range(len(t2.novelty[l])):
                    if t2.novelty[l][p][0]<novelty_parameters:                  
                        t2.novelty[l][p][0]+=1.0
           
             if float(listening_time)>=novelty_limit:
#                 print np.array(t2.novelty[track.track_genre])
#                 print np.shape(np.array(t2.novelty[track.track_genre])                 
                 if t2.novelty[track.track_genre][songs_keys[track.track_genre][track.track_pseudo]][0]==novelty_parameters:                
                     t2.novelty[track.track_genre][songs_keys[track.track_genre][track.track_pseudo]][0]=0.0                       
                         
                     
             t2.save()
             
             
             if str(titre_2)=='empty': 
                 print 'laaaa'                                   
                 return redirect(reverse('fiche_track',kwargs={'track_pseudo': titre_1}))
             else:   
                 print 'iiciii'
                 return redirect(reverse('solo',kwargs={'titre_1': titre_1,'titre_2':titre_2}))

## homepage
        elif 'liste' in request.POST:
            t=Traj.objects.filter(user=request.user).order_by('-start_time')[0]
            #name=str(t.path[len(t.path)-2])
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
                       
            
#            liste=request.POST.get('liste','')
#            t.path.append(liste)
            t.path.append([listening_time,percentage])
            
            t.path.append('end')
            t.save()
            
            #### history registering
            t2=history.objects.filter(user=request.user).order_by('-start_time')[0] 
            # on cherche le type de la musique
            
            genre=get_object_or_404(Tracks, track_pseudo=track_pseudo).track_genre   
#            genre=str(Tracks.objects.filter(track_pseudo=name)[0].track_genre)
            # on inscrit le nom du track     
            
           
            
            
            length_t2=len(t2.path)
             
            if str(t2.path[length_t2-2][0])!=track_pseudo:     
                
                 t2.path.append([track_pseudo,genre])    
                 t2.path.append([listening_time,percentage])
                 
                 
            for l in t2.novelty:
                for p in range(len(t2.novelty[l])):
                    if t2.novelty[l][p][0]<novelty_parameters:                  
                        t2.novelty[l][p][0]+=1.0
           
            
            
            if float(listening_time)>=novelty_limit:
#                 print np.array(t2.novelty[track.track_genre])
#                 print np.shape(np.array(t2.novelty[track.track_genre])
                 
                 if t2.novelty[track.track_genre][songs_keys[track.track_genre][track.track_pseudo]][0]==novelty_parameters:                
                     t2.novelty[track.track_genre][songs_keys[track.track_genre][track.track_pseudo]][0]=0.0          
               
                     
            t2.save()
            return redirect(reverse('homepage'))
        
## logout        
        elif 'liste3' in request.POST:
            t=Traj.objects.filter(user=request.user).order_by('-start_time')[0]
#            name=str(t.path[len(t.path)-2])
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
                       
            
            liste=request.POST.get('liste3','')
#            t.path.append(liste)
            t.path.append([listening_time,percentage])
            
            ## checker si end n est pqs deja mis
            ## voir si on keep track de la note de la zik aussi
            t.path.append('end')
            t.save()
            
            #### history registering
            t2=history.objects.filter(user=request.user).order_by('-start_time')[0] 
            # on cherche le type de la musique   
#            genre=str(Tracks.objects.filter(track_pseudo=name)[0].track_genre)
            genre=get_object_or_404(Tracks, track_pseudo=track_pseudo).track_genre   
            # on inscrit le nom du track           
            
            
            
            length_t2=len(t2.path)
             
            if str(t2.path[length_t2-2][0])!=track_pseudo:     
                
                 t2.path.append([track_pseudo,genre])    
                 t2.path.append([listening_time,percentage])
                 
                 
            
            for l in t2.novelty:
                for p in range(len(t2.novelty[l])):
                    if t2.novelty[l][p][0]<novelty_parameters:                  
                        t2.novelty[l][p][0]+=1.0
            if float(listening_time)>=novelty_limit:
#                 print np.array(t2.novelty[track.track_genre])
#                 print np.shape(np.array(t2.novelty[track.track_genre])
                 
                 if t2.novelty[track.track_genre][songs_keys[track.track_genre][track.track_pseudo]][0]==novelty_parameters:                
                     t2.novelty[track.track_genre][songs_keys[track.track_genre][track.track_pseudo]][0]=0.0          
              
            t2.save()
            return redirect(reverse('logout'))
        
################################################################
     
   
        
###############################################################         

        
@login_required         
def solo(request,titre_1,titre_2):
    novelty_parameters=2
    novelty_limit=60
    songs_keys=np.load(os.path.join(settings.STATIC_ROOT, 'data/songs_keys.npy')).item()  
    base_2=True
    track=get_object_or_404(Tracks, track_pseudo=titre_1)
    track2= get_object_or_404(Tracks, track_pseudo=titre_2)
    path='wcloud_pictures/'+titre_1+'.png'
    if Track_Coments.objects.filter(track=track,user=request.user).exists():
        has_yet_rated=True
        review=Track_Coments.objects.filter(track=track)
    else:
        has_yet_rated=False
    print has_yet_rated
    
    if request.method=='GET':
        
        # check si existe pas deja
        t=Traj.objects.filter(user=request.user).order_by('-start_time')[0]
        length=len(t.path)
        print 'sooloooo'
        if t.path[length-5]!=titre_1:
            t.path.append(titre_1)
            t.path.append(['None','None',titre_2])
        
        t.save()
        
#        if type(t.path[length-1])==list:
#                   
#            t.path.append(titre_1)
#            t.save() 
#            #return render(request,'fiche_track2.html',locals())
#        elif type(t.path[length-1].encode('ascii','ignore'))==str: 
#            if t.path[length-1]!=titre_1:    
#              
#                
#                t.path.append(titre_1)
#                t.path.append(['None','None',titre_2])
#                t.save() 
                
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
#                    if wordcloud!='':
#                        load_wordcloud(titre_1,wordcloud)
                    has_just_commented=True
                    time_before=float(request.POST.get('time_before_rated',''))
                return render(request,'fiche_track2.html',locals())
        elif 'solo' in request.POST:
             print 'methode = POST _solo________________'
             #c=request.POST.get('titre_2','')  
             t=Traj.objects.filter(user=request.user).order_by('-start_time')[0]   
             
#             name=str(t.path[len(t.path)-2])
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
             
             #liste=request.POST.get('liste2','')
            
#             t.path.append(['None','None',titre_2])
             length=len(t.path)
             if t.path[length-5]!=titre_1:
                 t.path.append([listening_time,'option'])
#          
             t.save()
             t2=history.objects.filter(user=request.user).order_by('-start_time')[0] 
             # on cherche le type de la musique
             genre=get_object_or_404(Tracks, track_pseudo=track.track_pseudo).track_genre   
#             genre=str(Tracks.objects.filter(track_pseudo=name)[0].track_genre)
             # on inscrit le nom du track           
             length_t2=len(t2.path)
             
             if str(t2.path[length_t2-2][0])!=track.track_pseudo:     
                
                 t2.path.append([track.track_pseudo,genre])    
                 t2.path.append([listening_time,percentage])
             
             for l in t2.novelty:
                for p in range(len(t2.novelty[l])):
                    if t2.novelty[l][p][0]<novelty_parameters:                  
                        t2.novelty[l][p][0]+=1.0
             if float(listening_time)>=novelty_limit:
               
#                 print np.shape(np.array(t2.novelty[track.track_genre])
                 
                 if t2.novelty[track.track_genre][songs_keys[track.track_genre][track.track_pseudo]][0]==novelty_parameters:                
                     t2.novelty[track.track_genre][songs_keys[track.track_genre][track.track_pseudo]][0]=0.0          
                
             t2.save()
             return redirect(reverse('fiche_track',kwargs={'track_pseudo': titre_2}))
# homepage

        elif 'home' in request.POST:
            t=Traj.objects.filter(user=request.user).order_by('-start_time')[0]   
            
            name=str(t.path[len(t.path)-2])
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
                       
            
           
#            t.path.append(['None','None',titre_2])
            length=len(t.path)
            if t.path[length-5]!=titre_1:
                 t.path.append([listening_time,'option'])
            else:
                t.path.append([0.0,0.0])
            
            ## checker si end n est pqs deja mis
            ## voir si on keep track de la note de la zik aussi
            t.path.append('end')
            t.save()
            
            t2=history.objects.filter(user=request.user).order_by('-start_time')[0] 
            # on cherche le type de la musique
            
#            genre=str(Tracks.objects.filter(track_pseudo=name)[0].track_genre)
            genre=get_object_or_404(Tracks, track_pseudo=name).track_genre   
            # on inscrit le nom du track           
      
            
            
            length_t2=len(t2.path)
             
            if str(t2.path[length_t2-2][0])!=name:     
                
                 t2.path.append([name,genre])    
                 t2.path.append([listening_time,percentage])
                 
                 
            for l in t2.novelty:
                for p in range(len(t2.novelty[l])):
                    if t2.novelty[l][p][0]<novelty_parameters:                  
                        t2.novelty[l][p][0]+=1.0
                        
            if float(listening_time)>=novelty_limit:
                
#                 print np.shape(np.array(t2.novelty[track.track_genre])
                 
                 if t2.novelty[track.track_genre][songs_keys[track.track_genre][track.track_pseudo]][0]==novelty_parameters:                
                     t2.novelty[track.track_genre][songs_keys[track.track_genre][track.track_pseudo]][0]=0.0          
                 
            t2.save()
            return redirect(reverse('homepage'))
# logout

        elif 'liste3' in request.POST:
            t=Traj.objects.filter(user=request.user).order_by('-start_time')[0]
            
            name=str(t.path[len(t.path)-2])
            
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
            
#            t.path.append(['None','None',titre_2])
            length=len(t.path)
            if t.path[length-5]!=titre_1:
                 t.path.append([listening_time,'option'])
            else:
                 t.path.append([0.0,0.0])
            ## checker si end n est pqs deja mis
            ## voir si on keep track de la note de la zik aussi
            t.path.append('end')
            t.save()
            
            t2=history.objects.filter(user=request.user).order_by('-start_time')[0] 
            # on cherche le type de la musique
            
#            genre=str(Tracks.objects.filter(track_pseudo=name)[0].track_genre)
            genre=get_object_or_404(Tracks, track_pseudo=name).track_genre   
            # on inscrit le nom du track           
            
            
            length_t2=len(t2.path)
             
            if str(t2.path[length_t2-2][0])!=name:     
                
                 t2.path.append([name,genre])    
                 t2.path.append([listening_time,percentage])
                 
                 
            for l in t2.novelty:
                for p in range(len(t2.novelty[l])):
                    if t2.novelty[l][p][0]<novelty_parameters:                  
                        t2.novelty[l][p][0]+=1.0
            if float(listening_time)>=novelty_limit:          
#                 print np.shape(np.array(t2.novelty[track.track_genre])
                 
                 if t2.novelty[track.track_genre][songs_keys[track.track_genre][track.track_pseudo]][0]==novelty_parameters:                
                     t2.novelty[track.track_genre][songs_keys[track.track_genre][track.track_pseudo]][0]=0.0          
               
            t2.save()
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
    if brainstorm!='':     
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
        wordcloud.to_file(os.path.join(settings.STATIC_ROOT+'wcloud_pictures/',track_pseudo+'.jpg'))
        




##############################################################################
##############################################################################
##############################################################################
##############################################################################

    
