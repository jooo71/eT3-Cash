# from django.contrib import admin
# from .models import User ,Transaction
# class UserAdmin(admin.ModelAdmin):
#     list_display = ('name', 'phone_number', 'balance', 'is_active', 'is_staff')  # Columns to display in the list view
#     search_fields = ('name', 'phone_number')  # Enable searching by name or phone number
#     list_filter = ('is_active', 'is_staff')  # Filters for active/staff status
#     ordering = ('name',)  # Default ordering by name
#     def delete_model(self, request, obj):
#         # Delete all transactions related to the user before deleting the user
#         Transaction.objects.filter(sender=obj).delete()
#         Transaction.objects.filter(recipient=obj).delete()
#         # Now delete the user
#         super().delete_model(request, obj)


# class TransactionAdmin(admin.ModelAdmin):
#     list_display = ('transaction_type', 'sender', 'recipient', 'amount', 'date')  # Display these columns in the list view
#     search_fields = ('sender__name', 'recipient__name', 'transaction_type')  # Enable searching by sender, recipient, or transaction type
#     list_filter = ('transaction_type', 'date')  # Filters for transaction type and date
#     ordering = ('-date',)  # Default ordering by date (newest first)




# admin.site.register(User, UserAdmin)
# admin.site.register(Transaction,TransactionAdmin)

from django.contrib import admin
from django.shortcuts import render
from django.urls import path
from django.http import HttpResponseRedirect
import pandas as pd
import io
from decimal import Decimal  # Import Decimal
from .models import User, Transaction
from django.utils import timezone
from django.shortcuts import redirect
from django.utils.html import format_html


class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'balance', 'is_active', 'is_staff')
    search_fields = ('name', 'phone_number')
    list_filter = ('is_active', 'is_staff')
    ordering = ('name',)

    def delete_model(self, request, obj):
        # Delete all transactions related to the user before deleting the user
        Transaction.objects.filter(sender=obj).delete()
        Transaction.objects.filter(recipient=obj).delete()
        # Now delete the user
        super().delete_model(request, obj)


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('transaction_type', 'sender', 'recipient', 'amount', 'date')
    search_fields = ('sender__name', 'recipient__name', 'transaction_type')
    list_filter = ('transaction_type', 'date')
    ordering = ('-date',)

    def get_urls(self):
        """
        Add a custom URL for the dashboard.
        """
        urls = super().get_urls()
        custom_urls = [
            path('dashboard/', self.admin_site.admin_view(self.dashboard_view), name='dashboard'),
        ]
        return custom_urls + urls

    def dashboard_view(self, request):
        """
        Render the dashboard page with charts.
        """
        return redirect('/admin/dashboard/')  # Replace with your dashboard URL

    def dashboard_button(self, obj):
        """
        Add a button to the admin page to access the dashboard.
        """
        return format_html('<a class="button" href="/admin/dashboard/">View Dashboard</a>')
    
    dashboard_button.short_description = "Dashboard"  # Label for the button

    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('import-csv/', self.admin_site.admin_view(self.import_csv), name='transaction_import_csv'),
        ]
        return custom_urls + urls

    def import_csv(self, request):
        if request.method == "POST":
            # Handle uploaded file
            csv_file = request.FILES.get("csv_file")
            if not csv_file:
                self.message_user(request, "No file uploaded", level="error")
                return HttpResponseRedirect("../")

            try:
                # Read CSV using pandas
                data = pd.read_csv(io.StringIO(csv_file.read().decode('utf-8')))

                for _, row in data.iterrows():
                    transaction_type = row.get('transaction_type')
                    sender_name = row.get('sender_name')
                    recipient_name = row.get('recipient_name')
                    amount = row.get('amount')
                    date = row.get('transaction_date')

                    # Validate and find related sender/recipient
                    sender = User.objects.filter(name=sender_name).first() if pd.notna(sender_name) else None
                    recipient = User.objects.filter(name=recipient_name).first() if pd.notna(recipient_name) else None

                    # Ensure sender and recipient are correct based on transaction type
                    if transaction_type == 'deposit' and sender is not None:
                        # Use current date if no date is provided
                        transaction_date = timezone.now() if pd.isna(date) else pd.to_datetime(date)

                        # Create deposit transaction and update sender's balance
                        transaction = Transaction.objects.create(
                            transaction_type=transaction_type,
                            sender=sender,
                            recipient=None,
                            amount=Decimal(amount) if pd.notna(amount) else Decimal(0),
                            date=transaction_date
                        )
                        # Update sender's balance
                        sender.balance = sender.balance + Decimal(amount) if pd.notna(amount) else sender.balance
                        sender.save()

                    elif transaction_type == 'withdraw' and sender is not None:
                        # Handle withdraw
                        transaction_date = timezone.now() if pd.isna(date) else pd.to_datetime(date)

                        # Create withdraw transaction and update sender's balance
                        transaction = Transaction.objects.create(
                            transaction_type=transaction_type,
                            sender=sender,
                            recipient=None,
                            amount=Decimal(amount) if pd.notna(amount) else Decimal(0),
                            date=transaction_date
                        )
                        # Update sender's balance (decrease balance)
                        sender.balance = sender.balance - Decimal(amount) if pd.notna(amount) else sender.balance
                        sender.save()

                    elif transaction_type == 'airtime' and sender is not None:
                        # Handle airtime transaction
                        transaction_date = timezone.now() if pd.isna(date) else pd.to_datetime(date)

                        # Create airtime transaction and update sender's balance
                        transaction = Transaction.objects.create(
                            transaction_type=transaction_type,
                            sender=sender,
                            recipient=None,
                            amount=Decimal(amount) if pd.notna(amount) else Decimal(0),
                            date=transaction_date
                        )
                        # Update sender's balance (decrease balance)
                        sender.balance = sender.balance - Decimal(amount) if pd.notna(amount) else sender.balance
                        sender.save()

                    elif transaction_type == 'transfer' and sender is not None and recipient is not None:
                        # Handle transfer transaction
                        transaction_date = timezone.now() if pd.isna(date) else pd.to_datetime(date)

                        # Create transfer transaction (both sender and recipient are involved)
                        transaction = Transaction.objects.create(
                            transaction_type=transaction_type,
                            sender=sender,
                            recipient=recipient,
                            amount=Decimal(amount) if pd.notna(amount) else Decimal(0),
                            date=transaction_date
                        )
                        # Update sender's balance (decrease balance)
                        sender.balance = sender.balance - Decimal(amount) if pd.notna(amount) else sender.balance
                        sender.save()

                        # Update recipient's balance (increase balance)
                        recipient.balance = recipient.balance + Decimal(amount) if pd.notna(amount) else recipient.balance
                        recipient.save()

                    elif transaction_type == 'bill' and sender is not None:
                        # Handle bill payment transaction
                        transaction_date = timezone.now() if pd.isna(date) else pd.to_datetime(date)

                        # Create bill payment transaction and update sender's balance
                        transaction = Transaction.objects.create(
                            transaction_type=transaction_type,
                            sender=sender,
                            recipient=None,
                            amount=Decimal(amount) if pd.notna(amount) else Decimal(0),
                            date=transaction_date
                        )
                        # Update sender's balance (decrease balance)
                        sender.balance = sender.balance - Decimal(amount) if pd.notna(amount) else sender.balance
                        sender.save()

                    else:
                        # Handle invalid data, such as missing sender or recipient
                        self.message_user(request, f"Invalid data in row: {row}", level="error")
                        continue

                self.message_user(request, "CSV imported successfully!")
                return HttpResponseRedirect("../")
            except Exception as e:
                self.message_user(request, f"Error importing CSV: {e}", level="error")
                return HttpResponseRedirect("../")

        return render(request, "admin/import_csv.html", context={'title': "Import CSV"})

    change_list_template = "admin/transaction_change_list.html"


admin.site.register(User, UserAdmin)
admin.site.register(Transaction, TransactionAdmin)