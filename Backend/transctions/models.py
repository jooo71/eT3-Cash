from django.db import models
from django.utils import timezone
from decimal import Decimal
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect


# Create your models here.
# class User(models.Model):
#     name = models.CharField(max_length=100)
#     phone_number = models.CharField(max_length=11, unique=True)
#     balance = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
#     password = models.CharField(max_length=100)
    

#     def deposit(self, amount):
#         self.balance += Decimal(amount)  # Ensure amount is Decimal
#         self.save()

#     def withdraw(self, amount):
#         if Decimal(amount) > self.balance:
#             raise ValueError("Insufficient balance!")
#         self.balance -= Decimal(amount)  # Ensure amount is Decimal
#         self.save()

#     def pay_bill(self, amount):
#         self.withdraw(amount)

#     def buy_airtime (self, amount):
#         self.withdraw(amount)

#     def __str__(self):
#         return self.name

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, phone_number, name, password=None, **extra_fields):
        if not phone_number:
            raise ValueError('The Phone number must be set')
        user = self.model(phone_number=phone_number, name=name, **extra_fields)
        user.set_password(password)  # Hash the password
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(phone_number, name, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    phone_number = models.CharField(max_length=15, unique=True)
    name = models.CharField(max_length=255)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'phone_number'  # Ensures phone_number is used for login
    REQUIRED_FIELDS = ['name']

    objects = UserManager()  # Your custom manager

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['name']

    def deposit(self, amount):
        """Method to deposit money to the user's balance."""
        if amount <= 0:
            raise ValueError("Deposit amount must be greater than zero.")
        self.balance += amount
        self.save()

    def withdraw(self, amount):
        """Method to withdraw money from the user's balance."""
        if amount <= 0:
            raise ValueError("Withdrawal amount must be greater than zero.")
        if self.balance < amount:
            raise ValueError("Insufficient balance.")
        self.balance -= amount
        self.save()

    def pay_bill(self, amount):
        """Method to pay bills from the user's balance."""
        if amount <= 0:
            raise ValueError("Bill payment amount must be greater than zero.")
        if self.balance < amount:
            raise ValueError("Insufficient balance to pay bill.")
        self.balance -= amount
        self.save()

    def buy_airtime(self, amount):
        """Method to buy airtime."""
        if amount <= 0:
            raise ValueError("Airtime amount must be greater than zero.")
        if self.balance < amount:
            raise ValueError("Insufficient balance for airtime purchase.")
        self.balance -= amount
        self.save()

    def __str__(self):
        return f'{self.name} ({self.phone_number})'


class Transaction(models.Model):
    sender = models.ForeignKey(User, related_name="sent_transactions", on_delete=models.CASCADE)    ## ForeignKey:a relationship between the Transaction model and the User model. Specifically, this defines the sender of the transaction as a User.
    recipient = models.ForeignKey(User, related_name="received_transactions", on_delete=models.CASCADE, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=50)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.transaction_type}: {self.sender} -> {self.recipient} | {self.amount}"



