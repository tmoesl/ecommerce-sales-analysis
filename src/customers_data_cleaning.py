# Import necessary libraries
import pandas as pd


# Define the function to clean the customers data
def clean_customers_data(base_path):
    """
    Cleans the customers data by dropping duplicates, invalid entries, filling null values, and changing data types.
    """
    # Define paths dynamically
    input_file = base_path / "data/processed/customers.csv"
    output_file = base_path / "data/cleaned/customers_cleaned.csv"

    # Load data
    df = pd.read_csv(input_file)
    initial_rows = df.shape[0]
    print(f"Original dimensions {df.shape}\n")  # 108127, 5

    # ----------------------------
    # DUPLICATES ON PRIMARY KEY
    # ----------------------------

    # Drop duplicates on primary key, keeping the row with the maximum created_on date [# 20499]
    df = df.sort_values(by="created_on").drop_duplicates(
        subset=["customer_id"], keep="last"
    )
    print(f"Dimensions after dropping duplicates: {df.shape}\n")

    # ----------------------------
    # INVALID ENTRIES ON PRIMARY KEY
    # ----------------------------

    # Drop invalid entries on primary key [# 657]
    df = df[df["customer_id"].str.len() == 8]
    print(f"Dimensions after dropping invalid entries: {df.shape}\n")

    # ----------------------------
    # NULL VALUES
    # ----------------------------

    # Check for null values
    nullvalues = df.isnull().sum()
    print(f"Null-Values: \n{nullvalues}\n")

    # Fill null values in specific columns [# 1146, # 1146]
    df["marketing_channel"] = df["marketing_channel"].fillna("unknown")
    df["account_creation_method"] = df["account_creation_method"].fillna("unknown")

    # Check for remaining null values
    nullvalues = df.isnull().sum()
    print(f"Null-Values: \n{nullvalues}\n")

    # ----------------------------
    # DATA TYPES
    # ----------------------------

    # Change data type of created_on to datetime
    df["created_on"] = pd.to_datetime(df["created_on"], errors="coerce")

    # ----------------------------
    # SAVE TO CSV
    # ----------------------------

    # Save cleaned data to CSV [# 86971, 6]
    final_rows = df.shape[0]
    print(f"Rows dropped during cleaning: {initial_rows - final_rows}")  # 21156
    print(f"Final dimensions: {df.shape}")
    df.to_csv(output_file, index=False)
