from datetime import datetime

class User:
    def __init__(self, name, phone_number, balance=0):
        self.name = name
        self.phone_number = phone_number
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount
        print(f"{self.name} has deposited {amount}. New balance is {self.balance}.")
        
    def withdraw(self, amount):
        if amount > self.balance:
            print("Insufficient balance!")
        else:
            self.balance -= amount
            print(f"{self.name} has withdrawn {amount}. New balance is {self.balance}.")


    def send_money(self, recipient , amount):
        if amount > self.balance:
            print("Insufficient balance!")
        else:
            self.balance -= amount
            recipient.balance += amount
            print(f"{self.name} sent {amount} to {recipient.name}. New balance is {self.balance}. {recipient.name}'s new balance is {recipient.balance}")


    def pay_bill(self, bill_name, amount):
        if amount > self.balance:
            print("Insufficient balance to pay the bill!")
        else:
            self.balance -= amount
            print(f"{self.name} paid {amount} for {bill_name}. New balance is {self.balance}.")


    def buy_airtime(self, amount):
        if amount > self.balance:
            print("Insufficient balance to buy airtime!")
        else:
            self.balance -= amount
            print(f"{self.name} bought {amount} worth of airtime. New balance is {self.balance}.")

    def get_balance(self):
        print(f"{self.name} balance is {self.balance}.")


class Transaction:
    def __init__(self, sender, recipient, amount, transaction_type):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.transaction_type = transaction_type
        self.date = datetime.now()

    def __repr__(self):
        recipient_name = self.recipient.name if self.recipient else "N/A"
        return f"[{self.date}] {self.transaction_type}: {self.sender.name} -> {recipient_name} | Amount: {self.amount}"

class eT3CashSystem:
    def __init__(self):
        self.users = {}
        self.transactions = []

    def add_user(self, user):
        if user.phone_number in self.users:
            print(f"User with phone number {user.phone_number} already exists.")
        else:
            self.users[user.phone_number] = user
            print(f"User {user.name} added to the system.")

    def get_user_by_phone(self, phone_number):
        return self.users.get(phone_number)

    def record_transaction(self, transaction):
        self.transactions.append(transaction)
        print(f"Transaction recorded: {transaction}")

    def get_transaction_history(self):
        for transaction in self.transactions:
            print(transaction)

    def perform_deposit(self, phone_number, amount):
        user = self.get_user_by_phone(phone_number)
        if user:
            user.deposit(amount)
            transaction = Transaction(user, None, amount, "Deposit")
            self.record_transaction(transaction)
        else:
            print("User not found.")

    def perform_withdrawal(self, phone_number, amount):
        user = self.get_user_by_phone(phone_number)
        if user:
            user.withdraw(amount)
            transaction = Transaction(user, None, amount, "Withdrawal")
            self.record_transaction(transaction)
        else:
            print("User not found.")

    def perform_transfer(self, sender_phone, recipient_phone, amount):
        sender = self.get_user_by_phone(sender_phone)
        recipient = self.get_user_by_phone(recipient_phone)
        if sender and recipient:
            sender.send_money(recipient, amount)
            transaction = Transaction(sender, recipient, amount, "Transfer")
            self.record_transaction(transaction)
        else:
            print("One or both users not found.")

    def perform_bill_payment(self, phone_number, bill_name, amount):
        user = self.get_user_by_phone(phone_number)
        if user:
            user.pay_bill(bill_name, amount)
            transaction = Transaction(user, None, amount, f"Bill Payment ({bill_name})")
            self.record_transaction(transaction)
        else:
            print("User not found.")

    def perform_airtime_purchase(self, phone_number, amount):
        user = self.get_user_by_phone(phone_number)
        if user:
            user.buy_airtime(amount)
            transaction = Transaction(user, None, amount, "Airtime Purchase")
            self.record_transaction(transaction)
        else:
            print("User not found.")

    def getting_balance(self,phone_number):
        user = self.get_user_by_phone(phone_number)
        if user:
            return user.get_balance()
        else:
            print("User not found.")

def main():
    eT3Cash = eT3CashSystem()

    # Adding some sample users
    eT3Cash.add_user(User("Youseif Essam", "01003793415", balance=100))
    eT3Cash.add_user(User("Mohammed Fahmy", "01110989460", balance=20))

    while True:
        print("\nChoose an action:")
        print("1. Deposit")
        print("2. Withdraw")
        print("3. Transfer")
        print("4. Pay Bill")
        print("5. Buy Airtime")
        print("6. View Transaction History")
        print("7. Get Balance")
        print("8. Exit")

        action = input("Enter the number of your action: ")

        if action == "1":
            phone_number = input("Enter your phone number: ")
            amount = float(input("Enter the amount to deposit: "))
            eT3Cash.perform_deposit(phone_number, amount)

        elif action == "2":
            phone_number = input("Enter your phone number: ")
            amount = float(input("Enter the amount to withdraw: "))
            eT3Cash.perform_withdrawal(phone_number, amount)

        elif action == "3":
            sender_phone = input("Enter your phone number: ")
            recipient_phone = input("Enter the recipient's phone number: ")
            amount = float(input("Enter the amount to transfer: "))
            eT3Cash.perform_transfer(sender_phone, recipient_phone, amount)

        elif action == "4":
            phone_number = input("Enter your phone number: ")
            bill_name = input("Enter the bill name: ")
            amount = float(input("Enter the amount to pay: "))
            eT3Cash.perform_bill_payment(phone_number, bill_name, amount)

        elif action == "5":
            phone_number = input("Enter your phone number: ")
            amount = float(input("Enter the amount for airtime purchase: "))
            eT3Cash.perform_airtime_purchase(phone_number, amount)

        elif action == "6":
            eT3Cash.get_transaction_history()
        
        elif action == "7":
            phone_number = input("Enter your phone number: ")
            eT3Cash.getting_balance(phone_number)

        elif action == "8":
            print("Exiting the system.")
            break

        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
