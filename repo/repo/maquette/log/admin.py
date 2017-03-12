from django.contrib import admin

# Register your models here.
# Register your models here.
from .models import Profile, Restaurant, Coments, Tracks,Track_Coments  , Traj

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user','area', 'age','region')
    #list_filter = ('occupation', )
    
    #ordering = ('occupation', )
    search_fields = ('area','age' )

admin.site.register(Profile, ProfileAdmin)

class RestaurantAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Restaurant._meta.fields]
    list_filter = ('name', )
    
    #ordering = ('occupation', )
    search_fields = ('name','neighborhood' )

admin.site.register(Restaurant, RestaurantAdmin)

class ComentsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Coments._meta.fields]
    list_filter = ('user','restaurant_name','restaurant' )
    
    #ordering = ('occupation', )
    search_fields = ('user','restaurant_name' )

admin.site.register(Coments, ComentsAdmin)

class TracksAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Tracks._meta.fields]
    list_filter = ('track_pseudo','track_link' , )
    
    #ordering = ('occupation', )
    search_fields = ('track_name','Artist','track_pseudo','track_link' )

admin.site.register(Tracks, TracksAdmin)




class Track_ComentsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Track_Coments._meta.fields]
    list_filter = ('user','track' )
    
    search_fields = ('user','track' )
    
admin.site.register(Track_Coments, Track_ComentsAdmin)


class TrajAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Traj._meta.fields]
    list_filter = ('user','start_time', )
    
    search_fields = ('user','start_time', )
    
admin.site.register(Traj, TrajAdmin)