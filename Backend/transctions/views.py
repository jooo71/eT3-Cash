
from pyexpat.errors import messages
import paypalrestsdk
import requests
from rest_framework import status
from rest_framework.response import Response

from transctions.utils import send_sms
from .models import User, Transaction
from .serializers import UserSerializer, TransactionSerializer
from decimal import Decimal
from rest_framework.authentication import BasicAuthentication , TokenAuthentication 
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import authenticate, login
from rest_framework_simplejwt.tokens import AccessToken

from django.shortcuts import render, redirect
from django.http import JsonResponse
# from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
# import json

# from django.views.decorators.http import require_http_methods
# from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout

from paypalrestsdk import Payment
from django.conf import settings

paypalrestsdk.configure({
    "mode": 'sandbox' ,  # sandbox or live
    "client_id": 'AT3qo7x5tCpCVcG2ille6ues5KwKNu0ut1MxuZQ3b9oBycvumPnhQuvMrNwBC1sVWCBTd-z9ZZcc_9nS',
    "client_secret":'EJptkuECtbJ-9XBn4kabUAqpfaP5nt-WYnt4aMZmh546W9F14OFAbUSvc7EYR-41IsHz5OGdkk-bWU8r',
})
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_paypal_payment(request):
    amount = request.data.get('amount')
    item_name = request.data.get('item_name')

    # Create PayPal payment
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {"payment_method": "paypal"},
        "transactions": [{
            "amount": {"total": str(amount), "currency": "USD"},
            "description": f"Purchase of {item_name}"   
        }],
        "redirect_urls": {
            "return_url": "http://localhost:8000/api/paypal/execute-paypal-payment/",
            "cancel_url": "http://localhost:8000/api/paypal/cancel-paypal-payment/"
        }
    })

    if payment.create():
        for link in payment.links:
            if link.rel == "approval_url":
                return Response({"approval_url": link.href})
    else:
        return Response({"error": payment.error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([AllowAny])
def execute_paypal_payment(request):
    payment_id = request.GET.get('paymentId')
    payer_id = request.GET.get('PayerID')
    
    payment = paypalrestsdk.Payment.find(payment_id)

    if payment.execute({"payer_id": payer_id}):
        # Update user's balance or complete the purchase
        return Response({"message": "Payment successful"})
    else:
        return Response({"error": payment.error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Home page view
# @api_view(['GET'])
# def home(request):
#     return Response({'message': 'Welcome to the API Home'})
# import requests
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from django.conf import settings

# @csrf_exempt
# def execute_payment(request):
#     if request.method == 'POST':
#         payment_id = request.POST.get('paymentId')  # The payment ID returned from PayPal
#         payer_id = request.POST.get('PayerID')      # The Payer ID returned after approval

#         url = f"{settings.PAYPAL_BASE_URL}/v1/payments/payment/{payment_id}/execute"
        
#         headers = {
#             'Content-Type': 'application/json',
#             'Authorization': f'Bearer {get_paypal_access_token()}'
#         }

#         data = {
#             "payer_id": payer_id
#         }

#         response = requests.post(url, headers=headers, json=data)
#         return JsonResponse(response.json(), status=response.status_code)
#     return JsonResponse({'error': 'Invalid request method'}, status=400)

# def get_paypal_access_token():
#     url = f"{settings.PAYPAL_BASE_URL}/v1/oauth2/token"
#     headers = {
#         'Accept': 'application/json',
#         'Accept-Language': 'en_US'
#     }
#     response = requests.post(url, headers=headers, auth=(settings.PAYPAL_CLIENT_ID, settings.PAYPAL_CLIENT_SECRET), data={'grant_type': 'client_credentials'})
#     return response.json()['access_token']


# # Deposit view
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def deposit(request):
    print("Request User:", request.user)  # Debugging line
    user = request.user
    amount = Decimal(request.data.get('amount'))
    # user = User.objects.get(phone_number=phone_number)
    user.deposit(amount)
    transaction = Transaction.objects.create(sender=user, amount=amount, transaction_type='deposit')
    return Response({'message': f'Deposited {amount} to {user.name}. New balance: {user.balance}'})

# # Withdraw view
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def withdraw(request):
    # Use the authenticated user from the request
    user = request.user
    amount = Decimal(request.data.get('amount'))

    try:
        # Attempt to withdraw the amount
        user.withdraw(amount)
        Transaction.objects.create(sender=user, amount=amount, transaction_type='withdraw')
        return Response({'message': f'Withdrew {amount} from {user.name}. New balance: {user.balance}'})
    except ValueError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# # Pay Bill view
VALID_BILL_TYPES = ['water', 'gas', 'electricity', 'internet']
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def pay_bill(request):
    # phone_number = request.data.get('phone').strip()
    user = request.user
    bill_name = request.data.get('bill_name') ## this line for front with java switch to under line 
    # bill_name = request.data.get('bill_name').strip()
    amount = Decimal(request.data.get('amount'))
    # user = User.objects.get(phone_number=phone_number)
        # Check if bill_name is empty or not in the allowed types
    if not bill_name or bill_name not in VALID_BILL_TYPES:
        return Response({'error': 'Invalid bill type. Only water, gas, electricity, and internet are allowed.'},
                        status=status.HTTP_400_BAD_REQUEST)
    try:
        user.pay_bill(amount)
        transaction = Transaction.objects.create(sender=user, amount=amount, transaction_type=f'Bill Payment ({bill_name})')
        return Response({'message': f'{user.name} paid {amount} for {bill_name}. New balance is {user.balance}'})
    except ValueError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# # Buy Airtime view
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def buy_airtime(request):
    user = request.user
    amount = Decimal(request.data.get('amount'))
    # user = User.objects.get(phone_number=phone_number)
    try:
        user.buy_airtime(amount)
        transaction = Transaction.objects.create(sender=user, amount=amount, transaction_type='Airtime Payment')
        return Response({'message': f'Bought {amount} worth of airtime. New balance: {user.balance}'})
    except ValueError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# # Transfer view
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def transfer(request):
    user = request.user
    recipient_phone = request.data.get('recipient_phone')
    amount = Decimal(request.data.get('amount'))

    try:
        recipient = User.objects.get(phone_number=recipient_phone)
    except User.DoesNotExist:
        return Response({'error': 'Recipient not found.'}, status=status.HTTP_404_NOT_FOUND)

    # Prevent transferring to self
    if user.phone_number == recipient_phone:
        return Response({'error': 'You cannot transfer to yourself.'}, status=status.HTTP_400_BAD_REQUEST)

    if user.balance >= amount:
        user.withdraw(amount)
        recipient.deposit(amount)
        transaction = Transaction.objects.create(sender=user, recipient=recipient, amount=amount, transaction_type='Transfer')
        return Response({'message': f'Transferred {amount} from {user.name} to {recipient.name}.',
                         'recipient_name': recipient.name })
    else:
        return Response({'error': 'Insufficient balance.'}, status=status.HTTP_400_BAD_REQUEST)

# # Check Balance view
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def balance(request):
    user = request.user  # Use the authenticated user from the request

    # Return the user's balance
    return Response({'message': f"{user.name}'s balance is {user.balance}.",'balance':user.balance})

# Transaction History view
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def transaction_history(request):
    user = request.user  # Get the authenticated user from the request

    # Fetch all transactions where the user is either the sender or recipient
    transactions = Transaction.objects.filter(sender=user) | Transaction.objects.filter(recipient=user)

    # Serialize the transactions
    serializer = TransactionSerializer(transactions, many=True)

    # Return the serialized data
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    phone_number = request.data.get('phone_number')
    password = request.data.get('password')
    name = request.data.get('name')

    # Check if all required fields are provided
    if phone_number is None or password is None or name is None:
        return Response({'error': 'Please provide phone number, name, and password.'}, status=status.HTTP_400_BAD_REQUEST)

    # Check if the phone number already exists
    if User.objects.filter(phone_number=phone_number).exists():
        return Response({'error': 'Phone number already registered.'}, status=status.HTTP_400_BAD_REQUEST)

    # Create a new user and hash the password using set_password
    user = User.objects.create(phone_number=phone_number, name=name)
    user.set_password(password)  # Ensure password is hashed
    user.save()

    # Generate only an access token for the new user
    access_token = AccessToken.for_user(user)

    return Response({
        'access': str(access_token),
    }, status=status.HTTP_201_CREATED)



@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    phone_number = request.data.get('phone_number')
    password = request.data.get('password')

    # Authenticate user
    user = authenticate(request, phone_number=phone_number, password=password)
    if user is not None:
        # Generate only an access token
        access_token = AccessToken.for_user(user)
        print(access_token)
        sms_message = "You have successfully logged in."
        send_sms(phone_number, sms_message)
        return Response({
            'access': str(access_token),
            'user':{
                'name': user.name,  # Assuming 'name' field exists in the User model
            }
        })
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
@permission_classes(IsAuthenticated)
def logout(request):
    # No need to handle refresh tokens or blacklisting, just return a response
    return Response({"message": "Successfully logged out."}, status=status.HTTP_200_OK)

##########################API front vue#########################3
def home(request):
    return render(request, 'home.html')

# @api_view(['GET', 'POST'])
# @permission_classes([AllowAny])
# def login_user(request):
#     if request.method == 'POST':
#         phone_number = request.data.get('phone_number')
#         password = request.data.get('password')

#         user = authenticate(request, phone_number=phone_number, password=password)
#         if user:
#             access_token = AccessToken.for_user(user)
#             return JsonResponse({'access': str(access_token), 'user': {'name': user.name}})
#         else:
#             return JsonResponse({'error': 'Invalid credentials'}, status=400)

#     return render(request, 'login.html')  # Render login form

# @api_view(['GET', 'POST'])
# @permission_classes([AllowAny])
# def register_user(request):
#     if request.method == 'POST':
#         phone_number = request.data.get('phone_number')
#         password = request.data.get('password')
#         name = request.data.get('name')

#         if User.objects.filter(phone_number=phone_number).exists():
#             return JsonResponse({'error': 'Phone number already registered.'}, status=400)

#         user = User.objects.create(phone_number=phone_number, name=name)
#         user.set_password(password)
#         user.save()

#         access_token = AccessToken.for_user(user)
#         return JsonResponse({'access': str(access_token)}, status=201)

#     return render(request, 'register.html')  # Render register form

# # from django.views.decorators.cache import cache_control

# # @cache_control(no_cache=True, must_revalidate=True, no_store=True)
# def dashboard_view(request):
#     return render(request, 'dashboard.html')

# def deposit_page(request):
#     return render(request, 'deposit.html')

# def withdraw_page(request):
#     return render(request, 'withdraw.html')

# def payBill_page(request):
#     return render(request, 'payBill.html')

# def buyAirtime_page(request):
#     return render(request, 'buyAirtime.html')

# def transfer_page(request):
#     return render(request, 'transfer.html')

# def transactionHistory_page(request):
#     return render(request, 'transactionHistory.html')

# def balance_page(request):
#     return render(request, 'balance.html')

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def transactionHistory(request):
#     user = request.user
#     transactions = Transaction.objects.filter(sender=user)  # Fetch transactions for the authenticated user

#     # Create a list to hold transaction data
#     transaction_data = []

#     for transaction in transactions:
#         transaction_data.append({
#             'date': transaction.date,  # Assuming you have a timestamp field `created_at`
#             'transaction_type': transaction.transaction_type,
#             'amount': transaction.amount,
#             'recipient': transaction.recipient.name if transaction.recipient else None,  # If you have a recipient field
#             'balance_after': user.balance  # Assuming you have a balance attribute on your user model
#         })

#     return Response({'transactions': transaction_data}, status=status.HTTP_200_OK)

# def get_paypal_access_token():
#     url = f"https://api.sandbox.paypal.com/v1/oauth2/token"
#     headers = {
#         'Accept': 'application/json',
#         'Accept-Language': 'en_US'
#     }
#     response = requests.post(url, headers=headers, auth=(
#         "AT3qo7x5tCpCVcG2ille6ues5KwKNu0ut1MxuZQ3b9oBycvumPnhQuvMrNwBC1sVWCBTd-z9ZZcc_9nS",
#         "EJptkuECtbJ-9XBn4kabUAqpfaP5nt-WYnt4aMZmh546W9F14OFAbUSvc7EYR-41IsHz5OGdkk-bWU8r"),
#                              data={'grant_type': 'client_credentials'})
#     return response.json()['access_token']

# def payment_success(request):
#     # Get the payment ID and Payer ID from the request
#     payment_id = request.GET.get('paymentId')
#     payer_id = request.GET.get('PayerID')

#     # Optional: Validate the payment with PayPal
#     access_token = get_paypal_access_token()
#     payment_url = f"https://api.sandbox.paypal.com/v1/payments/payment/{payment_id}"

#     headers = {
#         'Content-Type': 'application/json',
#         'Authorization': f'Bearer {access_token}'
#     }

#     response = requests.get(payment_url, headers=headers)

#     if response.status_code == 200:
#         payment_details = response.json()
#         # You can now access details like payment_details['transactions'] to display information
#         return render(request, 'payment_success.html', {'payment_details': payment_details})
#     else:
#         return render(request, 'payment_error.html', {'error': 'Failed to retrieve payment details.'})
    
# def execute_payment(request):
#     if request.method == 'POST':
#         payment_id = request.POST.get('paymentId')  # The payment ID returned from PayPal
#         payer_id = request.POST.get('PayerID')      # The Payer ID returned after approval

#         url = f"{settings.PAYPAL_BASE_URL}/v1/payments/payment/{payment_id}/execute"
        
#         headers = {
#             'Content-Type': 'application/json',
#             'Authorization': f'Bearer {get_paypal_access_token()}'
#         }

#         data = {
#             "payer_id": payer_id
#         }

#         response = requests.post(url, headers=headers, json=data)
#         return JsonResponse(response.json(), status=response.status_code)
#     return JsonResponse({'error': 'Invalid request method'}, status=400)

# def create_payment_paypal(request):
#     if request.method == 'POST':
#         access_token = get_paypal_access_token()
#         url = f"https://api.sandbox.paypal.com/v1/payments/payment"
#         payment_data = {
#             "intent": "sale",
#             "redirect_urls": {
#                 "return_url": request.build_absolute_uri('/payment/success/'),
#                 "cancel_url": request.build_absolute_uri('/payment/cancel/')
#             },
#             "payer": {
#                 "payment_method": "paypal"
#             },
#             "transactions": [{
#                 "amount": {
#                     "total": "100.00",  # Change this to the actual amount
#                     "currency": "USD"
#                 },
#                 "description": "Payment for order."
#             }]
#         }

#         response = requests.post(url, headers={
#             "Content-Type": "application/json",
#             "Authorization": f"Bearer {access_token}",
#         }, json=payment_data)

#         if response.status_code == 201:
#             approval_url = next(link['href'] for link in response.json()['links'] if link['rel'] == 'approval_url')
#             return redirect(approval_url)
#         else:
#             messages.error(request, "Failed to create payment.")
#             return redirect('payment_form')  # Redirect to your payment form view
#     return render(request, 'payment_form.html')


# views.py

import requests
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Sum

def get_paypal_access_token():
    url = "https://api.sandbox.paypal.com/v1/oauth2/token"
    headers = {
        'Accept': 'application/json',
        'Accept-Language': 'en_US'
    }
    response = requests.post(url, headers=headers, auth=(
        settings.PAYPAL_CLIENT_ID, settings.PAYPAL_CLIENT_SECRET
    ), data={'grant_type': 'client_credentials'})
    return response.json().get('access_token')

def create_payment_paypal(request):
    if request.method == 'POST':
        access_token = get_paypal_access_token()
        url = "https://api.sandbox.paypal.com/v1/payments/payment"
        payment_data = {
            "intent": "sale",
            "redirect_urls": {
                "return_url": request.build_absolute_uri('/payment/success/'),
                "cancel_url": request.build_absolute_uri('/payment/cancel/')
            },
            "payer": {
                "payment_method": "paypal"
            },
            "transactions": [{
                "amount": {
                    "total": "100.00",  # Adjust as needed
                    "currency": "USD"
                },
                "description": "Payment for order."
            }]
        }

        response = requests.post(url, headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
        }, json=payment_data)

        if response.status_code == 201:
            approval_url = next(link['href'] for link in response.json()['links'] if link['rel'] == 'approval_url')
            return redirect(approval_url)
        else:
            messages.error(request, "Failed to create payment.")
            return redirect('payment_form')  # Redirect to your payment form view

    return render(request, 'payment_form.html')

def execute_payment(request):
    if request.method == 'POST':
        payment_id = request.POST.get('paymentId')
        payer_id = request.POST.get('PayerID')
        url = f"https://api.sandbox.paypal.com/v1/payments/payment/{payment_id}/execute"
        
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {get_paypal_access_token()}'
        }

        data = {
            "payer_id": payer_id
        }

        response = requests.post(url, headers=headers, json=data)
        return JsonResponse(response.json(), status=response.status_code)

    return JsonResponse({'error': 'Invalid request method'}, status=400)

def payment_success(request):
    payment_id = request.GET.get('paymentId')
    payer_id = request.GET.get('PayerID')

    access_token = get_paypal_access_token()
    payment_url = f"https://api.sandbox.paypal.com/v1/payments/payment/{payment_id}"

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.get(payment_url, headers=headers)

    if response.status_code == 200:
        payment_details = response.json()
        return render(request, 'payment_success.html', {'payment_details': payment_details})
    else:
        return render(request, 'payment_error.html', {'error': 'Failed to retrieve payment details.'})
    
def payment_cancel(request):
    return render(request, 'payment_cancel.html', {'message': 'Payment canceled by user.'})

# def dashboard_view(request):
#     data_from_sql = get_sql_server_data()  # Get data from SQL Server
#     return render(request, 'dashboard.html', {'data': data_from_sql})


import pyodbc
from django.shortcuts import render

# def dashboard_view(request):
#     try:
#         # Establish SQL Server connection using pyodbc
#         conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
#                               'SERVER=DESKTOP-UQDT40R;'  # Replace with actual server
#                               'DATABASE=wallet;'  # Replace with actual database name
#                               'Trusted_Connection=yes;')

#         # Create a cursor to execute queries
#         cursor = conn.cursor()

#         # Query to fetch data from the table
#         cursor.execute('SELECT * FROM PartitionedTransactions')  # Replace with your actual table name
#         rows = cursor.fetchall()  # Fetch all rows from the query result

#         # Process the data into a more usable format (optional)
#         data = [row for row in rows]  # You can also create a dictionary or any other format if needed

#     except pyodbc.Error as e:
#         # If there's an error, log it or print it (optional)
#         print(f"Database error: {e}")
#         data = []  # Return an empty list or handle the error appropriately

#     finally:
#         # Always close the connection when done
#         conn.close()

#     # Pass the data to the template for rendering
#     return render(request, 'admin/dashboard.html', {'data': data})

import pyodbc
from django.shortcuts import render
from collections import Counter
import datetime

from django.shortcuts import render
import pyodbc

def dashboard_view(request):
    # SQL Server connection using pyodbc
    conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                          'SERVER=DESKTOP-UQDT40R;'  # Replace with actual server
                          'DATABASE=wallet;'  # Replace with actual database name
                          'Trusted_Connection=yes;')

    cursor = conn.cursor()


    # Query for Total Amount per Transaction Type
    cursor.execute('SELECT transaction_type, SUM(amount) AS total_amount  FROM PartitionedTransactions GROUP BY transaction_type')
    transaction_type_amount_data = cursor.fetchall()
    transaction_type_amount_labels = [row[0] for row in transaction_type_amount_data]
    transaction_type_amount_values = [float(row[1]) for row in transaction_type_amount_data]  # Convert Decimal to float

    # Query to get the most active users by total operations (sender or recipient)
    # Sender Transactions (sender_id):
        # For every transaction where a user is the sender, count that transaction.

    # Recipient Transactions (recipient_id):
        # For every transaction where a user is the recipient, count that transaction.

    # UNION ALL:
        # Combines both sender and recipient transactions into one list of users, so each user is counted for every transaction where they are either a sender or a recipient.

    # COUNT(*):
        # Counts the total number of operations (whether sending or receiving) for each user.

    # ORDER BY total_operations DESC:
        # Orders the results by the total number of operations, with the most active user at the top.   
    cursor.execute("""
    SELECT 
        user_id,
        COUNT(*) AS total_operations
    FROM (
        SELECT sender_id AS user_id
        FROM PartitionedTransactions
        WHERE sender_id IS NOT NULL
        
        UNION ALL
        
        SELECT recipient_id AS user_id
        FROM PartitionedTransactions
        WHERE recipient_id IS NOT NULL
    ) AS combined_users
    GROUP BY user_id
    ORDER BY total_operations DESC
    """)
    most_active_users_data = cursor.fetchall()

    # Process the most active users' data
    active_user_ids = [row[0] for row in most_active_users_data]  # User IDs
    total_operations = [row[1] for row in most_active_users_data]  # Total operations for each user

        # Query for Daily Operations
    cursor.execute('''
        SELECT CAST(transaction_date AS DATE) AS transaction_day, COUNT(*) AS total_operations
        FROM PartitionedTransactions
        GROUP BY CAST(transaction_date AS DATE)
        ORDER BY transaction_day DESC
    ''')
    daily_operations_data = cursor.fetchall()
    daily_operation_dates = [str(row[0]) for row in daily_operations_data]  # Ensure dates are in 'YYYY-MM-DD' format
    daily_operations_count = [row[1] for row in daily_operations_data]  # Number of operations

        # Query for Most Operations by Hour
    cursor.execute('''
        SELECT 
            DATEPART(HOUR, transaction_date) AS operation_hour,
            COUNT(*) AS total_operations
        FROM 
            PartitionedTransactions
        WHERE 
            transaction_date IS NOT NULL
        GROUP BY 
            DATEPART(HOUR, transaction_date)
        ORDER BY 
            total_operations DESC;
    ''')

    hourly_data = cursor.fetchall()
    hourly_labels = [str(row[0]) + ":00" for row in hourly_data]  # Hour labels (e.g., '14:00')
    hourly_values = [row[1] for row in hourly_data]  # Count of operations in each hour

    # Close the database connection
    cursor.close()
    conn.close()

    # Pass the data to the template for rendering with Chart.js
    return render(request, 'admin/dashboard.html', {
        'transaction_type_amount_labels': transaction_type_amount_labels,
        'transaction_type_amount_values': transaction_type_amount_values,
        'most_active_users_ids': active_user_ids,
        'most_active_users_operations': total_operations,
        'daily_operation_dates': daily_operation_dates,
        'daily_operations_count': daily_operations_count,
        'hourly_labels': hourly_labels,
        'hourly_values': hourly_values,
    })

