import argparse
import csv

def read_csv(file_path):
    data = []
    with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            data.append(row)
    return data

def print_columns(data, id, columns):
    for row in data:
        if row['ID'] == id:
            for column in columns:
                print(f"{column}: {row[column]}")

def main():
    parser = argparse.ArgumentParser(description="Read values from a CSV file based on specified columns and ID.")
    parser.add_argument("csv_file", help="Path to the CSV file")
    parser.add_argument("--id", type=int, help="ID of the row to retrieve", required=True)
    parser.add_argument("--columns", nargs='+', help="Columns to print", required=True)
    args = parser.parse_args()

    try:
        data = read_csv(args.csv_file)
        print_columns(data, str(args.id), args.columns)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

