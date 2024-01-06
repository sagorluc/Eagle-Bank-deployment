from django.db import models
from django.contrib.auth.models import User
from account.constants import ACCOUNT_TYPE, GENDER_TYPE

# Create your models here.
class BankAccountRegisterModel(models.Model):
    user = models.OneToOneField(User, on_delete= models.CASCADE, related_name= 'account')
    account_type = models.CharField(max_length=40, choices= ACCOUNT_TYPE)
    account_no = models.IntegerField(unique= True)
    birth_date = models.DateField(null= True, blank= True)
    gender_type = models.CharField(max_length= 50, choices= GENDER_TYPE)
    initial_deposit_date = models.DateField(auto_now_add= True)
    balance = models.DecimalField(default= 0, max_digits= 12, decimal_places= 2) # initial balance 0
    
    def __str__(self) -> str:
        return f"Account-No: {self.account_no}->{self.user.username}"
    
class UserRegisterAddressModel(models.Model):
    user = models.OneToOneField(User, on_delete= models.CASCADE, related_name= 'address')
    street_address = models.CharField(max_length= 50)
    city = models.CharField(max_length= 50)
    postal_code = models.IntegerField()
    country = models.CharField(max_length= 50)  
    
    def __str__(self) -> str:
        return f"City: {self.city}->{self.user.email}"