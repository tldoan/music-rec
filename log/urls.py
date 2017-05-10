from django.conf.urls import url


from . import views


urlpatterns = [
  
     url(r'^$', views.loggin, name='login'),
     
#      url(r'^fiche/(?P<track_pseudo>\w+)$', views.fiche_track, name='fiche_track'),
     url(r'^fiche/(?P<track_pseudo>.*)$', views.fiche_track, name='fiche_track'),
      
      url(r'^(?P<titre_1>.*)/(?P<titre_2>.*)$', views.solo, name='solo'),
    
      url(r'^recommend_songs$', views.recommend_songs, name='recommend_songs'),
      url(r'^save_rating$', views.save_rating, name='save_rating'),
      
      url(r'^auth$', views.auth, name='auth'),
      
      url(r'^logout$', views.loggout, name='logout'),
   
      url(r'^profil$', views.profil, name='profil'),
      
      url(r'^register$', views.register, name='register'),
      url(r'^change_password$', views.change_password, name='change_password'),
   
      
      url(r'^home', views.homepage, name='homepage'),
       url(r'^500', views.custom_500, name='500'),
  
  
]

handler500 = 'app.views.custom_500'
