from django.db import models
from django.conf import settings


User = settings.AUTH_USER_MODEL

class Product(models.Model):
    # foreginkey corelate two tables together. product table with user table in here
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)    # if user is deteled. it sets field or existinig object to null rather than deleting it.
    
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE) # it deletes everything including the existing object once the user is deleted
    
<<<<<<< HEAD
=======
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    
>>>>>>> parent of fdf1e2e (updated)
    title = models.CharField(max_length=120)
    content = models.TextField(null=True, blank=False)
    price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00
        )   # 4.00
    
    # inventory is a process to track the goods throughout the entire supply chain. From purchasing to end sales.
    inventory = models.IntegerField(default=0)
    featured = models.BooleanField(default=False)
    
    def has_inventory(self):
        return self.inventory > 0
        # return False
        
    def remove_item_from_inventory(self, save=True, count=1):
        current_inventory = self.inventory
        current_inventory -= count
        self.inventory = current_inventory
        
        if save == True:
            self.save()
        return self.inventory
        
            