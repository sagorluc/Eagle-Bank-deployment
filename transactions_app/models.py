from django.db import models
from account.models import BankAccountRegisterModel
from transactions_app.constants import TRANSACTIONS_TYPE

# Create your models here.
class TransactionModel(models.Model):
    
    # one account holder can have multiple transactions
    account = models.ForeignKey(BankAccountRegisterModel, related_name= 'transactions', on_delete= models.CASCADE)
    # transfer = models.IntegerField(null= True)
    amount = models.DecimalField(max_digits= 12, decimal_places= 2)
    balance_after_transaction = models.DecimalField(max_digits= 12, decimal_places= 2, null= True)
    transaction_type = models.IntegerField(choices= TRANSACTIONS_TYPE )
    timestamp = models.DateTimeField(auto_now_add= True) # jokhone transaction er kono activaties hobe sei time and date store korbe
    loan_approve = models.BooleanField(default= False)
    
    class Meta:
        ordering = ['timestamp']
    
     
