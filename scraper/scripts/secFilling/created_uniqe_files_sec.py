import os
import glob
import sys

HTML_FILES_NAME = ["primary-document.html", "full-submission.txt"]

def find_and_rename_files(folder_path):
    try:
        for dirpath, _, files in os.walk(folder_path):
            for file in files:
                if file in HTML_FILES_NAME:
                    # Extract the ticker and report type from the directory structure
                    report_type_dir = os.path.basename(os.path.dirname(dirpath))  # Get the report type directory
                    ticker_dir = os.path.basename(os.path.dirname(os.path.dirname(dirpath)))  # Get the ticker directory
                    
                    # Determine the new file extension
                    file_extension = file.split('.')[-1]
                    
                    # Create the new file name
                    new_file_name = f"{ticker_dir.upper()}_{report_type_dir}.{file_extension}"
                    
                    # Define the source and destination paths
                    source_path = os.path.join(dirpath, file)
                    destination_path = os.path.join(dirpath, new_file_name)  # Rename in place

                    # Rename the file
                    print(f"Renaming {source_path} to {destination_path}")
                    os.rename(source_path, destination_path)
    except Exception as e:
        print(f"Error occurred while renaming files: {e}")
        sys.exit(1)

def move_files_to_parent(folder_path):
    try:
        for dirpath, _, files in os.walk(folder_path, topdown=False):
            for file in files:
                if any(file.endswith(ext) for ext in ["html", "txt"]):
                    # Get the ticker and report type from the current directory structure
                    report_type_dir = os.path.basename(dirpath)  # Report type directory
                    cik_dir = os.path.basename(os.path.dirname(dirpath))  # CIK directory
                    ticker_dir = os.path.basename(os.path.dirname(os.path.dirname(dirpath)))  # Ticker directory
                    
                    if file.startswith(ticker_dir.upper()):
                        # Define the source and destination paths
                        source_path = os.path.join(dirpath, file)
                        destination_path = os.path.join(os.path.dirname(dirpath), file)  # Move to parent folder

                        # Move the file
                        print(f"Moving {source_path} to {destination_path}")
                        os.rename(source_path, destination_path)
                        
                        # Check if the directory is now empty and remove it if so
                        if not os.listdir(dirpath):
                            print(f"Removing empty directory: {dirpath}")
                            os.rmdir(dirpath)
    except Exception as e:
        print(f"Error occurred while moving files: {e}")
        sys.exit(1)

def main():
    try:
        base_path = "/Users/elmaliahmac/Documents/Full_stack/scraping_Twitter/scraper_project/scraper/saved_data/sec-edgar-filings"
        folders = glob.glob(f"{base_path}/*")
        folders.reverse()
        print(f"Processing folders: {folders}")
    except Exception as e:
        print(f"Error occurred while getting folders: {e}")
        sys.exit(1)

    if folders:
        for folder in folders:
            find_and_rename_files(folder)
        move_files_to_parent(base_path)

if __name__ == "__main__":
    main()
