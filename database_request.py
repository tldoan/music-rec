import os
#Setting up environment variable for django to work
os.environ['DJANGO_SETTINGS_MODULE'] = 'maquette.settings'
import django
django.setup()
#Importing models from django project
from django.db import transaction
print(os.getcwd())


#from log import models as main_app_models
from django.contrib.auth.models import User
user = User.objects.create_user('Maxime', 'maxime@crepes-bretonnes.com', 'm0nsup3rm0td3p4ss3')
user.id
user.save()
