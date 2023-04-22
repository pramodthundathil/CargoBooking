from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class StaffDetails(models.Model):
    
    staffid = models.ForeignKey(User,on_delete=models.CASCADE)
    staffcat = models.CharField(max_length=255,choices=(("Office Staff","Office Staff"),("Field staff","Field Staff")))
    
class Pricing(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255)
    image = models.FileField(upload_to="company_image")
    Normal_Amount = models.IntegerField()
    Basic_Amount = models.IntegerField()
    Paltinum_Amount = models.IntegerField()
    
class GoodBooking(models.Model):
    name = models.CharField(max_length=20)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    delivery_person_name = models.CharField(max_length=255)
    d_House = models.CharField(max_length=255)
    d_City = models.CharField(max_length=20)
    d_state = models.CharField(max_length=20)
    d_country = models.CharField(max_length=20)
    d_phone = models.CharField(max_length=20)
    d_email = models.CharField(max_length=20)
    from_address = models.CharField(max_length=255)
    weight = models.FloatField(null = True)
    book_date = models.DateField(auto_now_add=True)
    pickup_date = models.DateField(auto_now_add=False,null=True)
    deliverd_date = models.DateField(auto_now_add=False,null=True)
    status = models.CharField(max_length=20)
    status_2 = models.CharField(max_length=20,null=True)
    status_3 = models.CharField(max_length=20,null=True)
    trackid = models.CharField(max_length=20,null=True)
    complation_status = models.BooleanField(default=False)
    itemtype = models.CharField(max_length=255)
    order_taken = models.BooleanField(default=False)
    staff_person = models.IntegerField(null=True)
    company = models.IntegerField(null=True)
    total_amount = models.FloatField(null=True)
    
    
class Reqpayment(models.Model):
    booking = models.ForeignKey(GoodBooking,on_delete=models.CASCADE)
    status = models.BooleanField(default=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    
     
    
    
    

    

    
