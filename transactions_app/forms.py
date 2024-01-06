from django import forms
from transactions_app.models import TransactionModel
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm


# create a form for Deposit, Withdrawal, Loan, Loan Paid
class TransactionFrom(forms.ModelForm):
    class Meta:
        model = TransactionModel
        fields = ['amount', 'transaction_type']
        
    # Account holder can't choice Deposit, Withdrawal, Loan, Loan Paid.We will handle it from backend
    def __init__(self, *args, **kwargs):
        self.account = kwargs.pop('account') # onekgula kwargs er moddah account ke pop() kore variable e store korlam
        super().__init__(*args, **kwargs)
        
        # transaction_type disabled thakbe
        self.fields['transaction_type'].disabled = True 
        # and transaction_type user er theke hidden thakbe
        self.fields['transaction_type'].widget = forms.HiddenInput() 
        
    # save the data into database
    def save(self, commit = True):
        self.instance.account = self.account
        self.instance.balance_after_transaction = self.account.balance
        return super().save()

class DepositFrom(TransactionFrom):
    def clean_amount(self): # amount field ke filter korbo for deposit
        min_deposit = 100
        deposit_amount = self.cleaned_data.get('amount')
        
        if deposit_amount < min_deposit:
            raise forms.ValidationError(f"You need to deposit at least {min_deposit}.")
        
        return deposit_amount
    
class WithdrawalFrom(TransactionFrom):
    def clean_amount(self): # amount field ke filter korbo for withdrawal
        withdrawal_account = self.account
        min_withdrawal = 100
        max_withdrawal = 20000
        withdraw_balance = withdrawal_account.balance # Main Total amount
        withdrawal_amount = self.cleaned_data.get('amount')
        
        if withdrawal_amount < min_withdrawal:
            raise forms.ValidationError(f"You can withdraw minimum {min_withdrawal} Tk.")
        
        if withdrawal_amount > max_withdrawal:
            raise forms.ValidationError(f"You can't withdraw more the {max_withdrawal} Tk in a day.")
        
        if withdrawal_amount > withdraw_balance:
            raise forms.ValidationError(f"Insufficient balance !!\n \
                                        You can't withdrawal more then {withdrawal_account.balance} Tk.")
        
        return withdrawal_amount
    
    
class TransferMoneyFrom(TransactionFrom):               
    def clean_amount(self):
        user_acc = self.account  
        trans_acc = self.cleaned_data.get('account_no') 
        print(trans_acc)
        transfer_amount = self.cleaned_data.get('amount')
        max_transfer = 30000
        min_transfer = 50
        print(user_acc, transfer_amount,'line 66')
        
               
        if user_acc.balance < transfer_amount and user_acc.account_no != trans_acc:
            raise forms.ValidationError(f"Insufficient fund.Your current balance is {user_acc.balance} Tk.\n \
                But you want to transfer {transfer_amount} Tk.")
        
        if transfer_amount > max_transfer:
            raise forms.ValidationError(f"You can't transfer more then {max_transfer} Tk in a day")
        
        if transfer_amount < min_transfer:
            raise forms.ValidationError(f"Minimul transfer is {min_transfer} Tk.")
        
        
        return transfer_amount, trans_acc
           

class LoanRequestForm(TransactionFrom):
    def clean_amount(self):
        loan_amount = self.cleaned_data.get('amount')
        return loan_amount
    
class ChangePasswordForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['password1', 'password2']