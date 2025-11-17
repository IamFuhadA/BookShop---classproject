from django.db import models

# Create your models here.

class RegistrationDB(models.Model):
    username=models.CharField(max_length=30,null=True,blank=True)
    name=models.CharField(max_length=30,null=True,blank=True)
    mail=models.EmailField(max_length=50,null=True,blank=True)
    contact=models.IntegerField(null=True,blank=True)
    password=models.CharField(max_length=30,null=True,blank=True)
    confirm_password=models.CharField(max_length=30,null=True,blank=True)

class ContactDB(models.Model):
    name=models.CharField(max_length=30,null=True,blank=True)
    mail=models.EmailField(max_length=50,null=True,blank=True)
    subject = models.CharField(max_length=50,null=True,blank=True)
    message = models.TextField(null=True,blank=True)

class CartDB(models.Model):
    username=models.CharField(max_length=30,null=True,blank=True)
    title=models.CharField(max_length=30,null=True,blank=True)
    quantity=models.IntegerField(null=True,blank=True)
    price=models.IntegerField(null=True,blank=True)
    total_price=models.IntegerField(null=True,blank=True)
    book_img=models.ImageField(upload_to="Cart Image",null=True,blank=True)