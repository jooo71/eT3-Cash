import pyodbc
import pandas as pd

# Establish connection to SQL Server
conn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=DESKTOP-UQDT40R;'
    'DATABASE=wallet;'
    "Trusted_Connection=yes;"
)

# Query to fetch transaction data
# Query to fetch transaction data with sender and recipient
query = """
SELECT 
    ISNULL(sender_key, recipient_key) AS user_id, -- Use sender_key if not null, otherwise use recipient_key
    CASE
        WHEN sender_key IS NOT NULL THEN 'sent'
        WHEN recipient_key IS NOT NULL THEN 'received'
    END AS transaction_role,
    transaction_type_key,
    amount,
    transaction_date
FROM 
    fact_transactions
WHERE 
    sender_key IS NOT NULL OR recipient_key IS NOT NULL
"""

# Load data into a pandas DataFrame
data = pd.read_sql(query, conn)
conn.close()

# Display the data
print(data)
