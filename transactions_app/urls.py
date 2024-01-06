from django.urls import path
from transactions_app.views import DepositMoneyView, WithdrawMonyView,LoanRequestView,  TransactionReportView, PayLonaView, LonaListView, TransferMoneyView, ChangePassword

app_name = 'transactions_app'
urlpatterns = [
    path('deposit/', DepositMoneyView.as_view(), name = 'deposit'),
    path('withdrawal/', WithdrawMonyView.as_view(), name = 'withdrawal'),
    path('loan_request/', LoanRequestView.as_view(), name = 'loan_request'),
    path('report/', TransactionReportView.as_view(), name = 'transaction_report'),
    path('loans/<int:loan_id>/', PayLonaView.as_view(), name = 'pay_loan'),
    path('loans/', LonaListView.as_view(), name = 'loan_list'),
    path('transfer/', TransferMoneyView.as_view(), name = 'transfer'),
    path('change_pass/', ChangePassword, name = 'change_pass'),
]
