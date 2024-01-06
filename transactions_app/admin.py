from django.contrib import admin
from transactions_app.models import TransactionModel

# Register your models here.
@admin.register(TransactionModel)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['account', 'amount', 'balance_after_transaction', 'transaction_type', 'loan_approve']
    
    # backend theke loan approve korar por main balance er shathe add hobe
    def save_model(self, request, obj, form, change):
        obj.account.balance += obj.amount
        obj.balance_after_transaction = obj.account.balance
        obj.account.save()
        super().save_model(request, obj, form, change)