from typing import Any, Dict
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from datetime import datetime
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, View
from transactions_app.forms import  DepositFrom, WithdrawalFrom, LoanRequestForm, TransferMoneyFrom
from transactions_app.models import TransactionModel
from django.contrib import messages
from transactions_app.constants import DEPOSIT, WITHDRAWAL, LOAN, LOAN_PAID, TRANSFER_MONEY
from django.db.models import Sum
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth import update_session_auth_hash
from django import forms

# Create your views here.
class TransactionCreateMixin(LoginRequiredMixin, CreateView):
    template_name = 'transactions_form.html'
    model = TransactionModel
    title = ''
    success_url = reverse_lazy('transactions_app:transaction_report')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'account': self.request.user.account})
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'title': self.title})
        return context
    
    
class DepositMoneyView(TransactionCreateMixin):
    form_class = DepositFrom
    title = 'deposit'
    
    def get_initial(self):
        initial = {'transaction_type': DEPOSIT}
        return initial
    
    def form_valid(self, form):
        depo_money_amount = form.cleaned_data.get('amount')
        depo_money_account = self.request.user.account
        
        # jodi model e DateTimeField(auto_now_add=True) thake tahole ekhane timezone set korar dorkar nai. ar jodi nah thake tahole must needed
        # if not depo_money_account.initial_deposit_date:
        #     now = timezone.now()
        #     depo_money_account.initial_deposit_date = now
            
        depo_money_account.balance += depo_money_amount
        depo_money_account.save(update_fields = ['balance'])
        
        messages.success(self.request, f'{"{:,.2f}".format(float(depo_money_amount))}$ was deposited to your account successfully')
   
        return super().form_valid(form)
    
class WithdrawMonyView(TransactionCreateMixin):
    form_class = WithdrawalFrom
    title = 'Withdraw Money'
    
    def get_initial(self):
        initial = {'transaction_type': WITHDRAWAL}
        return initial
    
    def form_valid(self, form):
        withdraw_money_amount = form.cleaned_data.get('amount')
        withdraw_money_account = self.request.user.account
        
        withdraw_money_account.balance -= withdraw_money_amount
        withdraw_money_account.save(update_fields = ['balance'])
        
        messages.success(self.request, f'{"{:,.2f}".format(float(withdraw_money_amount))} Tk was Withdrawal in your account successfully !!')
        return super().form_valid(form)
    
class LoanRequestView(TransactionCreateMixin):
    form_class = LoanRequestForm
    title = 'Request For Loan'
    
    def get_initial(self):
        initial = {'transaction_type': LOAN}
        return initial
    
    
    def form_valid(self, form):
        loan_request_amount = form.cleaned_data.get('amount')
        loan_request_account = self.request.user.account
        
        # count the total loan by filtering
        current_loan_count = TransactionModel.objects.filter(account = loan_request_account, transaction_type = 3, loan_approve= True).count()
        
        if current_loan_count >= 3:
            return HttpResponse("You have cross the loan limits !!")
        
        messages.success(self.request, f'Loan request for {"{:,.2f}".format(float(loan_request_amount))} Tk Submitted successfully !!')
        
        return super().form_valid(form)
    
class TransferMoneyView(TransactionCreateMixin):
    template_name = 'transfer_money.html'
    form_class = TransferMoneyFrom
    title = 'Transfer Money'
    success_url = reverse_lazy('transactions_app:transactions_report')
    
    def get_initial(self):
        initial = {'transaction_type': TRANSFER_MONEY}
        return initial
    
    def form_valid(self, form):
        from_acc = self.request.user.account
        trans_acc = form.cleaned_data.get('account_no')
        trans_amount = form.cleaned_data.get('amount')
        
        from_acc.balance -= trans_amount
        from_acc.save(update_fields = ['balance'])
        
        trans_acc.balance += trans_amount
        trans_acc.save(update_fields = ['balance'])
        
        messages.success(self.request, f"Success Transfer {trans_amount} Tk.")
        
        return super().form_valid(form)
    
    
class TransactionReportView(LoginRequiredMixin, ListView):
    template_name = 'transactions_report.html'
    model = TransactionModel
    report_balance = 0 # filter korar pore or ageee amer total balance show korbe
    
    def get_queryset(self):
        queryset = super().get_queryset().filter(account = self.request.user.account)
        
        # user er start_date theke end_date e total koto taka transaction hoice 
        start_date_str = self.request.GET.get('start_date')
        end_date_str = self.request.GET.get('end_date')
        
        if start_date_str and end_date_str:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            
            # filtering the start_date and end_date
            queryset = queryset.filter(timestamp__date__gte=start_date, timestamp__date__lte=end_date)
            
            # get the total sum from database
            self.report_balance = TransactionModel.objects.filter(timestamp__date__gte=start_date, timestamp__date__lte=end_date).aggregate(Sum('amount'))['amount__sum']
        else:
            self.report_balance = self.request.user.account.balance
        return queryset.distinct()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({ 'account': self.request.user.account})
        return context
    
    
class PayLonaView(LoginRequiredMixin, View):
    def get(self, request, loan_id):
        loan = get_object_or_404(TransactionModel, id = loan_id) # models er sob property access korte parbo
        print(loan)
        
        if loan.loan_approve:
            user_account = loan.account # models er account
            if loan.amount < user_account.balance:
                user_account.balance -= loan.amount # models er amount
                loan.balance_after_transaction = user_account.balance # transaction balance update kora holo
                user_account.save()
                loan.loan_approve = True
                loan.transaction_type = LOAN_PAID
                loan.save()
                return redirect('transactions_app:loan_list')
            else:
                messages.error(self.request, f'Loan amount is grater the available balance !!')
        return redirect('transactions_app:loan_list')
        
            
class LonaListView(LoginRequiredMixin, ListView):
    model = TransactionModel
    template_name = 'loan_request.html'
    context_object_name = 'loans' # loan list ta ei loans context er moddah thakbe
    
    def get_queryset(self):
        user_account = self.request.user.account
        queryset = TransactionModel.objects.filter(account = user_account, transaction_type = 3)
        print(queryset)
        return queryset
    
     
    
def ChangePassword(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = SetPasswordForm(user= request.user, data= request.POST)
            if form.is_valid():
                form.save()
                update_session_auth_hash(request, form.user)
                return redirect('transactions_app:change_pass')
        else:
            form = SetPasswordForm(user= request.POST)
            # raise forms.ValidationError(request, f"Password does't matched")
        return render(request, 'change_pass.html', {'form': form})
    else:
        raise forms.ValidationError(request, "You are not authenticated user")
        # return redirect('transactions_app:change_pass')
         