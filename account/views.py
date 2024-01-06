from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import FormView
from account.forms import UserRegisterFrom, UserUpdateFrom
from account.models import BankAccountRegisterModel
from django.contrib.auth import login, logout
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.views import View

# Create your views here.

                # Registration view 
            # ==========================
class UserRegistrationView(FormView):
    template_name = 'account/user_registration.html'
    form_class = UserRegisterFrom
    success_url = reverse_lazy('register')
    
    def form_valid(self, form):
        # print(form.cleaned_data)
        log_in = form.save()
        login(self.request, log_in)
        return super().form_valid(form) # recursively call 
    
                    # Login view 
            # ==========================

class UserLoginView(LoginView):
    template_name = 'account/user_login.html'
    def get_success_url(self):
        return reverse_lazy('transactions_app:transaction_report')
    
                # Logout view 
            # ==========================
    
class UserLogoutView(LogoutView):
    def get_success_url(self):
        if self.request.user.is_authenticated:
            logout(self.request)
        return reverse_lazy('home')
    
    
                # get and post/update 
            # ==========================
class UserUpdateView(View):
    template_name = 'account/update.html'
    
    # instance show korbe form er moddeh
    def get(self, request):
        form = UserUpdateFrom(instance= request.user)
        return render(request, self.template_name, {'form': form})
    
    # instance update korbe 
    def post(self, request):
        form = UserUpdateFrom(request.POST, instance = request.user)
        if form.is_valid():
            form.save()
            return redirect('update')
        return render(request, self.template_name, {'form': form})

    