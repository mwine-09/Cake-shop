 
from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User
# from django.contrib.admin.models import Users

# Create your models here.




# class Message(models.Model):
#     user = models.ForeignKey(Users, on_delete=models.CASCADE)
#     body = models.TextField()
#     updated = models.DateTimeField(auto_now=True)
#     created = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         ordering = ['-updated', '-created']

#     def __str__(self):
#         return self.body[0:50]



class Category(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Item(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True) 
    name = models.CharField(max_length=100)
    price = models.FloatField()
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class Cart(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    created = models.DateTimeField(auto_now_add=True)
    total_ordering = models.IntegerField(default= 0)
    @property

    def total_odering(self, *args, **kwargs):
        self.total_ordering = self.quantity * self.item.price
        super(Cart, self).save(*args, **kwargs)
        x= self.total_ordering
        return x
    


    def __str__(self):
        return self.item.name


class cartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    created = models.DateTimeField(auto_now_add=True)
    total_ordering = models.IntegerField(default= 0)
    @property

    def total_odering(self, *args, **kwargs):
        self.total_ordering = self.quantity * self.price
        super(Cart, self).save(*args, **kwargs)
        x= self.total_ordering
        return x

    def __str__(self):
        return self.item.name



class Order(models.Model):
    User = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(default=1)
    created = models.DateTimeField(auto_now_add=True)
    total_ordering = models.IntegerField(default= 0)
    status = models.CharField(max_length=100, default='Pending')
    @property

    def total_odering(self, *args, **kwargs):
        self.total_ordering = self.quantity * self.price
        super(Cart, self).save(*args, **kwargs)
        x= self.total_ordering
        return x





class orderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    
    def __str__(self):
        return self.item.name






















 
# class Cart(models.Model):
#     name = models.CharField(max_length=100)
#     amount = models.IntegerField()
#     quantity = models.IntegerField(default= 1)
#     total_ordering = models.IntegerField(default= 0)
    
#     @property

#     def total_odering(self, *args, **kwargs):
#         self.total_ordering = self.quantity * self.amount
#         super(Cart, self).save(*args, **kwargs)
#         x= self.total_ordering
#         return x

#     def __str__(self):
#         return self.name
 

# class CartItem(models.Model):
#     Item = models.ForeignKey(Item, on_delete=models.CASCADE)
#     quantity = models.IntegerField(default=1)
#     price_ht = models.FloatField(blank=True)
#     cart = models.ForeignKey('Cart', on_delete=models.CASCADE)


#     def price_ttc(self):
#         TAX_AMOUNT = 19.25
#         return self.price_ht * (1 + TAX_AMOUNT /100.0)

#     def __str__(self):
#         return  self.client + " - " + self.product