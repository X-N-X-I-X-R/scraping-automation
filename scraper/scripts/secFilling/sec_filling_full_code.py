import logging
from re import T
from sec_edgar_downloader import Downloader
import os
from datetime import datetime, timedelta
from django.conf import settings
import glob
import sys

logger = logging.getLogger(__name__)

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

def process_downloaded_files():
    base_path = "/Users/elmaliahmac/Documents/Full_stack/scraping_Twitter/scraper_project/scraper/saved_data/sec-edgar-filings"
    folders = glob.glob(f"{base_path}/*")
    folders.reverse()
    print(f"Processing folders: {folders}")
    
    if folders:
        for folder in folders:
            find_and_rename_files(folder)
        move_files_to_parent(base_path)

def fetch_sec_fillings(ticker: str, report_type: str):
    try:
        logger.info("fetch_sec_fillings called with ticker: %s and report_type: %s", ticker, report_type)
        date = datetime.now()
        afters = date - timedelta(days=730)
        save_dir = os.path.join(settings.BASE_DIR, 'scraper', 'saved_data')
        logger.info("Save directory: %s", save_dir)
        
        # Check if the Downloader is initialized correctly
        try:
            dl = Downloader("LL", "news@gmail.com", save_dir)
        except Exception as e:
            logger.error("Failed to initialize Downloader: %s", str(e))
            raise
        # Check if the SEC API is responding
        try:
            num_filings = dl.get(report_type, ticker, limit=1, include_amends=True, after=afters.strftime("%Y-%m-%d"), before=date.strftime("%Y-%m-%d"), download_details=True)
        except Exception as e:
            logger.error("Failed to download filings: %s", str(e))
            raise
        logger.info("Number of filings downloaded: %s", num_filings)
        filing_paths = glob.glob(os.path.join(save_dir, '*'))
        logger.info("Filing paths found: %s", filing_paths)
        
        if filing_paths:
            filing_path = filing_paths[0]
            logger.info("Filing path: %s", filing_path)
            process_downloaded_files()  # Process files after download
            html_files = glob.glob(os.path.join(filing_path, '*.html'))  # Search for .html files in the filing directory
            logger.info("HTML files found: %s", html_files)
            if html_files:
                html_file_path = html_files[0]  # Use the first .html file found
                logger.info("HTML file path: %s", html_file_path)
                return os.path.relpath(html_file_path, settings.BASE_DIR)
            else:
                logger.error("No HTML file found in the report")
                raise FileNotFoundError("No HTML file found in the report")
        else:
            logger.error("No report found")
            raise FileNotFoundError("No report found")
    except Exception as e:
        logger.error("An error occurred in fetch_sec_fillings: %s", str(e))
        raise

def find_primary_docs(path):
    try:
        logger.info("find_primary_docs called with path: %s", path)
        primary_docs = []
        if os.path.isfile(path) and path.endswith('.html'):
            parent_dir = os.path.basename(os.path.dirname(path))
            logger.info("Parent directory: %s", parent_dir)
            if '_' in parent_dir:
                ticker, report_type, cik = parent_dir.split('_')  # Assuming the parent directory is in the format 'ticker_reporttype_cik'
                primary_docs.append({
                    'path': path,
                    'ticker': ticker,
                    'report_type': report_type,
                    'cik': cik
                })
            else:
                logger.error("Parent directory is not in the expected format: %s", parent_dir)
                raise ValueError("Parent directory is not in the expected format")
        else:
            for root, dirs, files in os.walk(path):
                for file in files:
                    if file == 'primary-document.html':
                        path = os.path.join(root, file)
                        parent_dir = os.path.basename(os.path.dirname(path))
                        logger.info("Parent directory: %s", parent_dir)
                        if '_' in parent_dir:
                            ticker, report_type, cik = parent_dir.split('_')  # Assuming the parent directory is in the format 'ticker_reporttype_cik'
                            primary_docs.append({
                                'path': path,
                                'ticker': ticker,
                                'report_type': report_type,
                                'cik': cik
                            })
                        else:
                            logger.error("Parent directory is not in the expected format: %s", parent_dir)
                            raise ValueError("Parent directory is not in the expected format")
        logger.info("Primary docs found: %s", primary_docs)
        return primary_docs
    except Exception as e:
        logger.error("An error occurred in find_primary_docs: %s", str(e))
        raise




