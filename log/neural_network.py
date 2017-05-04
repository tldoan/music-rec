import numpy as np
import csv


from django.conf import settings
import os


import timeit


from keras.models import model_from_json,load_model







from django.shortcuts import render,redirect, get_object_or_404
from .models import Profile, Tracks , Traj , history
import tensorflow as tf





from pulp import *
from operator import itemgetter
import pulp


import timeit




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
     
#                url=os.path.join(settings.STATIC_ROOT, 'model/state/state_model.json')
#                json_file = open(url, 'r')
#                type_actor = json_file.read()
#                json_file.close()
#                type_model = model_from_json(type_actor)
                
                # load weights into new model
                type_model=load_model(os.path.join(settings.STATIC_ROOT, 'model/state/state_model.h5'))
                type_model.load_weights(os.path.join(settings.STATIC_ROOT, 'model/state/state_weights.h5'))
 
        
                actor_policy=type_model.predict(ss).astype('float32')
        sess.close()

       
    
        ## choice
        CHOICE=np.random.choice(len(actor_policy[0]),1,p=(actor_policy/np.sum(actor_policy))[0] )
 
        url=os.path.join(settings.STATIC_ROOT, 'data/actor_policy_list.npy')
        r=list(np.load(url))

        return [r[CHOICE[0]],user_features]


## compute the values of all actions
def evaluate_actions(user,historic,track,w,t2):
    
    
        
    user_features=w[1]
    w[0]=['Country','Rock','Pop']
    
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
#            value=0
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
     
#                print single_action_model.predict(r).astype('float32')
#                print np.array(t2.novelty[i])
#                print np.exp(np.array(t2.novelty[i]).astype('float32')/4)
                print 'multiplication'
#                print type(np.multiply(single_action_model.predict(r).astype('float32'),2*np.exp(np.array(t2.novelty[i]).astype('float32')/4)))
#                print np.shape(np.multiply(single_action_model.predict(r).astype('float32'),2*np.exp(np.array(t2.novelty[i]).astype('float32')/4)))
                
                ddd=np.multiply(single_action_model.predict(r).astype('float32'),nov_recovery((np.array(t2.novelty[i]).astype('float32'))))
#                single_action_values[i]=single_action_model.predict(r).astype('float32')
                
                single_action_values[i]=ddd
                cc=np.argmax(single_action_values[i])
#                value+=single_action_values[i][cc][0]*historic[int(jj)]
#                print single_action_values[i]
#                print 'i ' +i
#                print 'argmax '+ str(cc)
#                print songs_list[i][cc]
                choice.append(songs_list[i][cc])
#            print 'value  len=4'
#            print value 
            return choice
        
        else:
            choice=PulpSolve(4,w,historic,user_features,t2)
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
       
       
       
       


def PulpSolve(N,w,historic,user_features,t2):
    
    start = timeit.default_timer()
    songs_keys=np.load(os.path.join(settings.STATIC_ROOT, 'data/songs_keys.npy')).item() 
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
            
        ddd=np.multiply(single_action_model.predict(rr).astype('float32'),nov_recovery(np.array(t2.novelty[i]).astype('float32')))
#        single_action_values[i]=single_action_model.predict(rr).astype('float32')
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
#        prob += lpSum(historic[int(jj)]*var[i]['X'][(r)]*single_action_values[i][list_correlations[i].index(r)] for r in L)
#        prob += lpSum(historic[int(jj)]*(-var[i]['L'][(r)])*single_action_values[i][list_correlations[i].index(r)] for r in L)

       
#    d=0   
#   
#    for i in w[0]:
##        nb[i]=1
#        L=songs_by_type[i].keys()
###        z = list(combination(L,2))
##        z=list_correlations[i]
##        corr=[(r) for r in z]
#        
#        
##        prob += lpSum(var[i]['X'][(r)]  for r in L) ==1
##        
##        
##        for r in z:
##            prob += var[i]['Y'][(r)]  <= var[i]['X'][r[0]]
##            prob += var[i]['Y'][(r)]  <= var[i]['X'][r[1]]
##            prob += var[i]['Y'][(r)]  <= var[i]['L'][r[0]]
##            prob += var[i]['Y'][(r)]  <= var[i]['L'][r[1]]
##        
##        for r in L:
##            prob+=var[i]['X'][r] <= var[i]['n'][r]
#    
#            
#        d+= lpSum(var[i]['n'][r] for r in L) 
#    prob+=d==N       
            
        
#    prob.writeLP(os.path.join(settings.STATIC_ROOT, 'lol.lp'))
#        prob.writeLP('lol.lp')
#    
    stop = timeit.default_timer()
    print 'tps pr add constraints'
    print stop - start 
#    
    start = timeit.default_timer()
#    prob.solve(pulp.COIN_CMD(dual=True,mip=1,msg=1))




#    prob.solve(pulp.GLPK(mip=1))
    
    



#    prob.solve(pulp.GUROBI(mip=1))



    pa=os.path.join(settings.STATIC_ROOT, 'cbc') 
    solver = pulp.COIN_CMD(path=pa,mip=1)

    prob.solve(solver)

    
    stop = timeit.default_timer()
    print "tps de solve"
    print stop - start 



#    prob.solve(pulp.solvers.LpSolver())



#    prob.solve(pulp.PULP_CBC_CMD(dual=True))
    
#    prob.solve(pulp.PULP_CBC_CMD(dual=True))

#    print pulp.value(prob.objective)

#    print 'constraints'
#    print len(prob.constraints)
#    print 'variables'
#    print len(prob.variables())
#    q=0
#    for v in prob.variables():
#        if v.varValue>0:
#            q=q+1
#            print v.name, "=", v.varValue
#                
#    print 'q = ' +str(q)
#    print pulp.value(prob.objective)
    start = timeit.default_timer()
    c=np.zeros(len(w[0]))
    for i in range(len(w[0])):
        c[i]=historic[int(genre_dict[w[0][i]])]
    x={}
    y={}
#        n={}
    restant=N-len(w[0])
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
    print 'nb'
    print nb
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
        if nb[i]==2:
            
            z=np.random.choice(len(y[i]),1,replace=False,p=(y[i].values()/np.sum(y[i].values())) )[0] 
#            print z
#            print y[i].keys()[z]
            choice.extend(y[i].keys()[z])
        else:
            z=np.random.choice(len(x[i]),nb[i],replace=False,p=(x[i].values()/np.sum(x[i].values())) )
#            print z
           
            for ii in z:         
                choice.append(x[i].keys()[ii])
    stop = timeit.default_timer()
    print "fin du prg"
    print stop - start 
        #print x[i].keys()[z]
#    print len(choice)
#   
#    print np.sum(var['Latin']['L'].values())
    
    return choice

        
def nov_recovery(x):
        return 1-np.exp(-x/1.3)
  
 
    
#import numpy as np
#import matplotlib.pyplot as plt
#t = np.arange(0., 5., 1)
#plt.plot(t, 1-np.exp(-t/1.45), 'bs')




        