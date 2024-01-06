from typing import Any
from django.contrib.auth.forms import UserCreationForm
from django import forms
from account.constants import ACCOUNT_TYPE, GENDER_TYPE
from django.contrib.auth.models import User
from account.models import BankAccountRegisterModel, UserRegisterAddressModel

class UserRegisterFrom(UserCreationForm):
      account_type = forms.ChoiceField(choices= ACCOUNT_TYPE)
      birth_date = forms.DateField(widget=forms.DateInput(attrs= {'type': 'date'}))
      gender_type = forms.ChoiceField(choices= GENDER_TYPE)
      street_address = forms.CharField(max_length= 50)
      city = forms.CharField(max_length= 50)
      postal_code = forms.IntegerField()
      country = forms.CharField(max_length= 50)  
      #repassword = forms.CharField(widget= forms.PasswordInput(attrs= {'placeholder': 'Confirme you password'}))
      
      class Meta:
          model = User
          fields = ['username', 'password1', 'password2', 'first_name', 'last_name',
                    'email', 'account_type', 'birth_date', 'gender_type', 'street_address',
                    'city','postal_code','country']
          
      def save(self, commit= True):
              our_user = super().save(commit = False) # save korbo nah
              if commit == True:
                  our_user.save()
                  
                  # getting data
                  account_type = self.cleaned_data.get('account_type')
                  birth_date = self.cleaned_data.get('birth_date')
                  gender_type = self.cleaned_data.get('gender_type')
                  street_address = self.cleaned_data.get('street_address')
                  city = self.cleaned_data.get('city')
                  postal_code = self.cleaned_data.get('postal_code')
                  country = self.cleaned_data.get('country')

                  # savings data into user address model/database
                  UserRegisterAddressModel.objects.create( 
                  user = our_user,
                  street_address = street_address,
                  city = city,
                  postal_code = postal_code,
                  country = country
                  
                  )
                  
                  # savings data into bank account register model/database
                  BankAccountRegisterModel.objects.create(
                  user = our_user,
                  account_type = account_type,
                  birth_date = birth_date,
                  gender_type = gender_type, 
                  account_no = 100000 + our_user.id
                  )
                  
                  return our_user
            
     # styleing the input button   
      def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
                
            for field in self.fields:
                # print(field)
                self.fields[field].widget.attrs.update({
                        
                        'class': (
                            'appearance-none block w-full bg-gray-200 '
                            'text-gray-700 border border-gray-200 rounded '
                            'py-3 px-4 leading-tight focus:outline-none '
                            'focus:bg-white focus:border-gray-500'
                        )
                    })

# update and auto create user_account.jodi account na thake then auto create korbe.               
class UserUpdateFrom(forms.ModelForm):
      account_type = forms.ChoiceField(choices= ACCOUNT_TYPE)
      birth_date = forms.DateField(widget=forms.DateInput(attrs= {'type': 'date'}))
      gender_type = forms.ChoiceField(choices= GENDER_TYPE)
      street_address = forms.CharField(max_length= 50)
      city = forms.CharField(max_length= 50)
      postal_code = forms.IntegerField()
      country = forms.CharField(max_length= 50) 
    
      class Meta:
            model = User
            fields = ['first_name', 'last_name', 'email']
      
      # styling build in forms      
      def __init__(self, *args, **kwargs):
          super().__init__(*args, **kwargs)
          for field in self.fields:
                # print(field)
                self.fields[field].widget.attrs.update({
                        
                        'class': (
                            'appearance-none block w-full bg-gray-200 '
                            'text-gray-700 border border-gray-200 rounded '
                            'py-3 px-4 leading-tight focus:outline-none '
                            'focus:bg-white focus:border-gray-500'
                        )
                    })
          # jodi user er account thake      
          if self.instance:
              try:
                  user_account = self.instance.account
                  user_address = self.instance.address
              except BankAccountRegisterModel.DoesNotExist:
                  user_account = None
                  user_address = None
                  
              if user_account:
                    self.fields['account_type'].initial = user_account.account_type
                    self.fields['gender_type'].initial = user_account.gender_type
                    self.fields['birth_date'].initial = user_account.birth_date
                    self.fields['street_address'].initial = user_address.street_address
                    self.fields['city'].initial = user_address.city
                    self.fields['postal_code'].initial = user_address.postal_code
                    self.fields['country'].initial = user_address.country
                    
      def save(self, commit = True):
          our_user = super().save(commit = False) # save korbo nah
          if commit:
             our_user.save()
             
             # jodi user er account na thake then create korbe
             user_account, created = BankAccountRegisterModel.objects.get_or_create(user= our_user)
             user_address , created = UserRegisterAddressModel.objects.get_or_create(user = our_user)
                          
             # getting data from user_account
             user_account.account_type = self.cleaned_data['account_type']
             user_account.birth_date = self.cleaned_data['birth_date']
             user_account.gender_type = self.cleaned_data['gender_type']
             user_account.save()
             
             # getting data from user_address
             user_address.street_address = self.cleaned_data['street_address']
             user_address.city = self.cleaned_data['city']
             user_address.postal_code = self.cleaned_data['postal_code']
             user_address.country = self.cleaned_data['country']
             user_address.save()
             
             return our_user
          
            
                    
                
                