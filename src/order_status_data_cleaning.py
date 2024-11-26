# Import necessary libraries
import pandas as pd


# Define the function to clean the order status data
def clean_order_status_data(base_path):
    """
    Cleans the customers data by dropping duplicates, invalid entries, filling null values, and changing data types.
    """
    # Define paths dynamically
    input_file = base_path / "data/processed/order_status.csv"
    output_file = base_path / "data/cleaned/order_status_cleaned.csv"

    # Load data
    df = pd.read_csv(input_file)
    initial_rows = df.shape[0]
    print(f"Original dimensions {df.shape}\n")  # 108127, 5

    # Load orders data
    reference_file = base_path / "data/cleaned/orders_cleaned.csv"
    orders = pd.read_csv(reference_file)
    order_id = orders["order_id"].unique()

    # ----------------------------
    # FILTER BY ORDER ID
    # ----------------------------

    # Filter rows to include only those with order_ids present in the orders DataFrame
    df = df[df["order_id"].isin(order_id)]
    print(f"Dimensions after filtering by order_id: {df.shape}\n")

    # ----------------------------
    # DUPLICATES ON PRIMARY KEY
    # ----------------------------

    # Drop duplicates on primary key [# 0]
    df = df.drop_duplicates(subset=["order_id"], keep="first")
    print(f"Dimensions after dropping duplicates: {df.shape}\n")

    # ----------------------------
    # NULL VALUES
    # ----------------------------

    # Check for null values
    nullvalues = df.isnull().sum()
    print(f"Null-Values: \n{nullvalues}\n")

    # Drop rows with null values in specific columns [# 1]
    df.dropna(subset=["purchase_ts"], inplace=True)
    print(f"Dimensions after dropping null values: {df.shape}\n")

    # ----------------------------
    # UNIQUE VALUES
    # ----------------------------

    # Check unique values
    nuniq = df.nunique()
    print(f"Unique values: \n{nuniq}\n")

    # ----------------------------
    # DATA TYPES
    # ----------------------------

    # Change data type of time columns to datetime
    time_columns = ["purchase_ts", "ship_ts", "delivery_ts", "refund_ts"]
    df[time_columns] = df[time_columns].apply(pd.to_datetime, errors="coerce")

    # Set refund_ts to NaT if it is greater than 2023-12-31
    df.loc[df["refund_ts"] > "2023-12-31 23:59:59", "refund_ts"] = pd.NaT

    # ----------------------------
    # SAVE TO CSV
    # ----------------------------

    # Save cleaned data to CSV [# 108126, 5]
    final_rows = df.shape[0]
    print(f"Rows dropped during cleaning: {initial_rows - final_rows}")  # 1
    print(f"Final dimensions: {df.shape}")
    df.to_csv(output_file, index=False)
