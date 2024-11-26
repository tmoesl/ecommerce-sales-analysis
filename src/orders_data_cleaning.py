# Import necessary libraries
import pandas as pd


# Define the function to clean the orders data
def clean_orders_data(base_path):
    """
    Cleans the orders data by dropping duplicates, invalid entries, null values, zero values, unique values, and changing data types.
    """
    # Define paths dynamically
    input_file = base_path / "data/processed/orders.csv"
    output_file = base_path / "data/cleaned/orders_cleaned.csv"

    # Load data
    df = pd.read_csv(input_file)
    initial_rows = df.shape[0]
    print(f"Original dimensions {df.shape}\n")  # 108127, 5

    # ----------------------------
    # DUPLICATES ON PRIMARY KEY
    # ----------------------------

    # Drop duplicates on primary key [# 0]
    df = df.drop_duplicates(subset=["order_id"], keep="first")
    print(f"Dimensions after dropping duplicates: {df.shape}\n")

    # ----------------------------
    # INVALID ENTRIES ON FOREIGN KEY
    # ----------------------------

    # Drop invalid entries on foreign key [# 807]
    df = df[df["customer_id"].str.len() == 8]
    print(f"Dimensions after dropping invalid entries: {df.shape}\n")

    # ----------------------------
    # NULL VALUES
    # ----------------------------

    # Check for null values [# 1, # 54, # 33]
    nullvalues = df.isnull().sum()
    print(f"Null-Values: \n{nullvalues}\n")

    # Drop rows with null values in specific columns
    df.dropna(subset=["purchase_ts", "currency", "usd_price"], inplace=True)
    print(f"Dimensions after dropping null values: {df.shape}\n")

    # ----------------------------
    # ZERO VALUES
    # ----------------------------

    # Drop rows with zero values in local_price and usd_price [# 104]
    df = df[(df["local_price"] != 0) & (df["usd_price"] != 0)]
    print(f"Dimensions after dropping zero values: {df.shape}\n")

    # ----------------------------
    # UNIQUE VALUES
    # ----------------------------

    # Check unique values
    nuniq = df.nunique()
    print(f"Unique values: \n{nuniq}\n")

    # In-depth analysis of unique values
    df["product_name"].value_counts()
    df["purchase_platform"].value_counts()

    # Create a mapping for product_name
    product_name_mapping = {
        "Apple Airpods Headphones": "Apple Airpods Headphones",
        "27in 4K gaming monitor": "Dell 27in 4K Gaming Monitor",
        "Samsung Charging Cable Pack": "Samsung Charging Cable Pack",
        "Samsung Webcam": "Samsung Slimfit Webcam",
        "Macbook Air Laptop": "Apple Macbook Air Laptop",
        "ThinkPad Laptop": "Lenovo ThinkPad Laptop",
        "Apple iPhone": "Apple iPhone",
        '27in"" 4k gaming monitor': "Dell 27in 4K Gaming Monitor",
        "bose soundsport headphones": "Bose Soundsport Headphones",
    }

    # Replace product_name with mapping
    df["product_name"] = df["product_name"].replace(product_name_mapping)

    # ----------------------------
    # DATA TYPES
    # ----------------------------

    # Change data type of purchase_ts to datetime
    df["purchase_ts"] = pd.to_datetime(df["purchase_ts"], errors="coerce")

    # Drop rows with invalid purchase_ts [# 29]
    df.dropna(subset=["purchase_ts"], inplace=True)
    print(f"Dimensions after dropping invalid purchase_ts: {df.shape}\n")

    # ----------------------------
    # SAVE TO CSV
    # ----------------------------

    # Save cleaned data to CSV [# 107022, 9]
    final_rows = df.shape[0]
    print(f"Rows dropped during cleaning: {initial_rows - final_rows}")  # 1028
    print(f"Final dimensions: {df.shape}")
    df.to_csv(output_file, index=False)
