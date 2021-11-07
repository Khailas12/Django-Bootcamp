from django.db import models
from django.conf import settings
from .storages import ProtectedStorage


User = settings.AUTH_USER_MODEL

# def get_storage_model():
#     if settings.DEBUG:
#         return ProtectedStorage()
#     return LiveProtectedStorage()   # in live production


class Product(models.Model):
    # foreginkey corelate two tables together. product table with user table in here
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)    # if user is deteled. it sets field or existinig object to null rather than deleting it.
    
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE) # it deletes everything including the existing object once the user is deleted
    
    
    image = models.ImageField(upload_to='products/', null=True, blank=True)     # this uploads to the location in static dir instead of storing it in the db
    video_link = models.TextField(blank=True, null=True)
    
    media = models.FileField(storage=ProtectedStorage, upload_to='products/', blank=True, null=True)
    
    title = models.CharField(max_length=120)
    content = models.TextField(null=True, blank=False)
    price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00
        )   # 4.00
    
    # inventory is a process to track the goods throughout the entire supply chain. From purchasing to end sales.
    inventory = models.IntegerField(default=0)
    featured = models.BooleanField(default=False)
    can_backorder = models.BooleanField(default=False)
    requires_shipping = models.BooleanField(default=False)
    
    
    @property
    def is_digital(self):
        return self.media != None and self.media != ''
    
    @property
    def requires_shipping(self):
        return not self.is_digital
    
    @property
    def can_order(self):
        if self.has_inventory():
            return True
        elif self.can_backorder:
            return True
        return False
    
    @property
    def order_btn_title(self):
        if self.can_order and not self.has_inventory():
            return 'Backorder'
        
        if not self.can_order:
            return 'Cannot Purchase'
        return 'Purchase'

    def has_inventory(self):
        return self.inventory > 0
        # return False

    def __str__(self):
        return self.title