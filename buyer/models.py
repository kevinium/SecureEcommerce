from django.db import models
from django.shortcuts import reverse
from django.conf import settings
from signup.models import seller
from signup.formatChecker import ContentTypeRestrictedFileField
# Create your models here.
class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    #category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    #image = models.ImageField(upload_to='images')
    image = ContentTypeRestrictedFileField(upload_to='images',content_types=['image/jpeg','image/jpg','image/png'],max_upload_size=5242880,blank=True, null=True)
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("buyer:product", kwargs={
            'slug': self.slug
        })

    def get_add_to_cart_url(self):
        return reverse("buyer:add-to-cart", kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse("buyer:remove-from-cart", kwargs={
            'slug': self.slug
        })


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_total_item_price(self):
        return self.quantity * self.item.price

class sellerItems(models.Model):
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    item = models.ManyToManyField(Item)
    #quantity = models.IntegerField(default=1)
    def get_seller(self):
        return self.seller

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    items = models.ManyToManyField(OrderItem)
    payment = models.ForeignKey('Payment', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.user.username
    
    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_total_item_price()
        return total


class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    order_id=models.CharField(max_length=100,blank=True)
    razorpay_order_id=models.CharField(max_length=100,blank=True)

    def __str__(self):
        return self.user.username
