from django.db import models
from django.conf import settings


User = settings.AUTH_USER_MODEL

class Product(models.Model):
    # foreginkey corelate two tables together. product table with user table in here
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)    # if user is deteled. it sets field or existinig object to null rather than deleting it.
    
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE) # it deletes everything including the existing object once the user is deleted
    
    title = models.CharField(max_length=120)
    content = models.TextField(null=True, blank=False)
    price = models.IntegerField(default=0)