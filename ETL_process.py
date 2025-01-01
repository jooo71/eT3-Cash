
import csv
import pyodbc
from datetime import datetime
import pandas as pd

# Database connection details
server = 'DESKTOP-UQDT40R'
database = 'wallet'
driver = 'ODBC Driver 17 for SQL Server'

# 1. Generate a CSV file with dummy data
def generate_csv(file_name):
    # Define sample transaction data
    transactions = [
        {"transaction_type": "withdraw", "sender_id": 2, "recipient_id": None, "amount": 30.00, "transaction_date": datetime.now()},
        {"transaction_type": "airtime", "sender_id": 1, "recipient_id": None, "amount": 22.00, "transaction_date": datetime.now()},
        {"transaction_type": "deposit", "sender_id": None, "recipient_id": 2, "amount": 555.00, "transaction_date": datetime.now()},
        {"transaction_type": "transfer", "sender_id": 3, "recipient_id": 4, "amount": 15.00, "transaction_date": datetime.now()},
        {"transaction_type": "bill", "sender_id": 4, "recipient_id": None, "amount": 60.00, "transaction_date": datetime.now()},

    ]
    
    # Write to CSV
    with open(file_name, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["transaction_type", "sender_id", "recipient_id", "amount", "transaction_date"])
        writer.writeheader()
        for transaction in transactions:
            transaction['amount'] = round(transaction['amount'], 2)
            transaction['transaction_date'] = transaction['transaction_date'].strftime('%Y-%m-%d %H:%M:%S')  # Format datetime
            writer.writerow(transaction)

    print(f"CSV file '{file_name}' generated successfully!")

# 2. Read the CSV file and load data into the database
def load_csv_to_db(file_name):
    
# Connect to the database using Windows Authentication
    connection = pyodbc.connect(
        f'DRIVER={driver};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
    )
    

    cursor = connection.cursor()
    
    try:
        # Read the CSV file
        data = pd.read_csv(file_name)

        # Insert each row into the database
        for _, row in data.iterrows():
            cursor.execute("""
                INSERT INTO [wallet].[dbo].[PartitionedTransactions] 
                (transaction_type, sender_id, recipient_id, amount, transaction_date)
                VALUES (?, ?, ?, ?, ?)
            """, (
                row['transaction_type'],
                int(row['sender_id']) if not pd.isnull(row['sender_id']) else None,
                row['recipient_id'] if not pd.isnull(row['recipient_id']) else None,
                float(row['amount']),
                row['transaction_date']
            ))
            

        connection.commit()
        print(f"Data from '{file_name}' loaded into the database successfully!")
    except Exception as e:
        print(f"Error loading data to the database: {e}")
        
        connection.rollback()
    finally:
        connection.close()

# 3. ETL: Transform and show updates
def etl_process():
    
# Connect to the database using Windows Authentication
    connection = pyodbc.connect(
        f'DRIVER={driver};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
    )

    cursor = connection.cursor()

    try:
        # Extract data
        query = """
        SELECT pt.transaction_id, 
               pt.transaction_type, 
               dtt.transaction_type_key, 
               pt.sender_id, 
               pt.recipient_id, 
               pt.amount, 
               pt.transaction_date
        FROM [wallet].[dbo].[PartitionedTransactions] pt
        JOIN [wallet].[dbo].[dim_transaction_types] dtt
        ON pt.transaction_type = dtt.transaction_type
        """
        data = pd.read_sql(query, connection)

        # Transformation: Example transformation
        data['transaction_month'] = pd.to_datetime(data['transaction_date']).dt.month
        data['transaction_year'] = pd.to_datetime(data['transaction_date']).dt.year
        data['day_of_week'] = data['transaction_date'].dt.day_name()
        data['quarter'] = data['transaction_date'].dt.quarter


        # Load (output to console for demo purposes)
        print("Transformed Data:")
        print(data)

    except Exception as e:
        print(f"ETL process failed: {e}")
    finally:
        connection.close()

# Main workflow
if __name__ == "__main__":
    csv_file_name = "transactions.csv"

    # Step 1: Generate CSV file
    generate_csv(csv_file_name)

    # Step 2: Load CSV data into the database
    load_csv_to_db(csv_file_name)

    # Step 3: Run ETL process
    etl_process()
