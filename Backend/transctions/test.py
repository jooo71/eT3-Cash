from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from transctions.models import User, Transaction
from decimal import Decimal
from django.test import TestCase ,SimpleTestCase
from django.urls import reverse, resolve
import transctions.views  

class TestUrls(SimpleTestCase):
    def test_deposit_url(self):
        url = reverse('api-deposit')
        self.assertEqual(resolve(url).func, transctions.views.deposit)

    def test_withdraw_url(self):
        url = reverse('api-withdraw')
        self.assertEqual(resolve(url).func, transctions.views.withdraw)

    def test_pay_bill_url(self):
        url = reverse('api-pay-bill')
        self.assertEqual(resolve(url).func, transctions.views.pay_bill)

    def test_buy_airtime_url(self):
        url = reverse('api-buy-airtime')
        self.assertEqual(resolve(url).func, transctions.views.buy_airtime)

    def test_transfer_url(self):
        url = reverse('api-transfer')
        self.assertEqual(resolve(url).func, transctions.views.transfer)

    def test_balance_url(self):
        url = reverse('api-balance')
        self.assertEqual(resolve(url).func, transctions.views.balance)

    def test_transaction_history_url(self):
        url = reverse('api-transaction-history')
        self.assertEqual(resolve(url).func, transctions.views.transaction_history)

    def test_register_user_url(self):
        url = reverse('register_user')
        self.assertEqual(resolve(url).func, transctions.views.register_user)

    def test_login_user_url(self):
        url = reverse('token_obtain_pair')
        self.assertEqual(resolve(url).func, transctions.views.login_user)

##################################################
class UserAPITestCase(APITestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(phone_number='0123456789', password='testpass', name='Test User')
        self.client = APIClient()
        
        # Authenticate the test client
        response = self.client.post(reverse('token_obtain_pair'), {
            'phone_number': '0123456789',
            'password': 'testpass'
        })
        self.access_token = response.data['access']
        # print(self.access_token)
        # Set the Authorization header
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
    
    # def test_deposit(self):
    # #     # Test deposit API
    #     url = reverse('api-deposit')
    #     response = self.client.post(url, {'amount': '100.00'})
        
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertIn('Deposited 100', response.data['message'])
    def test_deposit_multiple_cases(self):
        test_cases = [
            {'amount': '100.00', 'expected_status': status.HTTP_200_OK, 'message': 'Deposited 100'},
            {'amount': '-10.00', 'expected_status': status.HTTP_400_BAD_REQUEST, 'message': 'Deposit amount must be greater than zero'},
            {'amount': 'abc', 'expected_status': status.HTTP_400_BAD_REQUEST, 'message': 'Enter a valid amount'}
        ]
        
        url = reverse('api-deposit')
        for case in test_cases:
            response = self.client.post(url, {'amount': case['amount']})
            
            self.assertEqual(response.status_code, case['expected_status'])
            if case['expected_status'] == status.HTTP_200_OK:
                self.assertIn(case['message'], response.data['message'])
            else:
                self.assertIn(case['message'], response.data['error'])

    def test_withdraw(self):
        # Deposit first, so there's money to withdraw
        self.user.deposit(Decimal('100.00'))
        
        # Test withdraw API
        url = reverse('api-withdraw')
        response = self.client.post(url, {'amount': '50.00'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Withdrew 50', response.data['message'])
    
    def test_transfer(self):
        # Create recipient user
        recipient = User.objects.create_user(phone_number='0987654321', password='testpass', name='Recipient User')
        
        # Deposit money to the sender's account
        self.user.deposit(Decimal('100.00'))
        
        # Test transfer API
        url = reverse('api-transfer')
        response = self.client.post(url, {
            'recipient_phone': recipient.phone_number,
            'amount': '20.00'
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Transferred 20', response.data['message'])
        self.assertEqual(response.data['recipient_name'], recipient.name)

    def test_buy_airtime(self):
        # Test buy airtime API
        self.user.deposit(Decimal('100.00'))
        url = reverse('api-buy-airtime')
        response = self.client.post(url, {'amount': '10.00'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Bought 10.00 worth of airtime', response.data['message'])

    def test_pay_bill(self):
        # Test pay bill API
        self.user.deposit(Decimal('100.00'))  # Add money to user's balance
        url = reverse('api-pay-bill')
        response = self.client.post(url, {
            'amount': '30.00',
            'bill_type': 'Electricity'  # Include the bill type in the request
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('paid 30.00 for Electricity', response.data['message'])  # Check for the bill type in the message
        
        # Verify the balance after bill payment
        self.user.refresh_from_db()
        self.assertEqual(self.user.balance, Decimal('70.00'))  # 100.00 - 30.00 = 70.00


    def test_balance(self):
        # Test balance API
        url = reverse('api-balance')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('balance', response.data)

    def test_transaction_history(self):
        # Create some transactions
        self.user.deposit(Decimal('100.00'))
        Transaction.objects.create(sender=self.user, amount=Decimal('50.00'), transaction_type='deposit')

        # Test transaction history API
        url = reverse('api-transaction-history')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_register_user(self):
        # Test user registration API
        url = reverse('register_user')
        response = self.client.post(url, {
            'phone_number': '0111222333',
            'password': 'newpass123',
            'name': 'New User'
        })
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('access', response.data)
    
    def test_login_user(self):
        # Test user login API
        url = reverse('token_obtain_pair')
        response = self.client.post(url, {
            'phone_number': self.user.phone_number,
            'password': 'testpass'
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('name', response.data['user'])

######################################################
class FullUserFlowIntegrationTest(APITestCase):

    def test_user_registration_and_financial_operations(self):
        # Step 1: Register a new user
        register_url = reverse('register_user')
        register_response = self.client.post(register_url, {
            'phone_number': '0023456789',
            'name': 'Test2 User',
            'password': 'testpass'
        })
        self.assertEqual(register_response.status_code, status.HTTP_201_CREATED)

        # Step 2: Log in the user
        login_url = reverse('token_obtain_pair')
        login_response = self.client.post(login_url, {
            'phone_number': '0023456789',
            'password': 'testpass'
        })
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        token = login_response.data['access']  # Extract JWT token

        # Set Authorization header for future requests
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

        # Step 3: Deposit money
        deposit_url = reverse('api-deposit')
        deposit_response = self.client.post(deposit_url, {'amount': '100.00'})
        self.assertEqual(deposit_response.status_code, status.HTTP_200_OK)
        self.assertIn('Deposited 100', deposit_response.data['message'])

        # Step 4: Check balance
        user = User.objects.get(phone_number='0023456789')
        self.assertEqual(user.balance, Decimal('100.00'))

        #Step 5: Withdraw money
        withdraw_url = reverse('api-withdraw')
        withdraw_response = self.client.post(withdraw_url, {'amount': '50.00'})
        self.assertEqual(withdraw_response.status_code, status.HTTP_200_OK)
        self.assertIn('Withdrew 50', withdraw_response.data['message'])

        # Step 6: Check balance
        user = User.objects.get(phone_number='0023456789')
        self.assertEqual(user.balance, Decimal('50.00'))

