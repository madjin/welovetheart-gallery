import argparse
import csv
import subprocess

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

def generate_qr_code(nft_link, output_filename):
    subprocess.run(['qrencode', '-o', output_filename, nft_link])

def main():
    parser = argparse.ArgumentParser(description="Read values from a CSV file and generate QR code for NFT Link.")
    parser.add_argument("csv_file", help="Path to the CSV file")
    args = parser.parse_args()

    try:
        data = read_csv(args.csv_file)
        for row in data:
            id_value = row['ID']
            nft_link = row['NFT Link']
            output_filename = f"{id_value}_qrcode.png"
            
            # Generate QR code
            generate_qr_code(nft_link, output_filename)

            print(f"Generated QR code for ID {id_value} and saved to {output_filename}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
