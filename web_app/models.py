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

class CheckoutDB(models.Model):
    username = models.CharField(max_length=100,null=True,blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20,null=True,blank=True)
    address = models.TextField()
    sub_total = models.IntegerField()
    delivery_charge = models.IntegerField()
    total_amount = models.IntegerField()
    payment_type = models.CharField(max_length=50,null=True,blank=True)
