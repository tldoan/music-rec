from django.contrib.auth.models import User
from django import forms
from .models import Profile, Track_Coments, Traj







class ProfileForm(forms.ModelForm):
    class Meta:
        model=Profile
        fields = ('area','age','region')      
#    occupation = forms.ChoiceField(choices = occupations, required=True)
#    neighborhood = forms.ChoiceField(choices = neighborhoods, required=True) 
#    region=forms.ChoiceField(choices = regions,required=True)

class UserForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model=User
        fields=['username','password']
        
#                help_texts = {
#            'username': None,
#        }
#        fields=['username','password','email']
#        labels={'username': 'username'
#                ,}


        
class TracksForm(forms.ModelForm):   
    class Meta:
        model=Track_Coments
        fields = ('rating',) 
        
        
class TrajForm(forms.ModelForm):   
    class Meta:
        model=Traj
        fields = ('path',) 
        