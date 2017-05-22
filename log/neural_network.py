import numpy as np
import csv

from django.conf import settings
import os

import timeit

from keras.models import model_from_json

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
    
def convert_to_admissible_actions(action_to_display,N,t2):
    
    url=os.path.join(settings.STATIC_ROOT, 'csv/genre_list.csv')
    with open(url, 'rb') as csvfile:
        text = csv.reader(csvfile, delimiter=',')
        genre_dict = {rows[0]:rows[1] for rows in text}
    reverse_genre=dict((v,k) for k,v in genre_dict.iteritems())
        
    songs_by_type_features=np.load(os.path.join(settings.STATIC_ROOT, 'data/songs_by_type_features.npy')).item()
    #### get the genre to be displayed
#    print songs_by_type_features['Country'].keys().index('my_girl')
    genre=np.round((action_to_display[0][0][0:N]+1)*2.5).astype(int)

    genre_to_display=[]
    for i in genre:
        genre_to_display.append(reverse_genre[str(i)])
   

#    print genre_to_display
    ## normalizing all features to be in [0,1]
#    for i in songs_by_features:
#    
    songs_to_process=action_to_display[1].reshape(8,12)

    
    ###" renormalize everything
    index={}
    for i in range(len(genre_to_display)):
        if genre_to_display[i] not in index.keys():
            index[genre_to_display[i]]=[]
        index[genre_to_display[i]].append(i)
    
#    print index
    normalizer=np.ones(shape=(1,12)).astype('float32')
    ## key
    normalizer[0,4]=11.0
    
    ## loudness
    normalizer[0,6]=-60.0
    
    ## tempo BPM
    normalizer[0,8]=200.0  
    ## signature
    normalizer[0,9]=4.0 
    
#    normalizer[0,11]=100.0
#    normalizer[0,12]=5.0        
    
    
    ### reorganize the type
    feasible_songs=[]
    for i in index:
        
        ll=np.array(songs_by_type_features[i].values())
#        print ll
        ll=ll/normalizer        
        l=list(songs_by_type_features[i].keys())
        
        for j in index[i]:
         
            aa=np.sum(np.power((songs_to_process[j,:]-ll),2),axis=1)
            square_dist=aa.reshape(len(aa),1)
            normalized_square_dist=np.multiply(square_dist,nov_recovery((np.array(t2.novelty[i]))))
            min_index=np.argmin(normalized_square_dist)
#            print normalized_square_dist
            feasible_songs.append(l[min_index])
#            if l[min_index]=='my_girl':
#                print square_dist
#                print normalized_square_dist
#                print min_index
#                print l
                
            ## the song wont be choosen again
            ll[min_index,:]=100000
#        print 'ahah'
#        print np.shape(square_dist)
#        print np.shape(t2.novelty[i])
#        print np.shape(  (np.array(t2.novelty[i]))             )
#        print 'lool'
#        print np.shape(nov_recovery(np.array( t2.novelty[i] )))
#        print 'la distance'
#        print np.shape(normalized_square_dist)
#    print index
    
#    print feasible_songs
    return feasible_songs
        
        

        
        

#@profile
def display_songs(user,historic,track_pseudo,model,epsilon,N,t2):
        songs=np.load(os.path.join(settings.STATIC_ROOT, 'data/songs.npy')).item()
        
        
        ## epsilon-greedy policy
#        epsilon=0.0
        if np.random.rand(1)[0]<=epsilon:
        ## exploration
            choice=np.random.choice(len(songs.keys()), N)
            l=[]
            for i in choice:
                l.append(songs.keys()[i])
            
        
        else:
            
  
            url=os.path.join(settings.STATIC_ROOT, 'csv/user_features_list.csv')
            with open(url, 'rb') as csvfile:
                text = csv.reader(csvfile, delimiter=',')
                user_features_dict = {rows[0]:rows[1] for rows in text}            
            user_dim=len(user_features_dict)
        
            user_features=np.zeros(user_dim)
            
            profilee=get_object_or_404(Profile, user=user)   
            
            ## fill up the matrix
            user_features[int(user_features_dict[profilee.region])]=1
            user_features[int(user_features_dict[profilee.sex])]=1
            user_features[int(user_features_dict[profilee.age])]=1
            user_features[int(user_features_dict[profilee.area])]=1
            
            
            nb_to_display=np.ones(shape=(1,1))*N
            ss=[historic.reshape(1,len(historic)),songs[track_pseudo].reshape(1,len(songs[track_pseudo])),user_features.reshape(1,len(user_features)),nb_to_display]
#            print len(ss)
            
            g=settings.GRAPH
    
            with tf.Session(graph=g) as sess:
                
           
                model.load_weights(os.path.join(settings.STATIC_ROOT, 'model/uniq_model_weights.h5'))
    
                action_to_display=model.predict(ss)
      
            
            l=convert_to_admissible_actions(action_to_display,N,t2)

#        
#        print l
        return l
        
    

    
    
    
    
    
    
# encode the actor
#@profile
def predict_type(user,historic,track_pseudo,type_model):
    
        songs=np.load(os.path.join(settings.STATIC_ROOT, 'data/songs.npy')).item()

        url=os.path.join(settings.STATIC_ROOT, 'csv/user_features_list.csv')
        with open(url, 'rb') as csvfile:
            text = csv.reader(csvfile, delimiter=',')
            user_features_dict = {rows[0]:rows[1] for rows in text}            
        user_dim=len(user_features_dict)
    
        user_features=np.zeros(user_dim)
        
        profilee=get_object_or_404(Profile, user=user)   
        
        ## fill up the matrix
        user_features[int(user_features_dict[profilee.region])]=1
        user_features[int(user_features_dict[profilee.sex])]=1
        user_features[int(user_features_dict[profilee.age])]=1
        user_features[int(user_features_dict[profilee.area])]=1

#        state=np.concatenate((historic,songs[track_pseudo],user_features))  
        
       
###############
## a effacer
#        print len(songs[track_pseudo])
#        h=historic.reshape(1,len(historic))
#        u=user_features.reshape(1,len(user_features))
#        s=songs[track_pseudo].reshape(1,len(songs[track_pseudo]))
#        
#        ss=[h,s,u]
        ss=[historic.reshape(1,len(historic)),songs[track_pseudo].reshape(1,len(songs[track_pseudo])),user_features.reshape(1,len(user_features))]
##################
        
        ##############################################################
        ### load neural network
        
#        json_file = open(os.path.join(settings.STATIC_ROOT, 'model/state/state_model.json'), 'r')
#        loaded_model_json = json_file.read()
#        json_file.close()
#        type_model = model_from_json(loaded_model_json)


        g=settings.GRAPH
#        with g.as_default():
        with tf.Session(graph=g) as sess:  
#                    init = tf.initialize_all_variables()
#                    sess.run(init) 
            
                    type_model.load_weights(os.path.join(settings.STATIC_ROOT, 'model/state/state_weights.h5'))
#                    r.predict([rr,rrr,rrrr])
                
#                    r.load_weights(os.path.join(settings.STATIC_ROOT, 'model/state/state_weights.h5'))
#                    type_model.load_weights(os.path.join(settings.STATIC_ROOT, 'model/state/state_weights.h5'))

                    
    
#                    actor_policy=type_model.predict(ss).astype('float32')
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
   
#        init = tf.global_variables_initializer()
#        sess.run(init)   
    

#    w[0]=['Pop','Latin','Rock','Country']
    
    if len(w[0])==4:

#        json_file = open(os.path.join(settings.STATIC_ROOT, 'model/action/action_model.json'), 'r')
#        loaded_model_json = json_file.read()
#        json_file.close()
#        action_model = model_from_json(loaded_model_json)
        
        g=settings.GRAPH
        
        action_model=settings.ACTION_MODEL
        with tf.Session(graph=g) as sess:   
            ######### single actions no correlations
            songs_by_type=np.load(os.path.join(settings.STATIC_ROOT, 'data/songs_by_type.npy')).item()
            songs_list=np.load(os.path.join(settings.STATIC_ROOT, 'data/songs_list.npy')).item()
            songs=np.load(os.path.join(settings.STATIC_ROOT, 'data/songs.npy')).item()
            

            action_model.load_weights(os.path.join(settings.STATIC_ROOT, 'model/action/action_weights.h5'))
            
            ######## 4 types differents
            choice=[]
  
            for i in w[0]:
                
                
                
    #                single_action_values[i]=[]
            
    
                    s=np.array(songs_by_type[i].values())
                  
        
    #                    hist=np.tile(historic.astype('float32'),(len(s),1))
    #                    feat=np.tile(user_features.astype('float32'),(len(s),1))
    #                   
    #                    Z=np.zeros(shape=(len(s),len(songs['closer'])))
    #                    state_songs=np.tile(songs[track_pseudo],(len(s),1))
                    
    #                    r=[state_songs,s,Z ,hist,feat]
                    r=[np.tile(songs[track_pseudo],(len(s),1)),np.array(songs_by_type[i].values()),np.zeros(shape=(len(s),len(songs['closer']))),np.tile(historic.astype('float32'),(len(s),1)),np.tile(user_features.astype('float32'),(len(s),1))]
#                    print np.shape(r)
#                    print 'ici le shape de r de predict type'
        
        
        #                single_action_values[i]=ddd
        #                cc=np.argmax(single_action_values[i])
        #                cc=np.argmax(ddd)
        
        #                choice.append(songs_list[i][cc])
                   
        
        
        
                    ddd=np.multiply(action_model.predict(r).astype('float32'),nov_recovery((np.array(t2.novelty[i]).astype('float32'))))
                    c=[]
                    for k in ddd:
                        c.append(k[0])
                    MAX=np.max(ddd)
        
#                    print np.exp(c/(MAX*0.25))/np.sum(np.exp(c/(MAX*0.25)))
#                    choix=np.random.choice(len(ddd),1,p=c/np.sum(c),replace=True)
                    choix=np.random.choice(len(ddd),1,p=np.exp(c/(MAX*0.25))/np.sum(np.exp(c/(MAX*0.25))),replace=True)
                    
                    choice.append(songs_list[i][choix[0]])
        
                    
                    
#                    choice.append(songs_list[i][np.argmax(ddd)])
#            print ddd
#            p=ddd/np.sum(ddd)
##            print np.shape(p)
#            print list(p[:,0])
#            c=[]
#            for k in ddd:
#                c.append(k[0])
#
#            choix=np.random.choice(len(ddd),1,p=c/np.sum(c),replace=True)
#            print choix[0]
#            print songs_list[i][choix[0]]

#            sess.close()    
         

            

    
    else:
      
#            with tf.Session() as sess:  
        choice=PulpSolve(4,w,historic,user_features,t2,track_pseudo)
#                sess.close()     
#            return choice
        
                      
        
    return choice         
       
       
       

#@profile
def PulpSolve(N,w,historic,user_features,t2,track_pseudo):
    
#    start = timeit.default_timer()
     
    
############### loading data ##############
    url=os.path.join(settings.STATIC_ROOT, 'csv/genre_list.csv')
    with open(url, 'rb') as csvfile:
        text = csv.reader(csvfile, delimiter=',')
        genre_dict = {rows[0]:rows[1] for rows in text}
        
    songs_keys=np.load(os.path.join(settings.STATIC_ROOT, 'data/songs_keys.npy')).item()    
#    correlations_by_type=settings.CORRELATION
    correlations_by_type=np.load(os.path.join(settings.STATIC_ROOT, 'data/correlations_by_type.npy')).item()
    list_correlations=np.load(os.path.join(settings.STATIC_ROOT, 'data/list_correlations.npy')).item()
    songs_by_type=np.load(os.path.join(settings.STATIC_ROOT, 'data/songs_by_type.npy')).item()
    songs_list=np.load(os.path.join(settings.STATIC_ROOT, 'data/songs_list.npy')).item()
    songs=np.load(os.path.join(settings.STATIC_ROOT, 'data/songs.npy')).item()
    
    
    ## loading neural net model
#    json_file = open(os.path.join(settings.STATIC_ROOT, 'model/action/action_model.json'), 'r')
#    loaded_model_json = json_file.read()
#    json_file.close()
#    aa = model_from_json(loaded_model_json)
    
    g=settings.GRAPH
    action_model=settings.ACTION_MODEL
    with tf.Session(graph=g) as sess:  
        action_model.load_weights(os.path.join(settings.STATIC_ROOT, 'model/action/action_weights.h5'))
        
        
        double_action_values={}
        single_action_values={}
        start = timeit.default_timer()  
        prob = LpProblem("Songs recommendation",LpMaximize)
        var={}
        c=0    
        nb={}
        d=0 

        for i in w[0]:
            cc=0
            nb[i]=1
            var[i]={}
               
        ###########
        ########## double actions
            double_action_values[i]=[]
            single_action_values[i]=[]
#            hist=np.tile(historic,(len(correlations_by_type[i][0]),1)) 
#            feat=np.tile(user_features,(len(correlations_by_type[i][0]),1))
#            state_songs=np.tile(songs[track_pseudo],(len(correlations_by_type[i][0]),1))    

            
            
#            s1=np.array(correlations_by_type[i][0])
#            s2=np.array(correlations_by_type[i][1])
#            rr=[state_songs, s1 , s2 ,hist,feat]
            rr=[np.tile(songs[track_pseudo],(len(correlations_by_type[i][0]),1)) ,np.array(correlations_by_type[i][0]),np.array(correlations_by_type[i][1]), np.tile(historic,(len(correlations_by_type[i][0]),1)) , np.tile(user_features,(len(correlations_by_type[i][0]),1))                 ]
          

#            print np.shape(s1)
#            print np.shape(s2)
#            print np.shape(feat)
       
         
        
            jj=genre_dict[i]

            ## correlations actions
            double_action_values[i]=action_model.predict(rr)
#            print double_action_values[i]
#            print action_model.predict(rr)
            
            ###########
            ########## single actions
            s=np.array(songs_by_type[i].values())
#            hist=np.tile(historic,(len(s),1))
#            feat=np.tile(user_features,(len(s),1))
#            state_songs=np.tile(songs[track_pseudo],(len(s),1))   
#            Z=np.zeros(shape=(len(s),len(songs['closer'])))
            
#            rr=np.concatenate((hist,state_songs,s,feat),axis=1)
          
            rr=[np.tile(songs[track_pseudo],(len(s),1)),np.array(songs_by_type[i].values()),np.zeros(shape=(len(s),len(songs['closer']))) ,np.tile(historic,(len(s),1)),np.tile(user_features,(len(s),1))]
            
    
            
                    
            ddd=np.multiply(action_model.predict(rr).astype('float32'),nov_recovery(np.array(t2.novelty[i]).astype('float32')))
        
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
#        stop = timeit.default_timer()
#        print 'tps pr add constraints'
#        print stop - start 
    ##    
#        start = timeit.default_timer()
    #    prob.solve(pulp.COIN_CMD(dual=True,mip=1,msg=1))
        prob.solve(pulp.PULP_CBC_CMD(dual=True))
    
#        prob.solve(pulp.GLPK(mip=1))
        
    #    prob.solve(pulp.GUROBI(mip=1))
    #    pa='https://s3.ca-central-1.amazonaws.com/music-rec/solver/cbc'
        
    #    pa=os.path.join(settings.STATIC_ROOT, 'cbc') 
        
#        solver = pulp.COIN_CMD(dual=True,path='cbc')
#        
#    
#        prob.solve(solver)
    
        
#        stop = timeit.default_timer()
#        print "tps de solve"
#        print stop - start 
    
    
#        print 'constraints'
#        print len(prob.constraints)
#        print 'variables'
#        print len(prob.variables())
    
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
            

            if nb[i]%2==0:
            
    #            z=np.random.choice(len(y[i]),1,replace=False,p=(y[i].values()/np.sum(y[i].values())) )[0] 
#                print 'length'
#                print len(y[i])
#                print 'size de p'
#                print np.sum(y[i].values())
#                print y[i].values()
                
#                print len(proba)
                
                proba=y[i].values()/np.sum(y[i].values())
#                print proba
    
                z=np.random.choice(len(y[i]),nb[i]/2,replace=False,p=proba)
            
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
        return np.exp(-x/1.3)
  
 
    
#import numpy as np
#import matplotlib.pyplot as plt
#t = np.arange(0., 5., 1)
#plt.plot(t, np.exp(-t/3), 'bs')




        
