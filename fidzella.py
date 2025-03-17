##################
# Fidzella 1.0
# Cyberheisen
# 03172025
##################

import csv
import datetime
import pandas as pd
import os
import sys

def read_csv_to_dict(file_path):
    """Reads a CSV file and converts it into a list of dictionaries."""
    try:
        df = pd.read_csv(file_path)
        return df.to_dict(orient="records")
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

def process_data(fidelity_data):
    """
    Processes the list of dictionaries and returns a new transformed list.

    :param data: List of dictionaries from the CSV.
    :return: Transformed list of dictionaries.
    """
    tradezella_data = []
    for row in fidelity_data:
    
    # Ensure we ignore the bottom footer text
        fidelity_date = row.get("Run Date")
        isdate = is_valid_date(fidelity_date)
        if not isdate:
           break
        
    # Convert Buy/Sell
        fidelity_action = row.get("Action").upper()
        if "BOUGHT" in fidelity_action:
            action = "buy"
        else:
            if "SOLD" in fidelity_action:
                action = "sell"
            else:
                continue
            
    # Correct the Quantity Values
        fidelity_quantity = row.get("Quantity")
        if fidelity_quantity < 0:
            quantity = (fidelity_quantity * -1)
        else:
            quantity = (fidelity_quantity)

    # Make sure nan are not printed for "Fees"
        fidelity_fees = str(row.get("Fees ($)"))
        if fidelity_fees == 'nan':
            fidelity_fees = ''
        
        parsed = {
        "Date":row.get("Run Date"),
        "Time":"12:00:00",
        "Symbol":row.get("Symbol"),
        "Buy/Sell":action,
        "Quantity":quantity,
        "Price":row.get("Price ($)"),
        "Spread":"Stock",
        "Commision":row.get("Comission"),
        "Fees":fidelity_fees}
        
        tradezella_data.append(parsed)
        
    return tradezella_data

def write_csv(output_filename,tradezella_data):
    """
    Writes a list of dictionaries to a CSV file.

    :param output_filepath: Path to the output CSV file.
    :param data: List of dictionaries to be written to the file.
    """
    if not tradezella_data:
        print("No data to write.")
        return
    tradezella_headers = [
        "Date", "Time", "Symbol", "Buy/Sell", "Quantity",
        "Price", "Spread", "Expiration", "Strike", "Call/Put", "Commision", "Fees"
    ]
    with open(output_filename, "w+", encoding="utf-8", newline="") as f:
        fieldnames = tradezella_data[0].keys()
        writer = csv.DictWriter(f, fieldnames=tradezella_headers)
        writer.writeheader()
        writer.writerows(tradezella_data)

def is_valid_date(fidelity_date):
    try:
        datetime.datetime.strptime(fidelity_date.strip(), "%m/%d/%Y")
        return True
    except ValueError:
        return False
    
def main():
    """Main function that accepts a file path argument and processes the CSV."""
    if len(sys.argv) < 2:
        print("Usage: python fidzella.py <fidelity csv file path>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    output_filename = os.path.join(os.path.dirname(file_path),"tradezella.csv")
    print(output_filename)
    fidelity_data = read_csv_to_dict(file_path)
    tradezella_data = process_data(fidelity_data)
    write_csv(output_filename, tradezella_data)


if __name__ == "__main__":
    main()
