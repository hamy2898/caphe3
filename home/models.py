from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser


# Create your models here.

#Product
class Category(models.Model):
    title = models.CharField(max_length=100,default='')
    description = models.TextField(default='')
    active = models.BooleanField(default=True)

class Product(models.Model):
    title = models.CharField(max_length=255,default='')
    description = models.TextField(default='')
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    product_img = models.CharField(max_length=255,default='')
    price = models.IntegerField(default=0)
    active = models.BooleanField(default=True)

class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    title = models.CharField(max_length=255,default='')
    price = models.IntegerField(default=0)
    sale_price = models.IntegerField(default=0)
    investory = models.IntegerField(default=0)
    active = models.BooleanField(default=True)

class BaiViet(models.Model):
    baiviet_id = models.IntegerField(auto_created=True, primary_key=True)
    tieude = models.CharField(max_length=300)
    noidung = models.TextField()
    ngay_dang = models.DateTimeField(default=timezone.now)
    anhbia = models.CharField(max_length=300)


class Order(models.Model):
    order_id = models.AutoField(primary_key = 'true')
    custom = models.CharField(max_length=200)
    address = models.TextField(max_length=1000,default='')
    phone = models.CharField(max_length=15,default='')
    total = models.FloatField()
    date_create = models.DateTimeField(default=timezone.now)
    note = models.TextField()
    payment_status = models.IntegerField(blank=True,null=True)
    status = models.IntegerField()
    accept = models.BooleanField(default=False)


class OrderDetail(models.Model):
    detail_id = models.AutoField(primary_key = 'true')
    pro_name = models.CharField(max_length=255,default='')
    orders = models.ForeignKey('Order', on_delete=models.CASCADE)
    pro_price = models.IntegerField(null=False)
    pro_image = models.CharField(max_length=255,default='')
    quantity = models.IntegerField(null=False)
    status = models.SmallIntegerField(blank=True,null=True)

class Comment(models.Model):
    name = models.CharField(max_length=255)
    content = models.CharField(max_length=3000)
    date_create = models.DateTimeField(default=timezone.now)
    accept = models.BooleanField(default=False)
    email = models.EmailField(null=True)





