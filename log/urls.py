from django.conf.urls import url
from . import views
#from django.conf import settings

#from datetime import datetime
#from django.contrib.auth import views as auth_views


urlpatterns = [
  
      url(r'^login$', views.loggin, name='login'),
     # url(r'^fiche/(?P<pseudo>\w+)$', views.fiche_resto, name='fiche_resto'),
     
      url(r'^fiche/(?P<track_pseudo>\w+)$', views.fiche_track, name='fiche_track'),
      
      
      url(r'^(?P<titre_1>\w+)/(?P<titre_2>\w+)$', views.solo, name='solo'),
      
      
      
      url(r'^auth$', views.auth, name='auth'),
      
      url(r'^logout$', views.loggout, name='logout'),
      url(r'^profil$', views.ProfileFormView.as_view(), name='profil'),
#           url(r'^register$', views.UserFormView.as_view(), name='register'),
      url(r'^register$', views.register, name='register'),
      url(r'^change_password$', views.change_password, name='change_password'),
      url(r'^change_rating/(?P<track>\w+)$', views.change_rating, name='change_rating'),
      url(r'^home', views.homepage, name='homepage'),

    

#         
        
          
           
       
  
]

#if not settings.DEBUG:
 #   urlpatterns += patterns('',
 #       (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
 #   )
