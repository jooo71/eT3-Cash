# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.home, name='home'),
#     path('deposit/', views.deposit, name='deposit'),
#     path('withdraw/', views.withdraw, name='withdraw'),
#     path('transfer/', views.transfer, name='transfer'),
#     path('balance/', views.balance, name='balance'),
#     path('history/', views.transaction_history, name='history'),
#     path('pay_bill/', views.pay_bill, name='pay_bill'),
#     path('buy_airtime/', views.buy_airtime, name='buy_airtime'),
#     # path('', views.user_login, name='login'),

# ]

from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import dashboard_view


urlpatterns = [
    # path('', views.home, name='api-home'),
    path('api/deposit/', views.deposit, name='api-deposit'),
    path('api/withdraw/', views.withdraw, name='api-withdraw'),
    path('api/pay-bill/', views.pay_bill, name='api-pay-bill'),
    path('api/buy-airtime/', views.buy_airtime, name='api-buy-airtime'),
    path('api/transfer/', views.transfer, name='api-transfer'),
    path('api/balance/', views.balance, name='api-balance'),
    path('api/transaction-history/', views.transaction_history, name='api-transaction-history'),
    path('api/register/', views.register_user, name='register_user'),
    # path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/login/', views.login_user, name='token_obtain_pair'),
    # urls.py
    path('api/paypal/create-paypal-payment/', views.create_paypal_payment, name='create-paypal-payment'),
    path('api/paypal/execute-paypal-payment/', views.execute_paypal_payment, name='execute-paypal-payment'),
    path('api/payment/create/', views.create_payment_paypal, name='create_payment'),
    path('api/payment/execute/', views.execute_payment, name='execute_payment'),
    path('payment/success/', views.payment_success, name='payment_success'),  # Define this route
    path('payment/cancel/', views.payment_cancel, name='payment_cancel'), 
    path('dashboard/', dashboard_view, name='dashboard'),  # Define the URL


    # urls.py
    # path('api/purchase/', views.make_purchase, name='make_purchase'),

    # path('api/logout/', views.logout, name='token_obtain_pair'),
    # path('', views.home, name='home'),

    # path('login/', views.login_user, name='login'),  # Login page

    # path('register/', views.register_user, name='register'),

    # path('dashboard/',views.dashboard_view, name='dashboard'),
    # path('dashboard.html',views.dashboard_view, name='dashboard_view'),


    # path('deposit/', views.deposit, name='deposit'),
    # path('deposit.html', views.deposit_page, name='deposit_page'),

    # path('withdraw/', views.withdraw, name='withdraw'),
    # path('withdraw.html', views.withdraw_page, name='withdraw_page'),
    
    # path('payBill/', views.pay_bill, name='payBill'),
    # path('payBill.html', views.payBill_page, name='payBill_page'),

    # path('buyAirtime/', views.buy_airtime, name='buyAirtime'),
    # path('buyAirtime.html', views.buyAirtime_page, name='buyAirtime_page'),

    # path('transfer/', views.transfer, name='transfer'),
    # path('transfer.html', views.transfer_page, name='transfer_page'),

    # path('transactionHistory/', views.transactionHistory, name='transactionHistory'),
    # path('transactionHistory.html', views.transactionHistory_page, name='transactionHistory_page'),
    
    # path('balance/', views.balance, name='balance'),
    # path('balance.html', views.balance_page, name='balance_page'),

    # path('logout/',views.logout,name='logout'),
]
