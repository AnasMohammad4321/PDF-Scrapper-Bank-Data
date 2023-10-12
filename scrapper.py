import re
import csv
import pdfplumber
import os

def process_pdf(file, choice):
    """
    Extracts and processes financial transaction data from a PDF file and writes it to a CSV file.

    Args:
        file (str): The path to the input PDF file containing financial transaction data.
        choice (bool): A boolean value indicating whether to process withdrawals (False) or deposits (True).

    Returns:
        None
    """
    if choice == False:
        output_filename = os.path.splitext(file)[0] + "_withdrawals.csv"
        found_count = 0
        print_data = False
        total_amount = 0
        end = False

        with open(output_filename, 'w', newline='', encoding='utf-8') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(['Date', 'Description', 'Amount'])

            with pdfplumber.open(file) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    for line in text.split('\n'):
                        if "Total withdrawals and other subtractions" in line:
                            end = True
                            break

                        if "Withdrawals and other subtractions" in line:
                            found_count += 1
                            if found_count == 2:
                                print_data = True
                        if print_data:
                            if re.match(r'\d{1,2}/\d{1,2}/\d{2}', line):
                                date = line[:8].strip()
                                amount_end = line.rfind(' ')
                                amount_str = line[amount_end:].strip()
                                amount = float(amount_str.replace(',', ''))
                                description = line[8:amount_end].strip()

                                csvwriter.writerow([date, description, amount])
                                total_amount += amount
                    if end:
                        break

        print(f"Data has been successfully written to '{output_filename}' file.")
        print(f"Total Withdrawal Amount: {total_amount:.2f}")

    if choice == True:
        output_filename = os.path.splitext(file)[0] + "_deposits.csv"
        found_count = 0
        print_data = False
        total_amount = 0
        end = False

        with open(output_filename, 'w', newline='', encoding='utf-8') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(['Date', 'Description', 'Amount'])

            with pdfplumber.open(file) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    for line in text.split('\n'):
                        if "Total deposits and other additions" in line:
                            end = True
                            break

                        if "Deposits and other additions" in line:
                            found_count += 1
                            if found_count == 2:
                                print_data = True
                        if print_data:
                            if re.match(r'\d{1,2}/\d{1,2}/\d{2}', line):
                                date = line[:8].strip()
                                amount_end = line.rfind(' ')
                                amount_str = line[amount_end:].strip()
                                amount = float(amount_str.replace(',', ''))
                                description = line[8:amount_end].strip()

                                csvwriter.writerow([date, description, amount])
                                total_amount += amount
                    if end:
                        break

        print(f"Data has been successfully written to '{output_filename}' file.")
        print(f"Total Desposit Amount: {total_amount:.2f}")

def main():
    option = input("Enter 1 for Deposits or 2 for Withdrawals: ")
    choice = True if option == "1" else False if option == "2" else None

    pdf_files = [file for file in os.listdir() if file.endswith(".pdf")]
    
    if choice is not None:
        for file in pdf_files:
            process_pdf(file, choice)
    else:
        print("Invalid choice. Please enter 1 for Deposits or 2 for Withdrawals.")

if __name__ == "__main__":
    main()