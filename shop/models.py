from django.db import models
from django.contrib.auth.forms import User
# Create your models here.

class Category(models.Model):
    cid = models.AutoField
    cname = models.CharField(max_length=30)
    def __str__(self):
        return self.cname

class Shop(models.Model):
    id = models.CharField(max_length=30 , primary_key=True)
    sid = models.CharField(max_length=30)
    cat = models.ForeignKey(Category, on_delete=models.CASCADE, default=None)
    vendor = models.ForeignKey(User, on_delete=models.CASCADE, default=None)

    name = models.CharField(max_length=100)
    description = models.TextField()
    address = models.TextField(default=" ")
    img1 = models.ImageField(upload_to='images')
    img2 = models.ImageField(upload_to='images', default=None)
    longitude = models.CharField(max_length=3)
    latitude = models.CharField(max_length=3)
    def __str__(self):
        return self.id

