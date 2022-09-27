
from pickle import EMPTY_SET
from django.db import models
from taggit.managers import TaggableManager
from django.utils import timezone
from django.contrib.auth.models import User


class Product(models.Model):
    STATUS_CHOICES = (
        ('0' , 'Draft'),
        ('1',  'Published'),
    )
    title   = models.CharField(max_length=255)
    image   = models.ImageField(upload_to = 'post/')
    price =  models.IntegerField()
    slug    = models.SlugField(max_length=225, unique_for_date='published_at')
    status  = models.CharField(max_length=1, choices=STATUS_CHOICES, default='1')
    tags = TaggableManager()

    published_at = models.DateTimeField(default=timezone.now)
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)



class Customer(models.Model):
    user =models.OneToOneField(User, on_delete=models.CASCADE , null=True, blank=True)
    name =models.CharField(max_length=200, null=True)
    email =models.CharField(max_length=200 , null=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    date_orderd= models.DateTimeField(auto_now_add=True)
    complete= models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=200, null=True)
    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quanity for item in orderitems])
        return total
        
class OrderItem(models.Model):
    product = models. ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quanity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)



    @property
    def get_total(self):
        total = self.product.price * self.quanity
        return total
