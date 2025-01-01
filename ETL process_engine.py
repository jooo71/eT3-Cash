from datetime import datetime
import pandas as pd
from sqlalchemy import create_engine

# Database connection details
connection_string = 'mssql+pyodbc://@DESKTOP-UQDT40R/wallet?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes'
engine = create_engine(connection_string)

# Step 1: Extract Data
def extract_data():
    """
    Extracts data from the SQL database into Pandas DataFrames.
    """
    print("Extracting data from the database...")
    partitioned_transactions = pd.read_sql("SELECT * FROM [wallet].[dbo].[PartitionedTransactions]", engine)
    dim_transaction_types = pd.read_sql("SELECT * FROM [wallet].[dbo].[dim_transaction_types]", engine)
    print("Data extraction completed.")
    return partitioned_transactions, dim_transaction_types


# Step 2: Transform Data
def transform_data(partitioned_transactions, dim_transaction_types):
    """
    Transforms the data by mapping transaction types to keys
    and identifying any unmapped transaction types.
    """
    print("Transforming data...")
    # Merge the tables on 'transaction_type'
    merged_data = pd.merge(
        partitioned_transactions,
        dim_transaction_types,
        how='left',  # Use 'left' join to keep all records in partitioned_transactions
        left_on='transaction_type',
        right_on='transaction_type'
    )

    # Check for unmapped transaction types
    unmapped = merged_data[merged_data['transaction_type_key'].isna()]
    if not unmapped.empty:
        print("Unmapped transaction types found:")
        print(unmapped[['transaction_id', 'transaction_type']])
        # Optionally log these to a file for further analysis
        unmapped.to_csv("unmapped_transaction_types.csv", index=False)

    print("Transformation completed.")
    return merged_data


# Step 3: Load Data
def load_data(transformed_data):
    """
    Loads the transformed data back into the database.
    """
    print("Loading data into the database...")
    transformed_data.to_sql("Newfact_transcations", engine, if_exists="replace", index=False)
    print("Data loading completed.")


# Step 4: Insert New Records
def insert_data(new_records):
    """
    Inserts new records into the PartitionedTransactions table.
    """
    if new_records is not None:
        print("Inserting new records into PartitionedTransactions...")
        new_records_df = pd.DataFrame(new_records)
        
        # Make sure the transaction type exists in dim_transaction_types
        valid_transaction_types = pd.read_sql("SELECT transaction_type FROM [wallet].[dbo].[dim_transaction_types]", engine)
        valid_types = valid_transaction_types['transaction_type'].tolist()
        
        # Filter out invalid transaction types
        valid_new_records = [record for record in new_records if record['transaction_type'] in valid_types]
        
        if valid_new_records:
            new_records_df = pd.DataFrame(valid_new_records)
            new_records_df.to_sql("PartitionedTransactions", engine, if_exists="append", index=False)
            print("New records inserted.")
        else:
            print("No valid transaction types found in the new records.")
    else:
        print("No new records provided.")


# Main ETL Process
if __name__ == "__main__":
    # Define new records to insert (example format)
    new_records = [
        {
            "transaction_type": "airtime",   # Must match a type in dim_transaction_types
            "sender_id": 2,
            "recipient_id": None,
            "amount": 1500.0,
            "transaction_date": datetime.now()
        },
        {
            "transaction_type": "deposit",  # Must match a type in dim_transaction_types
            "sender_id": None,
            "recipient_id": 3,
            "amount": 55.0,
            "transaction_date": datetime.now()
        }
    ]

    # Insert new records into the PartitionedTransactions table
    insert_data(new_records)

    # Extract
    partitioned_transactions, dim_transaction_types = extract_data()

    # Transform
    transformed_data = transform_data(partitioned_transactions, dim_transaction_types)

    # Load
    load_data(transformed_data)