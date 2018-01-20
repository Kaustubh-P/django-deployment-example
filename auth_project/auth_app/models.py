from django.db import models
from django.contrib.auth.models import User

# Create your models here.
#This is model class to add information that the dafault user doesn't have
class UserProfileInfo(models.Model):

    #Create a relationship between this model and User in django-admin
    user = models.OneToOneField(User)

    #Add any additional attributes you want
    portfolio_site=models.URLField(blank=True)
    picture=models.ImageField(upload_to='profile_pics',blank=True)

    def __str__(self):
        #Buit-in attribute of django.contrib.auth.models.User models
        return self.user.username
