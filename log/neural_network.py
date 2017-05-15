import numpy as np
import csv

from django.conf import settings
import os

import timeit

from keras.models import load_model,model_from_json

from django.shortcuts import  get_object_or_404
from .models import Profile
import tensorflow as tf

from pulp import *
from operator import itemgetter
import pulp
#from memory_profiler import profile




def history_update(h):
        
        url=os.path.join(settings.STATIC_ROOT, 'csv/genre_list.csv')
        hist=h.path
        with open(url, 'rb') as csvfile:
            text = csv.reader(csvfile, delimiter=',')
            genre_dict = {rows[0]:rows[1] for rows in text}       
        historic=np.ones(len(genre_dict))
        temps=0
        power=0
        weight=0.9
        for i in reversed(hist):
            if type(i)==list:
                if type(i[0])==float:
                    temps=i[0]*np.power(weight,power) 
                    power+=1
                if type(i[0])==unicode:
                    historic[int(genre_dict[i[1]])]+=temps                
         
        historic=historic/np.sum(historic)
        return historic


# encode the actor
#@profile
def predict_type(user,historic,track_pseudo):
    
        songs=np.load(os.path.join(settings.STATIC_ROOT, 'data/songs.npy')).item()

        url=os.path.join(settings.STATIC_ROOT, 'csv/user_features_list.csv')
        with open(url, 'rb') as csvfile:
            text = csv.reader(csvfile, delimiter=',')
            user_features_dict = {rows[0]:rows[1] for rows in text}            
        user_dim=len(user_features_dict)
    
        user_features=np.zeros(user_dim)
        
        profile=get_object_or_404(Profile, user=user)   
        
        ## fill up the matrix
        user_features[int(user_features_dict[profile.region])]=1
        user_features[int(user_features_dict[profile.sex])]=1
        user_features[int(user_features_dict[profile.age])]=1
        user_features[int(user_features_dict[profile.area])]=1

#        state=np.concatenate((historic,songs[track_pseudo],user_features))  
        
        
###############
## a effacer
#        print len(songs[track_pseudo])
        h=historic.reshape(1,len(historic))
        u=user_features.reshape(1,len(user_features))
        s=songs[track_pseudo].reshape(1,len(songs[track_pseudo]))
        
        ss=[h,s,u]
##################
        
        
#        ss=state.reshape(1,len(state))
        
#        print np.shape(user_features)
#        print 'user_features'
#        print np.shape(historic)
#        print 'historic'
#        print np.shape(songs[track.track_pseudo]) 
#        print 'songs[tracks]'

             
        ##len(state)=211
      
        ##############################################################
        ### load neural network
        
        json_file = open(os.path.join(settings.STATIC_ROOT, 'model/state/state_model.json'), 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        type_model = model_from_json(loaded_model_json)
        print 'load from json'

        with tf.Session() as sess:  
#                type_model=load_model(os.path.join(settings.STATIC_ROOT, 'model/state/state_model.h5'))
                type_model.load_weights(os.path.join(settings.STATIC_ROOT, 'model/state/state_weights.h5'))
                
                init = tf.global_variables_initializer()
                sess.run(init)
                
                
                # load weights into new model
            
                

#                rr=np.ones(shape=(1,100))

                actor_policy=type_model.predict(ss).astype('float32')
                

#                print actor_policy
#                print 'print actor _policy !!!!!!!!!!!!!!!!!!!'
#                print np.max(actor_policy)
#                sess.close()

       
#        print actor_policy
        ## choice
        MAX=np.max(actor_policy)
        
        p=np.exp(actor_policy/(MAX*0.25))/np.sum(np.exp(actor_policy/(MAX*0.25)))
#        print p
        CHOICE=np.random.choice(len(actor_policy[0]),1,p=p[0] )
 
        url=os.path.join(settings.STATIC_ROOT, 'data/actor_policy_list.npy')
        r=list(np.load(url))

        return [r[CHOICE[0]],user_features]


## compute the values of all actions
#@profile
def evaluate_actions(user,historic,track_pseudo,w,t2):
    
    
    user_features=w[1]   
#        if len(r[CHOICE[0])<=2:
    
    
    
    json_file = open(os.path.join(settings.STATIC_ROOT, 'model/action/action_model.json'), 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    action_model = model_from_json(loaded_model_json)
    print 'load action from json'
    with tf.Session() as sess:  
#        init = tf.global_variables_initializer()
#        sess.run(init)
        
        start = timeit.default_timer()

        w[0]=['Pop','Latin','Country','Rock']
        if len(w[0])==4:
  
            ######### single actions no correlations
            songs_by_type=np.load(os.path.join(settings.STATIC_ROOT, 'data/songs_by_type.npy')).item()
            songs_list=np.load(os.path.join(settings.STATIC_ROOT, 'data/songs_list.npy')).item()
            songs=np.load(os.path.join(settings.STATIC_ROOT, 'data/songs.npy')).item()
            
#            url=os.path.join(settings.STATIC_ROOT, 'model/action/action_model.h5')
#            action_model = load_model(url)
            # load weights into the model
            action_model.load_weights(os.path.join(settings.STATIC_ROOT, 'model/action/action_weights.h5'))
            
            ######## 4 types differents
            choice=[]
            
            for i in w[0]:
                
                
                
#                single_action_values[i]=[]
            

                    s=np.array(songs_by_type[i].values())
                  
        
                    hist=np.tile(historic.astype('float32'),(len(s),1))
                    feat=np.tile(user_features.astype('float32'),(len(s),1))
                    #rr=np.ones(shape=(len(s),1))
                    Z=np.zeros(shape=(len(s),len(songs['closer'])))
                    state_songs=np.tile(songs[track_pseudo],(len(s),1))
                    
                    r=[state_songs,s,Z ,hist,feat]
          
        #                r=np.concatenate((hist,state_songs,s,feat),axis=1)        
                   
        
        
        #                single_action_values[i]=ddd
        #                cc=np.argmax(single_action_values[i])
        #                cc=np.argmax(ddd)
        
        #                choice.append(songs_list[i][cc])
                   
        
        
        
                    ddd=np.multiply(action_model.predict(r).astype('float32'),nov_recovery((np.array(t2.novelty[i]).astype('float32'))))
                    choice.append(songs_list[i][np.argmax(ddd)])
#            STATE=np.ones(shape=(144,20)) 
#            HIST=np.ones(shape=(144,6))
#            FEAT=np.ones(shape=(144,24))
#            R=[STATE,STATE,STATE ,HIST,FEAT]
#            action_model.predict(R).astype('float32')
#            print len(action_model.predict(R).astype('float32'))
            
            stop = timeit.default_timer()
            print 'tps pr compute neural net'
            print stop - start 
#            sess.close()    
             

                
                
#==============================================================================
#                 STATE.extend(np.tile(songs[track_pseudo],(len(s),1)))
#                 SONGS.extend(songs_by_type[i].values())
#                 HIST.extend(np.tile(historic.astype('float32'),(len(s),1)))
#                 FEAT.extend(np.tile(user_features.astype('float32'),(len(s),1)))
#                 ZEROS.extend(np.zeros(shape=(len(s),len(songs['closer']))))
#             R=[STATE,SONGS,ZEROS ,HIST,FEAT]
#             action_model.predict(R).astype('float32')
#             print len(action_model.predict(R).astype('float32'))
#==============================================================================

        
        else:
            print 'cettte branche'
#            with tf.Session() as sess:  
            choice=PulpSolve(4,w,historic,user_features,t2,track_pseudo)
#                sess.close()     
#            return choice
        
                      
        
    return choice         
       
       
       


def PulpSolve(N,w,historic,user_features,t2,track):
    
#    start = timeit.default_timer()
     
    
############### loading data ##############
    url=os.path.join(settings.STATIC_ROOT, 'csv/genre_list.csv')
    with open(url, 'rb') as csvfile:
        text = csv.reader(csvfile, delimiter=',')
        genre_dict = {rows[0]:rows[1] for rows in text}
        
    songs_keys=np.load(os.path.join(settings.STATIC_ROOT, 'data/songs_keys.npy')).item()    
    correlations_by_type=np.load(os.path.join(settings.STATIC_ROOT, 'data/correlations_by_type.npy')).item()
    list_correlations=np.load(os.path.join(settings.STATIC_ROOT, 'data/list_correlations.npy')).item()
    songs_by_type=np.load(os.path.join(settings.STATIC_ROOT, 'data/songs_by_type.npy')).item()
    songs_list=np.load(os.path.join(settings.STATIC_ROOT, 'data/songs_list.npy')).item()
    songs=np.load(os.path.join(settings.STATIC_ROOT, 'data/songs.npy')).item()
    
    #### correlation terms
    url=os.path.join(settings.STATIC_ROOT, 'model/double_actions/double_actions.h5')
    double_actions_model = load_model(url)
    
    ### single actions terms
    url=os.path.join(settings.STATIC_ROOT, 'model/single_action/single_action.h5')
    single_action_model = load_model(url)
    
    
    double_action_values={}
    single_action_values={}
    start = timeit.default_timer()  
    prob = LpProblem("Songs recommendation",LpMaximize)
    var={}
    c=0    
    nb={}
    d=0 
#    w[0]=['Pop']
    for i in w[0]:
        cc=0
        nb[i]=1
        var[i]={}
           
    ###########
    ########## double actions
        double_action_values[i]=[]
        single_action_values[i]=[]
        
#        coeff2=np.ones(shape=(len(correlations_by_type[i]),1))    
                   
        s=np.array(correlations_by_type[i])
        hist=np.tile(historic,(len(correlations_by_type[i]),1)) 
        feat=np.tile(user_features,(len(correlations_by_type[i]),1))
        state_songs=np.tile(songs[track.track_pseudo],(len(correlations_by_type[i]),1))    
        rr=np.concatenate((hist,state_songs,s,feat),axis=1)
 
#        coeff3=  (( (s[:,0]+s[:,181])*0.5) ).reshape(len(correlations_by_type[i]),1)
     
    
        jj=genre_dict[i]
        # load weights into new model

        double_action_values[i]=double_actions_model.predict(rr).astype('float32') 
       
        ###########
        ########## single actions
        s=np.array(songs_by_type[i].values())
        hist=np.tile(historic,(len(s),1))
        feat=np.tile(user_features,(len(s),1))
        state_songs=np.tile(songs[track.track_pseudo],(len(s),1))   
        
        rr=np.concatenate((hist,state_songs,s,feat),axis=1)
        
#        coeff=np.ones(shape=(len(s),1))
        
        
#        tt=np.array(s)
#        coeff2=(tt[:,0].reshape(len(s),1))/2
        
                
        ddd=np.multiply(single_action_model.predict(rr).astype('float32'),nov_recovery(np.array(t2.novelty[i]).astype('float32')))
#        single_action_values[i]=single_action_model.predict(rr).astype('float32')
#        print ddd
        single_action_values[i]=ddd
  
        
        
        L=songs_by_type[i].keys()
#        z = list(combination(L,2))
        z=list_correlations[i]
        corr=[(r) for r in z]
        
        #LpContinuous
        #LpBinary
        var[i]['Y']=LpVariable.dicts("y", corr, 0, 1, LpContinuous)
        var[i]['X']=LpVariable.dicts("x", L, 0, 1, LpContinuous)
        var[i]['L']=LpVariable.dicts("l", L, 0, 1, LpContinuous)
        var[i]['n']=LpVariable.dicts("n", L, 0, 1, LpContinuous)
        
        
        prob += lpSum(var[i]['X'][(r)]  for r in L) ==1
        
        
        for r in z:
            prob += var[i]['Y'][(r)]  <= var[i]['X'][r[0]]
            prob += var[i]['Y'][(r)]  <= var[i]['X'][r[1]]
            prob += var[i]['Y'][(r)]  <= var[i]['L'][r[0]]
            prob += var[i]['Y'][(r)]  <= var[i]['L'][r[1]]
        
  
        for r in L:
            prob+=var[i]['X'][r] <= var[i]['n'][r]
        
        ## ojective function
        
        d+= lpSum(var[i]['n'][r] for r in L) 
     
        cc+= lpSum(var[i]['Y'][(r)]*double_action_values[i][list_correlations[i].index(r)]*nov_recovery(t2.novelty[i][songs_keys[i][r[0]]][0])*nov_recovery(t2.novelty[i][songs_keys[i][r[1]]][0]) for r in z)
        +lpSum((var[i]['X'][(r)]-var[i]['L'][(r)])*single_action_values[i][songs_list[i].index(r)] for r in L)
#        -lpSum((-var[i]['L'][(r)])*single_action_values[i][songs_list[i].index(r)] for r in L)
        c+=cc*historic[int(jj)]
        ## objective value
    prob+=d==N 
    prob+=c     

#    
    stop = timeit.default_timer()
    print 'tps pr add constraints'
    print stop - start 
##    
    start = timeit.default_timer()
#    prob.solve(pulp.COIN_CMD(dual=True,mip=1,msg=1))
    prob.solve(pulp.PULP_CBC_CMD(dual=True))

#    prob.solve(pulp.GLPK(mip=1))
    
#    prob.solve(pulp.GUROBI(mip=1))
#    pa='https://s3.ca-central-1.amazonaws.com/music-rec/solver/cbc'
    
#    pa=os.path.join(settings.STATIC_ROOT, 'cbc') 
    
#    solver = pulp.COIN_CMD(dual=True,path='cbc')
    

#    prob.solve(solver)

    
    stop = timeit.default_timer()
    print "tps de solve"
    print stop - start 


#    print 'constraints'
#    print len(prob.constraints)
#    print 'variables'
#    print len(prob.variables())

#    start = timeit.default_timer()
    c=np.zeros(len(w[0]))
    for i in range(len(w[0])):
        c[i]=historic[int(genre_dict[w[0][i]])]
    x={}
    y={}
#        n={}
    restant=N-len(w[0])
#    print restant
#    print 'historic'
#    print historic
#    print c
#    print c/np.sum(c)
#    print 'restant'
#    print restant
    pion=np.random.choice(len(c),restant,p=c/np.sum(c),replace=True)
#    print pion
#    print 'pion'
    
    for i in pion:
        nb[w[0][i]]+=1
#    print 'nb'
#    print nb
    choice=[]
    for i in w[0]:
        
#        print type(var[i]['X'])
        x[i]={}
        y[i]={}
        for j in songs_by_type[i]:
            x[i][j]=var[i]['X'][j].value()
        for j in list_correlations[i]:
            y[i][j]=var[i]['Y'][j].value()
        
#        if nb[i]==1:
#            z=np.random.choice(len(x[i]),nb[i],replace=False,p=(x[i].values()/np.sum(x[i].values())) )[0]    
#            choice.append(x[i].keys()[z])
#            print z
#        if nb[i]==2:
        if nb[i]%2==0:
        
#            z=np.random.choice(len(y[i]),1,replace=False,p=(y[i].values()/np.sum(y[i].values())) )[0] 

            z=np.random.choice(len(y[i]),nb[i]/2,replace=False,p=(y[i].values()/np.sum(y[i].values())))
        
            for ee in z:
                choice.extend(y[i].keys()[ee])
#                choice.extend(y[i].keys()[z])
#            print choice
        else:
            z=np.random.choice(len(x[i]),nb[i],replace=False,p=(x[i].values()/np.sum(x[i].values())) )
#            print z
           
            for ii in z:         
                choice.append(x[i].keys()[ii])
#    stop = timeit.default_timer()
#    print "fin du prg"
#    print stop - start 

    
    return choice

        
def nov_recovery(x):
        return 1-np.exp(-x/1.3)
  
 
    
#import numpy as np
#import matplotlib.pyplot as plt
#t = np.arange(0., 5., 1)
#plt.plot(t, 1-np.exp(-t/1.45), 'bs')




        
