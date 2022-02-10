from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.



class Curr_Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    acc_name = models.CharField(max_length=500)
    acc_no = models.IntegerField()
    your_name = models.CharField(max_length=100)
    address = models.CharField(max_length=400)
    amount = models.IntegerField()
    mobile = models.IntegerField(default=0)
    city = models.CharField(max_length=100)
    desc = models.TextField(max_length=4000)
    created = models.DateField(auto_now_add=True)
    update = models.DateField(auto_now=True)
    def __str__(self):
        return self.acc_name


class Saving_Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    acc_name = models.CharField(max_length=500)
    acc_no = models.IntegerField()
    your_name = models.CharField(max_length=100)
    address = models.CharField(max_length=400)
    amount = models.IntegerField()
    mobile = models.IntegerField(default=0)
    city = models.CharField(max_length=100)
    desc = models.TextField(max_length=4000)
    created = models.DateField(auto_now_add=True)
    update = models.DateField(auto_now=True)
    def __str__(self):
        return self.acc_name


class Amount_Transfer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='users')
    request_user = models.ForeignKey(User, null=True, blank=True,related_name='req_user', on_delete=models.CASCADE)
    trans_amount = models.PositiveIntegerField(default=1,validators=[MaxValueValidator(10000),MinValueValidator(10)])


selectaccount = [
        ('Current','Current'),
        ('Saving','Saving'),
    ]
class Withdraw_Amount(models.Model):
    user = models.ForeignKey(User,null=True,blank=True,on_delete=models.CASCADE)
    your_name = models.CharField(max_length=500)
    type = models.CharField(max_length=100, choices=selectaccount, default='Current')
    acc_name = models.CharField(max_length=500)
    acc_no = models.IntegerField()
    withdraw_amount = models.IntegerField()
    withdraw_date = models.DateField(auto_now_add=True)