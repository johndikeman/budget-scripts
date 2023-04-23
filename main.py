import pandas as pd
import re, os

# Define global dictionaries for category replacements
DESCRIPTION_CATEGORY_REPLACEMENTS = {
    r'^AMAZON.COM.*': 'Online Shopping',
    r'^LYFT.*': 'Transportation',
    r'^UBER.*': 'Transportation',
    # Add more patterns as needed
}

CATEGORY_REPLACEMENTS = {
    r'^DINING.*': 'Food & Dining',
    r'^GROCERY.*': 'Groceries',
    r'^TRAVEL.*': 'Travel',
    # Add more patterns as needed
}

def process_usaa_ytd_transactions(csv_file_path):
    # Load the CSV file into a Pandas DataFrame
    df = pd.read_csv(csv_file_path)
    
    df.drop("Description", axis=1, inplace=True)
    # Multiply the "Amount" column by -1
    df["Amount"] = df["Amount"].astype(float) * -1
    
    # Convert the "Date" column to a datetime object
    df["Date"] = pd.to_datetime(df["Date"], format="%Y-%m-%d")
    
    # Check if the "Original Description" matches any regex pattern and update "Category" if needed
    for pattern, new_category in DESCRIPTION_CATEGORY_REPLACEMENTS.items():
        df.loc[df["Original Description"].str.contains(pattern, regex=True, na=False), "Category"] = new_category
    
    # Rename columns to match desired output
    df = df.rename(columns={"Original Description": "Description", "Category": "Category"})
    
    # Check if the "Category" matches any regex pattern and update it if needed
    for pattern, new_category in CATEGORY_REPLACEMENTS.items():
        df.loc[df["Category"].str.contains(pattern, regex=True, na=False), "Category"] = new_category
    
    # Keep only the desired columns
    df = df[["Date", "Description", "Category", "Amount"]]
    
    return df

def process_discover_transactions(file_path):
    df = pd.read_csv(file_path)
    df['Amount'] = df['Amount'].astype(float)
    df['Trans. Date'] = pd.to_datetime(df['Trans. Date'], format='%m/%d/%Y')
    df['Category'] = df['Category'].fillna('')
    df['Description'] = df['Description'].fillna('')
    
    for pattern, replacement in DESCRIPTION_CATEGORY_REPLACEMENTS.items():
        df.loc[df['Description'].str.contains(pattern, flags=re.IGNORECASE), 'Category'] = replacement
    
    for pattern, replacement in CATEGORY_REPLACEMENTS.items():
        df.loc[df['Category'].str.contains(pattern, flags=re.IGNORECASE), 'Category'] = replacement
    
    df = df.rename(columns={"Trans. Date": "Date"})
    
    return df[['Date', 'Description', 'Category', 'Amount']]



import os

def main_menu():
    transactions = None
    
    while True:
        print("Please select an option:")
        print("1. Import Discover Transactions")
        print("2. Import USAA Transactions")
        print("3. Write Transactions to output.csv")
        print("4. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == "1":
            csv_files = [f for f in os.listdir(".") if f.endswith(".csv")]
            print("Select the CSV file to import:")
            for i, file in enumerate(csv_files):
                print(f"{i+1}. {file}")
            csv_choice = input("Enter your choice: ")
            try:
                csv_choice = int(csv_choice)
                if csv_choice not in range(1, len(csv_files)+1):
                    raise ValueError
            except ValueError:
                print("Invalid choice. Please try again.")
                continue
            
            file_path = csv_files[csv_choice-1]
            if type(transactions) != pd.DataFrame:
                transactions = process_discover_transactions(file_path)
            else:
                new_transactions = process_discover_transactions(file_path)
                transactions = pd.concat([transactions, new_transactions])
            print("Transactions imported successfully!")
            
        elif choice == "2":
            csv_files = [f for f in os.listdir(".") if f.endswith(".csv")]
            print("Select the CSV file to import:")
            for i, file in enumerate(csv_files):
                print(f"{i+1}. {file}")
            csv_choice = input("Enter your choice: ")
            try:
                csv_choice = int(csv_choice)
                if csv_choice not in range(1, len(csv_files)+1):
                    raise ValueError
            except ValueError:
                print("Invalid choice. Please try again.")
                continue
            
            file_path = csv_files[csv_choice-1]
            if type(transactions) != pd.DataFrame:
                transactions = process_usaa_ytd_transactions(file_path)
            else:
                new_transactions = process_usaa_ytd_transactions(file_path)
                transactions = pd.concat([transactions, new_transactions])
            print("Transactions imported successfully!")
            
        elif choice == "3":
            if transactions is None:
                print("No transactions to write.")
                continue
            else:
                transactions.to_csv("output.csv", index=False)
                print("Transactions written to output.csv successfully!")
                
        elif choice == "4":
            break
        
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main_menu()