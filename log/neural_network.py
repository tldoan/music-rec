import numpy as np
import csv
from django.conf import settings
from .models import history, Profile, Tracks
import os
from django.shortcuts import render,redirect, get_object_or_404
from keras.models import Sequential
from keras.layers import Dense, Activation, Input
from scipy.optimize import linprog
import keras
import tensorflow as tf

from keras.models import model_from_json
import h5py
from pulp import *
from operator import itemgetter
import pulp


def history_update(user):
        
        h=history.objects.filter(user=user).order_by('-start_time')[0]  
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
def predict_type(user,historic,track):
    
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

        ## pas besoinde tracj)popularity et track_)nb _rating
        state=np.concatenate((historic,songs[track.track_pseudo],user_features))  
        ss=state.reshape(1,len(state))
        

             
        ##len(state)=205
      
        ##############################################################
        ### load neural network
        with tf.Session() as sess:
     
                url=os.path.join(settings.STATIC_ROOT, 'model/state/state_model.json')
                json_file = open(url, 'r')
                type_actor = json_file.read()
                json_file.close()
                type_model = model_from_json(type_actor)
                
                # load weights into new model
                type_model.load_weights(os.path.join(settings.STATIC_ROOT, 'model/state/state_weights.h5'))
 
        
                actor_policy=type_model.predict(ss).astype('float32')
        sess.close()

       
    
        ## choice
        CHOICE=np.random.choice(len(actor_policy[0]),1,p=(actor_policy/np.sum(actor_policy))[0] )
 
        url=os.path.join(settings.STATIC_ROOT, 'data/actor_policy_list.npy')
        r=list(np.load(url))

        return [r[CHOICE[0]],user_features]


## compute the values of all actions
def evaluate_actions(user,historic,track,w):
        
    user_features=w[1]
    w[0]=['Latin','Rock','Pop']
    
    url=os.path.join(settings.STATIC_ROOT, 'csv/genre_list.csv')
    with open(url, 'rb') as csvfile:
        text = csv.reader(csvfile, delimiter=',')
        genre_dict = {rows[0]:rows[1] for rows in text}
    

    
#        if len(r[CHOICE[0])<=2:
    with tf.Session() as sess:   


        if len(w[0])==4:
            ######### single actions no correlations
            songs_by_type=np.load(os.path.join(settings.STATIC_ROOT, 'data/songs_by_type.npy')).item()
            songs_list=np.load(os.path.join(settings.STATIC_ROOT, 'data/songs_list.npy')).item()
            
            url=os.path.join(settings.STATIC_ROOT, 'model/single_action/single_action.json')
            json_file = open(url, 'r')
            single_actions = json_file.read()
            json_file.close()
            single_action_model = model_from_json(single_actions)
            
            ######## 4 types differents
            choice=[]
            value=0
            single_action_values={}
            for i in w[0]:
                
                single_action_values[i]=[]

                s=np.array(songs_by_type[i].values())
                hist=np.tile(historic,(len(s),1))
                feat=np.tile(user_features,(len(s),1))
                r=np.concatenate((hist,s,feat),axis=1)
                
                jj=genre_dict[i]
               
                # load weights into new model
                single_action_model.load_weights(os.path.join(settings.STATIC_ROOT, 'model/single_action/single_action_weights_'+str(jj)+'.h5'))
     
               
                single_action_values[i]=single_action_model.predict(r).astype('float32')
                cc=np.argmax(single_action_values[i])
                value+=single_action_values[i][cc][0]*historic[int(jj)]
#                print single_action_values[i]
#                print 'i ' +i
#                print 'argmax '+ str(cc)
#                print songs_list[i][cc]
                choice.append(songs_list[i][cc])
            print 'value  len=4'
            print value 
            return choice
        
        else:
            choice=PulpSolve(4,w,historic,user_features)
            return choice
            
#        if len(w[0])==1:
#            N=4
#            #w[0][0]=genre
#            choice=PulpSolve(N,w[0][0],historic,user_features)[0]
#            return choice
#        
#        if len(w[0])==3:
#        #### double action + single action
#            songs_by_type=np.load(os.path.join(settings.STATIC_ROOT, 'data/songs_by_type.npy')).item()
#            songs_list=np.load(os.path.join(settings.STATIC_ROOT, 'data/songs_list.npy')).item()
#            correlations_by_type=np.load(os.path.join(settings.STATIC_ROOT, 'data/correlations_by_type.npy')).item()
#            list_correlations=np.load(os.path.join(settings.STATIC_ROOT, 'data/list_correlations.npy')).item()
#            
#            url=os.path.join(settings.STATIC_ROOT, 'model/double_actions/double_actions.json')
#            json_file = open(url, 'r')
#            double_actions = json_file.read()
#            json_file.close()
#            double_actions_model = model_from_json(double_actions)
#            
#            url=os.path.join(settings.STATIC_ROOT, 'model/single_action/single_action.json')
#            json_file = open(url, 'r')
#            single_actions = json_file.read()
#            json_file.close()
#            single_action_model = model_from_json(single_actions)
#            
#            
#           
#            value=np.zeros(3)
#            choice={}
#            for u in range(3): 
#                choice[u]=[]
#                single_action_values={}
#                for i in range(len(w[0])):
#                   
#                    if i==u:
#                        double_action_values=[]
#            
#                                  
#                        s=np.array(correlations_by_type[w[0][i]])
#                        hist=np.tile(historic,(len(correlations_by_type[w[0][i]]),1)) 
#                        feat=np.tile(user_features,(len(correlations_by_type[w[0][i]]),1))
#                        r=np.concatenate((hist,s,feat),axis=1)
#                           
#            
#                        jj=genre_dict[w[0][i]]
#                        
#                        double_actions_model.load_weights(os.path.join(settings.STATIC_ROOT, 'model/double_actions/double_actions_weights_'+str(jj)+'.h5'))
#                        
#                        double_action_values=double_actions_model.predict(r).astype('float32') 
#                        print w[0][i]
#                        
#    #                    print double_action_values
#                        cc=np.argmax(double_action_values)
##                        print cc
##                        print 'argmax double'
#                        print list_correlations[w[0][i]][cc]
#                        choice[u].extend([i for i in list_correlations[w[0][i]][cc]])
#                        print double_action_values[cc][0] 
#                        value[u]+=float(double_action_values[cc][0]*historic[int(jj)])
#                        
#                    else:
#                        
#                        single_action_values[w[0][i]]=[]
#    
#                        s=np.array(songs_by_type[w[0][i]].values())
#                        hist=np.tile(historic,(len(s),1))
#                        feat=np.tile(user_features,(len(s),1))
#                        r=np.concatenate((hist,s,feat),axis=1)
#                        
#                        jj=genre_dict[w[0][i]]
#                       
#                        # load weights into new model
#                        single_action_model.load_weights(os.path.join(settings.STATIC_ROOT, 'model/single_action/single_action_weights_'+str(jj)+'.h5'))
#             
#                       
#                        single_action_values[w[0][i]]=single_action_model.predict(r).astype('float32')
#                        cc=np.argmax(single_action_values[w[0][i]])
#    #                    print single_action_values[w[0][i]]
##                        print 'argmax '+ str(cc)
##                        print songs_list[w[0][i]][cc]
#                        choice[u].append(songs_list[w[0][i]][cc])
#                        print single_action_values[w[0][i]][cc][0]
#                        value[u]+=float(single_action_values[w[0][i]][cc][0]*historic[int(jj)])
#                    
#            print choice
#            print value
#            print value/np.sum(value)
#            CHOICE=np.random.choice(len(value),1,p=(value/np.sum(value)) )
#            return choice[CHOICE[0]]
#        
#        else:
#            ### length ==2
#            value=np.zeros(3)
#            url=os.path.join(settings.STATIC_ROOT, 'model/double_actions/double_actions.json')
#            json_file = open(url, 'r')
#            double_actions = json_file.read()
#            json_file.close()
#            double_actions_model = model_from_json(double_actions)
#            
#            correlations_by_type=np.load(os.path.join(settings.STATIC_ROOT, 'data/correlations_by_type.npy')).item()
#            list_correlations=np.load(os.path.join(settings.STATIC_ROOT, 'data/list_correlations.npy')).item()
#            
#        
#            choice={}
#            double_action_values={}
#            choice[0]=[]
#            
#            for i in range(len(w[0])):
#                ### 2 double correlation
#              
#                double_action_values[w[0][i]]=[]
#            
#                                  
#                s=np.array(correlations_by_type[w[0][i]])
#                hist=np.tile(historic,(len(correlations_by_type[w[0][i]]),1)) 
#                feat=np.tile(user_features,(len(correlations_by_type[w[0][i]]),1))
#                r=np.concatenate((hist,s,feat),axis=1)
#                   
#    
#                jj=genre_dict[w[0][i]]
#                
#                double_actions_model.load_weights(os.path.join(settings.STATIC_ROOT, 'model/double_actions/double_actions_weights_'+str(jj)+'.h5'))
#                
#                double_action_values[w[0][i]]=double_actions_model.predict(r).astype('float32') 
#              
#                
##                    print double_action_values
#                cc=np.argmax(double_action_values[w[0][i]])
##                        print cc
##                        print 'argmax double'
#        
#                value[0]+=double_action_values[w[0][i]][cc][0]*historic[int(jj)]*0.5
#                print double_action_values[w[0][i]][cc]
#                print value
#                print 'valuuee_______________________'
#                print cc
#                print list_correlations[w[0][i]][cc]
#                choice[0].extend([i for i in list_correlations[w[0][i]][cc]])
##                print double_action_values[w[0][i]][cc]
#            
#            choice[1]=PulpSolve(3,w[0][0],historic,user_features)[0]   
#            value[1]=PulpSolve(3,w[0][0],historic,user_features)[1] 
#            print value
#            print choice
#            print 'choice'
#            print choice[0]
#            return choice[0]
                             
               
    sess.close()              
       
       
       
       


def PulpSolve(N,w,historic,user_features):

############### loading values ##############
    url=os.path.join(settings.STATIC_ROOT, 'csv/genre_list.csv')
    with open(url, 'rb') as csvfile:
        text = csv.reader(csvfile, delimiter=',')
        genre_dict = {rows[0]:rows[1] for rows in text}
        
        
    correlations_by_type=np.load(os.path.join(settings.STATIC_ROOT, 'data/correlations_by_type.npy')).item()
    list_correlations=np.load(os.path.join(settings.STATIC_ROOT, 'data/list_correlations.npy')).item()
    songs_by_type=np.load(os.path.join(settings.STATIC_ROOT, 'data/songs_by_type.npy')).item()
    songs_list=np.load(os.path.join(settings.STATIC_ROOT, 'data/songs_list.npy')).item()
    
    #### correlation terms
    url=os.path.join(settings.STATIC_ROOT, 'model/double_actions/double_actions.json')
    json_file = open(url, 'r')
    double_actions = json_file.read()
    json_file.close()
    double_actions_model = model_from_json(double_actions)
    
    ### single actions terms
    url=os.path.join(settings.STATIC_ROOT, 'model/single_action/single_action.json')
    json_file = open(url, 'r')
    single_actions = json_file.read()
    json_file.close()
    single_action_model = model_from_json(single_actions)
    
    
    double_action_values={}
    single_action_values={}
    
    prob = LpProblem("Songs recommendation",LpMaximize)
    var={}
    c=0    
    for i in w[0]:
      
        var[i]={}
           
    ###########
    ########## double actions
        double_action_values[i]=[]
        single_action_values[i]=[]
        
                               
        s=np.array(correlations_by_type[i])
        hist=np.tile(historic,(len(correlations_by_type[i]),1)) 
        feat=np.tile(user_features,(len(correlations_by_type[i]),1))
        rr=np.concatenate((hist,s,feat),axis=1)
        
        jj=genre_dict[i]
        # load weights into new model
        double_actions_model.load_weights(os.path.join(settings.STATIC_ROOT, 'model/double_actions/double_actions_weights_'+str(jj)+'.h5'))  
        double_action_values[i]=double_actions_model.predict(rr).astype('float32') 
        
        ###########
        ########## single actions
        s=np.array(songs_by_type[i].values())
        hist=np.tile(historic,(len(s),1))
        feat=np.tile(user_features,(len(s),1))
        rr=np.concatenate((hist,s,feat),axis=1)
                    
        # load weights into new model
        single_action_model.load_weights(os.path.join(settings.STATIC_ROOT, 'model/single_action/single_action_weights_'+str(jj)+'.h5'))     
        single_action_values[i]=single_action_model.predict(rr).astype('float32')
        
  
    
#        print np.shape(double_action_values[i])
#        print np.shape(single_action_values[i])
        
        
        
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
        ## ojective function
        c+= lpSum(historic[int(jj)]*var[i]['Y'][(r)]*double_action_values[i][list_correlations[i].index(r)] for r in z)
        +lpSum(historic[int(jj)]*var[i]['X'][(r)]*single_action_values[i][songs_list[i].index(r)] for r in L)
        -lpSum(historic[int(jj)]*(-var[i]['L'][(r)])*single_action_values[i][songs_list[i].index(r)] for r in L)
        ## objective value
    
    prob+=c     
#        
#        prob += lpSum(historic[int(jj)]*var[i]['X'][(r)]*single_action_values[i][list_correlations[i].index(r)] for r in L)
#        prob += lpSum(historic[int(jj)]*(-var[i]['L'][(r)])*single_action_values[i][list_correlations[i].index(r)] for r in L)

         
    d=0   
    nb={}
    for i in w[0]:
        nb[i]=1
        L=songs_by_type[i].keys()
#        z = list(combination(L,2))
        z=list_correlations[i]
        corr=[(r) for r in z]
        
#        prob += 10*lpSum(var[i]['Y'][(r)] for r in z)+lpSum(var[i]['X'][(r)] for r in L)-lpSum((var[i]['L'][(r)]) for r in L)
#        prob += lpSum(var[i]['X'][(r)] for r in L)
#        prob += lpSum((-var[i]['L'][(r)]) for r in L)
        
        prob += lpSum(var[i]['X'][(r)]  for r in L) ==1
        
        
        for r in z:
            prob += var[i]['Y'][(r)]  <= var[i]['X'][r[0]]
            prob += var[i]['Y'][(r)]  <= var[i]['X'][r[1]]
            prob += var[i]['Y'][(r)]  <= var[i]['L'][r[0]]
            prob += var[i]['Y'][(r)]  <= var[i]['L'][r[1]]
        
        for r in L:
            prob+=var[i]['X'][r] <= var[i]['n'][r]
    
            
        d+= lpSum(var[i]['n'][r] for r in L) 
    prob+=d==N       
            
        
#    prob.writeLP(os.path.join(settings.STATIC_ROOT, 'lol.lp'))
#        prob.writeLP('lol.lp')
#    prob.solve(pulp.GLPK())
    prob.solve(pulp.COIN_CMD(dual=True))
#    prob.sovle()
#    prob.solve(pulp.PULP_CBC_CMD(dual=True))
# prob.solve(pulp.PULP_CBC_CMD(dual=True,mip=1))
# pulp.pulpTestAll()
#    print pulp.value(prob.objective)
    print 'constraints'
    print len(prob.constraints)
    print 'variables'
    print len(prob.variables())
#    q=0
#    for v in prob.variables():
#        if v.varValue>0:
#            q=q+1
#            print v.name, "=", v.varValue
#                
#    print 'q = ' +str(q)
#    print pulp.value(prob.objective)
    c=np.zeros(len(w[0]))
    for i in range(len(w[0])):
        c[i]=historic[int(genre_dict[w[0][i]])]
    x={}
    y={}
#        n={}
    restant=N-len(w[0])
    print 'historic'
    print historic
    print c
    print c/np.sum(c)
    print 'restant'
    print restant
    pion=np.random.choice(len(c),restant,p=c/np.sum(c),replace=True)
    print pion
    print 'pion'
    
    for i in pion:
        nb[w[0][i]]+=1
    print 'nb'
    print nb
    choice=[]
    for i in w[0]:
        
        print type(var[i]['X'])
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
        if nb[i]==2:
            print '22222222222222'
            z=np.random.choice(len(y[i]),1,replace=False,p=(y[i].values()/np.sum(y[i].values())) )[0] 
            print z
            print y[i].keys()[z]
            choice.extend(y[i].keys()[z])
        else:
            z=np.random.choice(len(x[i]),nb[i],replace=False,p=(x[i].values()/np.sum(x[i].values())) )
            print z
           
            for ii in z:         
                choice.append(x[i].keys()[ii])
        #print x[i].keys()[z]
#    print len(choice)
#   
#    print np.sum(var['Latin']['L'].values())
    
    return choice

        
#    for i in songs_by_type:
#            x[i]=X[i].value()
#    for i in list_correlations['Latin']:
#            y[i]=Y[i].value()
#    print x
            
#        rr=sorted(x.items(), key=itemgetter(1),reverse=True)
#        choice=[]
#        for i in range(N):
#            choice.append(rr[i][0])
#    return choice
#def PulpSolve(N,genre,historic,user_features):
#    
#    url=os.path.join(settings.STATIC_ROOT, 'csv/genre_list.csv')
#    with open(url, 'rb') as csvfile:
#        text = csv.reader(csvfile, delimiter=',')
#        genre_dict = {rows[0]:rows[1] for rows in text}
#        
#    correlations_by_type=np.load(os.path.join(settings.STATIC_ROOT, 'data/correlations_by_type.npy')).item()
#    list_correlations=np.load(os.path.join(settings.STATIC_ROOT, 'data/list_correlations.npy')).item()
#    songs_by_type=np.load(os.path.join(settings.STATIC_ROOT, 'data/songs_by_type.npy')).item()
#    #### only correlations will play a role  
#    url=os.path.join(settings.STATIC_ROOT, 'model/double_actions/double_actions.json')
#    json_file = open(url, 'r')
#    double_actions = json_file.read()
#    json_file.close()
#    double_actions_model = model_from_json(double_actions)
#    
#    
#    
#    
#    double_action_values=[]
#    
#                           # or w[0][0]
#    s=np.array(correlations_by_type[genre])
#    hist=np.tile(historic,(len(correlations_by_type[genre]),1)) 
#    feat=np.tile(user_features,(len(correlations_by_type[genre]),1))
#    r=np.concatenate((hist,s,feat),axis=1)
#       
#    
#    jj=genre_dict[genre]
#    
#    double_actions_model.load_weights(os.path.join(settings.STATIC_ROOT, 'model/double_actions/double_actions_weights_'+str(jj)+'.h5'))
#    
#    double_action_values=double_actions_model.predict(r).astype('float32') 
#    
#    print type(double_action_values)
#    print np.shape(double_action_values)
#    print 'loool'
#    #            print double_action_values(list_correlations[w[0][0]].index(('god_your_mama_and_me', 'every_time_i_hear_that_song')))[0]
#    #            print double_action_values[list_correlations['Pop'].index(('say_you_wont_let_go', 'pillowtalk'))]
#    
#    prob = LpProblem("Songs recommendation",LpMaximize)
#    L=songs_by_type[genre].keys()
#    
#    #            z = list(combination(L,2))
#    z=list_correlations[genre]
#    corr=[(i) for i in z]
#    
#    #LpContinuous
#    #LpBinary
#    Y=LpVariable.dicts("y", corr, 0, 1, LpContinuous)
#    X=LpVariable.dicts("x", L, 0, 1, LpContinuous)
#    
#    ## objective value
##    double_action_values[1]=1000
#    
#    prob += lpSum(Y[(i)]*double_action_values[list_correlations[genre].index(i)] for i in z),'total values'
#    
#    
#    prob += lpSum(X[i]  for i in L) <=N
#    
#    for i in z:
#        prob += Y[(i)]  <= X[i[0]]
#        prob += Y[(i)]  <= X[i[1]]
#    
#    prob.writeLP(os.path.join(settings.STATIC_ROOT, 'lol.lp'))
#    prob.solve()
#    
#
#    
##    q=0
###    for v in prob.variables():
###        if v.varValue>0:
###            q=q+1
###  #             print v.name, "=", v.varValue
##
##            
##    print 'q = ' +str(q)
#    print pulp.value(prob.objective)
#    
#    x={}
#    y={}
#    for i in songs_by_type['Latin'].keys():
#        x[i]=X[i].value()
#    for i in list_correlations['Latin']:
#        y[i]=Y[i].value()
#        
#    rr=sorted(x.items(), key=itemgetter(1),reverse=True)
#    choice=[]
#    for i in range(N):
#        choice.append(rr[i][0])
#    value=0
#    if N==3:       
#        tu=(rr[0][0],rr[1][0])
#        if tu in list_correlations[genre]:
#            indice=list_correlations[genre].index(tu)
#        else:
#            tu=(rr[1][0],rr[0][0])
#            indice=list_correlations[genre].index(tu)
#        print tu
#        value+=0.5*historic[int(jj)]*double_action_values[indice]
#        
#        tu=(rr[0][0],rr[2][0])
#        if tu in list_correlations[genre]:
#            indice=list_correlations[genre].index(tu)
#        else:
#            tu=(rr[2][0],rr[0][0])
#            indice=list_correlations[genre].index(tu)
#        print tu
#        value+=0.5*historic[int(jj)]*double_action_values[indice]
#        
#        tu=(rr[1][0],rr[2][0])
#        if tu in list_correlations[genre]:
#            indice=list_correlations[genre].index(tu)
#        else:
#            tu=(rr[2][0],rr[1][0])
#            indice=list_correlations[genre].index(tu)
#        print tu
#        value+=0.5*historic[int(jj)]*double_action_values[indice]
#                
#        
#        
#        
#    print [choice,value]
#    return [choice,value]





        