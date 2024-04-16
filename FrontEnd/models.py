from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import User
from BackEnd.models import *


# Create your models here.
class SignUp_Db(models.Model):
    Email=models.EmailField(max_length=100,null=True,blank=True,unique=True)
    Username=models.CharField(max_length=100,null=True,blank=True,unique=True)
    Password=models.CharField(max_length=100,null=True,blank=True)
    Cpassword=models.CharField(max_length=100,null=True,blank=True)
    last_login=models.DateTimeField(null=True,blank=True)
    password_reset_token = models.CharField(max_length=100, blank=True, null=True)
    token_expiration = models.DateTimeField(blank=True, null=True)

class Profile(models.Model):
    Username = models.CharField(max_length=200, blank=True)
    name = models.CharField(max_length=200, blank=True)
    age = models.IntegerField(null=True, blank=True)
    mobile = models.IntegerField(null=True, blank=True)
    state = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=200, blank=True)
    hobby = models.CharField(max_length=200, blank=True)
    profile_image = models.ImageField(
        default='Images/usericon1.png', upload_to='Images', null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s profile"



class CartDb(models.Model):
    Username = models.CharField(max_length=100,null=True,blank=True)
    painting = models.ForeignKey(paintings_Db, on_delete=models.CASCADE, related_name='cart_items', default=1)
    quantity = models.IntegerField(null=True,blank=True)
    price = models.IntegerField(null=True,blank=True)
    tprice = models.IntegerField(null=True,blank=True)





class WishlistDb(models.Model):
    Username = models.CharField(max_length=100,null=True,blank=True)
    product = models.ForeignKey(paintings_Db, on_delete=models.CASCADE)  # Assuming paintings_Db is your product model

    # Add any other fields you need


class Address(models.Model):
    Username = models.CharField(max_length=100,null=True,blank=True)
    firstname = models.CharField(max_length=100, null=True)
    lastname = models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=200)
    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255, blank=True)
    phone = models.IntegerField( blank=True, null=True)
    city = models.CharField( max_length=255,null=True)
    state = models.CharField( max_length=255,null=True)
    pincode = models.IntegerField(null=True, blank=True)
    default = models.BooleanField(default=False)

    def _str_(self):
        return self.user.username



class Order(models.Model):
    STATUS = (
        ('Order Confirmed', 'Order Confirmed'),
        ('Shipped', "Shipped"),
        ('Out for delivery', "Out for delivery"),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
        ('Returned', 'Returned'),
    )
    Username=models.CharField(max_length=100,null=True,blank=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    discount = models.IntegerField(blank=True, null=True)
    total_price = models.IntegerField(blank=True,null=True)
    shipping = models.IntegerField(blank=True,null=True)
    grand_total = models.IntegerField(blank=True,null=True)
    amount_to_be_paid = models.IntegerField(blank=True,null=True)
    is_deleted = models.BooleanField(default=False)
    payment_method = models.CharField(max_length=50)
    order_status =models.CharField(max_length=50,choices=STATUS,default='Order Confirmed')
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set when the object is first created
    order_id = models.CharField(max_length=100, unique=True)  # Assuming order_id is a unique identifier for each order


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to="Images", null=True, blank=True,)
    pname = models.CharField(max_length=30,blank=True,null=True)
    quantity = models.IntegerField()
    quantity = models.IntegerField()
    price = models.IntegerField()
    total_price=models.IntegerField(null=True)

class Subscription_Db(models.Model):
    Username=models.CharField(max_length=100,null=True,blank=True)
    amount= models.IntegerField(blank=True,null=True)

