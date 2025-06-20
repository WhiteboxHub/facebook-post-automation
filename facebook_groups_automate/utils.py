import random
import time
import os
import json
import csv
from datetime import datetime

def human_delay(a=2, b=5):
    """Random delay to mimic human behavior."""
    time.sleep(random.uniform(a, b))

def log(message):
    print(f"[INFO] {message}")

def get_last_run(path="last_run.json"):
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
        return data.get("last_run")

def set_last_run(path="last_run.json"):
    now = datetime.now().isoformat(timespec='seconds')
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"last_run": now}, f)
    return now

def validate_pdf_file(file_path):
    """Validate that the PDF file exists and is accessible."""
    if not file_path:
        return False, "No file path provided"
    
    if not os.path.exists(file_path):
        return False, f"File does not exist: {file_path}"
    
    if not file_path.lower().endswith('.pdf'):
        return False, f"File is not a PDF: {file_path}"
    
    # Check if file is readable
    try:
        with open(file_path, 'rb') as f:
            # Read first few bytes to check if it's a valid PDF
            header = f.read(4)
            if header != b'%PDF':
                return False, f"File is not a valid PDF: {file_path}"
    except Exception as e:
        return False, f"Cannot read file: {str(e)}"
    
    return True, "PDF file is valid"

def save_results_to_csv(results, filename):
    """Save posting results to a CSV file."""
    if not results:
        log("No results to save to CSV")
        return
    
    fieldnames = ["group_name", "url", "status", "error", "timestamp"]
    
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)
        
        log(f"Results saved to {filename}")
        
        # Print summary
        success_count = sum(1 for r in results if r["status"] == "SUCCESS")
        failed_count = sum(1 for r in results if r["status"] == "FAILED")
        skipped_count = sum(1 for r in results if r["status"] == "SKIPPED")
        
        log(f"CSV Summary: {success_count} successful, {failed_count} failed, {skipped_count} skipped")
        
    except Exception as e:
        log(f"Error saving CSV: {str(e)}") 