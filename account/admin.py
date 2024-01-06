from django.contrib import admin
from account.models import BankAccountRegisterModel, UserRegisterAddressModel

# Register your models here.
admin.site.register(BankAccountRegisterModel)
admin.site.register(UserRegisterAddressModel)
