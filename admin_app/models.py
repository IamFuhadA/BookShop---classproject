from django.db import models

# Create your models here.

class CategoryDB(models.Model):
    category_name = models.CharField(max_length=15,null=True,blank=True)
    Description = models.TextField(null=True,blank=True)
    cover_image = models.ImageField(upload_to='img/',null=True,blank=True)

class BookDB(models.Model):
    title = models.CharField(max_length=15,null=True,blank=True)
    author = models.CharField(max_length=15,null=True,blank=True)
    category = models.CharField(max_length=15,null=True,blank=True)
    price = models.IntegerField(null=True,blank=True)
    publisher = models.CharField(max_length=15,null=True,blank=True)
    description = models.TextField(null=True,blank=True)
    cover_image = models.ImageField(upload_to='img/',null=True,blank=True)
