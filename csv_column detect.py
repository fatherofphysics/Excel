import os
import shutil
import csv
import glob
import chardet

def create_folder_if_not_exists(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

def copy_files_to_folder(files, dest_folder):
    create_folder_if_not_exists(dest_folder)
    for file in files:
        shutil.copy(file, dest_folder)

def detect_encoding(file_path):
    with open(file_path, 'rb') as rawdata:
        result = chardet.detect(rawdata.read(100000))  # Adjust the read size as needed
    return result['encoding']

def process_csv_files(src_folder, dest_folder):
    # Get all CSV files in the source folder
    csv_files = glob.glob(os.path.join(src_folder, '*.csv'))

    for csv_file in csv_files:
        encoding = detect_encoding(csv_file)
        with open(csv_file, 'r', encoding=encoding) as file:
            # Read the CSV file
            reader = csv.reader(file)
            header = next(reader)

            # Check if the data goes up to column J
            if len(header) >= 10:  # Assuming columns are zero-indexed
                # No need to close the file here if you're just copying
                pass
                
            copy_files_to_folder([csv_file], dest_folder)
            print(f"Copied {csv_file} to {dest_folder} (Detected Encoding: {encoding})")

if __name__ == "__main__":
    source_folder = input("Enter csv folder path: ") 
    destination_folder = input("Enter destination folder name: ")

    process_csv_files(source_folder, destination_folder)
