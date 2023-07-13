from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True) #1 


#1 redeging email field - in auth table we have email filed but it allows same emails n number number of time we have to set constarint on this email field 
# how r we gonna tell jango we will use this class rather instead of the user class in the authentication sysytem
# 
# 
# 
# 
# 
# 
# 
#     