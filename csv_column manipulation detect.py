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
    try:
        with open(file_path, 'rb') as rawdata:
            result = chardet.detect(rawdata.read(100000))  # Adjust the read size as needed
        return result['encoding']
    except PermissionError:
        print(f"PermissionError: Cannot read the file '{file_path}'. Please check file permissions.")
        return None

def get_header(file_path, encoding):
    try:
        with open(file_path, 'r', encoding=encoding) as file:
            reader = csv.reader(file)
            return next(reader)
    except PermissionError:
        print(f"PermissionError: Cannot read the file '{file_path}'. Please check file permissions.")
        return None

def process_csv_files(src_folder, dest_folder, reference_csv_path):
    reference_encoding = detect_encoding(reference_csv_path)

    if reference_encoding is not None:
        reference_header = get_header(reference_csv_path, reference_encoding)

        # Get all CSV files in the source folder
        csv_files = glob.glob(os.path.join(src_folder, '*.csv'))

        for csv_file in csv_files:
            encoding = detect_encoding(csv_file)

            if encoding is not None:
                header = get_header(csv_file, encoding)

                # Check if the headers match
                if header == reference_header:
                    copy_files_to_folder([csv_file], dest_folder)
                    print(f"Copied {csv_file} to {dest_folder} (Detected Encoding: {encoding})")
                else:
                    print(f"Ignored {csv_file} as the header does not match the reference CSV")

if __name__ == "__main__":
    source_folder = input("Enter csv folder path: ")
    destination_folder = input("Enter destination folder name: ")
    reference_csv_path = input("Enter the path of the reference CSV file: ")

    process_csv_files(source_folder, destination_folder, reference_csv_path)
