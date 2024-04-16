from django.db import models



# Create your models here.

class paintings_Db(models.Model):
    STATUS = (
        ('In Stock', 'In Stock'),
        ('Out Of Stock', "Out Of Stock"),  
    )
    username=models.CharField(max_length=20,null=True,blank=True)
    pname = models.CharField(max_length=20, null=True, blank=True)
    picture = models.ImageField(upload_to="Images", null=True, blank=True)
    price = models.IntegerField(null=True, blank=True)
    picture_type = models.CharField(max_length=20, null=True, blank=True)
    location = models.CharField(max_length=20, null=True, blank=True)
    description = models.CharField(max_length=20, null=True, blank=True)
    no_copies = models.IntegerField(null=True, blank=True)
    artist_name = models.CharField(max_length=20, null=True, blank=True)
    artist_picture = models.ImageField(upload_to="Images", null=True, blank=True, default='../Images/usericon11.png')
    status =models.CharField(max_length=50,choices=STATUS,default='In Stock')


class painting_type_Db(models.Model):
    type=models.CharField(max_length=20,null=True,blank=True)

class artist_Db(models.Model):
    name=models.CharField(max_length=20,null=True,blank=True)
    link=models.CharField(max_length=20,null=True,blank=True)
    picture=models.ImageField(upload_to="Images",null=True,blank=True)
    year=models.CharField(max_length=20,null=True,blank=True)


class contact_Db(models.Model):
    username=models.CharField(max_length=20,null=True,blank=True)
    name = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(max_length=30, null=True, blank=True)
    phone = models.IntegerField(null=True, blank=True)
    subject = models.CharField(max_length=20, null=True, blank=True)
    message = models.CharField(max_length=20, null=True, blank=True)

class CouponDb(models.Model):
    code = models.CharField(max_length=50, unique=True)
    minimum_price = models.DecimalField(max_digits=10, decimal_places=0,default=0.00)
    discount_percentage = models.DecimalField(max_digits=10, decimal_places=0,default=0.00)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    status = models.BooleanField(default=True)

    @property
    def discount_decimal(self):
        return self.discount_percentage / 100  # Convert percentage to decimal

class AppliedCoupon(models.Model):
    Username=models.CharField(blank=True,null=True,max_length=100)
    coupon = models.ForeignKey(CouponDb, on_delete=models.CASCADE)
    discounted_amount = models.DecimalField(max_digits=10, decimal_places=0,null=True)
    totalprice=models.IntegerField(null=True)
    applied_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)


class Artclasses_Db(models.Model):
    mainimage=models.ImageField(upload_to="Images", null=True, blank=True)
    mainheading=models.CharField(blank=True,null=True,max_length=100)
    image1=models.ImageField(upload_to="Images", null=True, blank=True)
    subheading1=models.CharField(blank=True,null=True,max_length=100)
    link1=models.CharField(blank=True,null=True,max_length=100)
    description1=models.CharField(blank=True,null=True,max_length=100)
    image2=models.ImageField(upload_to="Images", null=True, blank=True)
    subheading2=models.CharField(blank=True,null=True,max_length=100)
    link2=models.CharField(blank=True,null=True,max_length=100)
    description2=models.CharField(blank=True,null=True,max_length=100)
    image3=models.ImageField(upload_to="Images", null=True, blank=True)
    subheading3=models.CharField(blank=True,null=True,max_length=100)
    link3=models.CharField(blank=True,null=True,max_length=100)
    description3=models.CharField(blank=True,null=True,max_length=100)
    image4=models.ImageField(upload_to="Images", null=True, blank=True)
    subheading4=models.CharField(blank=True,null=True,max_length=100)
    link4=models.CharField(blank=True,null=True,max_length=100)
    description4=models.CharField(blank=True,null=True,max_length=100)
    image5=models.ImageField(upload_to="Images", null=True, blank=True)
    subheading5=models.CharField(blank=True,null=True,max_length=100)
    link5=models.CharField(blank=True,null=True,max_length=100)
    description5=models.CharField(blank=True,null=True,max_length=100)



