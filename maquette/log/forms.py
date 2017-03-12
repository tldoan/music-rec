from django.contrib.auth.models import User
from django import forms
from .models import Profile, Coments, Track_Coments, Traj



#occupations= (
#    ('1', 'undergraduate'),
#    ('2', 'graduate'),
#    ('3', 'faculty'),
#    ('4', 'other'),
#)
#neighborhoods= (
#    ('1', 'downtown'),
#    ('2', 'plateau'),
#    ('3', 'westmount'),
#)
#
#regions= (
#    ('1', 'America'),
#    ('2', 'Europe'),
#    ('3', 'Asia'),
#)




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

class ComentsForm(forms.ModelForm):
    review=forms.CharField(widget=forms.Textarea,required=False)
    class Meta:
        model=Coments
        fields = ('rating',)  
        
        
class TracksForm(forms.ModelForm):   
    class Meta:
        model=Track_Coments
        fields = ('rating',) 
        
        
class TrajForm(forms.ModelForm):   
    class Meta:
        model=Traj
        fields = ('path',) 
        